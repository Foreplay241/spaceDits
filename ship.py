from datetime import datetime

from settings import *
from laser import Laser
from missle import Missle


class Ship(pg.sprite.Sprite):
    def __init__(self, game, x, y, redilot, shidpit, health=100, shield=100):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.redilot = redilot
        self.shidpit = shidpit
        self.min_x_vel = -2
        self.x_vel = 0
        self.max_x_vel = 2
        self.min_y_vel = -10
        self.y_vel = -5
        self.max_y_vel = -1
        self.outcome = "winner"

        # SHIP STATS
        self.health = health
        self.max_health = health
        self.shield = shield
        self.max_shield = shield
        self.shield_recharge_rate = 3
        self.laser_power = .15
        self.missle_power = .25
        self.engine_power = 10

        # WEAPON STUFF
        self.laser = None
        self.laser_img = pg.image.load(os.path.join("assets", "laser.png"))
        self.lasers = []
        self.laser_cool_down = 150
        self.missle = None
        self.missle_img = pg.image.load(os.path.join("assets", "missle.png"))
        self.missles = []
        self.missle_cool_down = 250
        self.prev_laser_time = pg.time.get_ticks()
        self.prev_missle_time = pg.time.get_ticks()

        self.can_shoot = True
        self.is_player = False
        self.redilot_age = self.redilot.cake_day - datetime.utcnow().timestamp()
        self.redilot_age = abs(int(self.redilot_age))

    def update(self):
        # KEEP VELOCITIES IN RANGE
        if self.x_vel > self.max_x_vel:
            self.x_vel = self.max_x_vel
        if self.x_vel < self.min_x_vel:
            self.x_vel = self.min_x_vel
        if self.y_vel > self.max_y_vel:
            self.y_vel = self.max_y_vel
        if self.y_vel < self.min_y_vel:
            self.y_vel = self.min_y_vel

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # KEEP SHIP IN WINDOW
        if self.rect.y <= DISPLAY_TOP:
            self.rect.y = DISPLAY_BOTTOM
        if self.rect.y > DISPLAY_BOTTOM:
            self.rect.y = DISPLAY_TOP
        if self.rect.x < DISPLAY_LEFT:
            self.rect.x = DISPLAY_RIGHT
        if self.rect.x > DISPLAY_RIGHT:
            self.rect.x = DISPLAY_LEFT

        # RECHARGE SHIELD AND CHECK FOR DEATH
        if self.shield < self.max_shield:
            self.shield += self.shield_recharge_rate
        if self.shield > self.max_shield:
            self.shield = self.max_shield

    def draw(self, window):
        pass

    def shoot(self, blaster):
        pass

    def fire_missle(self, podbay):
        pass

    def death(self):
        self.outcome = "loser"
        self.kill()

