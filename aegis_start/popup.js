// popup.js
(function() {
  const statusText = document.getElementById('status');
  const statusBadge = document.getElementById('status-badge');
  const resultEl = document.getElementById('result');
  const antivirusToggle = document.getElementById('antivirus-toggle');
  const toggleSubtitle = document.getElementById('toggle-subtitle');
  const statusDot = document.getElementById('status-dot');
  const connectionText = document.getElementById('connection-text');

  // Default settings
  const defaults = {
    antivirusEnabled: true,
    linkCheck: true,
    notify: true,
    apiBase: 'https://45.87.247.88/proxy',
    apiKey: ''
  };

  function setBadge(state) {
    if (statusBadge) {
      statusBadge.className = `badge ${state}`;
      const map = { ready: 'READY', scanning: 'SCANNING', safe: 'SAFE', suspicious: 'SUSPICIOUS', malicious: 'MALICIOUS', disabled: 'DISABLED' };
      statusBadge.textContent = map[state] || 'READY';
    }
  }

  function updateToggleState(enabled) {
    if (antivirusToggle) {
      antivirusToggle.checked = enabled;
    }
    const toggleTitle = document.querySelector('.toggle-title');
    if (toggleTitle) {
      toggleTitle.textContent = enabled ? 'Защита активна' : 'Защита отключена';
    }
    if (toggleSubtitle) {
      toggleSubtitle.textContent = enabled ? 'Сканирование ссылок и загрузок' : 'Все проверки отключены';
    }
    setBadge(enabled ? 'ready' : 'disabled');
  }

  function updateConnectionStatus(status, message) {
    if (statusDot) {
      statusDot.className = `status-dot ${status}`;
    }
    if (connectionText) {
      connectionText.textContent = message;
    }
  }

  async function loadSettings() {
    return new Promise((resolve) => {
      chrome.storage.sync.get(defaults, (settings) => {
        resolve(settings);
      });
    });
  }

  async function saveSettings(settings) {
    return new Promise((resolve) => {
      chrome.storage.sync.set(settings, () => {
        resolve();
      });
    });
  }

  async function checkConnection() {
    updateConnectionStatus('checking', 'Проверка подключения...');
    try {
      const settings = await loadSettings();
      const apiUrl = (settings.apiBase || 'https://45.87.247.88/proxy').replace(/\/$/, '');
      const res = await fetch(`${apiUrl}/health`, { method: 'GET' });
      if (res.ok) {
        updateConnectionStatus('online', 'Подключено к API');
      } else {
        updateConnectionStatus('offline', `API недоступен (${res.status})`);
      }
    } catch (e) {
      console.error('API connection error:', e);
      updateConnectionStatus('offline', 'Нет подключения к API');
    }
  }

  function createThreatLevel(verdict) {
    const threatLevel = document.createElement('div');
    threatLevel.className = `threat-level ${verdict}`;
    
    const icons = {
      safe: '✓',
      clean: '✓', 
      suspicious: '⚠',
      malicious: '✗',
      unknown: '?'
    };
    
    const labels = {
      safe: 'Безопасно',
      clean: 'Безопасно',
      suspicious: 'Подозрительно', 
      malicious: 'Опасно',
      unknown: 'Неизвестно'
    };
    
    threatLevel.innerHTML = `${icons[verdict] || '?'} ${labels[verdict] || 'Неизвестно'}`;
    return threatLevel;
  }

  function createEngineResults(engines) {
    if (!engines || typeof engines !== 'object') return null;
    
    const container = document.createElement('div');
    container.className = 'engine-results';
    
    Object.entries(engines).forEach(([name, verdict]) => {
      const item = document.createElement('div');
      item.className = 'engine-item';
      
      const nameEl = document.createElement('div');
      nameEl.className = 'engine-name';
      nameEl.textContent = name;
      
      const verdictEl = document.createElement('div');
      verdictEl.className = 'engine-verdict';
      verdictEl.textContent = verdict;
      
      item.appendChild(nameEl);
      item.appendChild(verdictEl);
      container.appendChild(item);
    });
    
    return container;
  }

  function renderResult(url, response) {
    resultEl.innerHTML = '';
    if (!response) {
      const div = document.createElement('div');
      div.className = 'muted';
      div.textContent = 'Нет данных.';
      resultEl.appendChild(div);
      return;
    }

    // Create analysis card
    const analysisCard = document.createElement('div');
    analysisCard.className = 'analysis-card';

    // Determine verdict
    let verdict = 'unknown';
    if (response.result) verdict = response.result.toLowerCase();
    else if (response.verdict) verdict = response.verdict.toLowerCase();
    else if (response.safe === true) verdict = 'clean';
    else if (response.safe === false) verdict = 'malicious';

    setBadge(verdict === 'clean' ? 'safe' : verdict);

    // Add threat level
    const threatLevel = createThreatLevel(verdict);
    analysisCard.appendChild(threatLevel);

    // Add URL pill with hover details
    const pills = document.createElement('div');
    pills.className = 'pill-row';
    
    const urlPill = document.createElement('span');
    urlPill.className = 'pill hover-details';
    urlPill.innerHTML = `${new URL(url).hostname} <span class="hover-trigger">?</span>`;
    
    const hoverPopup = document.createElement('div');
    hoverPopup.className = 'hover-popup';
    hoverPopup.textContent = `Полный URL: ${url}`;
    urlPill.appendChild(hoverPopup);
    
    pills.appendChild(urlPill);

    // Add additional pills
    if (response.engine) {
      const enginePill = document.createElement('span');
      enginePill.className = 'pill';
      enginePill.textContent = `Движок: ${response.engine}`;
      pills.appendChild(enginePill);
    }
    
    if (typeof response.score !== 'undefined') {
      const scorePill = document.createElement('span');
      scorePill.className = 'pill';
      scorePill.textContent = `Риск: ${response.score}/100`;
      pills.appendChild(scorePill);
    }

    analysisCard.appendChild(pills);

    // Add engine results if available
    const engineResults = createEngineResults(response.external_scans || response.engines);
    if (engineResults) {
      analysisCard.appendChild(engineResults);
    }

    // Add key-value details
    const kv = document.createElement('div');
    kv.className = 'kv';
    
    function addKV(k, v) {
      const kk = document.createElement('div'); 
      kk.className = 'k'; 
      kk.textContent = k;
      const vv = document.createElement('div'); 
      vv.className = 'v'; 
      vv.textContent = String(v);
      kv.appendChild(kk); 
      kv.appendChild(vv);
    }

    if (typeof response.safe !== 'undefined') addKV('Безопасно', response.safe ? 'Да' : 'Нет');
    if (response.threat_type) addKV('Тип угрозы', response.threat_type);
    if (response.categories) addKV('Категории', Array.isArray(response.categories) ? response.categories.join(', ') : response.categories);
    if (response.details) addKV('Детали', typeof response.details === 'string' ? response.details : JSON.stringify(response.details));
    if (response.source) addKV('Источник', response.source);
    if (response.timestamp) addKV('Время', new Date(response.timestamp).toLocaleString());

    if (kv.children.length > 0) {
      analysisCard.appendChild(kv);
    }

    resultEl.appendChild(analysisCard);
  }

  async function scanActiveTab() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.url) return;
    const settings = await loadSettings();
    if (!settings.antivirusEnabled) {
      if (statusText) statusText.innerText = 'Защита отключена';
      setBadge('disabled');
      if (resultEl) resultEl.innerHTML = '<div class="muted">Включите защиту для сканирования</div>';
      return;
    }
    if (statusText) statusText.innerText = 'Сканируем...';
    setBadge('scanning');
    try {
      const apiUrl = (settings.apiBase || 'https://45.87.247.88/proxy').replace(/\/$/, '');
      const headers = { 'Content-Type': 'application/json' };
      if (settings.apiKey) headers['X-API-Key'] = settings.apiKey;
      const apiResponse = await fetch(`${apiUrl}/check/url`, {
        method: 'POST', headers, body: JSON.stringify({ url: tab.url })
      });
      if (apiResponse.ok) {
        const data = await apiResponse.json();
        if (statusText) statusText.innerText = 'Готово';
        renderResult(tab.url, data);
      } else {
        const errorData = await apiResponse.text();
        throw new Error(`API Error: ${apiResponse.status} - ${errorData}`);
      }
    } catch (e) {
      if (statusText) statusText.innerText = 'Ошибка: ' + e.message;
      setBadge('suspicious');
      if (resultEl) resultEl.innerHTML = `<div class="muted">Не удалось проверить URL: ${e.message}</div>`;
    }
  }

  // Event listeners
  if (antivirusToggle) {
    antivirusToggle.addEventListener('change', async (e) => {
      const settings = await loadSettings();
      settings.antivirusEnabled = e.target.checked;
      await saveSettings(settings);
      updateToggleState(settings.antivirusEnabled);
      
      // Update background script
      chrome.runtime.sendMessage({
        type: 'antivirus_toggle',
        enabled: settings.antivirusEnabled
      });
    });
  }

  // Listen for settings changes from options page
  chrome.storage.onChanged.addListener((changes, namespace) => {
    if (namespace === 'sync') {
      // Reload settings and update UI
      loadSettings().then(settings => {
        updateToggleState(settings.antivirusEnabled);
      });
    }
  });

  // Scan button event listener
  const scanButton = document.getElementById('scan-tab');
  if (scanButton) {
    scanButton.addEventListener('click', (e) => {
      e.preventDefault();
      // Visual feedback
      scanButton.style.transform = 'translateY(1px)';
      setTimeout(() => {
        scanButton.style.transform = '';
      }, 100);
      scanActiveTab();
    });
  }
  
  // Options button event listener
  const optionsButton = document.getElementById('open-options');
  if (optionsButton) {
    optionsButton.addEventListener('click', (e) => {
      e.preventDefault();
      try {
        if (chrome.runtime.openOptionsPage) {
          chrome.runtime.openOptionsPage();
        } else {
          window.open('options.html', '_blank');
        }
      } catch (error) {
        console.error('Error opening options:', error);
        window.open('options.html', '_blank');
      }
    });
  }
  
  // Logs button event listener
  const logsButton = document.getElementById('open-logs');
  if (logsButton) {
    logsButton.addEventListener('click', (e) => {
      e.preventDefault();
      try {
        chrome.tabs.create({ url: 'chrome://extensions-internals' });
      } catch (error) {
        console.error('Error opening logs:', error);
        // Fallback to extensions page
        chrome.tabs.create({ url: 'chrome://extensions/' });
      }
    });
  }

  // Initialize
  async function init() {
    try {
      const settings = await loadSettings();
      updateToggleState(settings.antivirusEnabled);
      await checkConnection();
      
      // Auto-scan on open if enabled
      if (settings.antivirusEnabled) {
        setTimeout(() => scanActiveTab(), 100); // Small delay to ensure UI is ready
      }
    } catch (error) {
      console.error('Initialization error:', error);
      if (statusText) statusText.innerText = 'Ошибка инициализации';
      setBadge('disabled');
    }
  }

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();