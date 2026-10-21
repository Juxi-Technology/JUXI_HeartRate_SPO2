/* JUXI 心率血氧传感器 —— 浏览器上位机（Web Serial）+ 文档浏览器 */
(function () {
  'use strict';

  /* ==================== i18n ==================== */
  var I18N = {
    en: {
      tabTool: 'Web Tool',
      tabDocs: 'Docs',
      secSettings: 'Serial Port',
      baud: 'Baud rate',
      connect: 'Connect',
      disconnect: 'Disconnect',
      browserNote: 'Requires desktop Chrome or Edge (Web Serial). Safari and Firefox are not supported. Connect the sensor through a USB-to-TTL adapter and make sure its driver is installed.',
      secControl: 'Module Control',
      startCollect: 'Start Collection',
      stopCollect: 'Stop Collection',
      startMonitor: 'Start Monitoring',
      stopMonitor: 'Stop Monitoring',
      secTip: 'Usage Tips',
      tip: '1. Wiring: VCC -> 5V, GND -> GND, TX -> RX, RX -> TX\n2. Click Connect, choose the USB serial device in the browser dialog\n3. Start Collection lights the LED, then put your finger on the sensor',
      secData: 'Real-time Data',
      spo2: 'Blood Oxygen (SPO2)',
      hr: 'Heart Rate',
      hrUnit: 'BPM',
      temp: 'Temperature',
      status: 'Status',
      stDisconnected: 'Disconnected',
      stConnecting: 'Waiting for device selection...',
      stConnected: 'Connected, ready to collect',
      stCollecting: 'Collecting, LED is on',
      stCollectStopped: 'Collection stopped, LED is off',
      stMonitoring: 'Monitoring...',
      stMonitorStopped: 'Monitoring stopped',
      stError: 'Error',
      stLost: 'Device disconnected',
      stUnsupported: 'This browser does not support Web Serial',
      phNone: 'No device selected',
      phDevice: 'USB device',
      connectFail: 'Connection failed: ',
      language: 'Language',
      docLoading: 'Loading...',
      docFailed: 'Failed to load this page: ',
      filterLabel: 'Filter',
    },
    zh: {
      tabTool: '上位机',
      tabDocs: '使用文档',
      secSettings: '串口设置',
      baud: '波特率',
      connect: '连接串口',
      disconnect: '断开连接',
      browserNote: '需要桌面版 Chrome 或 Edge（Web Serial）。Safari、Firefox 不支持。请通过 USB 转 TTL 转接板连接传感器，并确认已安装驱动。',
      secControl: '模块控制',
      startCollect: '启动采集',
      stopCollect: '关闭采集',
      startMonitor: '开始监测',
      stopMonitor: '停止监测',
      secTip: '使用提示',
      tip: '1. 接线：VCC -> 5V, GND -> GND, TX -> RX, RX -> TX\n2. 点击「连接串口」，在浏览器弹窗中选择 USB 串口设备\n3. 「启动采集」后模块 LED 点亮，请将手指放在传感器上',
      secData: '实时数据',
      spo2: '血氧 (SPO2)',
      hr: '心率',
      hrUnit: '次/分',
      temp: '温度',
      status: '状态',
      stDisconnected: '未连接',
      stConnecting: '等待选择设备...',
      stConnected: '已连接，待采集',
      stCollecting: '采集已启动，LED已亮',
      stCollectStopped: '采集已关闭，LED已灭',
      stMonitoring: '正在监测...',
      stMonitorStopped: '监测已停止',
      stError: '错误',
      stLost: '设备已断开',
      stUnsupported: '当前浏览器不支持 Web Serial',
      phNone: '未选择设备',
      phDevice: 'USB 设备',
      connectFail: '连接失败：',
      language: '语言',
      docLoading: '加载中…',
      docFailed: '加载失败：',
      filterLabel: '滤波'
    }
  };

  var uiLang = localStorage.getItem('juxi.uiLang') || (/^zh/i.test(navigator.language) ? 'zh' : 'en');
  if (!I18N[uiLang]) uiLang = 'en';

  function t(key) {
    return (I18N[uiLang] && I18N[uiLang][key]) || (I18N.en[key] || key);
  }

  var $ = function (sel) { return document.querySelector(sel); };

  /* ==================== 通用状态 ==================== */
  var statusKey = 'stDisconnected';
  var statusClass = '';

  function setStatus(key, cls) {
    statusKey = key;
    statusClass = cls || '';
    var el = $('#statusText');
    el.textContent = t(key);
    el.removeAttribute('data-i18n');
    $('#statusDot').className = 'status-dot ' + statusClass;
  }

  function applyI18n() {
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      el.textContent = t(el.getAttribute('data-i18n'));
    });
    $('#tab-tool').textContent = t('tabTool');
    $('#tab-docs').textContent = t('tabDocs');
    document.querySelectorAll('#uiLangSwitch button').forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-lang') === uiLang);
    });
    setStatus(statusKey, statusClass);
    renderFilterInfo();
    refreshControls();
  }

  /* ==================== Web Serial ==================== */
  var CMD = {
    start: [0x20, 0x10, 0x00, 0x10, 0x00, 0x01, 0x02, 0x00, 0x01],
    stop: [0x20, 0x10, 0x00, 0x10, 0x00, 0x01, 0x02, 0x00, 0x02],
    hr: [0x20, 0x03, 0x00, 0x06, 0x00, 0x04],
    temp: [0x20, 0x03, 0x00, 0x0A, 0x00, 0x01]
  };

  var port = null;
  var writer = null;
  var reader = null;
  var rxBuf = new Uint8Array(0);
  var reading = false;
  var connected = false;
  var collecting = false;
  var monitoring = false;

  function crc16(bytes) {
    var crc = 0xFFFF;
    for (var i = 0; i < bytes.length; i++) {
      crc ^= bytes[i];
      for (var b = 0; b < 8; b++) {
        crc = (crc & 1) ? ((crc >>> 1) ^ 0xA001) : (crc >>> 1);
      }
    }
    return crc;
  }

  function withCrc(bytes) {
    var crc = crc16(bytes);
    return new Uint8Array(bytes.concat([crc & 0xFF, (crc >> 8) & 0xFF]));
  }

  function crcOk(frame) {
    if (frame.length < 3) return false;
    var body = Array.prototype.slice.call(frame, 0, frame.length - 2);
    var crc = crc16(body);
    return frame[frame.length - 2] === (crc & 0xFF) && frame[frame.length - 1] === (crc >> 8) & 0xFF;
  }

  function pushRx(chunk) {
    var next = new Uint8Array(rxBuf.length + chunk.length);
    next.set(rxBuf);
    next.set(chunk, rxBuf.length);
    rxBuf = next;
  }

  /* 从接收缓冲里取出一帧：20 03 <byteCount> <data...> <crcLo> <crcHi> */
  function takeFrame(byteCount) {
    var need = byteCount + 5;
    for (;;) {
      var idx = -1;
      for (var i = 0; i + 2 < rxBuf.length; i++) {
        if (rxBuf[i] === 0x20 && rxBuf[i + 1] === 0x03 && rxBuf[i + 2] === byteCount) {
          idx = i;
          break;
        }
      }
      if (idx < 0) {
        if (rxBuf.length > 512) rxBuf = rxBuf.slice(-16);
        return null;
      }
      if (rxBuf.length - idx < need) {
        if (idx > 0) rxBuf = rxBuf.slice(idx);
        return null;
      }
      var frame = rxBuf.slice(idx, idx + need);
      rxBuf = rxBuf.slice(idx + need);
      if (crcOk(frame)) return frame;
    }
  }

  function sleep(ms) {
    return new Promise(function (r) { setTimeout(r, ms); });
  }

  async function waitFrame(byteCount, timeoutMs) {
    var until = performance.now() + timeoutMs;
    while (performance.now() < until) {
      var f = takeFrame(byteCount);
      if (f) return f;
      await sleep(15);
    }
    return null;
  }

  async function send(cmd) {
    await writer.write(withCrc(cmd));
  }

  async function readLoop() {
    reading = true;
    try {
      reader = port.readable.getReader();
      while (reading) {
        var res = await reader.read();
        if (res.done) break;
        if (res.value) pushRx(res.value);
      }
    } catch (e) {
      if (reading && connected) handleLost();
    } finally {
      reading = false;
      if (reader) {
        try { reader.releaseLock(); } catch (e) { /* ignore */ }
        reader = null;
      }
    }
  }

  async function connect() {
    if (!('serial' in navigator)) {
      setStatus('stUnsupported', 'error');
      return;
    }
    var baud = parseInt($('#baud').value, 10) || 9600;
    setStatus('stConnecting', '');
    try {
      port = await navigator.serial.requestPort();
      await port.open({ baudRate: baud, dataBits: 8, stopBits: 1, parity: 'none', flowControl: 'none' });
    } catch (e) {
      port = null;
      if (e && e.name === 'NotFoundError') {
        setStatus('stDisconnected', '');
      } else {
        setStatus('stDisconnected', 'error');
        alert(t('connectFail') + (e && e.message ? e.message : e));
      }
      refreshControls();
      return;
    }
    rxBuf = new Uint8Array(0);
    resetFilters();
    writer = port.writable.getWriter();
    connected = true;
    collecting = false;
    monitoring = false;
    readLoop();
    setStatus('stConnected', 'connected');
    showPortInfo();
    refreshControls();
  }

  async function disconnect() {
    monitoring = false;
    collecting = false;
    reading = false;
    try { if (reader) await reader.cancel(); } catch (e) { /* ignore */ }
    try { if (writer) writer.releaseLock(); } catch (e) { /* ignore */ }
    try { if (port) await port.close(); } catch (e) { /* ignore */ }
    writer = null;
    reader = null;
    port = null;
    connected = false;
    setStatus('stDisconnected', '');
    showPortInfo();
    refreshControls();
  }

  function handleLost() {
    monitoring = false;
    collecting = false;
    connected = false;
    port = null;
    writer = null;
    setStatus('stLost', 'error');
    showPortInfo();
    refreshControls();
  }

  function showPortInfo() {
    var el = $('#portHint');
    if (!port) {
      el.textContent = t('phNone');
      return;
    }
    var info = port.getInfo ? port.getInfo() : {};
    if (info.usbVendorId && info.usbProductId) {
      var hex = function (v) { return ('000' + v.toString(16).toUpperCase()).slice(-4); };
      el.textContent = t('phDevice') + ' ' + hex(info.usbVendorId) + ':' + hex(info.usbProductId);
    } else {
      el.textContent = t('phDevice');
    }
  }

  function refreshControls() {
    var cBtn = $('#connectBtn');
    cBtn.textContent = connected ? t('disconnect') : t('connect');
    cBtn.classList.toggle('primary', !connected);
    cBtn.classList.toggle('danger', connected);
    $('#baud').disabled = connected;

    var colBtn = $('#collectBtn');
    colBtn.textContent = collecting ? t('stopCollect') : t('startCollect');
    colBtn.disabled = !connected;

    var monBtn = $('#monitorBtn');
    monBtn.textContent = monitoring ? t('stopMonitor') : t('startMonitor');
    monBtn.disabled = !connected || !collecting;
  }

  async function toggleCollect() {
    if (!connected || !writer) return;
    try {
      await send(collecting ? CMD.stop : CMD.start);
      collecting = !collecting;
      if (!collecting) stopMonitor();
      setStatus(collecting ? 'stCollecting' : 'stCollectStopped',
                collecting ? 'collecting' : 'stopped');
      refreshControls();
    } catch (e) {
      alert(t('connectFail') + (e && e.message ? e.message : e));
    }
  }

  function toggleMonitor() {
    if (!connected) return;
    if (monitoring) {
      monitoring = false;
      setStatus('stMonitorStopped', 'stopped');
    } else {
      monitoring = true;
      resetFilters();
      setStatus('stMonitoring', 'collecting');
      monitorLoop();
    }
    refreshControls();
  }

  function stopMonitor() {
    monitoring = false;
  }

  /* ---------- 读数滤波：滑动中位数 + 异常值剔除 ---------- */

  function median(values) {
    var a = values.slice().sort(function (x, y) { return x - y; });
    var mid = a.length >> 1;
    return a.length % 2 ? a[mid] : (a[mid - 1] + a[mid]) / 2;
  }

  /*
   * 每次采样返回窗口的中位数；明显偏离当前中位数的样本不计入窗口。
   * 连续 3 次被判异常说明测量条件已经变了（重新放手指等），清空窗口重新开始，
   * 避免一次真实跳变让读数被旧值锁死。
   */
  function makeFilter(opts) {
    var win = [];
    var rejects = 0;

    function current() { return win.length ? median(win) : null; }

    return {
      reset: function () { win = []; rejects = 0; },
      push: function (v) {
        if (v < opts.min || v > opts.max) {
          rejects++;
          return { value: current(), outlier: true };
        }
        if (win.length >= 2 && Math.abs(v - median(win)) > opts.maxDelta) {
          rejects++;
          if (rejects >= 3) {
            win = [v];
            rejects = 0;
            return { value: v, outlier: true };
          }
          return { value: current(), outlier: true };
        }
        rejects = 0;
        win.push(v);
        if (win.length > opts.window) win.shift();
        return { value: current(), outlier: false };
      }
    };
  }

  var METRIC_EL = { spo2: '#spo2', hr: '#hr', temp: '#temp' };
  var dropped = 0;
  var filters = {
    hr: makeFilter({ min: 35, max: 220, maxDelta: 40, window: 5 }),
    spo2: makeFilter({ min: 70, max: 100, maxDelta: 6, window: 5 }),
    temp: makeFilter({ min: 0, max: 60, maxDelta: 5, window: 5 })
  };

  function filtering() {
    return $('#filterToggle').checked;
  }

  function resetFilters() {
    Object.keys(filters).forEach(function (k) { filters[k].reset(); });
    dropped = 0;
    renderFilterInfo();
  }

  function renderFilterInfo() {
    var el = $('#filterInfo');
    el.textContent = dropped === 0 ? '' :
      (uiLang === 'zh'
        ? '已剔除 ' + dropped + ' 次异常读数'
        : dropped + ' outlier' + (dropped > 1 ? 's' : '') + ' dropped');
  }

  function showMetric(key, raw, digits) {
    var el = $(METRIC_EL[key]);
    if (raw === null) {
      el.textContent = '-1';
      filters[key].reset();
      return;
    }
    if (!filtering()) {
      el.textContent = digits ? raw.toFixed(digits) : String(Math.round(raw));
      return;
    }
    var res = filters[key].push(raw);
    if (res.outlier) {
      dropped++;
      renderFilterInfo();
    }
    if (res.value !== null) {
      el.textContent = digits ? res.value.toFixed(digits) : String(Math.round(res.value));
    }
  }

  async function monitorLoop() {
    while (monitoring && connected) {
      var started = performance.now();
      try {
        await send(CMD.hr);
        var f = await waitFrame(8, 600);
        if (!monitoring) break;
        if (f) {
          var spo2 = f[3];
          var hr = ((f[5] << 24) | (f[6] << 16) | (f[7] << 8) | f[8]) >>> 0;
          showMetric('spo2', spo2 === 0 ? null : spo2, 0);
          showMetric('hr', hr === 0 ? null : hr, 0);
        }

        await send(CMD.temp);
        var g = await waitFrame(2, 600);
        if (g) {
          showMetric('temp', g[3] + g[4] / 100, 1);
        }
      } catch (e) {
        if (connected) {
          setStatus('stError', 'error');
          monitoring = false;
          refreshControls();
        }
        break;
      }
      var rest = 2000 - (performance.now() - started);
      if (rest > 0) await sleep(rest);
    }
  }

  if ('serial' in navigator) {
    navigator.serial.addEventListener('disconnect', function (ev) {
      if (port && ev.target === port && connected) handleLost();
    });
  }

  /* ==================== 文档 ==================== */
  var DOC_LANGS = [
    ['en', 'English'], ['de', 'Deutsch'], ['es', 'Español'], ['fr', 'Français'],
    ['it', 'Italiano'], ['ja', '日本語'], ['ko', '한국어'],
    ['pt-br', 'Português (BR)'], ['pt-pt', 'Português (PT)'],
    ['zh-hans', '简体中文'], ['zh-hant', '繁體中文']
  ];
  var DOC_SECTIONS = [
    ['01-arduino', '01 · Arduino'],
    ['02-raspberry-pi', '02 · Raspberry Pi'],
    ['03-windows', '03 · Windows'],
    ['04-gui-tool', '04 · GUI Tool']
  ];

  var docLang = uiLang === 'zh' ? 'zh-hans' : 'en';
  var docSection = '01-arduino';
  var docRequest = 0;

  function initDocNav() {
    var sel = $('#docLang');
    sel.innerHTML = DOC_LANGS.map(function (l) {
      return '<option value="' + l[0] + '">' + l[1] + '</option>';
    }).join('');
    sel.value = docLang;
    sel.addEventListener('change', function () {
      docLang = sel.value;
      location.hash = '#/docs/' + docLang + '/' + docSection;
    });

    var nav = $('#docNav');
    nav.innerHTML = DOC_SECTIONS.map(function (s) {
      return '<button data-section="' + s[0] + '">' + s[1] + '</button>';
    }).join('');
    nav.addEventListener('click', function (ev) {
      var btn = ev.target.closest('button[data-section]');
      if (!btn) return;
      location.hash = '#/docs/' + docLang + '/' + btn.getAttribute('data-section');
    });
  }

  function markActiveSection() {
    document.querySelectorAll('#docNav button').forEach(function (b) {
      b.classList.toggle('active', b.getAttribute('data-section') === docSection);
    });
    $('#docLang').value = docLang;
  }

  function scrollToAnchor(id) {
    var target = id;
    try { target = decodeURIComponent(id); } catch (e) { /* ignore */ }
    var el = document.getElementById(target);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function resolveMdLink(href, baseUrl) {
    var url = new URL(href, baseUrl);
    var segs = url.pathname.split('/').filter(Boolean);
    segs.pop(); // README.md
    var section = segs.pop();
    var lang = segs.pop();
    var knownLang = DOC_LANGS.some(function (l) { return l[0] === lang; });
    var knownSection = DOC_SECTIONS.some(function (s) { return s[0] === section; });
    if (knownLang && knownSection) {
      location.hash = '#/docs/' + lang + '/' + section;
    }
  }

  async function loadDoc(lang, section) {
    docLang = lang;
    docSection = section;
    markActiveSection();

    var view = $('#docContent');
    var req = ++docRequest;
    view.innerHTML = '<p class="hint">' + t('docLoading') + '</p>';

    var path = lang + '/' + section + '/README.md';
    var baseUrl = new URL(path, location.href);
    try {
      var res = await fetch(path, { cache: 'no-cache' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      var text = await res.text();
      if (req !== docRequest) return;

      view.innerHTML = window.renderMarkdown(text);

      view.querySelectorAll('img').forEach(function (img) {
        var src = img.getAttribute('src');
        if (src && !/^(https?:|data:|\/)/.test(src)) {
          img.src = new URL(src, baseUrl).href;
        }
      });

      view.querySelectorAll('a').forEach(function (a) {
        var href = a.getAttribute('href');
        if (!href) return;
        if (href.charAt(0) === '#') {
          a.addEventListener('click', function (ev) {
            ev.preventDefault();
            scrollToAnchor(href.slice(1));
          });
          return;
        }
        if (/\.md(#|$)/.test(href)) {
          a.addEventListener('click', function (ev) {
            ev.preventDefault();
            resolveMdLink(href, baseUrl);
          });
          return;
        }
        if (/^https?:/.test(href)) {
          a.target = '_blank';
          a.rel = 'noopener';
          return;
        }
        a.href = new URL(href, baseUrl).href;
      });

      window.scrollTo({ top: 0 });
    } catch (e) {
      if (req !== docRequest) return;
      view.innerHTML = '<p class="doc-error">' + t('docFailed') + e.message + '</p>';
    }
  }

  /* ==================== 路由 ==================== */
  var lastView = null;

  function route() {
    var hash = location.hash || '#/tool';
    var parts = hash.replace(/^#\/?/, '').split('/');
    var view = parts[0] === 'docs' ? 'docs' : 'tool';

    if (lastView !== view) {
      lastView = view;
      window.scrollTo({ top: 0 });
    }

    $('#view-tool').hidden = view !== 'tool';
    $('#view-docs').hidden = view !== 'docs';
    $('#tab-tool').classList.toggle('active', view === 'tool');
    $('#tab-docs').classList.toggle('active', view === 'docs');

    if (view === 'docs') {
      var lang = parts[1] || (uiLang === 'zh' ? 'zh-hans' : 'en');
      var section = parts[2] || '01-arduino';
      if (!DOC_LANGS.some(function (l) { return l[0] === lang; })) lang = 'en';
      if (!DOC_SECTIONS.some(function (s) { return s[0] === section; })) section = '01-arduino';
      loadDoc(lang, section);
    }
  }

  /* ==================== 初始化 ==================== */
  function init() {
    if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
    applyI18n();
    initDocNav();
    showPortInfo();

    $('#connectBtn').addEventListener('click', function () {
      if (connected) disconnect();
      else connect();
    });
    $('#collectBtn').addEventListener('click', toggleCollect);
    $('#monitorBtn').addEventListener('click', toggleMonitor);

    document.querySelectorAll('.tab[data-view]').forEach(function (b) {
      b.addEventListener('click', function () {
        location.hash = '#/' + b.getAttribute('data-view');
      });
    });

    document.querySelectorAll('#uiLangSwitch button').forEach(function (b) {
      b.addEventListener('click', function () {
        uiLang = b.getAttribute('data-lang');
        localStorage.setItem('juxi.uiLang', uiLang);
        applyI18n();
        showPortInfo();
        if (!location.hash.indexOf('#/docs')) {
          docLang = uiLang === 'zh' ? 'zh-hans' : 'en';
          location.hash = '#/docs/' + docLang + '/' + docSection;
        }
      });
    });

    $('#baud').addEventListener('change', function () {
      localStorage.setItem('juxi.baud', $('#baud').value);
    });
    var savedBaud = localStorage.getItem('juxi.baud');
    if (savedBaud) $('#baud').value = savedBaud;

    var savedFilter = localStorage.getItem('juxi.filter');
    if (savedFilter === '0') $('#filterToggle').checked = false;
    $('#filterToggle').addEventListener('change', function () {
      localStorage.setItem('juxi.filter', $('#filterToggle').checked ? '1' : '0');
      resetFilters();
    });

    window.addEventListener('hashchange', route);
    route();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
