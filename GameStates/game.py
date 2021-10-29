from player import Player
from settings import *
from GameStates.gamestate import GameState
import praw


class Game(GameState):
    def __init__(self):
        super().__init__()
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
        pg.key.set_repeat(250, 50)

    def startup(self, persistent):
        """
        Create then run a new game with a player redilot.
        :param persistent:
        :return: None
        """
        if "Player" in persistent:
            self.player = persistent["Player"]
        else:
            self.player = Player(self, persistent["Player Redilot"], persistent["Player Shidpit"])
            self.player.is_player = True
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
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
            if event.key == pg.K_a:
                self.player.x_velocity -= 1
            if event.key == pg.K_d:
                self.player.x_velocity += 1
            if event.key == pg.K_w:
                self.player.y_velocity -= 1
                self.player.fuel_usage = -self.player.y_velocity
            if event.key == pg.K_s:
                self.player.y_velocity += 1
                self.player.fuel_usage = -self.player.y_velocity
            if event.key == pg.K_p:
                self.persist = {
                    "Player Redilot": self.player.redilot,
                    "Player Ship": self.player.shidpit,
                    "Player": self.player,
                }
                self.next_state_name = "PAUSE_MENU"
                self.done = True

        keys = pg.key.get_pressed()
        if keys[pg.K_u]:
            self.player.shoot(self.player.shidpit.left_blaster)
        if keys[pg.K_i]:
            self.player.shoot(self.player.shidpit.middle_blaster)
        if keys[pg.K_o]:
            self.player.shoot(self.player.shidpit.right_blaster)
        if keys[pg.K_j]:
            self.player.deploy(self.player.shidpit.left_missle_pod)
        if keys[pg.K_k]:
            self.player.deploy(self.player.shidpit.right_missle_pod)
        if keys[pg.K_m]:
            self.player.deploy(self.player.shidpit.bomb_bay)

    def update(self, dt):
        self.all_sprites.update()
        for laser in self.player.lasers:
            laser.update()

        if self.player.hull_points <= 0:
            self.player.death()
            self.persist = {
                "Player": self.player,
            }
            self.next_state_name = "DEAD_MENU"
            self.done = True

    def draw(self, screen):
        screen.fill(LIGHT_GREY)
        screen.blit(BG, (0, 0))
        self.all_sprites.draw(self.screen)
        for laser in self.player.lasers:
            laser.draw(self.screen)
        self.player.draw(self.screen)
