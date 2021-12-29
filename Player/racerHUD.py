from Player.HUD import HUD
from settings import *


class RHUD(HUD):
    def __init__(self, game, ship):
        super(RHUD, self).__init__(game, ship)
        self.color_list = [BLUE, DARK_BLUE, LIGHT_BLUE, RANDOM_BLUE, CORN_FLOWER_BLUE, FREE_SPEECH_BLUE]
