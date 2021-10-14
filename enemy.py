import random

from ship import *


class Enemy(Ship):

    def __init__(self, game, x, y, redilot, shidpit):
        super().__init__(game, x, y, redilot, shidpit)
        self.image = shidpit.img
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (50, 45))
        self.colorImage = pg.Surface(self.image.get_size()).convert_alpha()
        self.colorImage.fill(RANDOM_RED)
        self.image.blit(self.colorImage, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()

    def update(self):
        super(Enemy, self).update()
        self.choose_action()
        if self.rect.x == self.game.player.rect.x:
            self.shoot(None)

    def choose_action(self):
        # ALIGN X COORDS
        if self.rect.x >= self.game.player.rect.x:
            self.change_velocity(dx_vel=-1)
        if self.rect.x <= self.game.player.rect.x:
            self.change_velocity(dx_vel=1)
        # ALIGN Y COORDS
        if self.rect.y <= self.game.player.rect.y:
            self.change_velocity(dy_vel=1)
        if self.rect.y >= self.game.player.rect.y + 90:
            self.change_velocity(dy_vel=-1)

    def draw(self, window):
        super().draw(window)

    def shoot(self, blaster):
        now = pg.time.get_ticks()
        if now - self.prev_laser_time > self.laser_cool_down:
            self.prev_laser_time = pg.time.get_ticks()
            laser = Laser(self.game, self.rect.x + (self.image.get_width() / 2),
                          self.rect.y + ((self.image.get_height() * 2) / 3), self.laser_img, colormask=LIGHT_RED)
            laser.is_AI = True
            self.lasers.append(laser)
            self.game.all_sprites.add(laser)
            self.game.enemy_lasers.add(laser)

    def fire_missle(self, podbay):
        now = pg.time.get_ticks()
        if now - self.prev_missle_time > self.missle_cool_down:
            self.prev_missle_time = pg.time.get_ticks()
            missle = Missle(self.game, self.rect.x + (self.image.get_width() / 2),
                            self.rect.y + ((self.image.get_height() * 2) / 3), self.missle_img, colormask=ORANGE_RED)
            missle.is_AI = True
            self.missles.append(missle)
            self.game.all_sprites.add(missle)
            self.game.enemy_missles.add(missle)

    def death(self):
        super(Enemy, self).death()

    def change_velocity(self, dx_vel=0, dy_vel=0):
        if dx_vel == 0:
            dx_vel = random.randint(-1, 1)
        if dy_vel == 0:
            dy_vel = random.randint(-1, 1)
        self.x_vel += dx_vel
        self.y_vel += dy_vel
        print(dx_vel)
        print(dy_vel)
