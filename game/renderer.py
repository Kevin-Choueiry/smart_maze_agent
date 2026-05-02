import pygame
from config import (COLS, ROWS, CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT,DARK_BG, CELL_BG, FOG_BG, WALL_COLOR,BLUE, BLUE_LIGHT, RED, RED_LIGHT, ORANGE, ORANGE_LIGHT,GREEN, YELLOW, CYAN, GRAY, WHITE, HUD_BG, PATH_COLOR,)


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen   = screen
        self.font_sm  = pygame.font.SysFont('monospace', 15)
        self.font_md  = pygame.font.SysFont('monospace', 18, bold=True)
        self.font_lg  = pygame.font.SysFont('monospace', 28, bold=True)

        self._path_surf = pygame.Surface((COLS * CELL_SIZE, ROWS * CELL_SIZE), pygame.SRCALPHA)
        self._fog_surf = pygame.Surface((COLS * CELL_SIZE, ROWS * CELL_SIZE), pygame.SRCALPHA)

    #entry point
    def draw(self, passages, human, robot, state, wall_timer: int,fog_radius: int, wall_mutation_interval: int,flash_msg: str = '', fog_enabled: bool = True) -> None:
        hp = human.pos
        self.screen.fill(DARK_BG)
        self._draw_cells(hp, fog_radius)
        self._draw_path(robot.path, hp, fog_radius)
        self._draw_maze(passages, hp, fog_radius)
        self._draw_flags(state, hp, fog_radius)
        self._draw_agents(human, robot, hp, fog_radius)
        self._draw_hud(human, robot, state, wall_timer, wall_mutation_interval, fog_enabled)

        if flash_msg:
            self._draw_flash(flash_msg)
        if state.game_over:
            self._draw_game_over(state)

    #Fog

    @staticmethod
    def _visible(r: int, c: int, human_pos: tuple, fog_radius: int) -> bool:
        return abs(r - human_pos[0]) + abs(c - human_pos[1]) <= fog_radius

    #Maze drawing

    def _draw_cells(self, human_pos: tuple, fog_radius: int) -> None:
        for r in range(ROWS):
            for c in range(COLS):
                color = CELL_BG if self._visible(r, c, human_pos, fog_radius) else FOG_BG
                pygame.draw.rect(
                    self.screen, color,
                    (c * CELL_SIZE + 1, r * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2),
                )

    def _draw_maze(self, passages, human_pos: tuple, fog_radius: int) -> None:
        W = 2
        for r in range(ROWS):
            for c in range(COLS):
                if not self._visible(r, c, human_pos, fog_radius):
                    continue
                x, y = c * CELL_SIZE, r * CELL_SIZE
                if 'N' not in passages[r][c]:
                    pygame.draw.line(self.screen, WALL_COLOR,
                                     (x, y), (x + CELL_SIZE, y), W)
                if 'S' not in passages[r][c]:
                    pygame.draw.line(self.screen, WALL_COLOR,
                                     (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), W)
                if 'W' not in passages[r][c]:
                    pygame.draw.line(self.screen, WALL_COLOR,
                                     (x, y), (x, y + CELL_SIZE), W)
                if 'E' not in passages[r][c]:
                    pygame.draw.line(self.screen, WALL_COLOR,
                                     (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), W)

    #A*
    def _draw_path(self, path: list, human_pos: tuple, fog_radius: int) -> None:
        if len(path) < 2:
            return
        self._path_surf.fill((0, 0, 0, 0))
        half = CELL_SIZE // 2

        for i in range(1, len(path)):
            r1, c1 = path[i - 1]
            r2, c2 = path[i]
            # Only draw segments where both endpoints are in fog
            if not (self._visible(r1, c1, human_pos, fog_radius)
                    and self._visible(r2, c2, human_pos, fog_radius)):
                continue
            pygame.draw.line(
                self._path_surf, (*PATH_COLOR, 90),
                (c1 * CELL_SIZE + half, r1 * CELL_SIZE + half),
                (c2 * CELL_SIZE + half, r2 * CELL_SIZE + half),
                3,
            )

        if len(path) > 1:
            nr, nc = path[1]
            if self._visible(nr, nc, human_pos, fog_radius):
                pygame.draw.circle(
                    self._path_surf, (*PATH_COLOR, 160),
                    (nc * CELL_SIZE + half, nr * CELL_SIZE + half), 5,
                )
        self.screen.blit(self._path_surf, (0, 0))

    #Flags
    def _draw_flags(self, state, human_pos: tuple, fog_radius: int) -> None:
        half = CELL_SIZE // 2
        for flag in state.all_flags:
            r, c = flag
            if not self._visible(r, c, human_pos, fog_radius):
                continue
            fx, fy = c * CELL_SIZE + half, r * CELL_SIZE + half
            pygame.draw.line(self.screen, WHITE, (fx, fy + 9), (fx, fy - 10), 2)
            pygame.draw.polygon(
                self.screen, YELLOW,
                [(fx, fy - 10), (fx + 11, fy - 6), (fx, fy - 2)],
            )

    #Agents
    def _draw_agents(self, human, robot, human_pos: tuple, fog_radius: int) -> None:
        half = CELL_SIZE // 2
        r3   = CELL_SIZE // 3

        # Human always drawn
        hr, hc = human.pos
        hx, hy = hc * CELL_SIZE + half, hr * CELL_SIZE + half
        pygame.draw.circle(self.screen, BLUE,       (hx, hy), r3)
        pygame.draw.circle(self.screen, BLUE_LIGHT, (hx, hy), r3 - 3)

        # Robot only visible inside fog
        rr, rc = robot.pos
        if not self._visible(rr, rc, human_pos, fog_radius):
            return

        rx, ry = rc * CELL_SIZE + half, rr * CELL_SIZE + half
        # 'deceive' looks identical to 'pursue' — intentionally hidden from player
        is_flee = (robot.mode == 'flee')
        body_c  = RED    if is_flee else ORANGE
        face_c  = RED_LIGHT if is_flee else ORANGE_LIGHT
        eye_c   = (255, 50, 50) if is_flee else (255, 220, 50)

        pygame.draw.rect(self.screen, body_c,(rx - r3, ry - r3, r3 * 2, r3 * 2))
        pygame.draw.rect(self.screen, face_c,(rx - r3 + 2, ry - r3 + 2, r3 * 2 - 4, r3 * 2 - 4))
        pygame.draw.circle(self.screen, eye_c, (rx - 4, ry - 3), 3)
        pygame.draw.circle(self.screen, eye_c, (rx + 4, ry - 3), 3)


    def _draw_hud(self, human, robot, state, wall_timer: int,
                  wall_mutation_interval: int, fog_enabled: bool = True) -> None:
        hud_y = ROWS * CELL_SIZE
        hud_h = WINDOW_HEIGHT - hud_y
        pygame.draw.rect(self.screen, HUD_BG, (0, hud_y, WINDOW_WIDTH, hud_h))

        # Score
        score_surf = self.font_md.render(f'Score: {human.score}', True, WHITE)
        self.screen.blit(score_surf, (10, hud_y + 7))

        # Robot mode - never expose 'deceive' to the player
        displayed_mode = 'FLEE' if robot.mode == 'flee' else 'PURSUE'
        mode_color     = RED if robot.mode == 'flee' else GREEN
        mode_surf      = self.font_md.render(f'Robot: {displayed_mode}', True, mode_color)
        self.screen.blit(mode_surf, (160, hud_y + 7))

        # Wall-shift countdown + bar
        time_left = max(0, wall_mutation_interval - wall_timer)
        secs_left = time_left // 1000
        pygame.draw.rect(self.screen, GRAY, (340, hud_y + 14, 130, 10))
        filled = int(130 * (1 - time_left / wall_mutation_interval))
        pygame.draw.rect(self.screen, CYAN, (340, hud_y + 14, filled, 10))
        timer_surf = self.font_md.render(f'Shift: {secs_left}s', True, CYAN)
        self.screen.blit(timer_surf, (480, hud_y + 7))

        # Fog toggle indicator
        fog_color = CYAN if fog_enabled else GRAY
        fog_label = 'FOG: ON' if fog_enabled else 'FOG: OFF'
        fog_surf  = self.font_md.render(fog_label, True, fog_color)
        self.screen.blit(fog_surf, (WINDOW_WIDTH - fog_surf.get_width() - 10, hud_y + 7))

        # Hint row
        hint = self.font_sm.render(
            'Arrows: move  |  F: toggle fog  |  R: restart  |  M: menu  |  fake flag = -10 pts',
            True, GRAY,
        )
        self.screen.blit(hint, (10, hud_y + 34))

    #Overlays

    def _draw_flash(self, msg: str) -> None:
        surf = self.font_md.render(msg, True, RED)
        self.screen.blit(surf, (WINDOW_WIDTH // 2 - surf.get_width() // 2, 8))

    def _draw_game_over(self, state) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        self.screen.blit(overlay, (0, 0))

        color = GREEN if state.winner == 'human' else RED
        title = self.font_lg.render(state.message, True, color)
        tx    = WINDOW_WIDTH  // 2 - title.get_width()  // 2
        ty    = WINDOW_HEIGHT // 2 - title.get_height() // 2
        self.screen.blit(title, (tx, ty))

        sub = self.font_md.render('Press  R  to restart   |   M  for menu   |   Q  to quit',
                                  True, WHITE)
        self.screen.blit(sub, (WINDOW_WIDTH // 2 - sub.get_width() // 2, ty + 46))
