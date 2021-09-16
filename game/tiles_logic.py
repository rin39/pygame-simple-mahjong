import pygame

class Tile:
    def __init__(self, suit, number, image) -> None:
        self.suit = suit
        self.number = number
        self.image = image

    def __repr__(self) -> str:
        return f'{self.suit}{self.number}'


class Game_Tile:
    def __init__(self, x, y, image, scale, angle=0) -> None:
        width = image.get_width()
        height = image.get_height()
        scaled_image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image = pygame.transform.rotate(scaled_image, angle)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def make_button(self, surface, click, mentsu, to_discard) -> None:
        """
        Make tile clickable (for player hand)
        """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if click:
                mentsu.discard_tile(to_discard)
        self.draw(surface)

def make_player_hand(screen, click, player):
    """
    Make player hand in the bottom of the screen
    """
    x = 10
    y = 720
    for i, _ in enumerate(player.hand):
        Game_Tile(x, y, player.hand[i].image, 0.3).make_button(screen, click, player, i)
        x += 70

def make_discard(discarded_tiles, screen, x = 300, y = 500, angle = 0):
    if angle == 180 or angle == 0:
        if angle == 0:
            second_row_mod_y = 70
            third_row_mod_y = 140
        else:
            second_row_mod_y = -70
            third_row_mod_y = -140
        second_row_mod_x = -360
        third_row_mod_x = -720
        move = lambda x, y: (x + 60, y + 0)
    else:
        second_row_mod_y = 360
        third_row_mod_y = 720
        if angle == 90:
            second_row_mod_x = 70
            third_row_mod_x = 140
        else:
            second_row_mod_x = -70
            third_row_mod_x = -140
        move = lambda x, y: (x + 0, y - 60)

    for i, _ in enumerate(discarded_tiles):
        if i < 6:
            Game_Tile(x, y, discarded_tiles[i].image, 0.25, angle).draw(screen)
        if i >= 6 and i < 12:
            Game_Tile(x + second_row_mod_x, y + second_row_mod_y, discarded_tiles[i].image, 0.25, angle).draw(screen)
        if i >= 12:
            Game_Tile(x + third_row_mod_x, y + third_row_mod_y, discarded_tiles[i].image, 0.25, angle).draw(screen)
        x, y = move(x, y)
