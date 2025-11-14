// content_script.js
// Enhanced content script with hover analysis and visual indicators

let tooltip = null;
let hoverTimeout = null;
let currentHoveredLink = null;
let lastMouseX = 0;
let lastMouseY = 0;

// Create hover analysis tooltip
function createHoverTooltip() {
  if (tooltip) return tooltip;
  
  tooltip = document.createElement('div');
  tooltip.id = 'safebrowse-tooltip';
  tooltip.style.cssText = `
    position: fixed;
    background: #131a2b;
    color: #e6ecff;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-family: system-ui, -apple-system, sans-serif;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    z-index: 10000;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.2s;
    max-width: 250px;
    white-space: normal;
    text-align: center;
  `;
  document.body.appendChild(tooltip);
  return tooltip;
}

// Update tooltip position and content
function updateTooltip(tooltip, x, y, content, type = 'info') {
  tooltip.innerHTML = content;
  
  const colors = {
    safe: '#2ecc71',
    suspicious: '#f1c40f', 
    malicious: '#ff5c5c',
    unknown: '#93a0c0',
    info: '#4f8cff'
  };
  
  // Use solid border color to avoid invalid rgba from hex
  tooltip.style.borderColor = colors[type] || '#4f8cff';
  
  // Only update position if coordinates are provided
  if (typeof x === 'number' && typeof y === 'number') {
    tooltip.style.left = x + 10 + 'px';
    tooltip.style.top = y - 30 + 'px';
  }
  tooltip.style.opacity = '1';
}

// Hide tooltip
function hideTooltip(tooltip) {
  tooltip.style.opacity = '0';
}

// Format analysis result for display - слова с описанием
function formatAnalysisResult(result, url) {
  if (!result) return '<span style="color: #93a0c0;">Неизвестно</span>';
  
  // Ошибка сети/таймаут → показываем как подозрительно, но только для явных сетевых ошибок
  if (result && result.source === 'error') {
    const msg = String(result.details || '').toLowerCase();
    const isNetwork = msg.includes('failed to fetch') || msg.includes('networkerror') || msg.includes('timeout') || msg.includes('превышено время ожидания');
    if (isNetwork) {
      const errorMsg = result.details || 'Не удалось подключиться к серверу';
      return `
        <div style="text-align: center; line-height: 1.2;">
          <div style="color: #f1c40f; font-weight: bold; font-size: 14px; margin-bottom: 2px;">⚠ Подозрительно</div>
          <div style="color: #93a0c0; font-size: 11px;">${errorMsg}</div>
        </div>
      `;
    }
  }
  
  let verdict = 'unknown';
  if (result.safe === true) verdict = 'safe';
  else if (result.safe === false) verdict = 'malicious';
  else if (result.result) verdict = result.result.toLowerCase();
  else if (result.verdict) verdict = result.verdict.toLowerCase();
  
  const verdicts = {
    safe: { text: 'Безопасно', color: '#2ecc71', description: 'Ссылка не содержит угроз' },
    clean: { text: 'Безопасно', color: '#2ecc71', description: 'Ссылка не содержит угроз' },
    suspicious: { text: 'Подозрительно', color: '#f39c12', description: 'Требует внимания' },
    malicious: { text: 'Опасно', color: '#e74c3c', description: 'Обнаружены угрозы' },
    unknown: { text: 'Неизвестно', color: '#93a0c0', description: 'Не удалось проверить' }
  };
  
  const info = verdicts[verdict] || verdicts.unknown;
  const details = result.details || result.source || '';
  
  return `
    <div style="text-align: center; line-height: 1.2;">
      <div style="color: ${info.color}; font-weight: bold; font-size: 14px; margin-bottom: 2px;">
        ${info.text}
      </div>
      <div style="color: #93a0c0; font-size: 11px;">
        ${info.description}
      </div>
      ${details ? `<div style="color: #93a0c0; font-size: 10px; margin-top: 2px;">${details}</div>` : ''}
    </div>
  `;
}

// Initialize tooltip when DOM is ready
function initTooltip() {
  if (document.body) {
    createHoverTooltip();
  } else {
    setTimeout(initTooltip, 100);
  }
}
// Persistent port so background doesn't unload
const aegisPort = chrome.runtime.connect({ name: "aegis-port" });

aegisPort.onMessage.addListener((msg) => {
  if (msg.type === "hover_result" &&
      currentHoveredLink &&
      currentHoveredLink.href === msg.url) {

    const content = formatAnalysisResult(msg.res, msg.url);
    const verdict = msg.res?.safe === false ? 'malicious'
                   : msg.res?.safe === true ? 'safe'
                   : msg.res?.result?.toLowerCase() || 'unknown';

    updateTooltip(
      tooltip,
      msg.mouseX,
      msg.mouseY,
      content,
      verdict
    );
  }
});
// Enhanced link hover detection
document.addEventListener('mouseover', (e) => {
  const link = e.target.closest('a');
  if (!link || !link.href) return;
  if (!/^https?:/i.test(link.href)) return;
  
  // Check if hover analysis is enabled (не требуем ключ)
  chrome.storage.sync.get(['hoverScan', 'antivirusEnabled'], (result) => {
    if (!result.antivirusEnabled || !result.hoverScan) {
      return;
    }
    
    // Ensure tooltip is initialized
    if (!tooltip) {
      createHoverTooltip();
    }
    
    currentHoveredLink = link;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
    
    // Clear existing timeout
    if (hoverTimeout) {
      clearTimeout(hoverTimeout);
    }
    
    // Show tooltip immediately with loading state
    updateTooltip(tooltip, lastMouseX, lastMouseY, 'Проверка...', 'info');
    
    // Send hover message to background with mouse coords
    hoverTimeout = setTimeout(() => {
      chrome.runtime.sendMessage({
        type: 'hover_url', 
        url: link.href,
        mouseX: lastMouseX,
        mouseY: lastMouseY
      });
    }, 200); // Slightly faster debounce
  });
});

// Handle mouse leave
document.addEventListener('mouseout', (e) => {
  const link = e.target.closest && e.target.closest('a');
  if (!link || !link.href) return;
  
  // If moving within the same link, do nothing
  if (e.relatedTarget && link.contains(e.relatedTarget)) {
    return;
  }
  
  if (hoverTimeout) {
    clearTimeout(hoverTimeout);
    hoverTimeout = null;
  }
  
  if (tooltip) {
    hideTooltip(tooltip);
  }
  try { link.style.outline = ''; } catch(_) {}
  currentHoveredLink = null;
});

// Handle mouse move to update tooltip position
document.addEventListener('mousemove', (e) => {
  lastMouseX = e.clientX;
  lastMouseY = e.clientY;
  if (tooltip && tooltip.style.opacity === '1') {
    tooltip.style.left = lastMouseX + 10 + 'px';
    tooltip.style.top = lastMouseY - 30 + 'px';
  }
});

// Listen for analysis results from background
chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === 'hover_result' && currentHoveredLink && currentHoveredLink.href === msg.url) {
    if (!tooltip) {
      createHoverTooltip();
    }
    const content = formatAnalysisResult(msg.res, msg.url);
    let verdict = msg.res?.safe === false ? 'malicious' : 
                  msg.res?.safe === true ? 'safe' : 
                  msg.res?.result?.toLowerCase() || 'unknown';
    if (msg.res && msg.res.source === 'error') {
      const m = String(msg.res.details || '').toLowerCase();
      if (m.includes('failed to fetch') || m.includes('networkerror') || m.includes('timeout') || m.includes('превышено время ожидания')) {
        verdict = 'suspicious';
      }
    }
    // Update content and styling; if coords passed, snap to them for accuracy
    const x = typeof msg.mouseX === 'number' ? msg.mouseX : undefined;
    const y = typeof msg.mouseY === 'number' ? msg.mouseY : undefined;
    updateTooltip(tooltip, x, y, content, verdict);
  }
});

// Click handler for URL checking
document.addEventListener('click', (e) => {
  const a = e.target.closest && e.target.closest('a');
  if (!a || !a.href) return;
  if (!/^https?:/i.test(a.href)) return;
  chrome.runtime.sendMessage({type: 'check_url', url: a.href});
}, true);
// Visual indicator for dangerous links
function addVisualIndicator(link, verdict) {
  if (link.dataset.safebrowseIndicator) return; // Already processed
  
  const indicator = document.createElement('span');
  indicator.style.cssText = `
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-left: 4px;
    vertical-align: middle;
  `;
  
  if (verdict === 'malicious') {
    indicator.style.background = '#ff5c5c';
    indicator.title = 'Опасная ссылка';
  } else if (verdict === 'suspicious') {
    indicator.style.background = '#f1c40f';
    indicator.title = 'Подозрительная ссылка';
  } else {
    indicator.style.background = '#2ecc71';
    indicator.title = 'Безопасная ссылка';
  }
  
  link.appendChild(indicator);
  link.dataset.safebrowseIndicator = 'true';
}

// Initialize tooltip when script loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initTooltip);
} else {
  initTooltip();
}
