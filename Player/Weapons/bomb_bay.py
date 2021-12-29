from Player.Weapons.bomb import Bomb
from settings import *


class BombBay(pg.sprite.Sprite):
    def __init__(self, shidpit, pos, img, maxBombs=0, power=0.0, drop_rate=0):
        super(BombBay, self).__init__()
        self.shidpit = shidpit
        self.x, self.y = pos
        self.image = img
        sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        assetsPath = os.path.join(sourceFileDir, "assets")
        self.bomb_image = pg.image.load(os.path.join(assetsPath, 'bomb.png'))
        self.is_player = False
        self.canDrop = True

        self.max_bombs = 1
        self.current_bombs = 1
        self.power_hull = 1
        self.power_shield = 1
        self.drop_rate = 1

        self.bombs = []
        self.prev_shot_time = 0
        self.bomb_velocity = -7

    def fire(self, game):
        now = pg.time.get_ticks()
        if now - self.prev_shot_time > self.drop_rate and \
                self.current_bombs > 0:
            self.prev_shot_time = pg.time.get_ticks()
            bomb = Bomb(self.shidpit, (self.x + game.player.rect.x,
                                       self.y + game.player.rect.y),
                        self.bomb_image, colormask=LIGHT_BLUE)
            bomb.velocity = self.bomb_velocity + self.shidpit.ship_properties["y velocity"]
            self.bombs.append(bomb)
            game.all_sprites.add(bomb)

    def generate_bay(self):
        self.max_bombs = self.shidpit.body_dict["Max Bombs"]
        self.current_bombs = self.shidpit.body_dict["Max Bombs"]
        self.power_hull = 1
        self.power_shield = 1
        self.drop_rate = self.shidpit.body_dict["Drop Rate"]