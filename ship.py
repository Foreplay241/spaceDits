import os
from datetime import datetime

from settings import *
from laser import Laser
from missile import Missile


class Ship(pg.sprite.Sprite):
    def __init__(self, game, redilot, shidpit):
        super().__init__()
        self.game = game
        self.name = redilot.name + "_" + shidpit.submission_id
        self.pos = shidpit.ship_properties["position"]
        self.redilot = redilot
        self.shidpit = shidpit
        self.min_x_velocity = -2
        self.x_velocity = 0
        self.max_x_velocity = 2
        self.min_y_velocity = -10
        self.y_velocity = -5
        self.max_y_velocity = -1
        self.outcome = "undecided"

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
        self.weapons_dict = self.shidpit.weapons_dict

        self.laser = None
        self.laser_img = pg.image.load(os.path.join("assets", "laser.png"))
        self.lasers = []
        self.laser_fire_rate = 0
        self.laser_power_hull = 1 - self.shidpit.upvote_ratio
        self.laser_power_shield = self.shidpit.upvote_ratio

        self.missile = None
        self.missile_img = pg.image.load(os.path.join("assets", "missile.png"))
        self.missiles = []
        self.missile_cool_down = 250
        self.missile_power_hull = .65
        self.missile_power_shield = .15
        self.prev_laser_time = pg.time.get_ticks()
        self.prev_missile_time = pg.time.get_ticks()

        self.bomb = None
        self.bomb_img = pg.image.load(os.path.join("assets", "bomb.png"))
        self.bombs = []
        self.bomb_cool_down = 300
        self.bomb_power_hull = .90
        self.bomb_power_shield = .07

        self.can_shoot = True
        self.is_player = False
        self.redilot_age = self.redilot.cake_day - datetime.utcnow().timestamp()
        self.redilot_age = abs(int(self.redilot_age))

    def update(self):
        # KEEP VELOCITIES IN RANGE
        if self.x_velocity > self.max_x_velocity:
            self.x_velocity = self.max_x_velocity
        if self.x_velocity < self.min_x_velocity:
            self.x_velocity = self.min_x_velocity
        if self.y_velocity > self.max_y_velocity:
            self.y_velocity = self.max_y_velocity
        if self.y_velocity < self.min_y_velocity:
            self.y_velocity = self.min_y_velocity

        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
        self.shidpit.ship_properties["position"] = (self.rect.x, self.rect.y)
        self.shidpit.ship_properties["y velocity"] = self.y_velocity

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
            self.y_velocity = -1

    def draw(self, window):
        pass

    def shoot(self, blaster):
        blaster.fire(self.game)

    def deploy(self, podbay):
        podbay.fire(self.game)

    def release(self, bombay):
        bombay.drop

    def death(self):
        self.outcome = "loser"
        self.kill()
