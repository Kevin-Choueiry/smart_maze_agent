COLS = 20
ROWS = 15
CELL_SIZE = 40

WINDOW_WIDTH  = COLS * CELL_SIZE        # 800
WINDOW_HEIGHT = ROWS * CELL_SIZE + 70   # 670

FPS           = 60
NUM_FAKE_FLAGS = 3
FAKE_FLAG_PENALTY = 10

# ── Difficulty presets ───────────────────────────────────────────────────────
# Each preset overrides the four tunable gameplay parameters.
DIFFICULTY_PRESETS = {
    'Easy': {
        'robot_move_interval':    350,   # ms between robot steps
        'flee_distance':            3,   # cells before robot flees
        'wall_mutation_interval': 8000,  # ms between wall shifts
        'fog_radius':               7,   # visible cells radius
        'deception_chance':       0.0,   # probability of decoy path per move
        'labels': ['Slow robot', '7-cell vision', 'No deception', 'Walls: 8 s'],
    },
    'Medium': {
        'robot_move_interval':    220,
        'flee_distance':            4,
        'wall_mutation_interval': 5000,
        'fog_radius':               5,
        'deception_chance':       0.12,
        'labels': ['Normal speed', '5-cell vision', 'Some deception', 'Walls: 5 s'],
    },
    'Hard': {
        'robot_move_interval':    120,
        'flee_distance':            6,
        'wall_mutation_interval': 3000,
        'fog_radius':               4,
        'deception_chance':       0.28,
        'labels': ['Fast robot', '4-cell vision', 'Heavy deception', 'Walls: 3 s'],
    },
}

# ── Palette ──────────────────────────────────────────────────────────────────
BLACK        = (  0,   0,   0)
WHITE        = (255, 255, 255)
DARK_BG      = ( 15,  15,  25)
CELL_BG      = ( 22,  22,  38)
FOG_BG       = (  6,   6,  12)   # cells outside the fog radius
WALL_COLOR   = (190, 190, 215)
BLUE         = ( 60, 120, 220)
BLUE_LIGHT   = (130, 175, 255)
RED          = (210,  50,  50)
RED_LIGHT    = (255, 110, 110)
ORANGE       = (210, 120,  30)
ORANGE_LIGHT = (255, 175,  70)
GREEN        = ( 50, 200,  90)
YELLOW       = (255, 210,   0)
CYAN         = (  0, 195, 210)
GRAY         = (110, 110, 130)
PATH_COLOR   = ( 60, 210, 100)
HUD_BG       = ( 10,  10,  20)
PURPLE       = (140,  60, 220)
PURPLE_LIGHT = (190, 120, 255)
