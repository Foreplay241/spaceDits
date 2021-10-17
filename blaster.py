import pygame as pg
import random


class Blaster(pg.sprite.Sprite):
    def __init__(self, pos, img, maxCharge, power, fire_rate):
        super(Blaster, self).__init__()
        self.x, self.y = pos
        self.image = img
        self.name = "Blast"
        self.is_player = False
        self.max_charge = maxCharge
        self.current_charge = maxCharge
        self.power = power
        self.canShoot = True
        self.fire_rate = fire_rate

    def fire(self):
        pass
    