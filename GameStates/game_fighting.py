from GameStates.game import Game
import random
import pygame as pg
import os


class Fighting(Game):
    def __init__(self):
        super(Fighting, self).__init__()
        self.background_image = pg.image.load(os.path.join(self.backgroundPath, f"FighterBG{self.BGn}.png"))
        self.background_credit = pg.image.load(os.path.join(self.backgroundPath, "deep-foldcredit.png"))
        self.BGx = random.randint(-241, 0)
        self.background_image.blit(self.background_credit, (-self.BGx + random.randint(-15, 390), 0))

    def startup(self, persistent):
        super(Fighting, self).startup(persistent)

    def get_event(self, event):
        super(Fighting, self).get_event(event)

    def update(self, dt):
        super(Fighting, self).update(dt)

    def draw(self, screen):
        super(Fighting, self).draw(screen)
