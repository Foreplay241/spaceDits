import os
from settings import *
import pygame as pg
from Weapons.missile import Missile


class MissilePod(pg.sprite.Sprite):
    def __init__(self, shidpit, pos, img, maxMissiles=0, power=0.0, fire_rate=0):
        super(MissilePod, self).__init__()
        self.shidpit = shidpit
        self.x, self.y = pos
        self.image = img
        sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        assetsPath = os.path.join(sourceFileDir, "assets")
        self.missile_image = pg.image.load(os.path.join(assetsPath, 'missile.png'))

        self.is_player = False

        self.max_missiles = maxMissiles
        self.current_missiles = maxMissiles
        self.power_hull = power
        self.power_shield = 1 - power
        self.fire_rate = fire_rate

        self.canShoot = True
        self.missiles = []
        self.prev_shot_time = 0
        self.missile_velocity = -7

    def fire(self, game):
        now = pg.time.get_ticks()
        if now - self.prev_shot_time > self.fire_rate and self.canShoot:
            self.prev_shot_time = pg.time.get_ticks()
            missile = Missile(self.shidpit, (self.x + self.shidpit.ship_properties["position"][0],
                                             self.y + self.shidpit.ship_properties["position"][1]),
                              self.missile_image, colormask=LIGHT_BLUE)
            missile.velocity = self.missile_velocity + self.shidpit.ship_properties["y velocity"]
            self.missiles.append(missile)
            game.all_sprites.add(missile)
