import os
from datetime import datetime

from settings import *
from laser import Laser
from missle import Missle


class Ship(pg.sprite.Sprite):
    def __init__(self, game, x, y, redilot, shidpit):
        super().__init__()
        self.game = game
        self.name = redilot.name + "_" + shidpit.sub_id
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
        self.max_hull_points = self.redilot.max_hull_points + self.shidpit.max_hull_points
        self.hull_points = self.max_hull_points
        self.max_shield_points = self.redilot.max_shield_points + self.shidpit.max_shield_points
        self.shield_points = self.max_shield_points
        self.shield_recharge_rate = 3

        # ENGINE AND FUEL
        self.engine_power = 10
        self.fuel_usage_rate = 2
        self.max_fuel = 100
        self.current_fuel = 100

        # WEAPON STUFF
        self.weapons_dict = {}

        self.laser = None
        self.laser_img = pg.image.load(os.path.join("assets", "laser.png"))
        self.lasers = []
        self.laser_cool_down = 150
        self.laser_power_hull = .05
        self.laser_power_shield = .40

        self.bullet = None
        self.bullet_img = pg.image.load(os.path.join("assets", "bullet.png"))
        self.bullets = []
        self.bullet_cool_down = 200
        self.bullet_power_hull = .35
        self.bullet_power_shield = .02

        self.bomb = None
        self.bomb_img = pg.image.load(os.path.join("assets", "bomb.png"))
        self.bombs = []
        self.bomb_cool_down = 300
        self.bomb_power_hull = .90
        self.bomb_power_shield = .07

        self.missle = None
        self.missle_img = pg.image.load(os.path.join("assets", "missle.png"))
        self.missles = []
        self.missle_cool_down = 250
        self.missle_power_hull = .65
        self.missle_power_shield = .15
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
        if self.shield_points < self.max_shield_points:
            self.shield_points += self.shield_recharge_rate
        if self.shield_points > self.max_shield_points:
            self.shield_points = self.max_shield_points

        # USE FUEL
        self.current_fuel -= self.fuel_usage_rate * .01
        if self.current_fuel < 0:
            self.current_fuel = 0
            self.fuel_usage_rate = 0
            self.y_vel = -1

    def draw(self, window):
        pass

    def shoot(self, blaster):
        now = pg.time.get_ticks()
        if now - self.prev_laser_time > blaster["Fire Rate"]:
            self.prev_laser_time = pg.time.get_ticks()
            laser = Laser(self.game, self.rect.x + blaster["Position"][0],
                          self.rect.y + blaster["Position"][1], self.laser_img, colormask=LIGHT_BLUE)
            laser.is_player = True
            laser.velocity -= self.y_vel
            self.lasers.append(laser)
            self.game.all_sprites.add(laser)
            self.game.player_lasers.add(laser)

    def deploy(self, podbay):
        pass

    def release(self, bombay):
        pass

    def death(self):
        self.outcome = "loser"
        self.kill()

