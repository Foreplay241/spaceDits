import math

from settings import *
from pygame import Vector2


class Alien(pg.sprite.Sprite):
    def __init__(self, game, enement):
        super(Alien, self).__init__()
        self.game = game
        self.enement = enement
        self.enement.partPath = os.path.join(self.enement.partPath, "alien")
        self.image = enement.generate_img_img()
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (64, 64))
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        # HEALTH AND DEATH
        self.max_health = 10
        self.isTarget = False
        self.isDead = False

        # MOVEMENT VARIABLES
        self.direction = Vector2(0, 0)
        self.position = Vector2(random.randint(0, DISPLAY_WIDTH), random.randint(0, DISPLAY_HEIGHT))
        self.angle_speed = 0
        self.angle = 0
        self.min_speed = 0
        self.max_speed = 4
        self.x_vel = 0
        self.y_vel = 0
        self.enement.add_body()
        self.speed = self.enement.speed + (self.enement.gamma_part_num * .28)

    def update_target_status(self, targeted):
        self.isTarget = targeted


    def update(self):
        super(Alien, self).update()
        if self.angle_speed != 0:
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pg.transform.rotate(self.orig_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.direction * self.speed
        self.rect.center = self.position

    def turn_towards(self, ship):
        x_dir = 0
        y_dir = 0
        if ship.position[0] > self.position[0]:
            x_dir += 1
        if ship.position[0] < self.position[0]:
            x_dir += -1
        if ship.position[1] > self.position[1]:
            y_dir += 1
        if ship.position[1] < self.position[1]:
            y_dir += -1
        self.speed = clamp(self.speed, self.min_speed, self.max_speed)
        # self.speed = 0
        self.direction = Vector2(x_dir, y_dir)
