"""
Quantum Tic-Tac-Toe Engine — Qiskit 1.x Core
=============================================

Implements Allan Goff's Quantum Tic-Tac-Toe with:
1. Superposition moves: each turn places marks across two squares.
2. Entanglement graphs: moves sharing cells become quantum-entangled.
3. Cyclic collapse: when an entanglement cycle forms, a Qiskit circuit
   collapses all entangled moves into classical X's and O's.
4. Classical win verification (rows, columns, diagonals).

Author : Pratham D. (@pratham603-bit)
Event  : Qiskit Fall Fest 2026 — IIIT Kottayam
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator


class QuantumTicTacToeEngine:
    """
    Manages a 3x3 Quantum Tic-Tac-Toe game board with superposition moves
    and Qiskit-driven wavefunction collapse.
    """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """Reset board to initial state."""
        # Classical board: None or 'X' or 'O'
        self.classical_board: List[Optional[str]] = [None] * 9

        # History of quantum moves: list of dicts
        # { "move_id": int, "player": 'X'|'O', "squares": (sq1, sq2), "collapsed_to": sq or None }
        self.moves: List[Dict] = []
        self.current_player: str = "X"
        self.move_number: int = 1
        self.winner: Optional[str] = None
        self.winning_line: Optional[List[int]] = None
        self.is_game_over: bool = False
        self.log: List[str] = ["🎮 Game initialized. Player X's turn to place entangled marks."]
        self.last_circuit: Optional[QuantumCircuit] = None

    def get_square_contents(self, square: int) -> Dict:
        """
        Returns info for a board cell:
        - classical: 'X', 'O', or None
        - pending_marks: list of (player, move_id) currently sharing this square in superposition
        """
        if self.classical_board[square] is not None:
            return {
                "classical": self.classical_board[square],
                "pending": [],
            }

        pending = []
        for m in self.moves:
            if m["collapsed_to"] is None and square in m["squares"]:
                pending.append(f"{m['player']}{m['move_id']}")

        return {
            "classical": None,
            "pending": pending,
        }

    def can_place_move(self, sq1: int, sq2: int) -> Tuple[bool, str]:
        """Check if a quantum move between sq1 and sq2 is valid."""
        if self.is_game_over:
            return False, "Game is already over."
        if sq1 == sq2:
            return False, "Must select two distinct squares."
        if not (0 <= sq1 < 9 and 0 <= sq2 < 9):
            return False, "Squares must be between 0 and 8."
        if self.classical_board[sq1] is not None:
            return False, f"Square {sq1 + 1} is already classically occupied by {self.classical_board[sq1]}."
        if self.classical_board[sq2] is not None:
            return False, f"Square {sq2 + 1} is already classically occupied by {self.classical_board[sq2]}."
        return True, "Valid move."

    def place_move(self, sq1: int, sq2: int) -> Tuple[bool, str]:
        """
        Place a quantum move in superposition across two squares.
        Automatically checks for entanglement cycles and triggers collapse if found.
        """
        valid, msg = self.can_place_move(sq1, sq2)
        if not valid:
            return False, msg

        move_id = self.move_number
        player = self.current_player

        new_move = {
            "move_id": move_id,
            "player": player,
            "squares": (sq1, sq2),
            "collapsed_to": None,
        }
        self.moves.append(new_move)

        log_msg = f"⚛ Player {player} placed mark {player}{move_id} in superposition on squares {sq1 + 1} and {sq2 + 1}."
        self.log.append(log_msg)

        # Check for cycles
        cycle_found = self._detect_cycle()
        if cycle_found:
            collapse_msg = self.collapse_wavefunction()
            self.log.append(f"🌀 Entanglement loop detected! {collapse_msg}")
        else:
            # Switch turn
            self.current_player = "O" if self.current_player == "X" else "X"
            self.move_number += 1

        # Check win condition
        self._check_winner()

        return True, log_msg

    def _detect_cycle(self) -> bool:
        """
        Builds the entanglement graph of active (uncollapsed) moves.
        Detects if an undirected cycle exists.
        """
        active_moves = [m for m in self.moves if m["collapsed_to"] is None]
        if len(active_moves) < 2:
            return False

        # Build adjacency graph
        adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(9)}
        for m in active_moves:
            u, v = m["squares"]
            m_id = m["move_id"]
            adj[u].append((v, m_id))
            adj[v].append((u, m_id))

        # DFS for cycle detection
        visited: Set[int] = set()

        def dfs(node: int, parent_edge: Optional[int]) -> bool:
            visited.add(node)
            for neighbor, edge_id in adj[node]:
                if edge_id == parent_edge:
                    continue
                if neighbor in visited:
                    return True
                if dfs(neighbor, edge_id):
                    return True
            return False

        for node in range(9):
            if node not in visited:
                if dfs(node, None):
                    return True

        # Also trigger collapse if board is becoming crowded (e.g. >= 6 active moves)
        if len(active_moves) >= 6:
            return True

        return False

    def collapse_wavefunction(self) -> str:
        """
        Builds a Qiskit circuit with superposition and CNOT entanglement constraints,
        measures the circuit, and collapses active moves into definite classical squares.
        """
        active_moves = [m for m in self.moves if m["collapsed_to"] is None]
        if not active_moves:
            return "No active quantum moves to collapse."

        n_qubits = len(active_moves)
        qr = QuantumRegister(n_qubits, "qmark")
        cr = ClassicalRegister(n_qubits, "cmark")
        qc = QuantumCircuit(qr, cr)

        # 1. Put all active moves into superposition (H gate on each move qubit)
        for i in range(n_qubits):
            qc.h(qr[i])

        # 2. Add entanglement (CX) between moves that share squares
        for i in range(n_qubits):
            for j in range(i + 1, n_qubits):
                sq_i = set(active_moves[i]["squares"])
                sq_j = set(active_moves[j]["squares"])
                shared = sq_i.intersection(sq_j)
                if shared:
                    # Entangle the two moves because they compete for the same square
                    qc.cx(qr[i], qr[j])

        # 3. Measurement
        qc.measure(qr, cr)
        self.last_circuit = qc

        # 4. Execute on AerSimulator
        backend = AerSimulator()
        transpiled = transpile(qc, backend)
        job = backend.run(transpiled, shots=1)
        result = job.result().get_counts()
        bitstring = list(result.keys())[0].replace(" ", "")

        # Qiskit rightmost bit is qubit 0
        bits = bitstring[::-1]

        # 5. Resolve collapsed squares
        occupied = set(sq for sq, p in enumerate(self.classical_board) if p is not None)
        collapsed_report = []

        for i, move in enumerate(active_moves):
            bit = int(bits[i]) if i < len(bits) else 0
            primary = move["squares"][bit]       # 0 -> sq1, 1 -> sq2
            secondary = move["squares"][1 - bit]

            if primary not in occupied:
                chosen = primary
            elif secondary not in occupied:
                chosen = secondary
            else:
                # Square contested, find first empty square or tie
                empty_sqs = [sq for sq in range(9) if sq not in occupied]
                chosen = empty_sqs[0] if empty_sqs else primary

            move["collapsed_to"] = chosen
            self.classical_board[chosen] = move["player"]
            occupied.add(chosen)
            collapsed_report.append(f"{move['player']}{move['move_id']} → Square {chosen + 1}")

        # Switch to the next player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.move_number += 1

        return "Collapsed: " + ", ".join(collapsed_report)

    def _check_winner(self) -> None:
        """Evaluate if any player has achieved 3 in a row."""
        b = self.classical_board
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
            [0, 4, 8], [2, 4, 6]             # diags
        ]

        x_win = False
        o_win = False

        for line in lines:
            if b[line[0]] is not None and b[line[0]] == b[line[1]] == b[line[2]]:
                if b[line[0]] == "X":
                    x_win = True
                    self.winning_line = line
                elif b[line[0]] == "O":
                    o_win = True
                    self.winning_line = line

        if x_win and o_win:
            self.winner = "Draw"
            self.is_game_over = True
            self.log.append("🏆 Entanglement simultaneity! Both players scored — DRAW!")
        elif x_win:
            self.winner = "X"
            self.is_game_over = True
            self.log.append("🏆 Player X wins by classical alignment!")
        elif o_win:
            self.winner = "O"
            self.is_game_over = True
            self.log.append("🏆 Player O wins by classical alignment!")
        elif all(sq is not None for sq in b):
            self.winner = "Draw"
            self.is_game_over = True
            self.log.append("🏆 Board full — Game ended in a DRAW!")

    def get_circuit_figure(self) -> Optional[plt.Figure]:
        """Return a Matplotlib rendering of the last collapse circuit."""
        if self.last_circuit is None:
            return None
        try:
            fig = self.last_circuit.draw(output="mpl", style="iqp", plot_barriers=False, scale=0.75)
            if hasattr(fig, "set_size_inches"):
                fig.set_size_inches(6.0, 2.2)
            return fig
        except Exception:
            return None

    @property
    def board(self) -> List[Dict]:
        """Backward-compatible property returning list of cell dicts."""
        return [self.get_square_contents(i) for i in range(9)]

    @property
    def last_circuit_figure(self) -> Optional[plt.Figure]:
        """Backward-compatible property returning the circuit figure."""
        return self.get_circuit_figure()

