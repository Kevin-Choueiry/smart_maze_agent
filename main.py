import sys
import pygame

from config import ROWS, COLS, WINDOW_WIDTH, WINDOW_HEIGHT, FPS, NUM_FAKE_FLAGS
from maze.generator import generate_maze
from maze.mutator   import mutate_maze
from agents.human   import Human
from agents.robot   import Robot
from game.state     import GameState
from game.renderer  import Renderer
from game.menu      import run_menu


#Game factory

def new_game(diff: dict):
    passages = generate_maze(ROWS, COLS)
    human    = Human((0, 0))
    robot    = Robot(
        (ROWS - 1, COLS - 1), ROWS, COLS,
        flee_distance   = diff['flee_distance'],
        deception_chance= diff['deception_chance'],
    )
    state = GameState(ROWS, COLS, NUM_FAKE_FLAGS)
    state.place_flags(human.pos, robot.pos)
    robot.update_path(passages, state.real_flag, state.fake_flags, human.pos)
    return passages, human, robot, state


#Play loop

def play(screen: pygame.Surface, clock: pygame.time.Clock,
         renderer: Renderer, diff: dict) -> str:
    """
    Run one full game session.
    Returns 'menu' if the player wants to go back, 'quit' to exit.
    """
    robot_move_interval    = diff['robot_move_interval']
    wall_mutation_interval = diff['wall_mutation_interval']
    fog_radius             = diff['fog_radius']

    passages, human, robot, state = new_game(diff)
    wall_timer  = 0
    robot_timer = 0
    flash_msg   = ''
    flash_timer = 0
    fog_enabled = True

    while True:
        dt = clock.tick(FPS)

        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return 'quit'
                if event.key == pygame.K_m:
                    return 'menu'
                if event.key == pygame.K_f:
                    fog_enabled = not fog_enabled
                if event.key == pygame.K_r:
                    passages, human, robot, state = new_game(diff)
                    wall_timer = robot_timer = flash_timer = 0
                    flash_msg  = ''
                    continue

            if state.game_over:
                continue

            moved = human.handle_input(event, passages, ROWS, COLS)
            if moved:
                result = state.step_on_flag(human.pos, human)
                if result == 'fake':
                    flash_msg   = 'Fake flag!  -10 pts'
                    flash_timer = 2200

                state.check(human.pos, robot.pos)
                if not state.game_over:
                    robot.update_path(passages, state.real_flag,
                                      state.fake_flags, human.pos)

        #Timers
        if not state.game_over:
            wall_timer  += dt
            robot_timer += dt
            flash_timer  = max(0, flash_timer - dt)
            if flash_timer == 0:
                flash_msg = ''

            #Robot step
            if robot_timer >= robot_move_interval:
                robot_timer = 0
                robot.move()
                robot.try_trigger_deception(state.fake_flags)
                state.check(human.pos, robot.pos)
                if not state.game_over:
                    robot.update_path(passages, state.real_flag,
                                      state.fake_flags, human.pos)

            # Wall mutation
            if wall_timer >= wall_mutation_interval:
                wall_timer = 0
                mutate_maze(passages, ROWS, COLS)
                robot.update_path(passages, state.real_flag,
                                  state.fake_flags, human.pos)

        #Render
        effective_radius = fog_radius if fog_enabled else 999
        renderer.draw(
            passages, human, robot, state,
            wall_timer, effective_radius, wall_mutation_interval,
            flash_msg if flash_timer > 0 else '',
            fog_enabled,
        )
        pygame.display.flip()


#Entry point

def main() -> None:
    pygame.init()
    pygame.key.set_repeat(210, 55)
    screen   = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Adversarial Maze Agent')
    clock    = pygame.time.Clock()
    renderer = Renderer(screen)

    while True:
        diff   = run_menu(screen, clock)
        result = play(screen, clock, renderer, diff)
        if result == 'quit':
            pygame.quit()
            sys.exit()



if __name__ == '__main__':
    main()
