"""
Quantum Battleship & Quantum Arcade — Streamlit Tactical Interface
===================================================================

High-tech radar HUD and interactive quantum strategy games:
1. Quantum Battleship (Prominent 3-Tier Level Guide, Compact Tactical Field Manual, Sonar Scouting, & Screen Flash FX)
2. Quantum Tic-Tac-Toe (Vibrant Endpoint Selection, Synchronized Bridge Builder & Compact Circuit)
3. Quantum Academy (LaTeX Formulations & Core Principles)

Author : Pratham D. (@pratham603-bit)
Event  : Qiskit Fall Fest 2026 — IIIT Kottayam
Track  : Track 1: Quantum Games & Interactive Puzzles
"""

from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import streamlit as st
import streamlit.components.v1 as components
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.quantum_core import QuantumBattleshipEngine, ROW_LABELS
from src.quantum_tictactoe import QuantumTicTacToeEngine

# ======================================================================
# Page Configuration
# ======================================================================
st.set_page_config(
    page_title="Quantum Warfare: Battleship & Arcade",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ======================================================================
# Modern High-Tech CSS Theme with Detonation & Splash Full-Screen Flash
# ======================================================================
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=JetBrains+Mono:wght@300;400;500;600&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #050714;
    --bg-card: rgba(13, 20, 48, 0.92);
    --border-card: rgba(0, 212, 255, 0.3);
    --cyan: #00d4ff;
    --purple: #a855f7;
    --green: #00ff88;
    --red: #ff3366;
    --amber: #ffb800;
    --text-primary: #e2e8f0;
    --text-muted: #94a3b8;
}

.stApp {
    background: radial-gradient(circle at 50% 10%, #0d1b38 0%, #060919 60%, #03040c 100%) !important;
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5 {
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 1.5px;
}

.main-title {
    text-align: center;
    background: linear-gradient(90deg, #00d4ff, #a855f7, #00ff88);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.2rem;
    font-weight: 900;
    margin-bottom: 2px;
}

.subtitle {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--text-muted);
    letter-spacing: 1px;
    margin-bottom: 18px;
}

/* =====================================================================
   GLOBAL BUTTON STYLING — ELIMINATES ALL WHITE / BLANK BUTTONS
   ===================================================================== */
div.stButton > button,
button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, rgba(13, 20, 48, 0.95), rgba(20, 32, 68, 0.95)) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(0, 212, 255, 0.35) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5) !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.8) !important;
}

div.stButton > button:hover,
button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover {
    background: linear-gradient(135deg, rgba(20, 35, 80, 0.98), rgba(0, 212, 255, 0.25)) !important;
    border-color: #00d4ff !important;
    box-shadow: 0 0 18px rgba(0, 212, 255, 0.5) !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
}

div.stButton > button[kind="primary"],
button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #ff3366, #ff6600) !important;
    color: #ffffff !important;
    border: 2px solid #ffcc00 !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 800 !important;
    box-shadow: 0 0 25px rgba(255, 51, 102, 0.7), inset 0 0 12px rgba(255, 200, 0, 0.4) !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.9) !important;
    animation: selected-pulse 1.8s infinite alternate !important;
}

@keyframes selected-pulse {
    0% { box-shadow: 0 0 15px rgba(255, 51, 102, 0.6); }
    100% { box-shadow: 0 0 30px rgba(255, 200, 0, 0.9), 0 0 15px #ff3366; }
}

div.stButton > button:disabled,
button:disabled {
    background: rgba(10, 15, 30, 0.6) !important;
    border-color: rgba(255, 255, 255, 0.08) !important;
    color: #475569 !important;
    cursor: not-allowed !important;
    opacity: 0.65 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* =====================================================================
   FULL-SCREEN SCREEN FLASH FX
   ===================================================================== */
@keyframes full-screen-blast-anim {
    0% { opacity: 0.88; background: radial-gradient(circle, rgba(255, 51, 102, 0.95) 0%, rgba(255, 102, 0, 0.65) 45%, rgba(180, 0, 0, 0.95) 100%); }
    25% { opacity: 1; }
    100% { opacity: 0; }
}

@keyframes full-screen-splash-anim {
    0% { opacity: 0.88; background: radial-gradient(circle, rgba(0, 255, 136, 0.95) 0%, rgba(0, 212, 255, 0.65) 45%, rgba(0, 100, 80, 0.95) 100%); }
    25% { opacity: 1; }
    100% { opacity: 0; }
}

@keyframes full-screen-sonar-anim {
    0% { opacity: 0.8; background: radial-gradient(circle, rgba(255, 184, 0, 0.9) 0%, rgba(255, 140, 0, 0.5) 50%, rgba(80, 50, 0, 0.85) 100%); }
    25% { opacity: 0.95; }
    100% { opacity: 0; }
}

@keyframes full-screen-collapse-anim {
    0% { opacity: 0.85; background: radial-gradient(circle, rgba(168, 85, 247, 0.95) 0%, rgba(0, 212, 255, 0.65) 50%, rgba(50, 0, 100, 0.9) 100%); }
    25% { opacity: 1; }
    100% { opacity: 0; }
}

.full-screen-flash-hit {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 999999;
    animation: full-screen-blast-anim 1.5s ease-out forwards;
}

.full-screen-flash-miss {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 999999;
    animation: full-screen-splash-anim 1.5s ease-out forwards;
}

.full-screen-flash-sonar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 999999;
    animation: full-screen-sonar-anim 1.5s ease-out forwards;
}

.full-screen-flash-collapse {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 999999;
    animation: full-screen-collapse-anim 1.5s ease-out forwards;
}

/* In-Page Flash Banners */
@keyframes screen-red-blast {
    0% { background: rgba(255, 51, 102, 0.95); box-shadow: 0 0 60px #ff3366, inset 0 0 40px #ff9900; transform: scale(1.01); }
    50% { background: rgba(255, 102, 0, 0.7); box-shadow: 0 0 90px #ff6600, inset 0 0 60px #ff3300; }
    100% { background: rgba(45, 12, 28, 0.92); box-shadow: 0 0 25px rgba(255, 51, 102, 0.5); transform: scale(1.0); }
}

@keyframes screen-green-splash {
    0% { background: rgba(0, 255, 136, 0.92); box-shadow: 0 0 50px #00ff88, inset 0 0 40px #00d4ff; transform: scale(1.01); }
    50% { background: rgba(0, 212, 255, 0.65); box-shadow: 0 0 70px #00d4ff, inset 0 0 50px #00ff88; }
    100% { background: rgba(10, 32, 26, 0.9); box-shadow: 0 0 20px rgba(0, 255, 136, 0.35); transform: scale(1.0); }
}

.screen-flash-hit {
    animation: screen-red-blast 1.4s ease-out;
    border: 2px solid #ff3366;
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
    color: #ffffff;
    font-family: 'Orbitron', sans-serif;
    margin-bottom: 14px;
    box-shadow: 0 0 30px rgba(255, 51, 102, 0.6);
}

.screen-flash-miss {
    animation: screen-green-splash 1.4s ease-out;
    border: 2px solid #00ff88;
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
    color: #ffffff;
    font-family: 'Orbitron', sans-serif;
    margin-bottom: 14px;
    box-shadow: 0 0 25px rgba(0, 255, 136, 0.45);
}

/* Level Cards */
.level-card {
    background: rgba(10, 18, 42, 0.85);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 10px;
    padding: 12px 16px;
    text-align: center;
    transition: all 0.25s ease;
}
.level-card.active {
    border: 2px solid var(--cyan);
    background: rgba(0, 212, 255, 0.12);
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.35);
}
.level-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.92rem;
    font-weight: 700;
    margin-bottom: 3px;
}
.level-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    color: var(--text-muted);
}

/* Tactical Field Manual */
.guide-box {
    background: linear-gradient(135deg, rgba(8, 15, 38, 0.95), rgba(12, 24, 58, 0.95));
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 10px;
    padding: 12px 18px;
    margin: 12px 0 16px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.35);
}
.guide-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.88rem;
    font-weight: 800;
    color: #00d4ff;
    letter-spacing: 1px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.guide-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 10px;
}
.guide-step {
    background: rgba(15, 25, 55, 0.7);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 6px;
    padding: 8px 12px;
    display: flex;
    gap: 8px;
    align-items: flex-start;
}
.step-num {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 1rem;
    color: #ffb800;
    line-height: 1.2;
}
.step-content {
    font-size: 0.78rem;
    line-height: 1.4;
    color: #cbd5e1;
}
.step-content strong {
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    display: block;
    margin-bottom: 2px;
}

/* HUD Banner */
.hud-banner {
    background: linear-gradient(135deg, rgba(13, 25, 60, 0.95), rgba(6, 12, 30, 0.95));
    border: 1px solid var(--border-card);
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 14px;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.08);
}
.hud-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: 1.2px;
    color: #ffffff;
    margin-bottom: 2px;
}
.hud-desc {
    font-size: 0.82rem;
    color: var(--text-muted);
    line-height: 1.45;
}

/* Stat Box */
.stat-box {
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 8px;
    padding: 8px 12px;
    text-align: center;
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
    text-transform: uppercase;
}
.stat-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #ffffff;
}

/* Tactical Intel Box */
.intel-card {
    background: rgba(13, 22, 52, 0.92);
    border-left: 4px solid var(--cyan);
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.intel-card.hit {
    border-left-color: var(--red);
    background: rgba(45, 12, 28, 0.85);
}
.intel-card.miss {
    border-left-color: var(--green);
    background: rgba(10, 32, 26, 0.8);
}
.intel-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.88rem;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.intel-header.hit { color: var(--red); }
.intel-header.miss { color: var(--green); }
.intel-body {
    font-size: 0.82rem;
    color: var(--text-primary);
    line-height: 1.5;
}
.intel-principle {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px dashed rgba(255,255,255,0.15);
    font-size: 0.78rem;
    color: var(--cyan);
    font-family: 'JetBrains Mono', monospace;
}

/* Legend items */
.legend-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    background: rgba(8, 12, 30, 0.75);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 6px 14px;
    margin-bottom: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    align-items: center;
}
.legend-tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
.tag-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

/* Quantum Tic-Tac-Toe Bridge Builder Banner */
.bridge-builder-banner {
    background: rgba(13, 25, 60, 0.95);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 12px;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);
}
.bridge-builder-banner.active {
    border: 2px solid #ffcc00;
    background: linear-gradient(135deg, rgba(30, 25, 10, 0.95), rgba(15, 25, 60, 0.95));
    box-shadow: 0 0 20px rgba(255, 184, 0, 0.35);
}
.bb-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.88rem;
    font-weight: 700;
    margin-bottom: 4px;
}
.bb-status {
    font-size: 0.84rem;
    color: var(--text-muted);
}
.bb-flow {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 4px;
}
.bb-node {
    padding: 5px 10px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
}
.bb-node.selected {
    background: rgba(255, 51, 102, 0.25);
    border: 1px solid #ff3366;
    color: #ff6699;
    box-shadow: 0 0 12px rgba(255, 51, 102, 0.4);
}
.bb-node.pending {
    background: rgba(255, 184, 0, 0.2);
    border: 1px dashed #ffb800;
    color: #ffcc00;
    animation: pending-blink 1.5s infinite;
}
@keyframes pending-blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.55; }
}
.bb-link {
    color: #00d4ff;
    font-weight: bold;
    font-size: 0.85rem;
}
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)

# ======================================================================
# Header & Navigation
# ======================================================================
st.markdown('<div class="main-title">⚛ QUANTUM STRATEGY COMMAND</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">'
    'QISKIT 1.X TACTICAL NAVAL SIMULATION &amp; QUANTUM ARCADE &nbsp;·&nbsp; '
    'LEAD DEVELOPER: <strong>PRATHAM D.</strong> '
    '(<a href="https://github.com/pratham603-bit" target="_blank" style="color:#00d4ff;">@pratham603-bit</a>) '
    '&nbsp;·&nbsp; IIIT KOTTAYAM QISKIT FALL FEST 2026'
    '</div>',
    unsafe_allow_html=True,
)

selected_app = st.radio(
    "Select Game / Mode",
    ["🚢 Quantum Battleship (Tactical Campaign)", "⚔️ Quantum Tic-Tac-Toe (Entangled Duel)", "🔬 Quantum Physics Academy"],
    horizontal=True,
    label_visibility="collapsed",
)

# ======================================================================
# Session State Initialization
# ======================================================================
def init_battleship(difficulty="Captain (4x4)"):
    size_map = {"Cadet (3x3)": 3, "Captain (4x4)": 4, "Admiral (5x5)": 5}
    ammo_map = {"Cadet (3x3)": 8, "Captain (4x4)": 11, "Admiral (5x5)": 15}
    goals_map = {"Cadet (3x3)": 2, "Captain (4x4)": 3, "Admiral (5x5)": 4}

    g_size = size_map.get(difficulty, 4)
    eng = QuantumBattleshipEngine(grid_size=g_size)
    eng.auto_deploy_fleet(seed=42)

    if difficulty == "Admiral (5x5)":
        eng.enable_noise(depol_prob=0.03, readout_error=0.06)

    st.session_state.bs_engine = eng
    st.session_state.bs_difficulty = difficulty
    st.session_state.max_torpedoes = ammo_map.get(difficulty, 11)
    st.session_state.torpedoes_used = 0
    st.session_state.sonar_charges = 2
    st.session_state.last_strike = None
    st.session_state.sonar_report = None
    st.session_state.sonar_flash = False
    st.session_state.game_status = "ACTIVE"
    st.session_state.fleet_goal = goals_map.get(difficulty, 3)
    st.session_state.lock_combat_scroll = False

if "bs_engine" not in st.session_state:
    init_battleship("Captain (4x4)")

if "ttt_engine" not in st.session_state:
    st.session_state.ttt_engine = QuantumTicTacToeEngine()
    st.session_state.ttt_selected_sqs = []
    st.session_state.ttt_flash_event = None

# ======================================================================
# 1. QUANTUM BATTLESHIP
# ======================================================================
if selected_app == "🚢 Quantum Battleship (Tactical Campaign)":
    eng: QuantumBattleshipEngine = st.session_state.bs_engine

    # --- Prominent Level Guide & Combat Tier Selectors ---
    st.markdown("### 📋 Admiral's Tactical Briefing &amp; Combat Tiers")
    lvl_col1, lvl_col2, lvl_col3 = st.columns(3)

    cur_diff = st.session_state.bs_difficulty

    with lvl_col1:
        is_active = cur_diff == "Cadet (3x3)"
        st.markdown(
            f"""
            <div class="level-card {'active' if is_active else ''}">
                <div class="level-title" style="color:#00ff88;">🔰 LEVEL 1: CADET</div>
                <div class="level-meta">3×3 Grid · 2 Ships · 8 Torpedoes · 2 Sonar Pings</div>
                <div style="font-size:0.78rem; margin:4px 0; color:#cbd5e1;">Single-qubit 50% superposition without decoherence noise.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Select Cadet (3x3)", use_container_width=True, key="btn_cadet", disabled=is_active):
            init_battleship("Cadet (3x3)")
            st.rerun()

    with lvl_col2:
        is_active = cur_diff == "Captain (4x4)"
        st.markdown(
            f"""
            <div class="level-card {'active' if is_active else ''}">
                <div class="level-title" style="color:#00d4ff;">🎖️ LEVEL 2: CAPTAIN</div>
                <div class="level-meta">4×4 Grid · 3 Ships · 11 Torpedoes · 2 Sonar Pings</div>
                <div style="font-size:0.78rem; margin:4px 0; color:#cbd5e1;">Standard fleet with Bell-Pair Entanglement and linked wavefunctions.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Select Captain (4x4)", use_container_width=True, key="btn_captain", disabled=is_active):
            init_battleship("Captain (4x4)")
            st.rerun()

    with lvl_col3:
        is_active = cur_diff == "Admiral (5x5)"
        st.markdown(
            f"""
            <div class="level-card {'active' if is_active else ''}">
                <div class="level-title" style="color:#ff3366;">⚓ LEVEL 3: ADMIRAL</div>
                <div class="level-meta">5×5 Grid · 4 Ships · 15 Torpedoes · 1 Sonar Ping</div>
                <div style="font-size:0.78rem; margin:4px 0; color:#cbd5e1;">Phase Shields + Real NISQ Hardware Decoherence Noise active.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Select Admiral (5x5)", use_container_width=True, key="btn_admiral", disabled=is_active):
            init_battleship("Admiral (5x5)")
            st.rerun()

    # --- TACTICAL FIELD MANUAL (COMPACT & ALWAYS VISIBLE) ---
    st.markdown(
        """
        <div class="guide-box">
            <div class="guide-title">📖 TACTICAL FIELD MANUAL: HOW TO PLAY &amp; WIN (ZERO BLIND LUCK)</div>
            <div class="guide-grid">
                <div class="guide-step">
                    <div class="step-num">01</div>
                    <div class="step-content">
                        <strong>📡 SCOUT WITH SONAR FIRST</strong>
                        Don't fire blindly! Send Sonar Pings to read quantum amplitudes $P(|1\\rangle)$ along rows or columns without triggering collapse.
                    </div>
                </div>
                <div class="guide-step">
                    <div class="step-num">02</div>
                    <div class="step-content">
                        <strong>🔗 HUNT BELL PAIR VESSELS</strong>
                        Hostile cruisers share a linked Bell state ($|\\Phi^+\\rangle$). Sinking one vessel instantly collapses its partner with 1 torpedo!
                    </div>
                </div>
                <div class="guide-step">
                    <div class="step-num">03</div>
                    <div class="step-content">
                        <strong>💥 FIRE QUANTUM TORPEDOES</strong>
                        Torpedo impact executes projective measurement (<code>qc.measure</code>), collapsing superposition into <strong>💥 Hit (|1⟩)</strong> or <strong>🌊 Miss (|0⟩)</strong>.
                    </div>
                </div>
                <div class="guide-step">
                    <div class="step-num">04</div>
                    <div class="step-content">
                        <strong>🎯 SECURE FLEET VICTORY</strong>
                        Neutralize all required targets before your torpedo ammo runs out. Adapt to NISQ noise in Admiral mode!
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Combat Status & Stats ---
    stats = eng.get_game_stats()
    hits = stats["hits"]
    remaining_ammo = max(0, st.session_state.max_torpedoes - st.session_state.torpedoes_used)
    
    if hits >= st.session_state.fleet_goal and st.session_state.game_status == "ACTIVE":
        st.session_state.game_status = "VICTORY"
    elif remaining_ammo == 0 and hits < st.session_state.fleet_goal and st.session_state.game_status == "ACTIVE":
        st.session_state.game_status = "DEFEAT"

    # --- FULL-SCREEN & IN-PAGE FLASH FX ---
    last = st.session_state.last_strike
    if last is not None:
        target_lbl = last["target_label"]
        if last["hit"]:
            st.markdown('<div class="full-screen-flash-hit"></div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="screen-flash-hit">
                    <div style="font-size:1.25rem; font-weight:900; letter-spacing:1.5px;">💥🔥 DETONATION FLASH! DIRECT HIT ON HOSTILE SHIP! 🔥💥</div>
                    <div style="font-size:0.88rem; opacity:0.92; margin-top:3px;">SECTOR {target_lbl} DESTROYED — WAVEFUNCTION COLLAPSED INTO EIGENVALUE |1⟩!</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div class="full-screen-flash-miss"></div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="screen-flash-miss">
                    <div style="font-size:1.25rem; font-weight:900; letter-spacing:1.5px;">🌊💧 WATER SPLASH! TORPEDO DETONATED IN EMPTY SECTOR! 💧🌊</div>
                    <div style="font-size:0.88rem; opacity:0.92; margin-top:3px;">SECTOR {target_lbl} OBSERVED — WAVEFUNCTION COLLAPSED INTO EIGENVALUE |0⟩!</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    elif st.session_state.get("sonar_flash", False):
        st.markdown('<div class="full-screen-flash-sonar"></div>', unsafe_allow_html=True)
        st.session_state.sonar_flash = False

    # Status Bar
    status_color = "#00ff88" if st.session_state.game_status == "VICTORY" else ("#ff3366" if st.session_state.game_status == "DEFEAT" else "#00d4ff")
    status_msg = "🏆 VICTORY! ALL QUANTUM FLEET TARGETS NEUTRALIZED" if st.session_state.game_status == "VICTORY" else ("💀 MISSION FAILED! OUT OF TORPEDOES" if st.session_state.game_status == "DEFEAT" else f"COMBAT ACTIVE — {st.session_state.bs_difficulty.upper()}")

    st.markdown(
        f"""
        <div class="hud-banner">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                    <div class="hud-title">🚢 TACTICAL HUD: {st.session_state.bs_difficulty.upper()}</div>
                    <div class="hud-desc">
                        Target Goal: Destroy <strong>{st.session_state.fleet_goal} hostile quantum ships</strong>. Use Sonar to scout probabilities, then fire to collapse!
                    </div>
                </div>
                <div style="font-family:'Orbitron',sans-serif; font-weight:800; font-size:0.92rem; color:{status_color}; border:1px solid {status_color}; padding:5px 12px; border-radius:6px; background:rgba(0,0,0,0.4);">
                    {status_msg}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Counters
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(f'<div class="stat-box"><div class="stat-label">Torpedoes Left</div><div class="stat-value" style="color:{"#ff3366" if remaining_ammo <= 2 else "#00d4ff"};">{remaining_ammo} / {st.session_state.max_torpedoes}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-box"><div class="stat-label">Confirmed Hits</div><div class="stat-value" style="color:#00ff88;">{hits} / {st.session_state.fleet_goal}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-box"><div class="stat-label">Confirmed Misses</div><div class="stat-value" style="color:#94a3b8;">{stats["misses"]}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-box"><div class="stat-label">Sonar Pings Left</div><div class="stat-value" style="color:#ffb800;">{st.session_state.sonar_charges}</div></div>', unsafe_allow_html=True)
    with c5:
        if st.button("🔄 Reset Fleet", use_container_width=True):
            init_battleship(st.session_state.bs_difficulty)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- TACTICAL COMBAT ARENA ANCHOR (FOR SCROLL RETENTION) ---
    st.markdown('<div id="tactical-combat-arena"></div>', unsafe_allow_html=True)

    # Scroll lock handler: keeps view locked right at the radar console
    if st.session_state.get("lock_combat_scroll", False):
        components.html(
            """
            <script>
            const el = window.parent.document.getElementById("tactical-combat-arena");
            if (el) {
                el.scrollIntoView({ behavior: 'auto', block: 'start' });
            }
            </script>
            """,
            height=0,
        )
        st.session_state.lock_combat_scroll = False

    # --- Radar Grid & Integrated Reconnaissance Console ---
    left_grid_col, right_intel_col = st.columns([1.1, 0.9])

    with left_grid_col:
        st.markdown("### 🗺️ Sector Radar Grid")
        st.markdown(
            """
            <div class="legend-bar">
                <span class="legend-tag"><span class="tag-dot" style="background:#475569;"></span> ⬡ Fog of War</span>
                <span class="legend-tag"><span class="tag-dot" style="background:#00d4ff;"></span> ≋ Superposition</span>
                <span class="legend-tag"><span class="tag-dot" style="background:#a855f7;"></span> 🔗 Bell Pair</span>
                <span class="legend-tag"><span class="tag-dot" style="background:#ff3366;"></span> 💥 Hit |1⟩</span>
                <span class="legend-tag"><span class="tag-dot" style="background:#00ff88;"></span> ○ Miss |0⟩</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        grid_state = eng.get_grid_state()
        is_game_disabled = st.session_state.game_status != "ACTIVE"

        for r_idx, row in enumerate(grid_state):
            btn_cols = st.columns(len(row))
            for c_idx, cell in enumerate(row):
                q = cell["qubit"]
                lbl = cell["label"]
                state = cell["state"]
                is_measured = q in eng.measured_qubits

                # Button formatting
                is_last_target = (last is not None and last["target"] == q)
                btn_type = "primary" if is_last_target else "secondary"

                if is_last_target:
                    res_tag = "HIT" if state == "hit" else "MISS"
                    btn_label = f"🎯 {lbl} [{res_tag}]"
                    tooltip = f"Last targeted sector: {lbl} (Collapsed to {'|1⟩' if state == 'hit' else '|0⟩'})"
                elif state == "hit":
                    btn_label = f"💥 {lbl} [HIT]"
                    tooltip = f"Sector {lbl}: Collapsed to |1⟩ (Ship Destroyed)"
                elif state == "miss":
                    btn_label = f"○ {lbl} [MISS]"
                    tooltip = f"Sector {lbl}: Collapsed to |0⟩ (Empty Ocean)"
                elif state == "entangled":
                    btn_label = f"🔗 {lbl} [PAIR]"
                    tooltip = f"Sector {lbl}: Entangled Bell vessel. Striking will reveal both coordinates!"
                elif state == "superposition":
                    btn_label = f"≋ {lbl} [50%]"
                    tooltip = f"Sector {lbl}: Superposition |ψ⟩ = (|0⟩+|1⟩)/√2. Launch torpedo to observe!"
                else:
                    btn_label = f"⬡ {lbl}"
                    tooltip = f"Sector {lbl}: Unscanned water."

                if btn_cols[c_idx].button(
                    btn_label,
                    key=f"strike_{q}",
                    disabled=is_measured or is_game_disabled,
                    use_container_width=True,
                    help=tooltip,
                    type=btn_type,
                ):
                    strike_res = eng.fire_torpedo(q, shots=1)
                    st.session_state.torpedoes_used += 1
                    st.session_state.last_strike = strike_res
                    st.session_state.lock_combat_scroll = True
                    st.rerun()

    with right_intel_col:
        st.markdown("### 📡 Tactical Reconnaissance & Intelligence")

        # SONAR SCANNER TOOL MOVED DIRECTLY INTO INTELLIGENCE CONSOLE (PREVENTS SCROLLING)
        st.markdown(
            """
            <div style="background:rgba(15,25,55,0.75); border:1px solid rgba(255,184,0,0.3); border-radius:8px; padding:10px 14px; margin-bottom:12px;">
                <div style="font-family:'Orbitron',sans-serif; font-size:0.84rem; font-weight:700; color:#ffb800; margin-bottom:6px;">
                    📡 NON-DESTRUCTIVE SONAR SCANNER (SCOUT AMBIGUITY)
                </div>
            """,
            unsafe_allow_html=True,
        )
        s_c1, s_c2, s_c3 = st.columns([1, 1, 1.2])
        with s_c1:
            sonar_axis = st.selectbox("Scan Axis", ["Row", "Column"], key="sonar_axis")
        with s_c2:
            max_idx = eng.grid_size
            options = [f"Row {ROW_LABELS[i]}" if sonar_axis == "Row" else f"Col {i}" for i in range(max_idx)]
            sonar_target = st.selectbox("Coordinate", options, key="sonar_target")
            idx_val = options.index(sonar_target)
        with s_c3:
            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
            if st.button("📡 Send Sonar Ping", use_container_width=True, disabled=st.session_state.sonar_charges <= 0 or is_game_disabled):
                axis_key = "row" if sonar_axis == "Row" else "col"
                sonar_data = eng.sonar_ping(axis_key, idx_val)
                st.session_state.sonar_charges -= 1
                st.session_state.sonar_report = (sonar_target, sonar_data)
                st.session_state.sonar_flash = True
                st.session_state.lock_combat_scroll = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Sonar Ping Report (Rendered immediately below the Ping button)
        if st.session_state.sonar_report is not None:
            s_name, s_results = st.session_state.sonar_report
            active_signals = {k: v for k, v in s_results.items() if v > 0.1}
            signal_summary = ", ".join(f"<strong>{k}</strong>: {v:.0%}" for k, v in active_signals.items()) if active_signals else "No significant quantum amplitudes detected along this axis."
            st.markdown(
                f"""
                <div class="intel-card" style="border-left-color:#ffb800; background:rgba(30, 25, 10, 0.85);">
                    <div class="intel-header" style="color:#ffb800;">📡 SONAR PING REPORT: {s_name}</div>
                    <div class="intel-body">
                        Non-destructive amplitude scan complete.<br>
                        Quantum returns: {signal_summary}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Last Strike Detonation Report
        if last is None:
            st.markdown(
                """
                <div class="intel-card">
                    <div class="intel-header" style="color:#00d4ff;">SYSTEM STANDBY — READY FOR ORDERS</div>
                    <div class="intel-body">
                        No torpedo launches registered yet.<br>
                        Click any coordinate on the radar grid to fire a quantum torpedo. Use your Sonar to scan before shooting!
                    </div>
                    <div class="intel-principle">
                        💡 TACTICAL TIP: Bell Pairs are linked. If you strike one, its partner collapses simultaneously!
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            is_hit = last["hit"]
            target_lbl = last["target_label"]
            partner = last.get("entangled_partner")
            partner_res = last.get("partner_result")

            card_class = "hit" if is_hit else "miss"
            result_header = f"💥 DIRECT HIT! DETONATION AT {target_lbl}" if is_hit else f"🌊 WATER SPLASH! TORPEDO MISSED AT {target_lbl}"
            
            entangle_text = ""
            if partner is not None:
                p_lbl = eng.qubit_label(partner)
                p_text = "💥 DIRECT HIT (|1⟩)" if partner_res == 1 else "○ EMPTY OCEAN (|0⟩)"
                entangle_text = f"<br><br><strong>🔗 BELL-STATE ENTANGLEMENT TRIGGERED:</strong><br>Target <code>{target_lbl}</code> was paired with <code>{p_lbl}</code> in Bell state |Φ⁺⟩. Observing <code>{target_lbl}</code> forced <code>{p_lbl}</code> to collapse into <strong>{p_text}</strong>!"

            st.markdown(
                f"""
                <div class="intel-card {card_class}">
                    <div class="intel-header {'hit' if is_hit else 'miss'}">{result_header}</div>
                    <div class="intel-body">
                        Torpedo impact executed a computational-basis measurement (`qc.measure`).<br>
                        Wavefunction collapsed irreversibly into state <strong>|{last['result']}⟩</strong>.
                        {entangle_text}
                    </div>
                    <div class="intel-principle">
                        🔬 PHYSICS PRINCIPLE: Prior to measurement, the sector was in state |ψ⟩ = α|0⟩ + β|1⟩. Your strike acted as an observer, collapsing the superposition with probability P(|1⟩) = |β|².
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Compact Telemetry Tabs
        t1, t2, t3 = st.tabs(["📊 Probabilities", "⚡ Circuit", "📜 Event Log"])
        with t1:
            try:
                fig_amp = eng.get_amplitude_bar_chart(figsize=(7, 2.5))
                st.pyplot(fig_amp, use_container_width=True)
                plt.close(fig_amp)
            except Exception as e:
                st.caption(f"Telemetry: {e}")
        with t2:
            try:
                fig_circ = eng.get_circuit_figure(figsize=(8, 3.2))
                st.pyplot(fig_circ, use_container_width=True)
                plt.close(fig_circ)
            except Exception as e:
                st.caption(f"Circuit: {e}")
        with t3:
            logs = eng.battle_log[-5:] if eng.battle_log else ["Awaiting orders."]
            for l in reversed(logs):
                st.caption(f"• {l}")

# ======================================================================
# 2. QUANTUM TIC-TAC-TOE (VIBRANT SELECTION, BRIDGE BUILDER & FLASH FX)
# ======================================================================
elif selected_app == "⚔️ Quantum Tic-Tac-Toe (Entangled Duel)":
    ttt: QuantumTicTacToeEngine = st.session_state.ttt_engine

    # --- Flash Effects for Moves / Collapse ---
    if st.session_state.ttt_flash_event == "collapse":
        st.markdown('<div class="full-screen-flash-collapse"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="screen-flash-hit" style="border-color:#a855f7; box-shadow:0 0 35px rgba(168,85,247,0.7); background:rgba(40,15,60,0.92);">
                <div style="font-size:1.35rem; font-weight:900; letter-spacing:2px; color:#ffffff;">💥⚡ QUANTUM MEASUREMENT COLLAPSE! ⚡💥</div>
                <div style="font-size:0.9rem; opacity:0.95; margin-top:4px; color:#e2e8f0;">ENTANGLEMENT CYCLE CLOSED — QISKIT CIRCUIT PROJECTED QUANTUM MARKS INTO DEFINITE X AND O!</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.session_state.ttt_flash_event = None
    elif st.session_state.ttt_flash_event == "move":
        st.markdown(
            """
            <div class="screen-flash-miss" style="border-color:#00d4ff; box-shadow:0 0 25px rgba(0,212,255,0.5); background:rgba(6,25,45,0.92);">
                <div style="font-size:1.15rem; font-weight:900; letter-spacing:1px; color:#00d4ff;">⚡ QUANTUM BRIDGE ESTABLISHED! ⚡</div>
                <div style="font-size:0.85rem; opacity:0.95; margin-top:4px; color:#e2e8f0;">Superposition mark forged across chosen squares in Bell-like state (|A⟩+|B⟩)/√2.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.session_state.ttt_flash_event = None

    st.markdown(
        """
        <div class="hud-banner">
            <div class="hud-title">⚔️ QUANTUM TIC-TAC-TOE: ENTANGLED SUPERPOSITION DUEL</div>
            <div class="hud-desc">
                In Classical Tic-Tac-Toe, each move claims 1 square. In <strong>Quantum Tic-Tac-Toe</strong>, each turn you place a 
                <strong>Quantum Bridge across TWO squares at once</strong> ($X_1$ in Sq A &amp; Sq B). 
                When overlapping moves create an entanglement loop, a <strong>Qiskit quantum circuit</strong> executes measurement collapse to resolve them into classical X's and O's!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t_col1, t_col2 = st.columns([1.1, 0.9])

    with t_col1:
        player_color = "#00d4ff" if ttt.current_player == "X" else "#a855f7"
        st.markdown(f"### Current Turn: <span style='color:{player_color}; font-weight:800;'>PLAYER {ttt.current_player}</span>", unsafe_allow_html=True)
        
        # PROMINENT BRIDGE BUILDER SELECTION STATUS BANNER
        sel_list = st.session_state.ttt_selected_sqs
        if len(sel_list) == 0:
            st.markdown(
                f"""
                <div class="bridge-builder-banner">
                    <div class="bb-title" style="color:{player_color};">⚡ QUANTUM BRIDGE BUILDER (TURN {ttt.move_number} · PLAYER {ttt.current_player})</div>
                    <div class="bb-status">👉 <strong>STEP 1:</strong> Click any square on the 3×3 grid below to select <strong>ENDPOINT 1</strong>.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif len(sel_list) == 1:
            s1 = sel_list[0]
            st.markdown(
                f"""
                <div class="bridge-builder-banner active">
                    <div class="bb-title" style="color:#ffcc00;">⚡ QUANTUM BRIDGE IN PROGRESS (PLAYER {ttt.current_player}):</div>
                    <div class="bb-flow">
                        <span class="bb-node selected">📍 ENDPOINT 1: SQUARE {s1 + 1} SELECTED</span>
                        <span class="bb-link">━━━━━━━━⚡━━━━━━━━</span>
                        <span class="bb-node pending">👉 NOW CLICK ENDPOINT 2 TO COMPLETE BRIDGE!</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"✕ Cancel Selection (Deselect Square {s1 + 1})", key="btn_cancel_ttt_sel"):
                st.session_state.ttt_selected_sqs = []
                st.rerun()

        # 3x3 Tactical Board
        for r_i in range(3):
            cols = st.columns(3)
            for c_i in range(3):
                sq_idx = r_i * 3 + c_i
                sq_info = ttt.get_square_contents(sq_idx)
                is_selected = sq_idx in st.session_state.ttt_selected_sqs

                # Button formatting
                if sq_info["classical"] is not None:
                    cl = sq_info["classical"]
                    sq_text = f"🏆 [{cl}]"
                    disabled = True
                    btn_type = "secondary"
                else:
                    pending_marks = " ".join(sq_info["pending"])
                    if is_selected:
                        sq_text = f"🔥 [ENDPOINT 1: Sq {sq_idx + 1}]"
                        btn_type = "primary"
                    elif pending_marks:
                        sq_text = f"Sq {sq_idx + 1}\n({pending_marks})"
                        btn_type = "secondary"
                    else:
                        sq_text = f"Sq {sq_idx + 1}"
                        btn_type = "secondary"
                    disabled = ttt.is_game_over

                # Click Handler with IMMEDIATE RERUN
                if cols[c_i].button(
                    sq_text,
                    key=f"ttt_sq_btn_{sq_idx}",
                    disabled=disabled,
                    use_container_width=True,
                    type=btn_type,
                ):
                    if sq_idx in st.session_state.ttt_selected_sqs:
                        st.session_state.ttt_selected_sqs.remove(sq_idx)
                        st.rerun()
                    else:
                        st.session_state.ttt_selected_sqs.append(sq_idx)
                        if len(st.session_state.ttt_selected_sqs) == 2:
                            s1, s2 = st.session_state.ttt_selected_sqs
                            circ_before = ttt.last_circuit
                            success, msg = ttt.place_move(s1, s2)
                            st.session_state.ttt_selected_sqs = []
                            # Check if collapse occurred
                            if ttt.last_circuit is not None and ttt.last_circuit != circ_before:
                                st.session_state.ttt_flash_event = "collapse"
                            else:
                                st.session_state.ttt_flash_event = "move"
                            st.rerun()
                        else:
                            st.rerun()

        # Synchronized Quick Bridge Selector
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 🔗 Or Place Bridge by Coordinates:")
        bc1, bc2, bc3 = st.columns([1, 1, 1])
        avail_sqs = [i for i in range(9) if ttt.classical_board[i] is None]
        sq_options = [f"Square {i + 1}" for i in avail_sqs]

        with bc1:
            default_a = 0
            if len(st.session_state.ttt_selected_sqs) == 1 and st.session_state.ttt_selected_sqs[0] in avail_sqs:
                default_a = avail_sqs.index(st.session_state.ttt_selected_sqs[0])
            sel_a = st.selectbox("Endpoint A", sq_options if sq_options else ["None"], index=default_a if sq_options else 0, key="sel_bridge_a")
        with bc2:
            default_b = min(default_a + 1, len(sq_options) - 1) if sq_options else 0
            sel_b = st.selectbox("Endpoint B", sq_options if sq_options else ["None"], index=default_b, key="sel_bridge_b")
        with bc3:
            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
            if st.button("⚡ Connect Bridge", use_container_width=True, type="primary", disabled=ttt.is_game_over or len(sq_options) < 2):
                idx_a = avail_sqs[sq_options.index(sel_a)]
                idx_b = avail_sqs[sq_options.index(sel_b)]
                if idx_a == idx_b:
                    st.error("Both endpoints cannot be the same square!")
                else:
                    circ_before = ttt.last_circuit
                    success, msg = ttt.place_move(idx_a, idx_b)
                    st.session_state.ttt_selected_sqs = []
                    if ttt.last_circuit is not None and ttt.last_circuit != circ_before:
                        st.session_state.ttt_flash_event = "collapse"
                    else:
                        st.session_state.ttt_flash_event = "move"
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset Board", use_container_width=True):
            ttt.reset()
            st.session_state.ttt_selected_sqs = []
            st.session_state.ttt_flash_event = None
            st.rerun()

    with t_col2:
        st.markdown("### 🔬 Quantum Entanglement Tracker")
        
        if ttt.is_game_over:
            st.success(f"🏆 GAME COMPLETED! Winner: {ttt.winner}")
        else:
            st.markdown(
                f"""
                <div class="intel-card" style="border-left-color:{player_color};">
                    <div class="intel-header" style="color:{player_color};">TURN {ttt.move_number}: PLAYER {ttt.current_player}</div>
                    <div class="intel-body">
                        Place a quantum superposition mark spanning two squares. 
                        When players' bridges connect in a closed cycle, the Qiskit circuit triggers a simultaneous collapse!
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Compact Circuit Section
        with st.expander("⚡ Quantum Collapse Circuit (Compact)", expanded=True):
            circ_fig = ttt.get_circuit_figure()
            if circ_fig is not None:
                st.pyplot(circ_fig, use_container_width=True)
                plt.close(circ_fig)
            else:
                st.caption("No entanglement cycle triggered yet. Place overlapping moves to build the circuit!")

        st.markdown("##### 📜 Move History:")
        for log in reversed(ttt.log[-5:]):
            st.caption(f"• {log}")

# ======================================================================
# 3. QUANTUM PHYSICS ACADEMY (LATEX EQUATIONS & PHYSICS)
# ======================================================================
else:
    st.markdown(
        """
        <div class="hud-banner">
            <div class="hud-title">📖 QUANTUM ACADEMY: CORE PRINCIPLES &amp; EQUATIONS</div>
            <div class="hud-desc">
                Mathematical formulations and real-world game intuition powering Quantum Battleship &amp; Tic-Tac-Toe.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    qa_col1, qa_col2 = st.columns(2)

    with qa_col1:
        # Card 1: Superposition
        with st.container():
            st.markdown("#### 1. SUPERPOSITION ($H$ &amp; $RY$ GATES)")
            st.markdown("**Real-World Intuition:** A spinning coin in mid-air is neither heads nor tails until it lands. It exists in a linear probability combination of both states simultaneously.")
            st.markdown("**Mathematical Formulation:**")
            st.latex(r"|\psi\rangle = H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}")
            st.latex(r"R_Y(\theta)|0\rangle = \cos\frac{\theta}{2}|0\rangle + \sin\frac{\theta}{2}|1\rangle")
            st.caption("Strategic Gameplay Impact: In Battleship, ships do not sit at fixed coordinates—they exist across multiple sectors with 50% probability until observed.")
            st.divider()

        # Card 2: Bell Entanglement
        with st.container():
            st.markdown("#### 2. BELL-STATE ENTANGLEMENT ($H + CX$)")
            st.markdown("**Real-World Intuition:** Two magic dice linked across the ocean. Rolling one to show a 6 forces the other to reveal a 6 instantly, violating classical independence.")
            st.markdown("**Mathematical Formulation:**")
            st.latex(r"|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}")
            st.latex(r"E = P(\text{same}) - P(\text{diff}) = 1.0 \quad (\text{Classical } E \approx 0)")
            st.caption("Strategic Gameplay Impact: Patrol vessels are linked in Bell pairs. Striking one coordinate instantaneously collapses its partner coordinate across the board!")

    with qa_col2:
        # Card 3: Wavefunction Collapse
        with st.container():
            st.markdown("#### 3. PROJECTIVE MEASUREMENT (COLLAPSE)")
            st.markdown("**Real-World Intuition:** In quantum physics, observation is not passive discovery—it actively forces nature into a definite reality.")
            st.markdown("**Mathematical Formulation:**")
            st.latex(r"|\psi\rangle = \alpha|0\rangle + \beta|1\rangle \xrightarrow{\text{measure}} \begin{cases} |1\rangle & \text{with } P = |\beta|^2 \text{ (HIT)} \\ |0\rangle & \text{with } P = |\alpha|^2 \text{ (MISS)} \end{cases}")
            st.caption("Strategic Gameplay Impact: Launching a torpedo executes a computational-basis measurement (qc.measure), irreversibly collapsing the sector.")
            st.divider()

        # Card 4: NISQ Decoherence & Noise
        with st.container():
            st.markdown("#### 4. NISQ HARDWARE NOISE &amp; DECOHERENCE")
            st.markdown("**Real-World Intuition:** Real quantum computers suffer from thermal fluctuations and gate errors, creating false sonar returns.")
            st.markdown("**Mathematical Formulation:**")
            st.latex(r"\mathcal{E}(\rho) = (1 - p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)")
            st.caption("Strategic Gameplay Impact: Admiral Mode introduces depolarizing and readout noise, testing player adaptability against real quantum hardware degradation.")

# ======================================================================
# Footer
# ======================================================================
st.markdown(
    """
    <div style="text-align:center; margin-top:40px; padding:20px; border-top:1px solid rgba(0,212,255,0.1);">
        <span style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#64748b; letter-spacing:1px;">
            QUANTUM STRATEGY COMMAND v2.6.0 &nbsp;·&nbsp;
            BUILT WITH QISKIT 1.X &amp; STREAMLIT &nbsp;·&nbsp;
            © 2026 PRATHAM D. &nbsp;·&nbsp;
            <a href="https://github.com/pratham603-bit/TheQuantum-Paradox" target="_blank" style="color:#00d4ff; text-decoration:none;">GITHUB REPOSITORY</a>
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
