// background.js
const DEFAULTS = { antivirusEnabled: true, linkCheck: true, hoverScan: true, notify: true };

// Кеш результатов для быстрого анализа по наведению
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 минут

function getCached(url) {
  const cached = cache.get(url);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }
  cache.delete(url);
  return null;
}

function setCached(url, data) {
  cache.set(url, { data, timestamp: Date.now() });
}

function getConfig() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(DEFAULTS, (cfg) => resolve(cfg));
  });
}

async function getApiKey() {
  const storage = await new Promise(r => chrome.storage.sync.get(['apiKey'], r));
  return storage.apiKey || '';
}

async function getApiBase() {
  const storage = await new Promise(r => chrome.storage.sync.get(['apiBase'], r));
  return storage.apiBase || 'https://45.87.247.88/proxy';
}

async function scanUrl(url, useCache = true) {
  if (useCache) {
    const cached = getCached(url);
    if (cached) return cached;
  }
  const apiKey = await getApiKey();
  const apiBase = await getApiBase();
  try {
    const headers = { 'Content-Type': 'application/json' };
    if (apiKey) headers['X-API-Key'] = apiKey;
    const res = await fetch(`${apiBase.replace(/\/$/, '')}/check/url`, {
      method: 'POST', headers, body: JSON.stringify({ url })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const data = await res.json();
    setCached(url, data);
    return data;
  } catch (e) {
    return { safe: null, details: e.message, source: 'error' };
  }
}

function fetchWithTimeout(resource, options = {}, timeoutMs = 800) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);
  const opts = { ...options, signal: controller.signal };
  return fetch(resource, opts).finally(() => clearTimeout(id));
}

async function scanHover(url) {
  const apiKey = await getApiKey();
  const apiBase = await getApiBase();
  const headers = { 'Content-Type': 'application/json' };
  if (apiKey) headers['X-API-Key'] = apiKey;

  const basicReq = async (retry = true) => {
    try {
      const res = await fetchWithTimeout(`${apiBase.replace(/\/$/, '')}/check/url`, {
        method: 'POST', headers, body: JSON.stringify({ url })
      }, 5000);
      if (!res.ok) throw new Error(`url ${res.status}`);
      return res.json();
    } catch (e) {
      if (retry && (e.name === 'AbortError' || String(e).includes('timeout'))) {
        return basicReq(false);
      }
      throw e;
    }
  };

  try {
    const result = await basicReq();
    return result;
  } catch (err) {
    console.error('Hover scan error:', err);
    return { safe: null, details: String(err), source: 'error' };
  }
}

function maybeNotify(cfg, verdict, url) {
  if (!cfg.notify) return;
  if (verdict === 'malicious' || verdict === 'suspicious') {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon-48.png',
      title: verdict === 'malicious' ? 'Опасная ссылка' : 'Подозрительная ссылка',
      message: `${url}`
    });
  }
}

chrome.runtime.onMessage.addListener((msg, sender) => {
  if (msg && msg.type === 'antivirus_toggle') {
    chrome.storage.sync.get(DEFAULTS, (cfg) => {
      cfg.antivirusEnabled = msg.enabled;
      chrome.storage.sync.set(cfg);
    });
    return;
  }

  if (msg && msg.type === 'settings_updated') {
    chrome.storage.sync.set(msg.settings);
    return;
  }

  if (msg && msg.type === 'check_url') {
    const url = msg.url;
    getConfig().then(async (cfg) => {
      if (!cfg.antivirusEnabled || !cfg.linkCheck) return;
      const res = await scanUrl(url, false);
      const verdict = res.safe === false ? 'malicious' : res.safe === true ? 'clean' : 'unknown';
      maybeNotify(cfg, verdict, url);
    });
  }

  if (msg && msg.type === 'hover_url') {
    const url = msg.url;
    const tabId = sender && sender.tab && sender.tab.id;
    
    getConfig().then(async (cfg) => {
      if (!cfg.antivirusEnabled || !cfg.hoverScan) {
        return;
      }
      
      const apiKey = await getApiKey();
      if (!apiKey) return; // без ключа не запускаем ничего и не шлём hover_result
      
      try {
        const cached = getCached(url);
        const res = cached || await scanHover(url);
        
        if (!cached && res) setCached(url, res);
        if (tabId != null && res) {
          chrome.tabs.sendMessage(tabId, { type: 'hover_result', url, res, mouseX: msg.mouseX, mouseY: msg.mouseY });
        }
      } catch (e) {
        console.error('Hover processing error:', e);
        // молчим без отправки результата, чтобы не было анимации
      }
    });
  }
});

// Ensure content script is active on already open tabs after extension restart/update or browser startup
async function reinjectContentScriptIntoAllTabs() {
  try {
    const tabs = await new Promise(resolve => chrome.tabs.query({ url: ['http://*/*', 'https://*/*'] }, resolve));
    for (const tab of tabs) {
      try {
        if (!tab.id) continue;
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          files: ['content_script.js']
        });
      } catch (e) {
        // Ignore tabs where injection is not allowed
      }
    }
  } catch (e) {
    console.error('Failed to reinject content scripts:', e);
  }
}

chrome.runtime.onInstalled.addListener(() => {
  reinjectContentScriptIntoAllTabs();
});

chrome.runtime.onStartup.addListener(() => {
  reinjectContentScriptIntoAllTabs();
});

async function checkUrlSafety(url) {
  try {
    const response = await fetch(`${API_BASE_URL}/check/url`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
      },
      body: JSON.stringify({ url: url })
    });

    const result = await response.json();
    
    if (!result.safe) {
      // Показываем предупреждение
      chrome.notifications.create({
        type: "basic",
        iconUrl: "icons/warning-48.png",
        title: "Опасная ссылка!",
        message: `Обнаружена угроза: ${result.threat_type}`
      });
    }
    
    return result;
  } catch (error) {
    console.error("Check failed:", error);
    return { safe: true, error: "Check failed" };
  }
}