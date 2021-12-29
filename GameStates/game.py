from settings import *
from GameStates.gamestate import GameState
import pygame as pg


class Game(GameState):
    def __init__(self):
        super().__init__()
        self.BGn = random.randint(0, 9)
        self.sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        self.gamestatesAssetsPath = os.path.join(self.sourceFileDir, "assets")
        self.backgroundPath = os.path.join(self.gamestatesAssetsPath, "backgrounds")
        self.background_image = pg.image.load(os.path.join(self.backgroundPath, f"FighterBG{self.BGn}.png"))
        self.background_credit = pg.image.load(os.path.join(self.backgroundPath, "deep-foldcredit.png"))
        self.BGx = random.randint(-241, 0)
        self.background_image.blit(self.background_credit, (-self.BGx + random.randint(-15, 390), 0))
        self.running = False
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.mouse_pos = (0, 0)
        self.all_sprites = pg.sprite.Group()
        self.player_lasers = pg.sprite.Group()
        self.player_missles = pg.sprite.Group()
        self.player_bombs = pg.sprite.Group()
        self.players_lasers_hit = None
        self.players_missles_hit = None
        self.players_bombs_hit = None
        self.player = None
        self.HUD = None
        self.playing = False
        self.game_type = "MINING"
        pg.key.set_repeat(250, 50)

    def startup(self, persistent):
        """
        Create then run a new game with a player redilot.
        :param persistent:
        :return: None
        """
        if "Player" in persistent:
            self.player = persistent["Player"]
            self.game_type = persistent["Game Type"]
            self.all_sprites.add(self.player)

    def get_event(self, event):
        if event.type == pg.QUIT:
            if self.playing:
                self.playing = False
            self.running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.player.rect.collidepoint(self.mouse_pos):
                self.player.target = None
                print("Clicked player")
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = pg.mouse.get_pos()
        if event.type == pg.KEYUP:
            pass
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
            if event.key == pg.K_p:
                self.persist = {
                    "Player Redilot": self.player.redilot,
                    "Player Ship": self.player.shidpit,
                    "Game Type": self.game_type,
                    "Player": self.player,
                }
                self.next_state_name = "PAUSE_MENU"
                self.done = True

    def update(self, dt):
        self.all_sprites.update()

        if self.player.hull_points <= 0:
            self.player.death()
            self.persist = {
                "Player": self.player
            }
            self.next_state_name = "DEAD_MENU"
            self.done = True

    def draw(self, screen):
        screen.blit(self.background_image, (self.BGx, 0))
        self.all_sprites.draw(self.screen)
        self.player.draw(self.screen)
