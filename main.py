from settings import *
from home_menu import HomeMenu
from home_menu2 import HomeMenu2
from dead_menu import DeadMenu
from pause_menu import PauseMenu
from game import Game
import praw

"""
T1258O00393 confirmation number for Fidelity transfer 09/15/2021
"""


class App(object):
    def __init__(self, screen, states):
        pg.mixer.pre_init()
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.screen = screen
        self.states = states
        self.prev_state = None
        self.current_state = self.states["HOME_MENU2"]
        self.next_state = self.states["DEAD_MENU"]
        self.player_redditor = None
        self.enemy_redditor = None
        self.clock = pg.time.Clock()
        self.game = Game()
        # self.home_menu = HomeMenu()
        # self.home_menu2 = HomeMenu2()
        # self.pause_menu = PauseMenu()
        # self.dead_menu = DeadMenu()
        self.current_state.startup({})
        self.running = True

    def event_loop(self):
        """
        Events are passed for handling to the current state.
        :return:
        """
        for event in pg.event.get():
            self.current_state.get_event(event)

    def flip_state(self, current_state, new_state):
        """
        Switch game state to a different game state.
        :return: gamestate
        """
        self.prev_state = current_state
        self.prev_state.done = False
        persistent = self.current_state.persist
        self.current_state = new_state
        self.current_state.startup(persistent)
        return self.current_state

    def update(self, dt):
        """
        Check for state flip and update active state
        :param dt: milliseconds since last frame
        :return:
        """
        if self.current_state.done:
            # print(self.current_state.next_state_name)
            self.flip_state(self.current_state, self.states[self.current_state.next_state_name])
        self.current_state.update(dt)

    def draw(self):
        """
        Pass display surface to active state for drawing.
        :return:
        """
        self.current_state.draw(self.screen)

    def run(self):
        """
        Pretty much the entirety of the game's runtime will be
        spent inside this while loop.
        """
        while self.running:
            dt = self.clock.tick(FPS)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


if __name__ == '__main__':
    SCREEN = pg.display.set_mode(DISPLAY_SIZE)
    GAME_STATES = {
        "HOME_MENU": HomeMenu(),
        "HOME_MENU2": HomeMenu2(),
        "DEAD_MENU": DeadMenu(),
        "PAUSE_MENU": PauseMenu(),
        "DOG_FIGHT": Game(),
        }
    app = App(SCREEN, GAME_STATES)
    app.run()
    # hm = HomeMenu()
    # dm = DeadMenu()
    # hm.new()
    # while g.running:
    #     while g.playing:
    #         g.new()
    # dm.new()
