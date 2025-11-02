#!/usr/bin/env python3
# test_config.py
import sys
import os
sys.path.append('antivirus-core')

try:
    from app.config import logging_config, security_config
    print("✅ Config imports OK")
    print(f"Log level: {logging_config.LOG_LEVEL}")
    print(f"Max URL length: {security_config.MAX_URL_LENGTH}")
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
