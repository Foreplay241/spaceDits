import os
from settings import *
import pygame as pg
from missle import Missle


class MisslePod(pg.sprite.Sprite):
    def __init__(self, shidpit, pos, img, maxMissles=0, power=0, fire_rate=0):
        super(MisslePod, self).__init__()
        self.shidpit = shidpit
        self.x, self.y = pos
        self.image = img
        self.missle_image = pg.image.load(os.path.join('assets', 'missle.png'))
        self.name = "POD"
        self.is_player = False
        self.max_missles = maxMissles
        self.current_missles = maxMissles
        self.power = power
        self.canShoot = True
        self.fire_rate = fire_rate
        self.missles = []
        self.prev_shot_time = 0
        self.missle_velocity = -7

    def fire(self, game):
        now = pg.time.get_ticks()
        if now - self.prev_shot_time > self.fire_rate and self.canShoot:
            self.prev_shot_time = pg.time.get_ticks()
            missle = Missle(self.shidpit, (self.x + self.shidpit.ship_properties["position"][0],
                                           self.y + self.shidpit.ship_properties["position"][1]),
                            self.missle_image, colormask=LIGHT_BLUE)
            missle.velocity = self.missle_velocity + self.shidpit.ship_properties["y velocity"]
            self.missles.append(missle)
            game.all_sprites.add(missle)
