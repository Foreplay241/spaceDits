from settings import *
from GameStates.gamestate import GameState


class Menu(GameState):
    def __init__(self):
        super().__init__()
        pg.init()
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
        screen.fill(DARK_SALMON)
        player_draw_text(screen, "Basic menu", DARK_BROWN, 36, DISPLAY_TOP_CENTER)
        pg.display.flip()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
