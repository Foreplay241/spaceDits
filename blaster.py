import pygame as pg
import random


class Blaster(pg.sprite.Sprite):
    def __init__(self, pos, img, isPlayer=False, maxCharge=random.randint(45, 90), power=random.randint(15, 22)):
        super(Blaster, self).__init__()
        self.x, self.y = pos
        self.image = img
        self.is_player = isPlayer
        self.max_charge = maxCharge
        self.current_charge = maxCharge
        self.power = power

    def fire(self):
        pass
    