import random
from collections import deque


def _is_connected(passages: list[list[set]], rows: int, cols: int) -> bool:
    delta = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    visited = {(0, 0)}
    queue   = deque([(0, 0)])

    while queue:
        r, c = queue.popleft()
        for d, (dr, dc) in delta.items():
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited and 0 <= nr < rows and 0 <= nc < cols:
                if d in passages[r][c]:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    return len(visited) == rows * cols


def mutate_maze(passages: list[list[set]], rows: int, cols: int,num_mutations: int = 4) -> None:
    opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    delta    = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    directions = list(delta.keys())

    done = 0
    attempts = 0

    while done < num_mutations and attempts < 300:
        attempts += 1
        r  = random.randint(0, rows - 1)
        c  = random.randint(0, cols - 1)
        d  = random.choice(directions)
        dr, dc = delta[d]
        nr, nc = r + dr, c + dc

        if not (0 <= nr < rows and 0 <= nc < cols):
            continue

        rd = opposite[d]

        if d in passages[r][c]:
            # Opening exists try to close it
            passages[r][c].discard(d)
            passages[nr][nc].discard(rd)
            if _is_connected(passages, rows, cols):
                done += 1
            else:
                # Closing breaks connectivity - restore
                passages[r][c].add(d)
                passages[nr][nc].add(rd)
        else:
            # Wall exists open it
            passages[r][c].add(d)
            passages[nr][nc].add(rd)
            done += 1
