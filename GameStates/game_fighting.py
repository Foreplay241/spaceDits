from pygame.math import Vector2

from GameStates.game import Game
from Player.fighter import Fighter
from RedditFusions.create_enement import Enement
import random
import pygame as pg
import os
from settings import *

from alien import Alien


class Fighting(Game):
    def __init__(self):
        super(Fighting, self).__init__()
        self.background_image = pg.image.load(os.path.join(self.backgroundPath, f"FighterBG{self.BGn}.png"))
        self.background_credit = pg.image.load(os.path.join(self.backgroundPath, "deep-foldcredit.png"))
        self.BGx = random.randint(-241, 0)
        self.background_image.blit(self.background_credit, (-self.BGx + random.randint(-15, 390), 0))

        # ENEMY SET UP
        self.alien_list = []
        self.drone_list = []
        self.num_aliens = 1
        self.num_drones = 1

    def startup(self, persistent):
        super(Fighting, self).startup(persistent)
        self.num_aliens = persistent["Num of Comments"]
        if "Player Redilot" in persistent:
            self.player = Fighter(self, persistent["Player Redilot"], persistent["Player Shidpit"])
        self.all_sprites.add(self.player)
        for i in range(self.num_aliens):
            newTime = random.randint(MIN_CREATION_UTC, MAX_CREATION_UTC) + 0.0
            newEnemy = Enement(creation_time=newTime)
            newAlien = Alien(self, newEnemy)
            self.all_sprites.add(newAlien)
            self.alien_list.append(newAlien)

    def get_event(self, event):
        super(Fighting, self).get_event(event)
        if event.type == pg.KEYUP:
            if event.key == pg.K_a:
                self.player.angle_speed = 0
            if event.key == pg.K_d:
                self.player.angle_speed = 0
            if event.key == pg.K_w:
                self.player.angle_speed = 0
            if event.key == pg.K_s:
                self.player.angle_speed = 0
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                self.player.angle_speed = -1
            if event.key == pg.K_d:
                self.player.angle_speed = 1
            if event.key == pg.K_w:
                self.player.speed += .1
            if event.key == pg.K_s:
                self.player.speed -= .1
            if event.key == pg.K_z:
                self.player.barrel_roll()
            if event.key == pg.K_c:
                self.player.barrel_roll(False)

        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT] and keys[pg.K_a]:
            self.player.angle_speed = -18
        if keys[pg.K_LSHIFT] and keys[pg.K_d]:
            self.player.angle_speed = 18
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
            self.player.release(self.player.shidpit.bomb_bay)
        if keys[pg.K_t]:
            self.player.acquire_target()

    def update(self, dt):
        super(Fighting, self).update(dt)
        for laser in self.player.lasers:
            laser.update()
        for alien in self.alien_list:
            alien.turn_towards(self.player)

    def draw(self, screen):
        super(Fighting, self).draw(screen)
        for laser in self.player.lasers:
            laser.draw(self.screen)
