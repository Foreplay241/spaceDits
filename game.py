from player import Player
from enemy import Enemy
from settings import *
from gamestate import GameState
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
        self.enemy_lasers = pg.sprite.Group()
        self.enemy_missles = pg.sprite.Group()
        self.enemys_lasers_hit = None
        self.players_lasers_hit = None
        self.enemys_missles_hit = None
        self.players_missles_hit = None
        self.player = None
        self.enemy = None
        self.HUD = None
        self.playing = False
        pg.key.set_repeat(250, 50)

    def startup(self, persistent):
        """
        Create then run a new game with a player redilot and an enemy redilot.
        :param persistent:
        :return: None
        """
        if "Player" in persistent:
            self.player = persistent["Player"]
        else:
            self.player = Player(self, DISPLAY_WIDTH // 2, (DISPLAY_HEIGHT * 2) / 3,
                                 persistent["Player Redilot"], persistent["Player Ship"])
            self.player.is_player = True
        if "Enemy" in persistent:
            self.enemy = persistent["Enemy"]
        else:
            self.enemy = Enemy(self, DISPLAY_WIDTH // 2, DISPLAY_HEIGHT / 3,
                               persistent["Enemy Redilot"], persistent["Enemy Ship"])
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemy)

    def get_event(self, event):
        if event.type == pg.QUIT:
            if self.playing:
                self.playing = False
            self.running = False
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = pg.mouse.get_pos()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
            if event.key == pg.K_a:
                self.player.x_vel -= 1
                # self.enemy.change_velocity(dx_vel=-1)
            if event.key == pg.K_d:
                self.player.x_vel += 1
                # self.enemy.change_velocity(dx_vel=1)
            if event.key == pg.K_w:
                self.player.y_vel -= 1
                # self.enemy.change_velocity(dy_vel=-1)
                self.player.fuel_usage = -self.player.y_vel
            if event.key == pg.K_s:
                self.player.y_vel += 1
                # self.enemy.change_velocity(dy_vel=1)
                self.player.fuel_usage = -self.player.y_vel
            if event.key == pg.K_KP4:
                self.enemy.x_vel -= 1
            if event.key == pg.K_KP6:
                self.enemy.x_vel += 1
            if event.key == pg.K_KP8:
                self.enemy.y_vel -= 1
                self.enemy.fuel_usage = -self.enemy.y_vel
            if event.key == pg.K_KP5:
                self.enemy.y_vel += 1
                self.enemy.fuel_usage = -self.enemy.y_vel
            if event.key == pg.K_p:
                self.persist = {
                    "Player Redilot": self.player.redilot,
                    "Player Ship": self.player.shidpit,
                    "Player": self.player,
                    "Enemy Redilot": self.enemy.redilot,
                    "Enemy Ship": self.enemy.shidpit,
                    "Enemy": self.enemy
                }
                self.next_state_name = "PAUSE_MENU"
                self.done = True

        keys = pg.key.get_pressed()
        if keys[pg.K_q]:
            self.player.shoot(None)
        if keys[pg.K_e]:
            self.player.fire_missle(None)
        if keys[pg.K_KP7]:
            self.enemy.shoot(None)
        if keys[pg.K_KP9]:
            self.enemy.fire_missle(None)

    def update(self, dt):
        self.all_sprites.update()

        self.enemys_lasers_hit = pg.sprite.spritecollide(self.player, self.enemy_lasers, False)
        for h in self.enemys_lasers_hit:
            h.detonate(self.player)

        self.enemys_missles_hit = pg.sprite.spritecollide(self.player, self.enemy_missles, False)
        for h in self.enemys_missles_hit:
            h.detonate(self.enemy)

        self.players_lasers_hit = pg.sprite.spritecollide(self.enemy, self.player_lasers, False)
        for h in self.players_lasers_hit:
            h.detonate(self.enemy)

        self.players_missles_hit = pg.sprite.spritecollide(self.enemy, self.player_missles, False)
        for h in self.players_missles_hit:
            h.detonate(self.enemy)

        if self.player.health <= 0:
            self.player.death()
            self.enemy.kill()
            self.persist = {
                "Player": self.player,
                "Enemy": self.enemy
            }
            self.next_state_name = "DEAD_MENU"
            self.done = True

        if self.enemy.health <= 0:
            self.enemy.death()
            self.player.kill()
            self.persist = {
                "Player": self.player,
                "Enemy": self.enemy
            }
            self.next_state_name = "DEAD_MENU"
            self.done = True

    def draw(self, screen):
        screen.fill(LIGHT_GREY)
        screen.blit(BG, (0, 0))
        self.all_sprites.draw(self.screen)
        self.player.draw(self.screen)
