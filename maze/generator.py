import random


def generate_maze(rows: int, cols: int) -> list[list[set]]:
    passages = [[set() for _ in range(cols)] for _ in range(rows)]#a 2D list where initially closed
    visited  = [[False]  * cols for _ in range(rows)]

    stack = [(0, 0)]#LIFO first room in the left corner and mark as visited
    visited[0][0] = True

    opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    delta    = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

    while stack:
        r, c = stack[-1]

        unvisited = []
        for d, (dr, dc) in delta.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                unvisited.append((d, nr, nc))

        if unvisited:
            d, nr, nc = random.choice(unvisited)
            passages[r][c].add(d)
            passages[nr][nc].add(opposite[d])
            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()

    return passages
