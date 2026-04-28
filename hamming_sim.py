import streamlit as st
import numpy as np
import time

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="HammingViz · Error Correction Demo",
    page_icon="📡",
    layout="wide",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0e1a;
    color: #e8eaf0;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; }

/* ── Hero title ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #00d4ff 0%, #7b5ea7 60%, #ff6b6b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.hero-sub {
    font-size: 0.95rem;
    color: #6b7a99;
    font-family: 'Space Mono', monospace;
    margin-bottom: 2rem;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00d4ff;
    margin-bottom: 0.5rem;
    margin-top: 1.5rem;
}

/* ── Stat cards ── */
.stat-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 1rem 0;
}
.stat-card {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 14px 20px;
    min-width: 130px;
    flex: 1;
}
.stat-card .val {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #00d4ff;
    line-height: 1;
}
.stat-card .lbl {
    font-size: 0.72rem;
    color: #6b7a99;
    margin-top: 4px;
    letter-spacing: 0.5px;
}
.stat-card.green .val { color: #4ade80; }
.stat-card.red   .val { color: #f87171; }
.stat-card.yellow .val { color: #fbbf24; }

/* ── Bit grid ── */
.bit-grid-wrap {
    background: #0d1424;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 18px;
    margin: 8px 0;
    overflow-x: auto;
}
.bit-grid-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 2px;
    color: #6b7a99;
    margin-bottom: 12px;
    text-transform: uppercase;
}
.bit-row {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    align-items: center;
}
.bit {
    width: 32px;
    height: 32px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    transition: all 0.3s ease;
}
.bit.b1          { background: #1a3a5c; color: #60a5fa; border: 1px solid #2563eb; }
.bit.b0          { background: #1a1f2e; color: #6b7a99; border: 1px solid #2d3748; }
.bit.parity      { background: #2d1f4a; color: #a78bfa; border: 1px solid #7c3aed; }
.bit.error       { background: #4a1f1f; color: #f87171; border: 2px solid #ef4444; }
.bit.corrected   { background: #1a3a2a; color: #4ade80; border: 2px solid #22c55e; }
.bit.group-sep   { width: 8px; background: transparent; border: none; }

/* ── Pipeline flow ── */
.pipeline {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin: 1.5rem 0;
}
.pipe-step {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 0.8rem;
    font-family: 'Space Mono', monospace;
    color: #e8eaf0;
    white-space: nowrap;
}
.pipe-step.active {
    border-color: #00d4ff;
    color: #00d4ff;
    box-shadow: 0 0 12px rgba(0, 212, 255, 0.2);
}
.pipe-arrow {
    color: #2d3a52;
    font-size: 1.2rem;
}

/* ── Noise signal bars ── */
.signal-row {
    display: flex;
    gap: 4px;
    flex-wrap: wrap;
    align-items: flex-end;
    height: 60px;
    margin: 8px 0;
}
.sig-bar {
    width: 22px;
    border-radius: 3px 3px 0 0;
    transition: height 0.4s ease;
}

/* ── Result badge ── */
.result-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 8px;
}
.result-badge.success {
    background: #14532d;
    color: #4ade80;
    border: 1px solid #22c55e;
}
.result-badge.fail {
    background: #450a0a;
    color: #f87171;
    border: 1px solid #ef4444;
}

/* ── Slider label ── */
div[data-testid="stSlider"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    color: #6b7a99 !important;
    letter-spacing: 1px;
}

/* ── Text input ── */
div[data-testid="stTextInput"] input {
    background: #111827 !important;
    border: 1px solid #1e2d45 !important;
    border-radius: 8px !important;
    color: #e8eaf0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1rem !important;
}

/* ── Button ── */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #0369a1, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 10px 28px !important;
    letter-spacing: 0.5px;
    transition: opacity 0.2s;
}
div[data-testid="stButton"] button:hover { opacity: 0.85 !important; }

/* divider */
.divider { border: none; border-top: 1px solid #1e2d45; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CORE MATH  (swap these functions with your own)
# ─────────────────────────────────────────────

# Hamming(7,4) generator matrix rows for parity bits
def hamming_encode_group(bits4):
    """Encode 4 data bits → 7-bit Hamming codeword.
    Layout: [p1, p2, d1, p3, d2, d3, d4]
    """
    d = bits4
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]

def hamming_decode_group(bits7):
    """Decode 7-bit codeword → (4 data bits, error_position or None)."""
    b = bits7
    s1 = b[0] ^ b[2] ^ b[4] ^ b[6]
    s2 = b[1] ^ b[2] ^ b[5] ^ b[6]
    s3 = b[3] ^ b[4] ^ b[5] ^ b[6]
    syndrome = s1 * 1 + s2 * 2 + s3 * 4
    error_pos = syndrome - 1 if syndrome > 0 else None
    corrected = list(b)
    if error_pos is not None:
        corrected[error_pos] ^= 1
    data = [corrected[2], corrected[4], corrected[5], corrected[6]]
    return data, error_pos

def text_to_bits(text):
    bits = []
    for ch in text:
        byte = ord(ch)
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8:
            break
        val = 0
        for b in byte_bits:
            val = (val << 1) | b
        try:
            chars.append(chr(val))
        except Exception:
            chars.append("?")
    return "".join(chars)

def encode_message(bits):
    """Pad to multiple of 4, encode all groups."""
    while len(bits) % 4 != 0:
        bits = bits + [0]
    encoded = []
    for i in range(0, len(bits), 4):
        encoded.extend(hamming_encode_group(bits[i:i+4]))
    return encoded

def bpsk_modulate(bits):
    return np.array([1.0 if b == 1 else -1.0 for b in bits])

def add_awgn(signal, snr_db):
    snr_linear = 10 ** (snr_db / 10.0)
    noise_std = 1.0 / np.sqrt(2 * snr_linear)
    noise = np.random.normal(0, noise_std, len(signal))
    return signal + noise

def bpsk_demodulate(received):
    return [1 if v > 0 else 0 for v in received]

def decode_message(bits28, n_groups):
    decoded_bits = []
    error_positions = []   # global bit index in the 28-bit stream
    for g in range(n_groups):
        chunk = bits28[g*7:(g+1)*7]
        if len(chunk) < 7:
            break
        data, epos = hamming_decode_group(chunk)
        decoded_bits.extend(data)
        if epos is not None:
            error_positions.append(g * 7 + epos)
    return decoded_bits, error_positions

def run_simulation(message, snr_db):
    original_bits = text_to_bits(message)
    encoded_bits  = encode_message(list(original_bits))
    n_groups      = len(encoded_bits) // 7

    signal         = bpsk_modulate(encoded_bits)
    noisy_signal   = add_awgn(signal, snr_db)
    received_bits  = bpsk_demodulate(noisy_signal)

    # find which positions flipped
    flipped = [i for i in range(len(encoded_bits)) if encoded_bits[i] != received_bits[i]]

    decoded_bits, corrected_positions = decode_message(received_bits, n_groups)
    received_text = bits_to_text(decoded_bits[:len(original_bits)])

    return {
        "original_bits":    original_bits,
        "encoded_bits":     encoded_bits,
        "received_bits":    received_bits,
        "noisy_signal":     noisy_signal,
        "flipped":          flipped,
        "corrected_pos":    corrected_positions,
        "decoded_bits":     decoded_bits[:len(original_bits)],
        "received_text":    received_text,
        "n_groups":         n_groups,
    }


# ─────────────────────────────────────────────
#  BIT GRID HTML BUILDER
# ─────────────────────────────────────────────

def bit_grid_html(bits, label, flipped=None, corrected_pos=None, show_parity=False, group_size=7):
    flipped       = set(flipped or [])
    corrected_pos = set(corrected_pos or [])
    html = f'<div class="bit-grid-wrap"><div class="bit-grid-title">{label}</div><div class="bit-row">'

    for i, b in enumerate(bits):
        # group separator
        if group_size and i > 0 and i % group_size == 0:
            html += '<span class="bit group-sep"></span>'

        # determine class
        if i in corrected_pos:
            cls = "corrected"
        elif i in flipped:
            cls = "error"
        elif show_parity and (i % 7 in [0, 1, 3]):   # parity positions in Hamming(7,4)
            cls = "parity"
        elif b == 1:
            cls = "b1"
        else:
            cls = "b0"

        html += f'<span class="bit {cls}">{b}</span>'

    html += '</div></div>'
    return html


# ─────────────────────────────────────────────
#  NOISY SIGNAL HTML BUILDER
# ─────────────────────────────────────────────

def signal_html(noisy, sent, max_show=56):
    noisy = noisy[:max_show]
    sent  = sent[:max_show]
    html  = '<div class="bit-grid-wrap"><div class="bit-grid-title">RECEIVED ANALOG VALUES (BPSK + AWGN)</div>'
    html += '<div style="display:flex;gap:4px;flex-wrap:wrap;align-items:flex-end;margin:4px 0;">'

    for i, (v, s) in enumerate(zip(noisy, sent)):
        norm_h  = min(abs(v) / 2.5, 1.0)
        bar_h   = int(norm_h * 48) + 4
        correct = (v > 0) == (s > 0)
        color   = "#60a5fa" if v > 0 else "#f87171"
        if not correct:
            color = "#fbbf24"  # yellow = wrong decision

        direction = "column" if v > 0 else "column-reverse"
        html += (
            f'<div style="display:flex;flex-direction:{direction};align-items:center;height:60px;">'
            f'<div style="width:14px;height:{bar_h}px;background:{color};border-radius:2px;opacity:0.85;"></div>'
            f'</div>'
        )

    html += '</div>'
    html += '<div style="font-family:Space Mono,monospace;font-size:0.65rem;color:#6b7a99;margin-top:6px;">'
    html += '🔵 correct decision &nbsp;&nbsp; 🔴 correct decision (neg) &nbsp;&nbsp; 🟡 wrong decision (bit flip!)'
    html += '</div></div>'
    return html


# ─────────────────────────────────────────────
#  APP LAYOUT
# ─────────────────────────────────────────────

st.markdown('<div class="hero-title">📡 HammingViz</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Hamming(7,4) · BPSK · AWGN · Real-time bit correction demo</div>', unsafe_allow_html=True)

# ── Pipeline banner ──
st.markdown("""
<div class="pipeline">
  <div class="pipe-step">📝 Text Input</div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">🔢 Bits</div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">🔐 Hamming Encode</div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">📶 BPSK Modulate</div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">⚡ AWGN Channel</div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">📊 Demodulate</div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">🔧 Hamming Decode</div>
  <div class="pipe-arrow">→</div>
  <div class="pipe-step">✅ Output</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Controls ──
col_in, col_snr, col_btn = st.columns([3, 2, 1])

with col_in:
    st.markdown('<div class="section-label">Message</div>', unsafe_allow_html=True)
    message = st.text_input("", value="hi", label_visibility="collapsed", max_chars=8,
                            help="Keep it short — each char = 8 bits = 2 encoded groups")

with col_snr:
    st.markdown('<div class="section-label">SNR (dB) — drag to add noise</div>', unsafe_allow_html=True)
    snr_db = st.slider("", min_value=0.0, max_value=10.0, value=5.0, step=0.5,
                       label_visibility="collapsed")

with col_btn:
    st.markdown('<div class="section-label">&nbsp;</div>', unsafe_allow_html=True)
    transmit = st.button("⚡ Transmit")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Run simulation on button OR on any change ──
if message.strip() == "":
    st.info("Type a message above and hit Transmit.")
    st.stop()

r = run_simulation(message.strip(), snr_db)

# ── Stats row ──
st.markdown('<div class="section-label">Transmission Stats</div>', unsafe_allow_html=True)
errors_introduced = len(r["flipped"])
errors_corrected  = len(r["corrected_pos"])
errors_remaining  = errors_introduced - errors_corrected
success           = r["received_text"] == message.strip()

st.markdown(f"""
<div class="stat-row">
  <div class="stat-card"><div class="val">{len(r['original_bits'])}</div><div class="lbl">bits sent</div></div>
  <div class="stat-card"><div class="val">{len(r['encoded_bits'])}</div><div class="lbl">bits encoded</div></div>
  <div class="stat-card red"><div class="val">{errors_introduced}</div><div class="lbl">errors introduced</div></div>
  <div class="stat-card green"><div class="val">{errors_corrected}</div><div class="lbl">errors corrected</div></div>
  <div class="stat-card {'red' if errors_remaining>0 else 'green'}">
    <div class="val">{errors_remaining}</div><div class="lbl">errors remaining</div>
  </div>
  <div class="stat-card yellow"><div class="val">{snr_db} dB</div><div class="lbl">SNR</div></div>
</div>
""", unsafe_allow_html=True)

# ── Result badge ──
if success:
    st.markdown(f'<div class="result-badge success">✓ &nbsp; Received: &nbsp;<b>"{r["received_text"]}"</b> — Perfect recovery!</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="result-badge fail">✗ &nbsp; Received: &nbsp;<b>"{r["received_text"]}"</b> — Uncorrectable error</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  BIT FLIP REVEAL  (Idea 3)
# ─────────────────────────────────────────────

st.markdown('<div class="section-label">Bit-by-Bit Journey</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🔢 Original Bits", "🔐 After Encoding", "⚡ After Channel (Flip Reveal)", "🔧 After Correction"])

with tab1:
    st.markdown(
        bit_grid_html(r["original_bits"], f"RAW BITS FROM '{message}' ({len(r['original_bits'])} bits)", group_size=8),
        unsafe_allow_html=True
    )
    st.markdown("**Purple** = parity bits added by Hamming encoder · **Blue** = data 1 · **Grey** = data 0", unsafe_allow_html=True)

with tab2:
    st.markdown(
        bit_grid_html(r["encoded_bits"], f"HAMMING ENCODED — {len(r['encoded_bits'])} bits ({r['n_groups']} groups of 7)",
                      show_parity=True, group_size=7),
        unsafe_allow_html=True
    )
    st.markdown("Each group of 7: positions 1, 2, 4 are **parity bits** (purple) · positions 3, 5, 6, 7 carry data", unsafe_allow_html=True)

with tab3:
    st.markdown(
        bit_grid_html(r["received_bits"], f"RECEIVED BITS — {len(r['flipped'])} flipped (🔴 red = error)",
                      flipped=r["flipped"], group_size=7),
        unsafe_allow_html=True
    )
    st.markdown("**Red** = bit flipped by noise · Everything else survived the channel", unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(signal_html(r["noisy_signal"], bpsk_modulate(r["encoded_bits"])), unsafe_allow_html=True)

with tab4:
    # build post-correction display: show corrected positions in green, remaining errors in red
    remaining_errors = set(r["flipped"]) - set(r["corrected_pos"])
    st.markdown(
        bit_grid_html(r["encoded_bits"],  # show what it *should* be after correction
                      f"AFTER HAMMING CORRECTION — 🟢 green = corrected · 🔴 red = uncorrectable",
                      flipped=list(remaining_errors),
                      corrected_pos=r["corrected_pos"],
                      group_size=7),
        unsafe_allow_html=True
    )
    st.markdown("**Green** = Hamming found and fixed this bit · **Red** = error survived (only if >1 error/group)", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  BER vs SNR  (live plot)
# ─────────────────────────────────────────────

st.markdown('<div class="section-label">BER vs SNR — Uncoded vs Hamming(7,4)</div>', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def compute_ber_curve(text, trials=400):
    snr_range = np.arange(0, 10.5, 0.5)
    ber_coded, ber_uncoded = [], []
    bits = text_to_bits(text)
    enc  = encode_message(list(bits))
    n    = len(bits)
    ne   = len(enc)
    for snr in snr_range:
        errs_coded, errs_raw = 0, 0
        for _ in range(trials):
            # coded path
            sig   = bpsk_modulate(enc)
            noisy = add_awgn(sig, snr)
            rx    = bpsk_demodulate(noisy)
            dec, _ = decode_message(rx, ne // 7)
            errs_coded += sum(a != b for a, b in zip(bits, dec[:n]))
            # uncoded path
            sig2   = bpsk_modulate(bits)
            noisy2 = add_awgn(sig2, snr)
            rx2    = bpsk_demodulate(noisy2)
            errs_raw += sum(a != b for a, b in zip(bits, rx2[:n]))
        ber_coded.append(errs_coded / (trials * n))
        ber_uncoded.append(errs_raw   / (trials * n))
    return snr_range.tolist(), ber_coded, ber_uncoded

with st.spinner("Computing BER curve…"):
    snrs, ber_c, ber_u = compute_ber_curve(message.strip())

import pandas as pd
chart_data = pd.DataFrame({"SNR (dB)": snrs, "Hamming Coded": ber_c, "Uncoded": ber_u}).set_index("SNR (dB)")
st.line_chart(chart_data, color=["#4ade80", "#f87171"])
st.caption("Green = Hamming coded · Red = uncoded  |  Lower BER = better")

# ── Footer ──
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="font-family:Space Mono,monospace;font-size:0.65rem;color:#2d3a52;text-align:center;">'
    'Hamming(7,4) · BPSK · AWGN · Real simulation — not a visualisation wrapper</p>',
    unsafe_allow_html=True
)
