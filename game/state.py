import random


class GameState:
    def __init__(self, rows: int, cols: int, num_fake_flags: int = 3):
        self.rows          = rows
        self.cols          = cols
        self.num_fake      = num_fake_flags
        self.real_flag:  tuple      = (0, 0)
        self.fake_flags: list[tuple] = []
        self.all_flags:  list[tuple] = []
        self.game_over   = False
        self.winner      = ''# the huaman or the robt
        self.message     = ''

    def place_flags(self, human_pos: tuple, robot_pos: tuple) -> None:
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]

        def far_enough(cell):
            hr, hc = human_pos
            rr, rc = robot_pos
            return (
                cell not in {human_pos, robot_pos}
                and abs(cell[0]- hr) + abs(cell[1] -hc) > 3
                and abs(cell[0]- rr) +abs(cell[1] - rc) > 3
            )

        candidates = [c for c in all_cells if far_enough(c)]
        random.shuffle(candidates)

        self.real_flag  = candidates[0]
        self.fake_flags = list(candidates[1: 1 + self.num_fake])
        self.all_flags  = [self.real_flag] + self.fake_flags

    #Per-frame check
    def check(self, human_pos: tuple, robot_pos: tuple) -> None:
        if self.game_over:
            return

        if robot_pos == self.real_flag:
            self._end('robot', 'Robot reached the flag!  Robot wins!')
        elif human_pos == robot_pos:
            self._end('human', 'You caught the robot!  Human wins!')
        elif human_pos == self.real_flag:
            self._end('human', 'You secured the real flag!  Human wins!')

    #Flag interaction
    def step_on_flag(self, pos: tuple, human) -> str:#Returns 'real' 'fake' '' and updates human score if fake
        if pos == self.real_flag:
            return 'real'
        if pos in self.fake_flags:
            human.score -= 10
            self.fake_flags.remove(pos)
            self.all_flags.remove(pos)
            return 'fake'
        return ''

    #Internal
    def _end(self, winner: str, message: str) -> None:
        self.game_over = True
        self.winner    = winner
        self.message   = message
