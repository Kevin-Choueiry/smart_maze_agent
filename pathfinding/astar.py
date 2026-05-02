import heapq


def heuristic(a: tuple, b: tuple) -> int:
    return abs(a[0] -b[0])+ abs(a[1]- b[1])#manattan distance


def astar(passages: list[list[set]], start: tuple, goal: tuple,rows: int, cols: int) -> list[tuple]:
    if start == goal:
        return [start]

    #Open list: (f, g, cell) mirrors PATH* S sorted by h (=f) in C++
    h0 = heuristic(start, goal)
    open_list: list = [(h0, 0, start)]

    # came_from reconstructs the path (replaces storing full path[] in Node)
    came_from: dict = {}

    # best_g mirrors the find()+update check: skip if a cheaper path exists
    best_g: dict = {start: 0}

    delta = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

    while open_list:
        f, g, current = heapq.heappop(open_list)   # pop best (like StackTop+Pop)

        #Goal test (mirrors: if head.path[N-1] == fs.path[N-1])
        if current == goal:
            path = []
            node = goal
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            return path[::-1]

        # Stale entry — a cheaper route was already processed
        if g > best_g.get(current, float('inf')):
            continue

        r, c = current

        #Successeurs: expand neighbours reachable through open passages
        for d, (dr, dc) in delta.items():
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if d not in passages[r][c]:
                continue

            neighbour = (nr, nc)
            new_g = g + 1                               # uniform edge cost
            new_f = new_g + heuristic(neighbour, goal)  # Tmp.h = Tmp.g + T[j].cost

            #find()+update: keep only the best g for each node
            if new_g < best_g.get(neighbour, float('inf')):
                best_g[neighbour]    = new_g
                came_from[neighbour] = current
                heapq.heappush(open_list, (new_f, new_g, neighbour))

    return []   #no path found(not possible as i did the _is_connected check before)
