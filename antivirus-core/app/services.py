# app/services.py (ОБНОВЛЕННАЯ ВЕРСИЯ)
import asyncio
import hashlib
import time
import re
import os
import tempfile
import subprocess
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse

from app.database import db_manager
from app.external_apis.manager import external_api_manager
from app.logger import logger
from app.validators import security_validator
from app.cache import disk_cache

class AnalysisService:
    """
    Улучшенный сервис анализа с интеграцией внешних API
    """
    
    def __init__(self, use_external_apis: bool = True):
        self.use_external_apis = use_external_apis
        # Простой in-memory кэш: ключ -> (истекает_в_мс, результат)
        self._cache: Dict[str, Any] = {}
        self._cache_ttl_seconds = 300
        # YARA правила (простые сигнатуры)
        self._yara_rules = self._load_yara_rules()

    def _cache_get(self, key: str) -> Optional[Dict[str, Any]]:
        # Сначала проверяем in-memory кэш
        item = self._cache.get(key)
        if item:
            expires_at_ms, value = item
            if time.time() * 1000 > expires_at_ms:
                self._cache.pop(key, None)
                return None
            return value
        
        # Затем проверяем диск-кэш
        disk_result = disk_cache.get(key)
        if disk_result:
            # Восстанавливаем в in-memory кэш
            self._cache_set(key, disk_result)
            return disk_result
        
        return None

    def _cache_set(self, key: str, value: Dict[str, Any]):
        expires_at_ms = int(time.time() * 1000 + self._cache_ttl_seconds * 1000)
        self._cache[key] = (expires_at_ms, value)
        # Также сохраняем в диск-кэш
        disk_cache.set(key, value, self._cache_ttl_seconds)

    def _load_yara_rules(self) -> List[Dict[str, Any]]:
        """Загружает простые YARA-подобные правила для детектирования"""
        return [
            {
                "name": "suspicious_pe_header",
                "pattern": b"MZ",
                "description": "Windows PE executable detected",
                "threat_score": 20
            },
            {
                "name": "powershell_script",
                "pattern": b"powershell",
                "description": "PowerShell script detected",
                "threat_score": 30
            },
            {
                "name": "base64_encoded",
                "pattern": b"base64",
                "description": "Base64 encoded content detected",
                "threat_score": 15
            },
            {
                "name": "suspicious_urls",
                "pattern": b"http://",
                "description": "HTTP URLs detected (potentially suspicious)",
                "threat_score": 10
            }
        ]

    def _scan_with_yara_rules(self, file_content: bytes) -> Dict[str, Any]:
        """Сканирование файла с помощью простых YARA-подобных правил"""
        detected_rules = []
        total_threat_score = 0
        
        for rule in self._yara_rules:
            if rule["pattern"] in file_content:
                detected_rules.append({
                    "rule_name": rule["name"],
                    "description": rule["description"],
                    "threat_score": rule["threat_score"]
                })
                total_threat_score += rule["threat_score"]
        
        return {
            "detected_rules": detected_rules,
            "total_threat_score": total_threat_score,
            "is_suspicious": total_threat_score > 50
        }
    
    async def analyze_url(self, url: str, use_external_apis: bool = None) -> Dict[str, Any]:
        """Улучшенный анализ URL с внешними API"""
        try:
            logger.info(f"🔍 Analyzing URL: {url}")
            # Нормализация URL (убираем якорь, приводим к нижнему регистру хоста)
            try:
                from urllib.parse import urlsplit, urlunsplit
                parts = urlsplit(url)
                normalized_netloc = parts.netloc.lower()
                url = urlunsplit((parts.scheme, normalized_netloc, parts.path, parts.query, ""))
            except Exception:
                pass
            # Кэш
            cache_key = f"url:{url}"
            cached = self._cache_get(cache_key)
            if cached is not None:
                return cached
            
            # 1. Проверка в локальной базе данных
            # КРИТИЧНО: Обработка ошибок соединения с БД с автоматическим восстановлением
            try:
                url_threat = db_manager.check_url(url)
            except Exception as db_error:
                logger.warning(f"Database check failed for {url}, retrying: {db_error}")
                # Повторная попытка после короткой задержки
                import asyncio
                await asyncio.sleep(0.1)
                try:
                    url_threat = db_manager.check_url(url)
                except Exception as retry_error:
                    logger.error(f"Database check failed after retry: {retry_error}")
                    url_threat = None
            
            if url_threat:
                return {
                    "safe": False,
                    "threat_type": url_threat["threat_type"],
                    "details": f"Local database: {url_threat['description']}",
                    "source": "local_db"
                }
            
            # 2. Проверка домена в локальной базе
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            # Кэшируем clean-домены агрессивнее (короткий LRU на уровне памяти)
            domain_cache_key = f"domain-clean:{domain}"
            recently_clean = self._cache_get(domain_cache_key)
            if recently_clean:
                result = {
                    "safe": True,
                    "threat_type": None,
                    "details": "Domain recently verified as clean",
                    "source": "cache",
                    "confidence": 80
                }
                self._cache_set(cache_key, result)
                return result
            
            # КРИТИЧНО: Обработка ошибок соединения с БД
            try:
                domain_threats = db_manager.check_domain(domain)
            except Exception as db_error:
                logger.warning(f"Database domain check failed for {domain}: {db_error}")
                domain_threats = []
            
            if domain_threats:
                return {
                    "safe": False,
                    "threat_type": domain_threats[0]["threat_type"],
                    "details": f"Domain {domain} has {len(domain_threats)} known threats",
                    "source": "local_db"
                }
            
            # 3. Проверка через внешние API (если включено)
            external_result = None
            should_use_external = use_external_apis if use_external_apis is not None else self.use_external_apis
            if should_use_external:
                try:
                    logger.info(f"🔍 Checking external APIs for: {url}")
                    # Более короткий таймаут для ускорения hover, без потери качества
                    external_result = await asyncio.wait_for(
                        external_api_manager.check_url_multiple_apis(url), 
                        timeout=8.0
                    )
                    logger.info(f"🔍 External API result: safe={external_result.get('safe')}, threat_type={external_result.get('threat_type')}")
                    
                    # Если внешние API обнаружили угрозу - сохраняем в БД и возвращаем
                    if not external_result.get("safe", True):
                        logger.warning(f"🚨 External APIs detected threat for {url}: {external_result}")
                        try:
                            # Map external API threat types to database allowed types
                            threat_type = external_result.get("threat_type", "malware")
                            if threat_type == "malicious":
                                threat_type = "malware"
                            db_manager.add_malicious_url(
                                url,
                                threat_type,
                                external_result.get("details", "Detected by external scan"),
                            )
                        except Exception as save_err:
                            logger.error(f"Failed to persist URL threat: {save_err}")
                        return {
                            **external_result,
                            "source": "external_apis",
                            "confidence": external_result.get("confidence", 80)
                        }
                    else:
                        logger.info(f"✅ External APIs found {url} to be safe")
                except asyncio.TimeoutError:
                    logger.error(f"External API check timed out for {url}")
                    # Продолжаем с локальной проверкой если внешние API недоступны
                except Exception as e:
                    logger.error(f"External API check failed: {e}", exc_info=True)
                    # Продолжаем с локальной проверкой если внешние API недоступны
            
            # 4. Локальная эвристика (если внешние API чистые или недоступны)
            heuristic_result = self._url_heuristic_analysis(url, domain)
            
            # 5. Объединяем результаты - ПРИОРИТЕТ ВНЕШНИМ API
            if external_result and not external_result.get("safe", True):
                # Внешние API обнаружили угрозу - это приоритет
                result = {
                    **external_result,
                    "source": "external_apis",
                    "confidence": external_result.get("confidence", 80)
                }
                self._cache_set(cache_key, result)
                return result
            elif not heuristic_result.get("safe", True):
                # Локальная эвристика обнаружила угрозу
                result = {
                    **heuristic_result,
                    "source": "heuristic",
                    "external_scans": external_result.get("external_scans", {}) if external_result else {}
                }
                self._cache_set(cache_key, result)
                return result
            elif external_result and external_result.get("safe", True):
                # Внешние API чистые, локальная проверка тоже чистая
                result = {
                    "safe": True,
                    "threat_type": None,
                    "details": "URL appears to be safe (local + external verification)",
                    "source": "combined",
                    "external_scans": external_result.get("external_scans", {}),
                    "confidence": max(heuristic_result.get("confidence", 50), 
                                    external_result.get("confidence", 50))
                }
                self._cache_set(cache_key, result)
                # Отмечаем домен как недавно чистый (короткий TTL внутри disk_cache тоже есть)
                self._cache_set(domain_cache_key, {"clean": True})
                return result
            else:
                # Все проверки чистые (только локальные)
                result = {
                    "safe": True,
                    "threat_type": None,
                    "details": "URL appears to be safe",
                    "source": "local_only",
                    "confidence": heuristic_result.get("confidence", 50)
                }
                self._cache_set(cache_key, result)
                return result
                
        except Exception as e:
            # КРИТИЧНО: Детальное логирование ошибок анализа
            import traceback
            error_trace = traceback.format_exc()
            error_type = type(e).__name__
            
            logger.error(
                f"❌ URL analysis error for {url}:\n"
                f"  Type: {error_type}\n"
                f"  Message: {str(e)}\n"
                f"  Traceback:\n{error_trace}",
                exc_info=True
            )
            
            # Возвращаем безопасный результат вместо падения
            return {
                "safe": None,  # None означает "неизвестно", а не "опасно"
                "threat_type": "analysis_error",
                "details": f"Analysis temporarily unavailable: {error_type}",
                "source": "error"
            }
    
    async def analyze_file_hash(self, file_hash: str, use_external_apis: bool = None) -> Dict[str, Any]:
        """Улучшенная проверка файла по хэшу с внешними API"""
        try:
            logger.info(f"🔍 Analyzing file hash with external APIs: {file_hash}")
            cache_key = f"hash:{file_hash}"
            cached = self._cache_get(cache_key)
            if cached is not None:
                return cached
            
            # 1. Локальная проверка с обработкой ошибок БД
            try:
                hash_threat = db_manager.check_hash(file_hash)
            except Exception as db_error:
                logger.warning(f"Database hash check failed for {file_hash}, retrying: {db_error}")
                import asyncio
                await asyncio.sleep(0.1)
                try:
                    hash_threat = db_manager.check_hash(file_hash)
                except Exception as retry_error:
                    logger.error(f"Database hash check failed after retry: {retry_error}")
                    hash_threat = None
            
            if hash_threat:
                return {
                    "safe": False,
                    "threat_type": hash_threat["threat_type"],
                    "details": hash_threat["description"],
                    "source": "local_db"
                }
            
            # 2. Проверка через VirusTotal
            should_use_external = use_external_apis if use_external_apis is not None else self.use_external_apis
            if should_use_external:
                try:
                    external_result = await external_api_manager.check_file_hash_multiple_apis(file_hash)
                    
                    if not external_result.get("safe", True):
                        # Сохраняем угрозу в локальную базу для будущих проверок
                        db_manager.add_malicious_hash(
                            file_hash, 
                            external_result.get("threat_type", "malware"),
                            f"Detected by external scan: {external_result.get('details', '')}"
                        )
                        
                        return {
                            **external_result,
                            "source": "external_apis"
                        }
                    
                    # Если файл чистый по внешним проверкам
                    result = {
                        "safe": True,
                        "threat_type": None,
                        "details": "File hash not found in any malware database",
                        "source": "external_apis",
                        "confidence": external_result.get("confidence", 90)
                    }
                    self._cache_set(cache_key, result)
                    return result
                    
                except Exception as e:
                    logger.error(f"External file hash check failed: {e}")
                    # Продолжаем с локальным результатом
            
            # 3. Локальный результат если внешние API недоступны
            result = {
                "safe": True,
                "threat_type": None,
                "details": "File hash not found in local malware database",
                "source": "local_db_only"
            }
            self._cache_set(cache_key, result)
            return result
            
        except Exception as e:
            # КРИТИЧНО: Детальное логирование ошибок анализа файла
            import traceback
            error_trace = traceback.format_exc()
            error_type = type(e).__name__
            
            logger.error(
                f"❌ File hash analysis error for {file_hash}:\n"
                f"  Type: {error_type}\n"
                f"  Message: {str(e)}\n"
                f"  Traceback:\n{error_trace}",
                exc_info=True
            )
            
            # Возвращаем безопасный результат вместо падения
            return {
                "safe": None,  # None означает "неизвестно"
                "threat_type": "analysis_error",
                "details": f"Analysis temporarily unavailable: {error_type}",
                "source": "error"
            }
    
    # ... остальные методы остаются аналогичными, но с добавлением async/await ...

    async def analyze_uploaded_file(self, file_content: bytes, original_filename: str) -> Dict[str, Any]:
        """Анализ загруженного файла: вычисление SHA-256/MD5/SHA1, базовая типизация и проверка по базам/внешним API."""
        try:
            sanitized_name = security_validator.sanitize_filename(original_filename)
            sha256_hash = hashlib.sha256(file_content).hexdigest()
            md5_hash = hashlib.md5(file_content).hexdigest()
            sha1_hash = hashlib.sha1(file_content).hexdigest()

            # Простейшая идентификация типа файла
            file_type = "unknown"
            if file_content.startswith(b"PK\x03\x04"):
                file_type = "zip_archive"
            elif file_content.startswith(b"MZ"):
                file_type = "win_pe"
            elif file_content.startswith(b"%PDF"):
                file_type = "pdf"
            elif file_content.startswith(b"#!/bin/bash") or file_content.startswith(b"#!/bin/sh"):
                file_type = "shell_script"
            elif b"powershell" in file_content.lower():
                file_type = "powershell_script"

            # YARA-сканирование
            yara_result = self._scan_with_yara_rules(file_content)

            # Проверка по sha256
            hash_result = await self.analyze_file_hash(sha256_hash)

            # Поведенческий анализ
            behavioral_score = self._behavioral_analysis(file_content, file_type)

            # Объединяем результаты
            final_safe = hash_result.get("safe", True) and not yara_result["is_suspicious"] and behavioral_score < 50
            final_threat_type = None
            if not hash_result.get("safe", True):
                final_threat_type = hash_result.get("threat_type", "malware")
            elif yara_result["is_suspicious"]:
                final_threat_type = "suspicious_content"
            elif behavioral_score >= 50:
                final_threat_type = "suspicious_behavior"

            # Создаем базовый результат
            base_result = {
                "filename": sanitized_name,
                "file_hash": sha256_hash,
                "md5": md5_hash,
                "sha1": sha1_hash,
                "file_type": file_type,
                "safe": final_safe,
                "threat_type": final_threat_type,
                "details": hash_result.get("details", ""),
                "source": "combined_analysis",
                "yara_detections": yara_result["detected_rules"],
                "behavioral_score": behavioral_score,
                "confidence": self._calculate_confidence(hash_result, yara_result, behavioral_score)
            }
            
            # Добавляем взвешенную оценку риска
            risk_assessment = self._calculate_risk_score(base_result)
            base_result.update(risk_assessment)
            
            return base_result
        except Exception as e:
            # КРИТИЧНО: Детальное логирование ошибок анализа загруженного файла
            import traceback
            error_trace = traceback.format_exc()
            error_type = type(e).__name__
            
            logger.error(
                f"❌ Uploaded file analysis error for {original_filename}:\n"
                f"  Type: {error_type}\n"
                f"  Message: {str(e)}\n"
                f"  Traceback:\n{error_trace}",
                exc_info=True
            )
            
            # Возвращаем безопасный результат вместо падения
            return {
                "filename": original_filename,
                "safe": None,  # None означает "неизвестно"
                "threat_type": "analysis_error",
                "details": f"Analysis temporarily unavailable: {error_type}",
                "source": "error",
            }

    def _url_heuristic_analysis(self, url: str, domain: str) -> Dict[str, Any]:
        """Смягчённая эвристика анализа URL для снижения ложных срабатываний"""
        threat_score = 0
        details = []

        # IP-адрес вместо домена — сильный сигнал, но редкий в нормальном серфинге
        if re.match(r"^\d+\.\d+\.\d+\.\d+$", domain):
            threat_score += 50
            details.append("Uses IP address instead of domain")

        # Очень длинные URL — учитываем только экстремальные случаи
        if len(url) > 300:
            threat_score += 20
            details.append("URL is extremely long")
        elif len(url) > 200:
            threat_score += 10
            details.append("URL is very long")

        # Много поддоменов — повышаем пороги
        subdomain_count = len(domain.split('.'))
        if subdomain_count > 6:
            threat_score += 20
            details.append("Too many subdomains (>6)")
        elif subdomain_count > 4:
            threat_score += 10
            details.append("Many subdomains (>4)")

        # Дефисы в домене больше не считаем признаком сами по себе

        # Подозрительные TLD — оставляем как слабый сигнал
        suspicious_tlds = {"zip", "review", "click", "xyz", "top", "work"}
        tld = domain.split('.')[-1] if '.' in domain else ''
        if tld in suspicious_tlds:
            threat_score += 10
            details.append(f"Suspicious TLD: .{tld}")

        # Наличие '@' в URL — сильный сигнал
        if '@' in url:
            threat_score += 30
            details.append("Contains '@' symbol in URL")

        # Количество параметров — учитываем только очень большое число
        try:
            from urllib.parse import urlparse, parse_qs
            q = parse_qs(urlparse(url).query)
            if len(q) > 30:
                threat_score += 20
                details.append("Too many query parameters (>30)")
            elif len(q) > 20:
                threat_score += 10
                details.append("Many query parameters (>20)")
        except Exception:
            pass

        # Гораздо более высокий порог срабатывания, чтобы не метить обычные сайты
        if threat_score >= 70:
            return {
                "safe": False,
                "threat_type": "suspicious",
                "details": f"Heuristic detection: {', '.join(details)}",
                "threat_score": threat_score,
                "confidence": min(95, 50 + threat_score)  # Higher confidence for higher threat scores
            }

        return {
            "safe": True,
            "threat_type": None,
            "details": "Heuristic analysis passed",
            "threat_score": threat_score,
            "confidence": max(50, 100 - threat_score)  # Higher confidence for lower threat scores
        }

    def _behavioral_analysis(self, file_content: bytes, file_type: str) -> int:
        """Поведенческий анализ файла"""
        score = 0
        
        # Анализ размера файла
        if len(file_content) > 50 * 1024 * 1024:  # > 50MB
            score += 20
        elif len(file_content) < 100:  # < 100 bytes
            score += 15
        
        # Анализ энтропии (простая проверка)
        if self._calculate_entropy(file_content) > 7.5:
            score += 25  # Высокая энтропия может указывать на шифрование/упаковку
        
        # Анализ строк
        suspicious_strings = [
            b"cmd.exe", b"powershell", b"reg add", b"net user", 
            b"schtasks", b"wmic", b"rundll32", b"certutil"
        ]
        for suspicious in suspicious_strings:
            if suspicious in file_content.lower():
                score += 10
        
        # Анализ по типу файла
        if file_type == "win_pe":
            score += 5  # PE файлы потенциально опасны
        elif file_type == "powershell_script":
            score += 20  # PowerShell скрипты часто используются для атак
        elif file_type == "shell_script":
            score += 15  # Shell скрипты могут быть опасны
        
        return min(score, 100)  # Максимум 100 баллов

    def _calculate_entropy(self, data: bytes) -> float:
        """Вычисление энтропии данных"""
        if not data:
            return 0.0
        
        # Подсчет частоты байтов
        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1
        
        # Вычисление энтропии: -sum(p * log2(p))
        import math
        entropy = 0.0
        data_len = len(data)
        for count in byte_counts:
            if count > 0:
                probability = count / data_len
                entropy -= probability * math.log2(probability)
        
        return entropy

    def _calculate_confidence(self, hash_result: Dict[str, Any], yara_result: Dict[str, Any], behavioral_score: int) -> int:
        """Вычисление общей уверенности в результате"""
        confidence_scores = []
        
        # Уверенность от хэш-проверки
        if hash_result.get("safe", True):
            confidence_scores.append(90)
        else:
            confidence_scores.append(95)  # Высокая уверенность в детектировании по хэшу
        
        # Уверенность от YARA
        if yara_result["is_suspicious"]:
            confidence_scores.append(80)
        else:
            confidence_scores.append(70)
        
        # Уверенность от поведенческого анализа
        if behavioral_score >= 50:
            confidence_scores.append(75)
        else:
            confidence_scores.append(85)
        
        return sum(confidence_scores) // len(confidence_scores)

    def _calculate_risk_score(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Взвешенная оценка риска с объяснениями"""
        risk_factors = []
        total_score = 0
        
        # Фактор 1: Хэш-проверка (вес 40%)
        if not results.get("safe", True):
            hash_score = 80
            risk_factors.append({
                "factor": "hash_database",
                "weight": 40,
                "score": hash_score,
                "description": "File hash found in malware database"
            })
            total_score += hash_score * 0.4
        
        # Фактор 2: YARA детекции (вес 30%)
        yara_detections = results.get("yara_detections", [])
        if yara_detections:
            yara_score = min(90, len(yara_detections) * 20)
            risk_factors.append({
                "factor": "yara_signatures",
                "weight": 30,
                "score": yara_score,
                "description": f"Detected {len(yara_detections)} suspicious patterns"
            })
            total_score += yara_score * 0.3
        
        # Фактор 3: Поведенческий анализ (вес 20%)
        behavioral_score = results.get("behavioral_score", 0)
        if behavioral_score > 0:
            risk_factors.append({
                "factor": "behavioral_analysis",
                "weight": 20,
                "score": behavioral_score,
                "description": f"Behavioral analysis score: {behavioral_score}"
            })
            total_score += behavioral_score * 0.2
        
        # Фактор 4: Тип файла (вес 10%)
        file_type = results.get("file_type", "unknown")
        type_scores = {
            "win_pe": 60,
            "powershell_script": 70,
            "shell_script": 50,
            "zip_archive": 30,
            "pdf": 20,
            "unknown": 10
        }
        type_score = type_scores.get(file_type, 10)
        risk_factors.append({
            "factor": "file_type",
            "weight": 10,
            "score": type_score,
            "description": f"File type: {file_type}"
        })
        total_score += type_score * 0.1
        
        # Определяем уровень риска
        if total_score >= 80:
            risk_level = "critical"
        elif total_score >= 60:
            risk_level = "high"
        elif total_score >= 40:
            risk_level = "medium"
        elif total_score >= 20:
            risk_level = "low"
        else:
            risk_level = "minimal"
        
        return {
            "risk_score": int(total_score),
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "explanation": self._generate_risk_explanation(risk_level, risk_factors)
        }
    
    def _generate_risk_explanation(self, risk_level: str, risk_factors: List[Dict[str, Any]]) -> str:
        """Генерация объяснения уровня риска"""
        explanations = {
            "critical": "Критический риск: файл содержит известные вредоносные сигнатуры или демонстрирует крайне подозрительное поведение",
            "high": "Высокий риск: файл имеет множественные признаки вредоносности",
            "medium": "Средний риск: файл демонстрирует некоторые подозрительные характеристики",
            "low": "Низкий риск: файл имеет минимальные подозрительные признаки",
            "minimal": "Минимальный риск: файл не демонстрирует признаков вредоносности"
        }
        
        base_explanation = explanations.get(risk_level, "Неизвестный уровень риска")
        
        if risk_factors:
            factor_descriptions = [f["description"] for f in risk_factors if f["score"] > 20]
            if factor_descriptions:
                base_explanation += f". Основные факторы риска: {', '.join(factor_descriptions)}"
        
        return base_explanation

# Создаем экземпляр сервиса с включенными внешними API
analysis_service = AnalysisService(use_external_apis=True)