from Player.racerHUD import RHUD
from Player.ship import *


class Racer(Ship):
    def __init__(self, game, redilot, shidpit):
        super().__init__(game, redilot, shidpit)
        self.HUD = RHUD(self.game, self)

    def update(self):
        super(Racer, self).update()
        if self.position[1] <= DISPLAY_TOP:
            self.position[1] = DISPLAY_BOTTOM - 90
        if self.position[1] > DISPLAY_BOTTOM:
            self.position[1] = DISPLAY_TOP
        if self.position[0] < DISPLAY_LEFT:
            self.position[0] = DISPLAY_RIGHT
        if self.position[0] > DISPLAY_RIGHT:
            self.position[0] = DISPLAY_LEFT

    def draw(self, window):
        super(Racer, self).draw(window)
        self.HUD.draw(window, (0, DISPLAY_HEIGHT - 90))
