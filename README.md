# Adversarial Maze Agent

A two-player adversarial game built in **Python + Pygame** for the AI university project (I3335).  
A human navigates a procedurally generated, dynamically shifting maze while an AI robot races to reach a hidden flag using **A\* pathfinding**.

---

## How to Run

```bash
pip install pygame
python main.py
```

**Controls**

| Key | Action |
|-----|--------|
| Arrow keys | Move the human player |
| R | Restart (same difficulty) |
| M | Return to main menu |
| Q / Escape | Quit |

---

## Project Structure

```
smart_maze_agent/
├── main.py               # Entry point, game loop, menu routing
├── config.py             # All constants, palette, difficulty presets
├── requirements.txt
│
├── maze/
│   ├── generator.py      # Recursive backtracking maze generation
│   └── mutator.py        # Dynamic wall toggling with connectivity guard
│
├── pathfinding/
│   └── astar.py          # A* (adapted from course C++ implementation)
│
├── agents/
│   ├── human.py          # Arrow-key player movement
│   └── robot.py          # AI: pursue / flee / deceive modes
│
└── game/
    ├── menu.py           # Start screen & difficulty selector
    ├── state.py          # Win/loss conditions, flag placement
    └── renderer.py       # Pygame drawing with fog-of-war support
```

---

## Game Rules

### Human Player
- Move through the maze with the arrow keys.
- **Win** by catching the robot (standing on the same cell) **or** stepping on the real flag before the robot does.
- All four flags look identical — watch the robot's live A\* path to deduce which one is real.
- Stepping on a **fake flag** costs **−10 points**.

### Robot (AI Agent)
- Navigates autonomously using A\*.
- **Win** by reaching the real flag before being caught.
- Recalculates its path after every move and every wall mutation.

---

## Difficulty Levels

Selected on the start screen (keys **1 / 2 / 3** or mouse click):

| Setting | Easy | Medium | Hard |
|---------|------|--------|------|
| Robot speed | 350 ms/step | 220 ms/step | 120 ms/step |
| Flee threshold | 3 cells | 4 cells | 6 cells |
| Wall shift | every 8 s | every 5 s | every 3 s |
| Fog radius | 7 cells | 5 cells | 4 cells |
| Deception | none | occasional | heavy |

---

## AI Components

### 1 - Maze Generation (`maze/generator.py`)
Iterative **recursive backtracking** (depth-first search):
- Uses an explicit stack — no Python recursion limit issues.
- Carves random passages until every cell is visited exactly once.
- Guarantees a **perfect maze** — exactly one path between any two cells.

### 2 - A\* Pathfinding (`pathfinding/astar.py`)
Python adaptation of the C++ A\* from the course slides:

| C++ concept | Python equivalent |
|-------------|-------------------|
| `Node { path[], g, h }` | heap entry `(f, g, cell)` + `came_from` dict |
| `PATH* S` — open list sorted by `h` | `heapq` min-heap (sorted by `f = g + h`) |
| `sort(S)` | `heapq` maintains order automatically |
| `find(S, node)` + update | `best_g` dict — O(1) lookup |
| `Successeurs(head)` | loop over four neighbours through open passages |
| `Tmp.h = Tmp.g + T[j].cost` | `new_f = new_g + heuristic(neighbour, goal)` |

Heuristic: **Manhattan distance** — admissible on a unit-cost grid.

### 3 - Robot Behaviour (`agents/robot.py`)

| Mode | Condition | Action |
|------|-----------|--------|
| **Pursue** | Human > `flee_distance` away | A\* path toward the real flag |
| **Flee** | Human ≤ `flee_distance` away | A\* path toward the farthest reachable cell (BFS from human) |
| **Deceive** | In pursue mode + random trigger | A\* path toward a random **fake** flag for 7–13 steps, then revert |

- **Deception is invisible to the player** — the HUD always shows "PURSUE"; the robot looks identical in both modes. The player must infer intent from the observed path.
- After deception ends a cooldown (~25 moves) prevents immediate re-triggering.

### 4 - Dynamic Wall Mutation (`maze/mutator.py`)
Every N seconds (difficulty-dependent), up to 4 random wall edges are toggled:
- Opening a wall is always safe.
- Closing a wall only applies if a **BFS connectivity check** confirms all 300 cells remain reachable.
- Forces the robot to re-plan in real time.

### 5 - Fog of War (`game/renderer.py`)
The human can only see cells within their **fog radius** (Manhattan distance):
- Cells outside the radius render as near-black — walls, flags, and the robot are hidden.
- The robot's A\* path is only drawn for segments that fall inside the fog.
- The player must move toward the robot to observe its path and deduce the real flag.

### 6 - Start Screen & Difficulty Menu (`game/menu.py`)
- Three clickable difficulty cards with per-preset stat labels.
- Keyboard shortcuts 1 / 2 / 3 for fast selection.
- Press **M** in-game to return to the menu at any time.

---

## Visualisation

| Element | Meaning |
|---------|---------|
| Blue circle | Human player |
| Orange square | Robot — pursue or deceive mode (looks the same intentionally) |
| Red square | Robot — flee mode |
| Green line | Robot's live A\* path (only visible inside the fog radius) |
| Yellow flag | Any flag — real or fake, all identical |
| Dark cells | Outside the player's fog of war |
| Cyan progress bar | Countdown to next wall shift |

---

## Technical Details

| Component | Detail |
|-----------|--------|
| Language | Python 3 |
| Graphics | Pygame 2 |
| Grid | 20 × 15 cells, 40 px each |
| Pathfinding | A\* with Manhattan heuristic |
| Robot AI | Pursue / Flee / Deceive with per-difficulty tuning |
| Fog of war | Manhattan-radius visibility, dynamic per frame |
| Deception | Probabilistic fake-path injection, hidden from player |
