import random

from settings import *
from GameStates.gamestate import GameState


class Menu(GameState):
    def __init__(self):
        super().__init__()
        pg.init()
        self.BGn = random.randint(0, 9)
        sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        gamestatesAssetsPath = os.path.join(sourceFileDir, "assets")
        backgroundPath = os.path.join(gamestatesAssetsPath, "backgrounds")
        self.background_image = pg.image.load(os.path.join(backgroundPath, f"MenuBG{self.BGn}.png"))
        self.background_credit = pg.image.load(os.path.join(backgroundPath, "deep-foldcredit.png"))
        self.BGx = random.randint(-241, 0)
        self.background_image.blit(self.background_credit, (-self.BGx + random.randint(-15, 390),
                                                            DISPLAY_HEIGHT - self.background_credit.get_height()))
        self.is_active = True
        self.mouse_pos = (0, 0)

    def startup(self, persistent):
        print("menu")

    def get_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = pg.mouse.get_pos()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pg.display.flip()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
