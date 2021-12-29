import random
from GameStates.game import Game
import pygame as pg
import os

from Player.racer import Racer


class Racing(Game):
    def __init__(self):
        super(Racing, self).__init__()
        self.background_image = pg.image.load(os.path.join(self.backgroundPath, f"RacingBG{self.BGn}.png"))
        self.background_credit = pg.image.load(os.path.join(self.backgroundPath, "deep-foldcredit.png"))
        self.BGx = random.randint(-241, 0)
        self.background_image.blit(self.background_credit, (-self.BGx + random.randint(-15, 390), 0))

    def startup(self, persistent):
        super(Racing, self).startup(persistent)
        if "Player Redilot" in persistent:
            self.player = Racer(self, persistent["Player Redilot"], persistent["Player Shidpit"])
        self.all_sprites.add(self.player)

    def get_event(self, event):
        super(Racing, self).get_event(event)

    def update(self, dt):
        super(Racing, self).update(dt)

    def draw(self, screen):
        super(Racing, self).draw(screen)
