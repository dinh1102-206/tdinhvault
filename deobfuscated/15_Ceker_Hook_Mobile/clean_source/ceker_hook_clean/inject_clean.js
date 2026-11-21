// Author: tdinh
// Decoded by: tdinh cute
// Target: inject.js (Ceker Hook Mobile v3 - Audio DSP Decoy)
// Status: Fully deobfuscated

(function () {
  'use strict';

  let _0x1fc676 = 1;
  let _0x26b3d0 = 0;
  let _0x46e2ab = 0;
  let _0x3efc44 = 0;
  let _0x42f04f = 1;
  let _0x1e57f8 = -20;
  let _0xcaae2b = 4;
  let _0x52a82b = 0;
  let _0x1856f3 = 0;
  let _0x13d88d = 0;
  let _0x5ee839 = 0;
  let _0x28aa6f = 80;
  let _0x5eee10 = 0;
  let _0x119c91 = null;
  let _0x259030 = null;
  let _0x6cd1dd = null;
  let _0x95fdca = null;
  let _0x46c1a7 = null;
  let _0x2230f1 = null;
  let _0x2c248c = null;
  let _0x22e952 = null;
  let _0x509cd5 = null;
  let _0x583285 = null;
  let _0x104698 = null;
  let _0x24a0a3 = null;
  let _0x54b06d = null;
  let _0x4525d7 = null;
  let _0x6f39a8 = null;
  let _0xcb307e = null;
  let _0x1b8d3a = null;
  let _0x27de57 = null;
  let _0x2a2176 = null;
  let _0x3444be = null;
  let _0x4a2610 = null;
  let _0x350ae5 = null;
  let _0x293fbf = null;
  let _0x362627 = null;
  let _0x36b5fa = null;
  let _0x4ab546 = null;
  let _0x2b2252 = null;
  const _0x1f655d = 8192;
  const _0x3af666 = 2048;
  const _0x2437cb = 2048;
  const _0x5b575e = new Float32Array(_0x1f655d);
  let _0x72eba5 = 0;
  let _0x4918aa = 0;
  let _0x2df564 = false;
  let _0x3b725f = 1;
  let _0x37fdf2 = false;
  let _0x3b83db = false;
  let _0x4da203 = 0.003;
  let _0x201829 = 400;
  let _0x31928f = false;
  let _0x4228d4 = 8;
  let _0x138f82 = 4;
  let _0x2e914c = false;
  let _0x2b25d9 = false;
  let _0x36cdd7 = null;
  let _0x37bd63 = null;
  let _0x6cb510 = null;
  function _0x46601a() {
    if (!_0x6cd1dd || _0x6cd1dd.state === "closed") {
      _0x6cd1dd = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (_0x6cd1dd.state === "suspended") {
      _0x6cd1dd.resume().catch(_0x2493cf => console.warn("[Ceker] resume:", _0x2493cf));
    }
    return _0x6cd1dd;
  }
  function _0x4a98b9(_0x471d69, _0x187609, _0x2fac0a) {
    const _0x5f1dd4 = _0x471d69.sampleRate;
    const _0x21a12d = Math.floor(_0x5f1dd4 * _0x187609);
    const _0x4fd729 = _0x471d69.createBuffer(2, _0x21a12d, _0x5f1dd4);
    for (let _0x3322a5 = 0; _0x3322a5 < 2; _0x3322a5++) {
      const _0x3be2ce = _0x4fd729.getChannelData(_0x3322a5);
      for (let _0x1cc0f4 = 0; _0x1cc0f4 < _0x21a12d; _0x1cc0f4++) {
        _0x3be2ce[_0x1cc0f4] = (Math.random() * 2 - 1) * Math.pow(1 - _0x1cc0f4 / _0x21a12d, _0x2fac0a);
      }
    }
    return _0x4fd729;
  }
  function _0x5430e8(_0x2f5f6c) {
    _0x583285 = _0x2f5f6c.createConvolver();
    _0x583285.buffer = _0x4a98b9(_0x2f5f6c, 3.5, 2.8);
    _0x104698 = _0x2f5f6c.createGain();
    _0x104698.gain.value = 1;
    _0x24a0a3 = _0x2f5f6c.createGain();
    _0x24a0a3.gain.value = 0;
    _0x54b06d = _0x2f5f6c.createGain();
    _0x54b06d.gain.value = 1;
    _0x104698.connect(_0x54b06d);
    _0x583285.connect(_0x24a0a3);
    _0x24a0a3.connect(_0x54b06d);
  }
  function _0x89e622(_0x64e3c) {
    if (!_0x104698 || !_0x6cd1dd) {
      return;
    }
    _0x104698.gain.setTargetAtTime(1 - _0x64e3c * 0.5, _0x6cd1dd.currentTime, 0.02);
    _0x24a0a3.gain.setTargetAtTime(_0x64e3c, _0x6cd1dd.currentTime, 0.02);
  }
  function _0x18fe71(_0xfd45ca) {
    const _0xce2b03 = Math.max(-1, Math.min(1, _0xfd45ca));
    return {
      left: Math.max(0, 1 - _0xce2b03),
      right: Math.max(0, 1 + _0xce2b03)
    };
  }
  function _0x42b946(_0x50cbcc) {
    const _0x181647 = _0x18fe71(_0x50cbcc);
    if (_0x95fdca && _0x6cd1dd) {
      _0x95fdca.gain.setTargetAtTime(_0x181647.left, _0x6cd1dd.currentTime, 0.01);
      _0x46c1a7.gain.setTargetAtTime(_0x181647.right, _0x6cd1dd.currentTime, 0.01);
    }
  }
  function _0x20b53c(_0x22979c) {
    _0x22e952 = _0x22979c.createChannelMerger(2);
    _0x22e952.connect(_0x509cd5);
    const _0x5672c8 = _0x18fe71(_0x46e2ab);
    _0x95fdca = _0x22979c.createGain();
    _0x95fdca.gain.value = _0x5672c8.left;
    _0x46c1a7 = _0x22979c.createGain();
    _0x46c1a7.gain.value = _0x5672c8.right;
    _0x2230f1 = _0x22979c.createChannelSplitter(2);
    _0x2c248c = _0x22979c.createChannelMerger(2);
    _0x2230f1.connect(_0x95fdca, 0);
    _0x2230f1.connect(_0x46c1a7, 1);
    _0x95fdca.connect(_0x2c248c, 0, 0);
    _0x46c1a7.connect(_0x2c248c, 0, 1);
    _0x2c248c.connect(_0x22e952, 0, 0);
    _0x2c248c.connect(_0x22e952, 0, 1);
  }
  window.addEventListener("__midnight_mic_setGain", _0x3e6c69 => {
    _0x1fc676 = _0x3e6c69.detail.value;
    if (_0x119c91 && _0x6cd1dd) {
      _0x119c91.gain.setTargetAtTime(_0x1fc676, _0x6cd1dd.currentTime, 0.01);
    }
    window.dispatchEvent(new CustomEvent("__midnight_mic_gainChanged", {
      detail: {
        currentGain: _0x1fc676,
        active: _0x119c91 !== null
      }
    }));
  });
  window.addEventListener("__midnight_mic_setPitch", _0x4b4ec6 => {
    _0x26b3d0 = _0x4b4ec6.detail.value;
    _0x3b725f = Math.pow(2, _0x26b3d0 / 12);
    window.dispatchEvent(new CustomEvent("__midnight_mic_pitchChanged", {
      detail: {
        currentPitch: _0x26b3d0,
        active: _0x119c91 !== null
      }
    }));
  });
  window.addEventListener("__midnight_mic_setPan", _0x47d827 => {
    _0x46e2ab = _0x47d827.detail.value;
    _0x42b946(_0x46e2ab);
    window.dispatchEvent(new CustomEvent("__midnight_mic_panChanged", {
      detail: {
        currentPan: _0x46e2ab,
        active: _0x119c91 !== null
      }
    }));
  });
  window.addEventListener("__midnight_mic_setReverb", _0x436344 => {
    _0x3efc44 = _0x436344.detail.value;
    _0x89e622(_0x3efc44);
    window.dispatchEvent(new CustomEvent("__midnight_mic_reverbChanged", {
      detail: {
        currentReverb: _0x3efc44,
        active: _0x119c91 !== null
      }
    }));
  });
  window.addEventListener("__midnight_mic_setMasterVol", _0x2e27be => {
    _0x42f04f = _0x2e27be.detail.value;
    if (_0xcb307e && _0x6cd1dd) {
      _0xcb307e.gain.setTargetAtTime(_0x42f04f, _0x6cd1dd.currentTime, 0.01);
    }
    window.dispatchEvent(new CustomEvent("__midnight_mic_masterVolChanged", {
      detail: {
        value: _0x42f04f
      }
    }));
  });
  window.addEventListener("__midnight_mic_setComp", _0x2badbf => {
    _0x1e57f8 = _0x2badbf.detail.threshold;
    _0xcaae2b = _0x2badbf.detail.ratio;
    _0x52a82b = _0x2badbf.detail.gain;
    if (_0x1b8d3a) {
      _0x1b8d3a.threshold.value = _0x1e57f8;
      _0x1b8d3a.ratio.value = _0xcaae2b;
    }
    window.dispatchEvent(new CustomEvent("__midnight_mic_compChanged", {
      detail: {
        threshold: _0x1e57f8,
        ratio: _0xcaae2b,
        gain: _0x52a82b
      }
    }));
  });
  window.addEventListener("__midnight_mic_setEq", _0x33009a => {
    _0x1856f3 = _0x33009a.detail.bass;
    _0x13d88d = _0x33009a.detail.mid !== undefined ? _0x33009a.detail.mid : _0x13d88d;
    _0x5ee839 = _0x33009a.detail.treble;
    if (_0x27de57 && _0x6cd1dd) {
      _0x27de57.gain.setTargetAtTime(_0x1856f3, _0x6cd1dd.currentTime, 0.02);
    }
    if (_0x2a2176 && _0x6cd1dd) {
      _0x2a2176.gain.setTargetAtTime(_0x13d88d, _0x6cd1dd.currentTime, 0.02);
    }
    if (_0x3444be && _0x6cd1dd) {
      _0x3444be.gain.setTargetAtTime(_0x5ee839, _0x6cd1dd.currentTime, 0.02);
    }
    window.dispatchEvent(new CustomEvent("__midnight_mic_eqChanged", {
      detail: {
        bass: _0x1856f3,
        mid: _0x13d88d,
        treble: _0x5ee839
      }
    }));
  });
  window.addEventListener("__midnight_mic_setHighpass", _0x108532 => {
    _0x28aa6f = _0x108532.detail.freq;
    if (_0x4a2610 && _0x6cd1dd) {
      _0x4a2610.frequency.setTargetAtTime(_0x28aa6f, _0x6cd1dd.currentTime, 0.02);
    }
    window.dispatchEvent(new CustomEvent("__midnight_mic_highpassChanged", {
      detail: {
        freq: _0x28aa6f
      }
    }));
  });
  window.addEventListener("__midnight_mic_setPresence", _0x3396bd => {
    _0x5eee10 = _0x3396bd.detail.gain;
    if (_0x350ae5 && _0x6cd1dd) {
      _0x350ae5.gain.setTargetAtTime(_0x5eee10, _0x6cd1dd.currentTime, 0.02);
    }
    window.dispatchEvent(new CustomEvent("__midnight_mic_presenceChanged", {
      detail: {
        gain: _0x5eee10
      }
    }));
  });
  window.addEventListener("__midnight_mic_setNoiseGate", _0x2f2a90 => {
    _0x37fdf2 = _0x2f2a90.detail.enabled;
    _0x4da203 = _0x2f2a90.detail.threshold;
    if (_0x2b25d9) {
      _0x16960c();
    }
    window.dispatchEvent(new CustomEvent("__midnight_mic_noiseGateChanged", {
      detail: {
        enabled: _0x37fdf2,
        threshold: _0x4da203
      }
    }));
  });
  window.addEventListener("__midnight_mic_setFeedbackNotch", _0x35061e => {
    _0x3b83db = _0x35061e.detail.enabled;
    _0x201829 = _0x35061e.detail.frequency;
    if (_0x362627) {
      _0x362627.frequency.value = _0x201829;
    }
    if (_0x2b25d9) {
      _0x16960c();
    }
    window.dispatchEvent(new CustomEvent("__midnight_mic_feedbackNotchChanged", {
      detail: {
        enabled: _0x3b83db,
        frequency: _0x201829
      }
    }));
  });
  window.addEventListener("__midnight_mic_setBitcrush", _0x525d2 => {
    _0x31928f = _0x525d2.detail.enabled;
    if (_0x525d2.detail.bits !== undefined) {
      _0x4228d4 = _0x525d2.detail.bits;
    }
    if (_0x525d2.detail.rate !== undefined) {
      _0x138f82 = _0x525d2.detail.rate;
    }
    window.dispatchEvent(new CustomEvent("__midnight_mic_bitcrushChanged", {
      detail: {
        enabled: _0x31928f,
        bits: _0x4228d4,
        rate: _0x138f82
      }
    }));
  });
  window.addEventListener("__midnight_mic_setX2Boost", _0x56d2f4 => {
    _0x2e914c = _0x56d2f4.detail.enabled;
    if (_0x2b2252 && _0x6cd1dd) {
      _0x2b2252.gain.setTargetAtTime(_0x2e914c ? 2 : 1, _0x6cd1dd.currentTime, 0.01);
    }
    window.dispatchEvent(new CustomEvent("__midnight_mic_x2BoostChanged", {
      detail: {
        enabled: _0x2e914c
      }
    }));
  });
  function _0x4fe900(_0x1944e3) {
    if (!_0x293fbf) {
      _0x293fbf = _0x1944e3.createBiquadFilter();
      _0x293fbf.type = "lowpass";
      _0x293fbf.frequency.value = 4000;
      _0x293fbf.Q.value = 0.7;
    }
    if (!_0x362627) {
      _0x362627 = _0x1944e3.createBiquadFilter();
      _0x362627.type = "notch";
      _0x362627.frequency.value = _0x201829;
      _0x362627.Q.value = 1;
    }
    if (!_0x36b5fa) {
      _0x36b5fa = _0x1944e3.createScriptProcessor(512, 1, 1);
      let _0x2f9bb0 = 1;
      const _0x5b0157 = 0.005;
      const _0x582a81 = 0.08;
      _0x36b5fa.onaudioprocess = _0x25a78d => {
        const _0x4e8483 = _0x25a78d.inputBuffer.getChannelData(0);
        const _0x2740d9 = _0x25a78d.outputBuffer.getChannelData(0);
        let _0x3ed1a3 = 0;
        for (let _0x375e72 = 0; _0x375e72 < _0x4e8483.length; _0x375e72++) {
          _0x3ed1a3 += _0x4e8483[_0x375e72] * _0x4e8483[_0x375e72];
        }
        const _0x4bf47f = Math.sqrt(_0x3ed1a3 / _0x4e8483.length);
        const _0xf9f16f = _0x4bf47f < _0x4da203 ? 0.2 : 1;
        const _0x297b5b = _0xf9f16f > _0x2f9bb0 ? Math.exp(-1 / (_0x5b0157 * _0x1944e3.sampleRate)) : Math.exp(-1 / (_0x582a81 * _0x1944e3.sampleRate));
        _0x2f9bb0 = _0xf9f16f + (_0x2f9bb0 - _0xf9f16f) * _0x297b5b;
        const _0x48904b = Math.max(0.2, _0x2f9bb0);
        for (let _0x43e8fd = 0; _0x43e8fd < _0x2740d9.length; _0x43e8fd++) {
          _0x2740d9[_0x43e8fd] = _0x4e8483[_0x43e8fd] * _0x48904b;
        }
      };
    }
    if (!_0x4ab546) {
      _0x4ab546 = _0x1944e3.createScriptProcessor(512, 1, 1);
      let _0x563998 = 0;
      let _0x1016a1 = 0;
      _0x4ab546.onaudioprocess = _0x1c3e75 => {
        const _0x1e6878 = _0x1c3e75.inputBuffer.getChannelData(0);
        const _0x2dcdb1 = _0x1c3e75.outputBuffer.getChannelData(0);
        if (!_0x31928f) {
          _0x2dcdb1.set(_0x1e6878);
          return;
        }
        const _0x331f6b = Math.pow(2, _0x4228d4) - 1;
        const _0x56cc1e = Math.max(1, Math.round(_0x138f82));
        for (let _0x4b64c2 = 0; _0x4b64c2 < _0x1e6878.length; _0x4b64c2++) {
          if (_0x1016a1 <= 0) {
            _0x563998 = Math.round(_0x1e6878[_0x4b64c2] * _0x331f6b) / _0x331f6b;
            _0x1016a1 = _0x56cc1e;
          }
          _0x1016a1--;
          _0x2dcdb1[_0x4b64c2] = _0x563998;
        }
      };
    }
    if (!_0xcb307e) {
      _0xcb307e = _0x1944e3.createGain();
      _0xcb307e.gain.value = _0x42f04f;
    }
    if (!_0x2b2252) {
      _0x2b2252 = _0x1944e3.createGain();
      _0x2b2252.gain.value = _0x2e914c ? 2 : 1;
    }
    if (!_0x1b8d3a) {
      _0x1b8d3a = _0x1944e3.createDynamicsCompressor();
      _0x1b8d3a.threshold.value = _0x1e57f8;
      _0x1b8d3a.ratio.value = _0xcaae2b;
      _0x1b8d3a.knee.value = 6;
      _0x1b8d3a.attack.value = 0.005;
      _0x1b8d3a.release.value = 0.05;
    }
    if (!_0x27de57) {
      _0x27de57 = _0x1944e3.createBiquadFilter();
      _0x27de57.type = "lowshelf";
      _0x27de57.frequency.value = 200;
      _0x27de57.gain.value = _0x1856f3;
    }
    if (!_0x2a2176) {
      _0x2a2176 = _0x1944e3.createBiquadFilter();
      _0x2a2176.type = "peaking";
      _0x2a2176.frequency.value = 1000;
      _0x2a2176.Q.value = 0.8;
      _0x2a2176.gain.value = _0x13d88d;
    }
    if (!_0x3444be) {
      _0x3444be = _0x1944e3.createBiquadFilter();
      _0x3444be.type = "highshelf";
      _0x3444be.frequency.value = 4000;
      _0x3444be.gain.value = _0x5ee839;
    }
    if (!_0x4a2610) {
      _0x4a2610 = _0x1944e3.createBiquadFilter();
      _0x4a2610.type = "highpass";
      _0x4a2610.frequency.value = _0x28aa6f;
      _0x4a2610.Q.value = 0.7;
    }
    if (!_0x350ae5) {
      _0x350ae5 = _0x1944e3.createBiquadFilter();
      _0x350ae5.type = "peaking";
      _0x350ae5.frequency.value = 3500;
      _0x350ae5.Q.value = 1.2;
      _0x350ae5.gain.value = _0x5eee10;
    }
  }
  function _0x16960c() {
    if (!_0x259030 || !_0x119c91 || !_0x6cd1dd) {
      return;
    }
    try {
      _0x259030.disconnect();
      if (_0x4a2610) {
        _0x4a2610.disconnect();
      }
      if (_0x293fbf) {
        _0x293fbf.disconnect();
      }
      if (_0x362627) {
        _0x362627.disconnect();
      }
      if (_0x36b5fa) {
        _0x36b5fa.disconnect();
      }
      if (_0x4ab546) {
        _0x4ab546.disconnect();
      }
      if (_0x27de57) {
        _0x27de57.disconnect();
      }
      if (_0x2a2176) {
        _0x2a2176.disconnect();
      }
      if (_0x350ae5) {
        _0x350ae5.disconnect();
      }
      if (_0x3444be) {
        _0x3444be.disconnect();
      }
      if (_0x1b8d3a) {
        _0x1b8d3a.disconnect();
      }
      if (_0xcb307e) {
        _0xcb307e.disconnect();
      }
      if (_0x2b2252) {
        _0x2b2252.disconnect();
      }
    } catch (_0x106c10) {}
    let _0x54f670 = _0x259030;
    if (_0x4a2610) {
      _0x54f670.connect(_0x4a2610);
      _0x54f670 = _0x4a2610;
    }
    if (_0x293fbf) {
      _0x54f670.connect(_0x293fbf);
      _0x54f670 = _0x293fbf;
    }
    if (_0x3b83db && _0x362627) {
      _0x54f670.connect(_0x362627);
      _0x54f670 = _0x362627;
    }
    if (_0x37fdf2 && _0x36b5fa) {
      _0x54f670.connect(_0x36b5fa);
      _0x54f670 = _0x36b5fa;
    }
    if (_0x4ab546) {
      _0x54f670.connect(_0x4ab546);
      _0x54f670 = _0x4ab546;
    }
    if (_0x27de57) {
      _0x54f670.connect(_0x27de57);
      _0x54f670 = _0x27de57;
    }
    if (_0x2a2176) {
      _0x54f670.connect(_0x2a2176);
      _0x54f670 = _0x2a2176;
    }
    if (_0x350ae5) {
      _0x54f670.connect(_0x350ae5);
      _0x54f670 = _0x350ae5;
    }
    if (_0x3444be) {
      _0x54f670.connect(_0x3444be);
      _0x54f670 = _0x3444be;
    }
    if (_0x1b8d3a) {
      _0x54f670.connect(_0x1b8d3a);
      _0x54f670 = _0x1b8d3a;
    }
    if (_0xcb307e) {
      _0x54f670.connect(_0xcb307e);
      _0x54f670 = _0xcb307e;
    }
    if (_0x2b2252) {
      _0x54f670.connect(_0x2b2252);
      _0x54f670 = _0x2b2252;
    }
    _0x54f670.connect(_0x119c91);
  }
  window.addEventListener("__midnight_mic_getStatus", () => {
    window.dispatchEvent(new CustomEvent("__midnight_mic_statusResponse", {
      detail: {
        active: _0x119c91 !== null,
        currentGain: _0x1fc676,
        currentPitch: _0x26b3d0,
        currentPan: _0x46e2ab,
        currentReverb: _0x3efc44,
        masterVol: _0x42f04f,
        compThreshold: _0x1e57f8,
        compRatio: _0xcaae2b,
        compGain: _0x52a82b,
        eqBass: _0x1856f3,
        eqMid: _0x13d88d,
        eqTreble: _0x5ee839,
        highpass: _0x28aa6f,
        presence: _0x5eee10,
        noiseGateEnabled: _0x37fdf2,
        feedbackNotchEnabled: _0x3b83db,
        noiseThreshold: _0x4da203,
        notchFrequency: _0x201829,
        bitcrushEnabled: _0x31928f,
        bitcrushBits: _0x4228d4,
        bitcrushRate: _0x138f82,
        x2BoostEnabled: _0x2e914c
      }
    }));
  });
  function _0x3e8146(_0x4308ca) {
    _0x4308ca = (_0x4308ca % _0x1f655d + _0x1f655d) % _0x1f655d;
    const _0x428356 = Math.floor(_0x4308ca);
    const _0x403e67 = (_0x428356 + 1) % _0x1f655d;
    const _0x33aa72 = _0x4308ca - _0x428356;
    return _0x5b575e[_0x428356] * (1 - _0x33aa72) + _0x5b575e[_0x403e67] * _0x33aa72;
  }
  function _0x3b4fb7(_0x5ea895, _0x15cd67) {
    const _0x3ef79a = _0x3b725f;
    const _0x181c96 = _0x5ea895.length;
    if (!_0x2df564) {
      _0x4918aa = 0;
      _0x72eba5 = 0;
      _0x2df564 = true;
    }
    const _0x258944 = _0x3ef79a - 1;
    const _0x5a02ff = _0x2437cb * 0.5;
    const _0x437c94 = Math.PI * 2 / _0x2437cb;
    for (let _0x1f0af7 = 0; _0x1f0af7 < _0x181c96; _0x1f0af7++) {
      _0x5b575e[_0x72eba5] = _0x5ea895[_0x1f0af7];
      _0x72eba5 = (_0x72eba5 + 1) % _0x1f655d;
      const _0x3f5285 = _0x4918aa;
      let _0x481283 = _0x3f5285 + _0x5a02ff;
      if (_0x481283 >= _0x2437cb) {
        _0x481283 -= _0x2437cb;
      }
      const _0x354e2f = _0x3e8146(_0x72eba5 - _0x3af666 + _0x3f5285);
      const _0x4eb697 = _0x3e8146(_0x72eba5 - _0x3af666 + _0x481283);
      const _0x414c08 = 0.5 - Math.cos(_0x437c94 * _0x3f5285) * 0.5;
      const _0x1065a0 = 0.5 - Math.cos(_0x437c94 * _0x481283) * 0.5;
      _0x15cd67[_0x1f0af7] = _0x354e2f * _0x414c08 + _0x4eb697 * _0x1065a0;
      _0x4918aa += _0x258944;
      if (_0x4918aa >= _0x2437cb) {
        _0x4918aa -= _0x2437cb;
      } else if (_0x4918aa < 0) {
        _0x4918aa += _0x2437cb;
      }
    }
  }
  const _0x2e0cc7 = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);
  navigator.mediaDevices.getUserMedia = async function (_0x4ca692) {
    const _0x191ac4 = _0x4ca692 && _0x4ca692.audio;
    const _0x7b4f5e = await _0x2e0cc7(_0x4ca692);
    if (!_0x191ac4) {
      return _0x7b4f5e;
    }
    const _0x1ec78b = _0x46601a();
    if (_0x1ec78b.state === "suspended") {
      await _0x1ec78b.resume();
    }
    const _0x11c130 = _0x1ec78b.createMediaStreamSource(_0x7b4f5e);
    _0x36cdd7 = _0x11c130;
    _0x259030 = _0x1ec78b.createScriptProcessor(4096, 1, 1);
    _0x259030.onaudioprocess = _0x488c67 => {
      const _0x4e013d = _0x488c67.inputBuffer.getChannelData(0);
      const _0x4f6d51 = _0x488c67.outputBuffer.getChannelData(0);
      if (_0x26b3d0 === 0) {
        _0x4f6d51.set(_0x4e013d);
      } else {
        _0x3b4fb7(_0x4e013d, _0x4f6d51);
      }
    };
    _0x119c91 = _0x1ec78b.createGain();
    _0x119c91.gain.value = _0x1fc676;
    _0x509cd5 = _0x1ec78b.createMediaStreamDestination();
    _0x5430e8(_0x1ec78b);
    _0x89e622(_0x3efc44);
    _0x20b53c(_0x1ec78b);
    _0x4fe900(_0x1ec78b);
    _0x11c130.connect(_0x259030);
    _0x16960c();
    _0x119c91.connect(_0x104698);
    _0x119c91.connect(_0x583285);
    _0x54b06d.connect(_0x2230f1);
    const _0x261053 = _0x2b2252 || _0xcb307e || _0x119c91;
    _0x4525d7 = _0x1ec78b.createAnalyser();
    _0x4525d7.fftSize = 256;
    _0x4525d7.smoothingTimeConstant = 0.8;
    _0x261053.connect(_0x4525d7);
    _0x4525d7.connect(_0x1ec78b.createGain());
    _0x6f39a8 = _0x1ec78b.createAnalyser();
    _0x6f39a8.fftSize = 512;
    _0x6f39a8.smoothingTimeConstant = 0.7;
    _0x261053.connect(_0x6f39a8);
    _0x6f39a8.connect(_0x1ec78b.createGain());
    if (_0x37bd63) {
      clearInterval(_0x37bd63);
    }
    _0x37bd63 = setInterval(() => {
      if (!_0x4525d7) {
        return;
      }
      const _0x9a4f82 = new Uint8Array(_0x4525d7.fftSize);
      _0x4525d7.getByteTimeDomainData(_0x9a4f82);
      let _0x3ad6e4 = 0;
      for (let _0xca4b3 = 0; _0xca4b3 < _0x9a4f82.length; _0xca4b3++) {
        const _0x55ce37 = (_0x9a4f82[_0xca4b3] - 128) / 128;
        _0x3ad6e4 += _0x55ce37 * _0x55ce37;
      }
      const _0xe618e3 = Math.sqrt(_0x3ad6e4 / _0x9a4f82.length);
      window.dispatchEvent(new CustomEvent("__midnight_mic_meterData", {
        detail: {
          value: _0xe618e3
        }
      }));
    }, 50);
    if (_0x6cb510) {
      clearInterval(_0x6cb510);
    }
    _0x6cb510 = setInterval(() => {
      if (!_0x6f39a8) {
        return;
      }
      const _0x3721a6 = new Uint8Array(_0x6f39a8.frequencyBinCount);
      _0x6f39a8.getByteFrequencyData(_0x3721a6);
      window.dispatchEvent(new CustomEvent("__midnight_mic_analyzerData", {
        detail: {
          data: Array.from(_0x3721a6)
        }
      }));
    }, 30);
    _0x2b25d9 = true;
    const _0x2c4728 = _0x509cd5.stream;
    _0x7b4f5e.getVideoTracks().forEach(_0xbd74ea => _0x2c4728.addTrack(_0xbd74ea));
    const _0x5d29d7 = _0x7b4f5e.getAudioTracks();
    const _0xa97b35 = _0x2c4728.getAudioTracks();
    _0x5d29d7.forEach((_0x198398, _0x316113) => {
      if (_0xa97b35[_0x316113]) {
        _0xa97b35[_0x316113].addEventListener("ended", () => _0x198398.stop());
        const _0x44e8dd = _0xa97b35[_0x316113].stop.bind(_0xa97b35[_0x316113]);
        _0xa97b35[_0x316113].stop = function () {
          _0x44e8dd();
          _0x198398.stop();
        };
        _0x198398.addEventListener("mute", () => {
          if (_0xa97b35[_0x316113]) {
            _0xa97b35[_0x316113].enabled = false;
          }
        });
        _0x198398.addEventListener("unmute", () => {
          if (_0xa97b35[_0x316113]) {
            _0xa97b35[_0x316113].enabled = true;
          }
        });
      }
    });
    Object.defineProperty(_0x2c4728, "active", {
      get: () => _0x7b4f5e.active
    });
    window.dispatchEvent(new CustomEvent("__midnight_mic_statusResponse", {
      detail: {
        active: true,
        currentGain: _0x1fc676,
        currentPitch: _0x26b3d0,
        currentPan: _0x46e2ab,
        currentReverb: _0x3efc44,
        masterVol: _0x42f04f,
        compThreshold: _0x1e57f8,
        compRatio: _0xcaae2b,
        compGain: _0x52a82b,
        eqBass: _0x1856f3,
        eqMid: _0x13d88d,
        eqTreble: _0x5ee839,
        highpass: _0x28aa6f,
        presence: _0x5eee10,
        noiseGateEnabled: _0x37fdf2,
        feedbackNotchEnabled: _0x3b83db,
        noiseThreshold: _0x4da203,
        notchFrequency: _0x201829,
        bitcrushEnabled: _0x31928f,
        bitcrushBits: _0x4228d4,
        bitcrushRate: _0x138f82,
        x2BoostEnabled: _0x2e914c
      }
    }));
    return _0x2c4728;
  };
  window.addEventListener("beforeunload", () => {
    if (_0x37bd63) {
      clearInterval(_0x37bd63);
    }
    if (_0x6cb510) {
      clearInterval(_0x6cb510);
    }
    if (_0x6cd1dd && _0x6cd1dd.state !== "closed") {
      _0x6cd1dd.close().catch(() => {});
    }
  });
  console.log("[Ceker] Ceker Mic v4 inject loaded.");
})();