import sys
import pygame
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, DIFFICULTY_PRESETS,DARK_BG, HUD_BG, WHITE, GRAY, CYAN,RED, GREEN, YELLOW, ORANGE, BLUE_LIGHT,BLACK,)


_CARD_ACCENT = {'Easy':(50, 200, 90), 'Medium':(255, 200, 0), 'Hard':(210, 50, 50)}
_CARD_DIM    = {'Easy':(20, 70, 35), 'Medium':(80, 65, 10), 'Hard': (70, 20, 20)}


def run_menu(screen: pygame.Surface, clock: pygame.time.Clock) -> dict:
    font_title = pygame.font.SysFont('monospace', 36, bold=True)
    font_sub   = pygame.font.SysFont('monospace', 16)
    font_card  = pygame.font.SysFont('monospace', 20, bold=True)
    font_label = pygame.font.SysFont('monospace', 13)

    #Menu 
    difficulties = ['Easy', 'Medium', 'Hard']
    key_map      = {pygame.K_1:'Easy',pygame.K_2: 'Medium',pygame.K_3:'Hard'}

    #Card calculations
    card_w, card_h = 210, 165
    gap            = 15
    total_w        = 3 * card_w + 2 * gap
    card_x_start   = (WINDOW_WIDTH - total_w) 
    card_y         = 280

    #Create card rects for mouse interaction
    cards = {}
    for i, name in enumerate(difficulties):
        x = card_x_start + i * (card_w + gap)
        cards[name] = pygame.Rect(x, card_y, card_w, card_h)

    hovered = None

    while True:
        mx, my = pygame.mouse.get_pos()
        hovered = next((n for n, r in cards.items() if r.collidepoint(mx, my)), None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); 
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit(); 
                    sys.exit()
                if event.key in key_map:
                    return DIFFICULTY_PRESETS[key_map[event.key]]#return what is in the config for the key pressed
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hovered:
                    return DIFFICULTY_PRESETS[hovered]

        #Background
        screen.fill(DARK_BG)

        #Subtle grid lines
        for r in range(0, WINDOW_HEIGHT, 40):
            pygame.draw.line(screen, (25, 25, 40), (0, r), (WINDOW_WIDTH, r), 1)
        for c in range(0, WINDOW_WIDTH, 40):
            pygame.draw.line(screen, (25, 25, 40), (c, 0), (c, WINDOW_HEIGHT), 1)

        #Title
        title = font_title.render('MAZE  AGENT', True, CYAN)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 60))


        #Description
        desc_lines = [
            "Hunt the AI robot through a shifting maze.",
            "Watch its live path to deduce the real flag - beware of decoys.",
        ]
        for i, line in enumerate(desc_lines):
            s = font_label.render(line, True, (160, 160, 180))
            screen.blit(s, (WINDOW_WIDTH // 2 - s.get_width() // 2, 148 + i * 18))

        sel_label = font_sub.render('SELECT  DIFFICULTY', True, WHITE)
        screen.blit(sel_label, (WINDOW_WIDTH // 2 - sel_label.get_width() // 2, 222))

        #Difficulty cards
        for i, name in enumerate(difficulties):
            rect   = cards[name]
            accent = _CARD_ACCENT[name]
            dim    = _CARD_DIM[name]
            is_hov = (name == hovered)

            bg_color = tuple(min(255, v + 15) for v in dim) if is_hov else dim
            pygame.draw.rect(screen, bg_color, rect, border_radius=8)

            #Difficulty name
            name_surf = font_card.render(name.upper(), True, accent)
            screen.blit(name_surf, (rect.centerx - name_surf.get_width() // 2, rect.y + 14))

            #Key shortcut badge
            badge_txt = font_label.render(f'[{i + 1}]', True, accent)
            screen.blit(badge_txt, (rect.right - badge_txt.get_width() - 8, rect.y + 8))

            #Labels
            preset = DIFFICULTY_PRESETS[name]
            for j, lbl in enumerate(preset['labels']):
                col  = WHITE if is_hov else (180, 180, 200)
                surf = font_label.render(f'. {lbl}', True, col)
                screen.blit(surf, (rect.x + 12, rect.y + 44 + j * 24))

        #Footer hint
        hint = font_sub.render('Click a card  or  press  1 / 2 / 3  to start', True, GRAY)
        screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, card_y + card_h + 30))

        controls = font_label.render(
            'In-game: Arrow keys = move   R = restart   Q / Esc = quit', True, (80, 80, 100)
        )
        screen.blit(controls, (WINDOW_WIDTH // 2 - controls.get_width() // 2,card_y + card_h + 58))

        pygame.display.flip()
