import pygame


class Human:
    #modification I want a human instance to have a starting position and a score attribute that starts at 100
    def __init__(self, pos: tuple):
        self.pos   = pos
        self.score = 100

    def handle_input(self, event, passages: list[list[set]],rows: int, cols: int) -> bool:
        #Process a keudown event move the player if the passage is open and return true if moved
        if event.type != pygame.KEYDOWN:
            return False

        key_to_dir = {pygame.K_UP:('N',-1,0),pygame.K_DOWN:('S',1,0),pygame.K_LEFT:('W',0,-1),pygame.K_RIGHT:('E',0,1),}

        if event.key not in key_to_dir:
            return False

        d, dr, dc = key_to_dir[event.key]
        r, c = self.pos
        nr, nc = r + dr, c + dc

        if 0 <= nr < rows and 0 <= nc < cols and d in passages[r][c]:
            self.pos = (nr, nc)
            return True

        return False
