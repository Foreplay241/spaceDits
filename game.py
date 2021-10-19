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
            self.player = Player(self, persistent["Player Redilot"], persistent["Player Ship"])
            self.player.is_player = True
        if "Enemy" in persistent:
            self.enemy = persistent["Enemy"]
        else:
            self.enemy = Enemy(self, persistent["Enemy Redilot"], persistent["Enemy Ship"])
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemy)

    def get_event(self, event):
        if event.type == pg.QUIT:
            if self.playing:
                self.playing = False
            self.running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.player.rect.collidepoint(self.mouse_pos):
                self.player.target = None
                print("Clicked player")
            if self.enemy.rect.collidepoint(self.mouse_pos):
                self.player.target = self.enemy
                print("Clicked enemy")
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
            if event.key == pg.K_KP4:
                self.enemy.x_velocity -= 1
            if event.key == pg.K_KP6:
                self.enemy.x_velocity += 1
            if event.key == pg.K_KP8:
                self.enemy.y_velocity -= 1
                self.enemy.fuel_usage = -self.enemy.y_velocity
            if event.key == pg.K_KP5:
                self.enemy.y_velocity += 1
                self.enemy.fuel_usage = -self.enemy.y_velocity
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
        if keys[pg.K_u]:
            self.player.shoot(self.player.weapons_dict["blaster1"])
        if keys[pg.K_i]:
            self.player.shoot(self.player.weapons_dict["blaster2"])
        if keys[pg.K_o]:
            self.player.shoot(self.player.weapons_dict["blaster3"])
        if keys[pg.K_j]:
            self.player.deploy(self.player.weapons_dict["pod1"])
        if keys[pg.K_k]:
            self.player.deploy(self.player.weapons_dict["pod2"])
        if keys[pg.K_m]:
            self.player.release(self.player.weapons_dict["bay"])
        if keys[pg.K_KP7]:
            self.enemy.shoot(None)
        if keys[pg.K_KP9]:
            self.enemy.deploy(None)

    def update(self, dt):
        self.all_sprites.update()
        for laser in self.player.lasers:
            laser.update()

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

        if self.player.hull_points <= 0:
            self.player.death()
            self.enemy.kill()
            self.persist = {
                "Player": self.player,
                "Enemy": self.enemy
            }
            self.next_state_name = "DEAD_MENU"
            self.done = True

        if self.enemy.hull_points <= 0:
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
        for laser in self.player.lasers:
            laser.draw(self.screen)
        self.player.draw(self.screen)
