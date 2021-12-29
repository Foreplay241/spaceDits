import math

from pygame import Vector2

from Player.Weapons.laser import Laser
from settings import *


class Blaster(pg.sprite.Sprite):
    def __init__(self, shidpit, pos, img):
        super(Blaster, self).__init__()
        self.shidpit = shidpit
        self.x, self.y = pos
        self.image = img
        sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        assetsPath = os.path.join(sourceFileDir, "assets")
        self.laser_image = pg.image.load(os.path.join(assetsPath, 'laser.png'))
        self.is_player = False

        self.max_charge = 1
        self.current_charge = 1
        self.charge_rate = 1
        self.charge_cost = 1
        self.power_hull = 1
        self.power_shield = 1
        self.fire_rate = 1

        self.HUD_bar_color = BLACK
        self.canShoot = True
        self.charge_depleted = False

        self.lasers = []
        self.prev_shot_time = 0
        self.laser_velocity = -6
        self.direction = Vector2(1, 1)

    def update(self):
        super(Blaster, self).update()
        self.charge()

    def generate_blaster(self):
        self.max_charge = self.shidpit.nose_dict["Max Charge"]
        self.current_charge = self.shidpit.nose_dict["Max Charge"]
        self.charge_rate = self.shidpit.nose_dict["Charge Rate"]
        self.charge_cost = self.shidpit.nose_dict["Charge Cost"]
        self.power_hull = 1
        self.power_shield = 1
        self.fire_rate = self.shidpit.nose_dict["Fire Rate"]

    def fire(self, game, target):
        now = pg.time.get_ticks()
        angleRad = math.atan2(Vector2(0, 0)[1] - target.position[1],
                              target.position[0] - Vector2(0, 0)[0])
        if now - self.prev_shot_time > self.fire_rate and \
                self.current_charge > 0 and \
                self.canShoot:
            self.current_charge -= self.charge_cost
            self.prev_shot_time = pg.time.get_ticks()
            newLaser = Laser(self.shidpit, (self.x + game.player.rect.x,
                                            self.y + game.player.rect.y),
                             self.laser_image, colormask=LIGHT_BLUE,
                             direction=self.direction.rotate(math.degrees(angleRad)))
            self.lasers.append(newLaser)
            game.all_sprites.add(newLaser)
        else:
            pass

    def charge(self):
        if not self.charge_depleted:
            self.HUD_bar_color = ROYAL_BLUE
            self.current_charge += self.charge_rate
            if self.current_charge > self.max_charge:
                self.current_charge = self.max_charge
            if self.current_charge <= 0:
                self.charge_depleted = True
                self.canShoot = False
        if self.charge_depleted:
            self.HUD_bar_color = INDIAN_RED
            self.current_charge += self.max_charge // 241
            if self.current_charge >= self.max_charge:
                self.charge_depleted = False
                self.canShoot = True
