"""
Robot AI agent.

Behaviour modes
---------------
pursue   Human > flee_distance away  → A* toward real flag
flee     Human ≤ flee_distance away  → A* toward farthest reachable cell
deceive  (pursue sub-mode)           → A* toward a random fake flag for a
                                       fixed number of steps, then revert.
                                       Shown externally as 'pursue' so the
                                       player cannot distinguish it from
                                       genuine flag-seeking behaviour.
"""

import random
from collections import deque
from pathfinding.astar import astar, heuristic


class Robot:
    def __init__(self, pos: tuple, rows: int, cols: int,
                 flee_distance: int = 4, deception_chance: float = 0.12):
        self.pos              = pos
        self.rows             = rows
        self.cols             = cols
        self.path: list[tuple] = []
        self.mode             = 'pursue'          # 'pursue' | 'flee' | 'deceive'
        self.flee_distance    = flee_distance
        self.deception_chance = deception_chance
        self._decoy_target: tuple | None = None
        self._decoy_steps    = 0                  # robot moves remaining in decoy run
        self._decoy_cooldown = 0                  # moves before next decoy is allowed

    # ── Public API ────────────────────────────────────────────────────────────

    def update_path(self, passages: list[list[set]],
                    real_flag: tuple, fake_flags: list[tuple],
                    human_pos: tuple) -> None:
        """Recalculate the planned path based on current game state."""
        dist = heuristic(self.pos, human_pos)

        # Flee takes highest priority
        if dist <= self.flee_distance:
            self.mode          = 'flee'
            self._decoy_steps  = 0
            self._decoy_target = None
            target = self._flee_target(passages, human_pos)
            self.path = astar(passages, self.pos, target, self.rows, self.cols)
            return

        # Active deception run
        if self._decoy_steps > 0 and self._decoy_target:
            if self.pos == self._decoy_target:
                self._end_deception()
            else:
                self.mode = 'deceive'
                self.path = astar(passages, self.pos, self._decoy_target,
                                  self.rows, self.cols)
                return

        # Normal pursuit
        self.mode = 'pursue'
        self.path = astar(passages, self.pos, real_flag, self.rows, self.cols)

    def move(self) -> None:
        """Advance one step along the pre-computed path."""
        if len(self.path) > 1:
            self.pos  = self.path[1]
            self.path = self.path[1:]

        if self._decoy_steps > 0:
            self._decoy_steps -= 1
            if self._decoy_steps == 0:
                self._end_deception()

        if self._decoy_cooldown > 0:
            self._decoy_cooldown -= 1

    def try_trigger_deception(self, fake_flags: list[tuple]) -> None:
        """Called once per robot move; may start a deception run."""
        if (self.mode == 'pursue'
                and fake_flags
                and self.deception_chance > 0
                and self._decoy_steps == 0
                and self._decoy_cooldown == 0
                and random.random() < self.deception_chance):
            self._decoy_target  = random.choice(fake_flags)
            self._decoy_steps   = random.randint(7, 13)
            self._decoy_cooldown = 0    # cooldown set when deception ends

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _end_deception(self) -> None:
        self._decoy_steps    = 0
        self._decoy_target   = None
        self._decoy_cooldown = 25   # ~25 robot moves (~5 s) before next decoy
        self.mode = 'pursue'

    def _flee_target(self, passages: list[list[set]], human_pos: tuple) -> tuple:
        """BFS from human; return the reachable cell farthest from the human."""
        delta = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
        dist  = {human_pos: 0}
        queue = deque([human_pos])

        while queue:
            r, c = queue.popleft()
            for d, (dr, dc) in delta.items():
                nb = (r + dr, c + dc)
                if nb not in dist and 0 <= nb[0] < self.rows and 0 <= nb[1] < self.cols:
                    if d in passages[r][c]:
                        dist[nb] = dist[(r, c)] + 1
                        queue.append(nb)

        best = max(dist, key=lambda cell: dist[cell])
        if best == self.pos:
            for cell in sorted(dist, key=lambda c: -dist[c]):
                if cell != self.pos:
                    return cell
        return best
