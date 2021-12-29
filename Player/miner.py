from Player.minerHUD import MHUD
from Player.ship import *


class Miner(Ship):
    def __init__(self, game, redilot, shidpit):
        super().__init__(game, redilot, shidpit)
        self.HUD = MHUD(self.game, self)
        self.speed = .2
        self.max_speed = 3
        self.min_speed = -3

    def update(self):
        super(Miner, self).update()

    def draw(self, window):
        super(Miner, self).draw(window)
        self.HUD.draw(window, (0, DISPLAY_HEIGHT - 90))
