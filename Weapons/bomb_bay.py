from Weapons.bomb import Bomb
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

        self.max_bombs = maxBombs
        self.current_charge = maxBombs
        self.power_hull = power
        self.power_shield = power
        self.fire_rate = drop_rate

        self.canShoot = True
        self.bombs = []
        self.prev_shot_time = 0
        self.bomb_velocity = -7

    def fire(self, game):
        now = pg.time.get_ticks()
        if now - self.prev_shot_time > self.fire_rate and self.canShoot:
            self.prev_shot_time = pg.time.get_ticks()
            bomb = Bomb(self.shidpit, (self.x + self.shidpit.ship_properties["position"][0],
                                       self.y + self.shidpit.ship_properties["position"][1]),
                        self.bomb_image, colormask=LIGHT_BLUE)
            bomb.velocity = self.bomb_velocity + self.shidpit.ship_properties["y velocity"]
            self.bombs.append(bomb)
            game.all_sprites.add(bomb)
