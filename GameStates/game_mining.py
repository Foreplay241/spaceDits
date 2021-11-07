from GameStates.game import Game
import pygame as pg
import os
import random
from RedditFusions.create_subteroid import Subteroid


class Mining(Game):
    def __init__(self):
        super(Mining, self).__init__()
        self.background_image = pg.image.load(os.path.join(self.backgroundPath, f"MiningBG{self.BGn}.png"))
        self.background_credit = pg.image.load(os.path.join(self.backgroundPath, "deep-foldcredit.png"))
        self.BGx = random.randint(-241, 0)
        self.background_image.blit(self.background_credit, (-self.BGx + random.randint(-15, 390), 0))

    def startup(self, persistent):
        super(Mining, self).startup(persistent)

    def get_event(self, event):
        super(Mining, self).get_event(event)

    def update(self, dt):
        super(Mining, self).update(dt)

    def draw(self, screen):
        super(Mining, self).draw(screen)
