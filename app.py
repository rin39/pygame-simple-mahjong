# Import pygame
import pygame
# import python libraries
import random
# Import game modules
from game.settings import screen, clock, FPS
from game.tiles import wall, hi_img
import game.tiles_logic


class Mentsu:
    def __init__(self) -> None:
        self.hand = []
        self.discarded_tiles = []

    def __len__(self) -> int:
        return len(self.hand)

    def make_initial_hand(self, modifier = 0):
        # Get 13 random tiles from the wall
        self.hand = random.sample(wall, 13 + modifier)
        # Remove from the wall taken tiles
        remove_tiles_from_wall(self.hand)

    def bot_discard_tile(self):
        if len(wall) != 0:
            # Draw
            random_tile = random.choice(wall)
            self.hand.append(random_tile)
            wall.remove(random_tile)
            # Discard tile
            tsumogiri = self.hand[13]
            del self.hand[13]
            self.discarded_tiles.append(tsumogiri)

    def draw_tile(self):
        if len(wall) != 0:
            random_tile = random.choice(wall)
            self.hand.append(random_tile)
            wall.remove(random_tile)

    def discard_tile(self, index):
        if len(wall) != 0:
            discarded_tile = self.hand[index]
            self.discarded_tiles.append(discarded_tile)
            del self.hand[index]
            self.hand.sort(key = lambda x: (x.suit, x.number))
            # Bots
            shimocha.bot_discard_tile()
            toimen.bot_discard_tile()
            kamicha.bot_discard_tile()


def remove_tiles_from_wall(tiles):
    for tile in tiles:
        if tile in wall:
            wall.remove(tile)


# Define Mentsu
player = Mentsu()
toimen = Mentsu()
shimocha = Mentsu()
kamicha = Mentsu()

# Make dead wall and define dora
wanpai = random.sample(wall, 14)
remove_tiles_from_wall(wanpai)
dora = random.choice(wanpai)
wanpai.remove(dora)
uradora = random.choice(wanpai)
wanpai.remove(uradora)

# Make initial hands
player.make_initial_hand()
toimen.make_initial_hand()
shimocha.make_initial_hand()
kamicha.make_initial_hand()
player.hand.sort(key = lambda x: (x.suit, x.number))

# Define Dealer
oya = random.randint(1, 4)
if oya == 1: # Player
    indicator_x = 450
    indicator_y = 455
elif oya == 2: # 対面
    toimen.bot_discard_tile()
    kamicha.bot_discard_tile()
    indicator_x = 450
    indicator_y = 300
elif oya == 3: # 下家
    shimocha.bot_discard_tile()
    toimen.bot_discard_tile()
    kamicha.bot_discard_tile()
    indicator_x = 550
    indicator_y = 350
else: # 上家
    kamicha.bot_discard_tile()
    indicator_x = 350
    indicator_y = 350

click = False
running = True

def wait_click():
    while True:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
        if event.type == pygame.QUIT:
            exit()


while running:
    if len(player) < 14:
        player.draw_tile()

    screen.fill((50, 50, 50))

    dora_indicator = game.tiles_logic.Game_Tile(450, 350, dora.image, 0.3).draw(screen)
    wind_indicator = game.tiles_logic.Game_Tile(indicator_x, indicator_y, hi_img, 0.15).draw(screen)

    game.tiles_logic.make_player_hand(screen, click, player)

    game.tiles_logic.make_discard(player.discarded_tiles, screen)
    game.tiles_logic.make_discard(shimocha.discarded_tiles, screen, 700, 550, 90)
    game.tiles_logic.make_discard(toimen.discarded_tiles, screen, 300, 200, 180)
    game.tiles_logic.make_discard(kamicha.discarded_tiles, screen, 200, 550, 270)

    pygame.display.update()
    clock.tick(FPS)

    click = wait_click()

    game.tiles_logic.make_player_hand(screen, click, player)

    click = False


pygame.quit()
