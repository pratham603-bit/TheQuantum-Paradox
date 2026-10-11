"""
Quantum Battleship Engine — Qiskit 1.x Production Core
========================================================

Production-grade quantum game engine implementing superposition ship
placement, Bell-state entanglement, projective measurement collapse,
phase interference countermeasures, and NISQ noise simulation.

Author : Pratham D. (@pratham603-bit)
Version: 1.0.0
Track  : Quantum Games & Interactive Puzzles
Event  : Qiskit Fall Fest 2026 — IIIT Kottayam
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROW_LABELS = "ABCDEFGHIJKLMNOP"

BELL_LABELS: Dict[str, str] = {
    "phi_plus":  "|Φ⁺⟩",
    "phi_minus": "|Φ⁻⟩",
    "psi_plus":  "|Ψ⁺⟩",
    "psi_minus": "|Ψ⁻⟩",
}


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class QuantumBattleshipEngine:
    """
    Maps an *N × N* strategic fleet grid to quantum registers and exposes
    the full spectrum of quantum-mechanical gameplay operations.

    Each grid cell is backed by one qubit.  The engine maintains a
    measurement-free *logical circuit* for statevector introspection and
    builds temporary *measurement circuits* when torpedoes are fired.

    Parameters
    ----------
    grid_size : int
        Side length of the square grid (default 4 → 16 qubits).
    """

    # ------------------------------------------------------------------ #
    #  Initialisation
    # ------------------------------------------------------------------ #

    def __init__(self, grid_size: int = 4) -> None:
        self.grid_size: int = grid_size
        self.n_qubits: int = grid_size * grid_size

        # Quantum / classical registers
        self.qr = QuantumRegister(self.n_qubits, "ship")
        self.cr = ClassicalRegister(self.n_qubits, "sonar")
        self.circuit = QuantumCircuit(self.qr, self.cr)

        # ---- state bookkeeping ----------------------------------------
        self.measured_qubits: set[int] = set()
        self.measurement_results: Dict[int, int] = {}
        self.entangled_pairs: List[Tuple[int, int, str]] = []
        self.superposition_qubits: set[int] = set()
        self.phase_shields: Dict[int, str] = {}
        self.gate_log: List[str] = []
        self.battle_log: List[str] = []

        # ---- backends -------------------------------------------------
        self.ideal_backend = AerSimulator(method="statevector")
        self.noisy_backend: Optional[AerSimulator] = None
        self.use_noise: bool = False
        self._noise_params: Tuple[float, float] = (0.0, 0.0)

    # ------------------------------------------------------------------ #
    #  Coordinate helpers
    # ------------------------------------------------------------------ #

    def coord_to_qubit(self, row: int, col: int) -> int:
        """Map grid coordinate *(row, col)* → qubit index."""
        return row * self.grid_size + col

    def qubit_to_coord(self, qubit: int) -> Tuple[int, int]:
        """Map qubit index → *(row, col)*."""
        return divmod(qubit, self.grid_size)

    def qubit_label(self, qubit: int) -> str:
        """Human-readable label, e.g. ``'B3'``."""
        r, c = self.qubit_to_coord(qubit)
        return f"{ROW_LABELS[r]}{c}"

    # ------------------------------------------------------------------ #
    #  Ship Placement — Superposition
    # ------------------------------------------------------------------ #

    def place_superposition_ship(
        self,
        qubits: List[int],
        theta: Optional[float] = None,
    ) -> List[str]:
        """
        Distribute ship existence across *qubits* via superposition.

        * ``theta is None`` → Hadamard (equal 50/50 superposition).
        * ``theta`` given   → *RY(θ)* for weighted amplitudes.

        |ψ⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩

        Returns a list of human-readable log entries.
        """
        logs: List[str] = []
        for q in qubits:
            if q in self.measured_qubits:
                logs.append(
                    f"⚠ Qubit {self.qubit_label(q)} already collapsed — skipped."
                )
                continue

            if theta is not None:
                self.circuit.ry(theta, self.qr[q])
                entry = (
                    f"≋  RY({theta:.2f}) applied to {self.qubit_label(q)} "
                    f"— P(hit) = {math.sin(theta / 2) ** 2:.1%}"
                )
            else:
                self.circuit.h(self.qr[q])
                entry = (
                    f"≋  Hadamard applied to {self.qubit_label(q)} "
                    f"— 50 / 50 superposition"
                )

            self.superposition_qubits.add(q)
            self.gate_log.append(entry)
            self.battle_log.append(entry)
            logs.append(entry)

        return logs

    # ------------------------------------------------------------------ #
    #  Bell-State Entangled Flotilla
    # ------------------------------------------------------------------ #

    def entangle_patrol_pair(
        self,
        qubit_a: int,
        qubit_b: int,
        bell_state: str = "phi_plus",
    ) -> Tuple[bool, str]:
        """
        Prepare a Bell pair between *qubit_a* and *qubit_b*.

        Supported Bell states
        ---------------------
        * ``phi_plus``  — |Φ⁺⟩ = (|00⟩ + |11⟩) / √2
        * ``phi_minus`` — |Φ⁻⟩ = (|00⟩ − |11⟩) / √2
        * ``psi_plus``  — |Ψ⁺⟩ = (|01⟩ + |10⟩) / √2
        * ``psi_minus`` — |Ψ⁻⟩ = (|01⟩ − |10⟩) / √2

        Returns ``(success, message)``.
        """
        if qubit_a in self.measured_qubits or qubit_b in self.measured_qubits:
            msg = "⚠ Cannot entangle already-collapsed qubits."
            return False, msg

        if qubit_a == qubit_b:
            return False, "⚠ Cannot entangle a qubit with itself."

        # Core Bell circuit: H then CX
        self.circuit.h(self.qr[qubit_a])
        self.circuit.cx(self.qr[qubit_a], self.qr[qubit_b])

        # Variant adjustments
        if bell_state == "phi_minus":
            self.circuit.z(self.qr[qubit_a])
        elif bell_state == "psi_plus":
            self.circuit.x(self.qr[qubit_b])
        elif bell_state == "psi_minus":
            self.circuit.z(self.qr[qubit_a])
            self.circuit.x(self.qr[qubit_b])

        label = BELL_LABELS.get(bell_state, "|Φ⁺⟩")
        self.entangled_pairs.append((qubit_a, qubit_b, bell_state))
        self.superposition_qubits.update({qubit_a, qubit_b})

        msg = (
            f"🔗  Bell pair {label} deployed: "
            f"{self.qubit_label(qubit_a)} ⟷ {self.qubit_label(qubit_b)}"
        )
        self.gate_log.append(msg)
        self.battle_log.append(msg)
        return True, msg

    # ------------------------------------------------------------------ #
    #  Phase & Interference Countermeasures
    # ------------------------------------------------------------------ #

    def apply_phase_shield(
        self,
        target_qubit: int,
        gate_type: str = "Z",
        angle: Optional[float] = None,
    ) -> Tuple[bool, str]:
        """
        Introduce destructive quantum interference on *target_qubit*.

        Phase gates rotate the relative phase between |0⟩ and |1⟩
        amplitudes without changing measurement probabilities in the
        computational basis — but they *do* alter interference patterns
        and entanglement correlations.

        Supported gates: ``Z``, ``S``, ``T``, ``RZ`` (requires *angle*).
        """
        if target_qubit in self.measured_qubits:
            return False, "⚠ Cannot shield a collapsed qubit."

        gate_map = {
            "Z": lambda: self.circuit.z(self.qr[target_qubit]),
            "S": lambda: self.circuit.s(self.qr[target_qubit]),
            "T": lambda: self.circuit.t(self.qr[target_qubit]),
        }

        if gate_type in gate_map:
            gate_map[gate_type]()
        elif gate_type == "RZ" and angle is not None:
            self.circuit.rz(angle, self.qr[target_qubit])
        else:
            return False, f"⚠ Unknown gate type '{gate_type}'."

        self.phase_shields[target_qubit] = gate_type
        label_angle = f"({angle:.2f})" if gate_type == "RZ" and angle else ""
        msg = (
            f"🛡  {gate_type}{label_angle}-shield activated "
            f"on {self.qubit_label(target_qubit)}"
        )
        self.gate_log.append(msg)
        self.battle_log.append(msg)
        return True, msg

    # ------------------------------------------------------------------ #
    #  Projective Measurement — Fire Torpedo
    # ------------------------------------------------------------------ #

    def fire_torpedo(
        self, target_qubit: int, shots: int = 1
    ) -> Dict:
        """
        Execute a projective basis measurement on *target_qubit*.

        Measurement semantics:
        * |1⟩ → Hit (ship detected at coordinate)
        * |0⟩ → Miss (empty waters)

        If the qubit is part of an entangled Bell pair whose partner has
        not yet been measured, the partner collapses *simultaneously*
        (demonstrating non-local correlations).

        The logical circuit is updated with ``reset → X`` (if |1⟩) to
        ensure all subsequent operations respect the collapsed eigenstate.

        Returns a result dictionary with keys: ``target``, ``target_label``,
        ``result``, ``hit``, ``already_measured``, ``counts``,
        ``entangled_partner``, ``partner_result``.
        """
        if target_qubit in self.measured_qubits:
            prev = self.measurement_results[target_qubit]
            return {
                "target": target_qubit,
                "target_label": self.qubit_label(target_qubit),
                "result": prev,
                "hit": prev == 1,
                "already_measured": True,
                "counts": {str(prev): shots},
                "entangled_partner": None,
                "partner_result": None,
            }

        # --- Find entangled partner (if any) ---------------------------
        entangled_partner: Optional[int] = None
        for qa, qb, _ in self.entangled_pairs:
            if target_qubit == qa and qb not in self.measured_qubits:
                entangled_partner = qb
                break
            if target_qubit == qb and qa not in self.measured_qubits:
                entangled_partner = qa
                break

        qubits_to_measure: List[int] = [target_qubit]
        if entangled_partner is not None:
            qubits_to_measure.append(entangled_partner)

        # --- Build measurement circuit (copy) --------------------------
        meas_circuit = self.circuit.copy()
        for q in qubits_to_measure:
            meas_circuit.measure(self.qr[q], self.cr[q])

        backend = self._get_backend()
        transpiled = transpile(meas_circuit, backend)
        job = backend.run(transpiled, shots=max(shots, 1))
        counts = job.result().get_counts()

        # --- Parse most-probable outcome -------------------------------
        most_probable = max(counts, key=counts.get)
        bitstring = most_probable.replace(" ", "")
        padded = bitstring.zfill(self.n_qubits)
        # Qiskit convention: rightmost bit = qubit 0
        reversed_bits = padded[::-1]

        for q in qubits_to_measure:
            bit_val = int(reversed_bits[q]) if q < len(reversed_bits) else 0
            self.measurement_results[q] = bit_val
            self.measured_qubits.add(q)

            # Collapse the logical circuit so future ops respect outcome
            self.circuit.reset(self.qr[q])
            if bit_val == 1:
                self.circuit.x(self.qr[q])

        target_result = self.measurement_results[target_qubit]
        partner_result = (
            self.measurement_results.get(entangled_partner)
            if entangled_partner is not None
            else None
        )

        # --- Battle-log entry ------------------------------------------
        hit_miss = "💥 HIT" if target_result == 1 else "○ MISS"
        log_entry = (
            f"🎯  Torpedo → {self.qubit_label(target_qubit)}: "
            f"{hit_miss}  |{target_result}⟩"
        )
        if entangled_partner is not None and partner_result is not None:
            p_hm = "💥 HIT" if partner_result == 1 else "○ MISS"
            log_entry += (
                f"  ⟨entangled collapse → "
                f"{self.qubit_label(entangled_partner)}: {p_hm}  "
                f"|{partner_result}⟩⟩"
            )
        self.battle_log.append(log_entry)

        return {
            "target": target_qubit,
            "target_label": self.qubit_label(target_qubit),
            "result": target_result,
            "hit": target_result == 1,
            "already_measured": False,
            "counts": counts,
            "entangled_partner": entangled_partner,
            "partner_result": partner_result,
        }

    # ------------------------------------------------------------------ #
    #  NISQ Noise Simulation
    # ------------------------------------------------------------------ #

    def enable_noise(
        self,
        depol_prob: float = 0.02,
        readout_error: float = 0.05,
    ) -> str:
        """
        Construct a noise model with depolarising gate errors and
        asymmetric readout errors, simulating physical NISQ decoherence.

        Parameters
        ----------
        depol_prob : float
            Single-qubit depolarising error probability.
            Two-qubit gates receive ``min(10×p, 1.0)``.
        readout_error : float
            Symmetric classical readout bit-flip probability.
        """
        noise_model = NoiseModel()

        # Single-qubit depolarising error
        err_1q = depolarizing_error(depol_prob, 1)
        noise_model.add_all_qubit_quantum_error(
            err_1q, ["h", "x", "y", "z", "s", "t", "ry", "rz"]
        )

        # Two-qubit depolarising error (typically ~10× single-qubit rate)
        err_2q = depolarizing_error(min(depol_prob * 10, 1.0), 2)
        noise_model.add_all_qubit_quantum_error(err_2q, ["cx"])

        # Readout error (symmetric)
        p = readout_error
        ro = ReadoutError([[1 - p, p], [p, 1 - p]])
        noise_model.add_all_qubit_readout_error(ro)

        self.noisy_backend = AerSimulator(noise_model=noise_model)
        self.use_noise = True
        self._noise_params = (depol_prob, readout_error)

        msg = (
            f"📡  NISQ noise enabled — depolarising p={depol_prob:.3f}, "
            f"readout ε={readout_error:.3f}"
        )
        self.battle_log.append(msg)
        return msg

    def disable_noise(self) -> str:
        """Switch back to ideal statevector simulator."""
        self.use_noise = False
        msg = "📡  Switched to ideal statevector simulator."
        self.battle_log.append(msg)
        return msg

    def _get_backend(self) -> AerSimulator:
        """Return the active simulation backend."""
        if self.use_noise and self.noisy_backend is not None:
            return self.noisy_backend
        return self.ideal_backend

    # ------------------------------------------------------------------ #
    #  Telemetry & Visualisation
    # ------------------------------------------------------------------ #

    def get_statevector_probabilities(self) -> Dict[int, float]:
        """
        Return per-qubit marginal P(|1⟩) for every cell.

        For already-measured qubits the collapsed eigenvalue is returned
        directly (1.0 for hit, 0.0 for miss).
        """
        try:
            # Build a measurement-free copy for SV calculation
            sv_circuit = self.circuit.copy()
            sv_circuit.remove_final_measurements(inplace=True)

            sv = Statevector(sv_circuit)
            probs_dict = sv.probabilities_dict()

            qubit_probs: Dict[int, float] = {}
            for q in range(self.n_qubits):
                if q in self.measured_qubits:
                    qubit_probs[q] = float(self.measurement_results[q])
                else:
                    # Marginalise: sum P over all bitstrings where qubit q = 1
                    p1 = 0.0
                    for bitstring, prob in probs_dict.items():
                        padded = bitstring.zfill(self.n_qubits)
                        rev = padded[::-1]
                        if q < len(rev) and rev[q] == "1":
                            p1 += prob
                    qubit_probs[q] = p1
            return qubit_probs

        except Exception:
            # Fallback heuristic when SV computation fails
            return {
                q: (
                    float(self.measurement_results[q])
                    if q in self.measured_qubits
                    else (0.5 if q in self.superposition_qubits else 0.0)
                )
                for q in range(self.n_qubits)
            }

    def get_circuit_figure(
        self, figsize: Tuple[float, float] = (14, 6)
    ) -> plt.Figure:
        """Return a Matplotlib figure of the current quantum circuit."""
        try:
            fig = self.circuit.draw(
                output="mpl",
                style="iqp",
                plot_barriers=False,
            )
            if hasattr(fig, "set_size_inches"):
                fig.set_size_inches(figsize)
            return fig
        except Exception:
            fig, ax = plt.subplots(figsize=figsize)
            ax.text(
                0.5, 0.5,
                "Circuit visualisation unavailable",
                ha="center", va="center", fontsize=14, color="#888",
            )
            ax.set_facecolor("#0a0a2e")
            fig.patch.set_facecolor("#0a0a2e")
            ax.axis("off")
            return fig

    def get_histogram_figure(
        self, counts: Dict[str, int], figsize: Tuple[float, float] = (8, 4)
    ) -> plt.Figure:
        """Return a Matplotlib histogram from measurement counts."""
        try:
            fig = plot_histogram(counts, figsize=figsize)
            return fig
        except Exception:
            fig, ax = plt.subplots(figsize=figsize)
            labels = list(counts.keys())
            values = list(counts.values())
            ax.bar(labels, values, color="#00d4ff")
            ax.set_facecolor("#0a0a2e")
            fig.patch.set_facecolor("#0a0a2e")
            ax.tick_params(colors="white")
            ax.set_ylabel("Counts", color="white")
            return fig

    def get_amplitude_bar_chart(
        self, figsize: Tuple[float, float] = (10, 4)
    ) -> plt.Figure:
        """Bar chart of per-qubit P(|1⟩) probability amplitudes."""
        probs = self.get_statevector_probabilities()
        labels = [self.qubit_label(q) for q in range(self.n_qubits)]
        values = [probs[q] for q in range(self.n_qubits)]

        colours = []
        for q in range(self.n_qubits):
            if q in self.measured_qubits:
                colours.append("#ff3366" if probs[q] > 0.5 else "#4a5568")
            elif q in self.superposition_qubits:
                colours.append("#00d4ff")
            else:
                colours.append("#1a1a4e")

        fig, ax = plt.subplots(figsize=figsize)
        ax.bar(labels, values, color=colours, edgecolor="#333", linewidth=0.5)
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("P( |1⟩ )", color="white", fontsize=11)
        ax.set_xlabel("Grid Cell", color="white", fontsize=11)
        ax.set_title(
            "Probability Amplitude Distribution", color="white", fontsize=13
        )
        ax.set_facecolor("#0d1117")
        fig.patch.set_facecolor("#0d1117")
        ax.tick_params(colors="white", labelsize=8)
        ax.spines["bottom"].set_color("#333")
        ax.spines["left"].set_color("#333")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.axhline(y=0.5, color="#555", linestyle="--", linewidth=0.8, alpha=0.6)
        plt.tight_layout()
        return fig

    # ------------------------------------------------------------------ #
    #  Grid State Snapshot
    # ------------------------------------------------------------------ #

    def get_grid_state(self) -> List[List[Dict]]:
        """
        Build a 2-D grid of cell-state dictionaries for the UI layer.

        Each cell contains:
            qubit, row, col, label, state, probability,
            is_entangled, has_shield, measurement
        """
        probs = self.get_statevector_probabilities()
        grid: List[List[Dict]] = []

        for row in range(self.grid_size):
            grid_row: List[Dict] = []
            for col in range(self.grid_size):
                q = self.coord_to_qubit(row, col)

                is_entangled = any(
                    q in (qa, qb) for qa, qb, _ in self.entangled_pairs
                )
                is_measured = q in self.measured_qubits
                is_super = q in self.superposition_qubits
                has_shield = q in self.phase_shields

                if is_measured:
                    state = "hit" if self.measurement_results[q] == 1 else "miss"
                elif is_entangled and is_super:
                    state = "entangled"
                elif is_super:
                    state = "superposition"
                else:
                    state = "fog"

                grid_row.append(
                    {
                        "qubit": q,
                        "row": row,
                        "col": col,
                        "label": self.qubit_label(q),
                        "state": state,
                        "probability": probs.get(q, 0.0),
                        "is_entangled": is_entangled and not is_measured,
                        "has_shield": has_shield,
                        "measurement": self.measurement_results.get(q),
                    }
                )
            grid.append(grid_row)
        return grid

    # ------------------------------------------------------------------ #
    #  Auto-Deploy Fleet (demo / quick-start)
    # ------------------------------------------------------------------ #

    def auto_deploy_fleet(self, seed: Optional[int] = None) -> List[str]:
        """
        Automatically place a randomised quantum fleet scaled to grid size:
        * 3x3: 2 superposition ships, 1 Bell pair
        * 4x4: 4 superposition ships, 2 Bell pairs, 1 shield
        * 5x5: 6 superposition ships, 2 Bell pairs, 2 shields
        """
        rng = np.random.default_rng(seed)
        all_qubits = list(range(self.n_qubits))
        rng.shuffle(all_qubits)

        logs: List[str] = []
        n_ships = max(2, self.grid_size - 1)
        n_pairs = 1 if self.grid_size <= 3 else 2

        # -- Superposition ships ----------------------------------------
        ship_qubits = sorted(all_qubits[:n_ships])
        logs += self.place_superposition_ship(ship_qubits)

        # -- Bell pairs (from remaining qubits) -------------------------
        remaining = all_qubits[n_ships:]
        pair_count = 0
        for i in range(0, len(remaining) - 1, 2):
            if pair_count >= n_pairs:
                break
            qa, qb = remaining[i], remaining[i + 1]
            ok, msg = self.entangle_patrol_pair(qa, qb, "phi_plus")
            if ok:
                logs.append(msg)
                pair_count += 1

        # -- Phase shields on random superposition qubits --------------
        shield_candidates = list(self.superposition_qubits)
        if shield_candidates and self.grid_size >= 4:
            rng.shuffle(shield_candidates)
            for q in shield_candidates[:min(2, len(shield_candidates))]:
                ok, msg = self.apply_phase_shield(q, "S")
                if ok:
                    logs.append(msg)

        self.battle_log.insert(0, "⚛  Fleet auto-deployed!")
        return logs

    def sonar_ping(self, axis: str, index: int) -> Dict[str, float]:
        """
        Non-destructive quantum sonar scan along a row ('row') or column ('col').
        Returns coordinate label -> P(|1⟩) probability amplitude without collapsing.
        """
        probs = self.get_statevector_probabilities()
        results: Dict[str, float] = {}
        if axis == "row":
            for col in range(self.grid_size):
                q = self.coord_to_qubit(index, col)
                results[self.qubit_label(q)] = probs.get(q, 0.0)
        else:
            for row in range(self.grid_size):
                q = self.coord_to_qubit(row, index)
                results[self.qubit_label(q)] = probs.get(q, 0.0)
        return results

    # ------------------------------------------------------------------ #
    #  Game Statistics
    # ------------------------------------------------------------------ #

    def get_game_stats(self) -> Dict[str, int]:
        """Return current game statistics as a flat dictionary."""
        return {
            "total_cells": self.n_qubits,
            "measured": len(self.measured_qubits),
            "hits": sum(
                1 for v in self.measurement_results.values() if v == 1
            ),
            "misses": sum(
                1 for v in self.measurement_results.values() if v == 0
            ),
            "superposition_active": len(
                self.superposition_qubits - self.measured_qubits
            ),
            "entangled_pairs": len(self.entangled_pairs),
            "shields_active": len(
                {q for q in self.phase_shields if q not in self.measured_qubits}
            ),
            "gates_applied": len(self.gate_log),
        }

    # ------------------------------------------------------------------ #
    #  Reset
    # ------------------------------------------------------------------ #

    def reset(self) -> None:
        """Full game-state reset."""
        self.__init__(self.grid_size)


# ---------------------------------------------------------------------------
# Noise Sweep Utility (for notebooks / benchmarks)
# ---------------------------------------------------------------------------

def noise_sweep(
    grid_size: int = 4,
    depol_range: Optional[List[float]] = None,
    shots: int = 1024,
    seed: int = 42,
) -> Tuple[List[float], List[float]]:
    """
    Run a depolarising-error sweep and return ``(p_values, hit_fidelities)``.

    For each depolarising probability *p* in *depol_range* the full
    auto-deploy scenario is simulated with *shots* samples and the
    fraction of shots matching the ideal (noiseless) outcome is recorded.
    This quantifies hit-fidelity degradation under realistic NISQ noise.
    """
    if depol_range is None:
        depol_range = [round(x * 0.01, 3) for x in range(0, 21)]

    # --- ideal reference -----------------------------------------------
    ideal_eng = QuantumBattleshipEngine(grid_size)
    ideal_eng.auto_deploy_fleet(seed=seed)

    ideal_circuit = ideal_eng.circuit.copy()
    for q in range(ideal_eng.n_qubits):
        ideal_circuit.measure(ideal_eng.qr[q], ideal_eng.cr[q])

    ideal_bk = AerSimulator(method="statevector")
    ideal_job = ideal_bk.run(
        transpile(ideal_circuit, ideal_bk), shots=shots
    )
    ideal_counts = ideal_job.result().get_counts()
    ideal_outcome = max(ideal_counts, key=ideal_counts.get)

    # --- noisy sweep ---------------------------------------------------
    fidelities: List[float] = []
    for p in depol_range:
        eng = QuantumBattleshipEngine(grid_size)
        eng.auto_deploy_fleet(seed=seed)

        if p > 0:
            eng.enable_noise(depol_prob=p, readout_error=p * 2)

        meas_circ = eng.circuit.copy()
        for q in range(eng.n_qubits):
            meas_circ.measure(eng.qr[q], eng.cr[q])

        bk = eng._get_backend()
        job = bk.run(transpile(meas_circ, bk), shots=shots)
        counts = job.result().get_counts()

        fidelity = counts.get(ideal_outcome, 0) / shots
        fidelities.append(fidelity)

    return depol_range, fidelities
