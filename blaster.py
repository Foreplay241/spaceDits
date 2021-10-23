import pygame as pg
from laser import Laser
import os
from settings import *
import random


class Blaster(pg.sprite.Sprite):
    def __init__(self, shidpit, pos, img, maxCharge=0, power=0.0, fire_rate=0):
        super(Blaster, self).__init__()
        self.shidpit = shidpit
        self.x, self.y = pos
        self.image = img
        self.laser_image = pg.image.load(os.path.join('assets', 'laser.png'))
        self.is_player = False

        self.max_charge = maxCharge
        self.current_charge = maxCharge
        self.charge_rate = maxCharge//3
        self.power_hull = 1 - power
        self.power_shield = power
        self.fire_rate = fire_rate

        self.canShoot = True

        self.lasers = []
        self.prev_shot_time = 0
        self.laser_velocity = -7

    def fire(self, game):
        now = pg.time.get_ticks()
        if now - self.prev_shot_time > self.fire_rate and self.canShoot:
            self.prev_shot_time = pg.time.get_ticks()
            laser = Laser(self.shidpit, (self.x + self.shidpit.ship_properties["position"][0],
                                         self.y + self.shidpit.ship_properties["position"][1]),
                          self.laser_image, colormask=LIGHT_BLUE)
            laser.velocity = self.laser_velocity + self.shidpit.ship_properties["y velocity"]
            self.lasers.append(laser)
            game.all_sprites.add(laser)
