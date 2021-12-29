from pygame import Vector2

from settings import *


class Laser(pg.sprite.Sprite):
    def __init__(self, game, pos, img, colormask=LIME, direction=Vector2(0, 0)):
        super(Laser, self).__init__()
        self.game = game
        self.x, self.y = pos
        self.image = img
        self.image = pg.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.orig_image = self.image
        self.colorImage = pg.Surface(self.image.get_size()).convert_alpha()
        self.colorImage.fill(colormask)
        self.image.blit(self.colorImage, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.velocity = 0
        self.is_player = False
        self.is_AI = False
        self.power_level = 0
        self.damage = 0

        self.angle_speed = 0
        self.direction = direction
        self.angle = 0
        self.position = pos
        self.speed = 4

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def update(self):
        self.position += self.direction * self.speed
        self.rect.center = self.position
