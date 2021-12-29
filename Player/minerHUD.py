from Player.HUD import HUD
from settings import *


class MHUD(HUD):
    def __init__(self, game, ship):
        super(MHUD, self).__init__(game, ship)
        self.color_list = [ARMY_GREEN, DARK_GREEN, LIGHT_GREEN, RANDOM_GREEN, LAWN_GREEN, FREE_SPEECH_GREEN]
