import os
from datetime import datetime

from pygame.math import Vector2

from settings import *


class Ship(pg.sprite.Sprite):
    name: str
    orig_image: pg.Surface

    def __init__(self, game, redilot, shidpit):
        super().__init__()
        self.game = game
        self.name = redilot.redditor_name + "_" + shidpit.submission_id
        self.position = shidpit.ship_properties["position"]
        self.redilot = redilot
        self.shidpit = shidpit
        self.outcome = "undecided"
        self.isOffScreen = False
        self.image = self.shidpit.ship_img
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.orig_image = self.image
        self.HUD_color_theme = GREY

        # MOVEMENT VARIABLES
        self.direction = Vector2(0, -1)
        self.position = Vector2(420, 420)
        self.angle_speed = 0
        self.angle = 0
        self.speed = 0

        # MINING AND RACING MOVEMENT VARIABLES
        self.x_velocity = 0
        self.min_x_velocity = self.redilot.min_x_velocity
        self.max_x_velocity = self.redilot.max_x_velocity
        self.y_velocity = -5
        self.min_y_velocity = self.redilot.min_y_velocity
        self.max_y_velocity = self.redilot.max_y_velocity

        # HEALTH STATS
        self.max_hull_points = self.redilot.max_hull_points + self.shidpit.max_hull_points
        self.hull_points = self.max_hull_points
        self.max_shield_points = self.redilot.max_shield_points + self.shidpit.max_shield_points
        self.shield_points = self.max_shield_points
        self.shield_recharge_rate = 3

        # ENGINE AND FUEL
        self.engine_power = 10
        self.max_speed = 6
        self.min_speed = .5
        self.fuel_usage_rate = 2
        self.max_fuel = 100
        self.current_fuel = 100

    def update(self):
        if self.angle_speed != 0:
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pg.transform.rotate(self.orig_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.direction * self.speed
        self.rect.center = self.position

        # RECHARGE SHIELD
        if self.shield_points < self.max_shield_points:
            self.shield_points += self.shield_recharge_rate
        if self.shield_points > self.max_shield_points:
            self.shield_points = self.max_shield_points

        # CHECK SPEED AND USE FUEL
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < self.min_speed:
            self.speed = self.min_speed
        self.fuel_usage_rate = self.speed
        self.current_fuel -= self.fuel_usage_rate * .01
        if self.current_fuel < 0:
            self.current_fuel = 0
            self.fuel_usage_rate = 0
            # self.min_speed = 0.2
            # self.max_speed = 0.5

    def draw(self, window):
        pass

    def death(self):
        self.outcome = "loser"
        self.kill()
