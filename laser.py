from settings import *


class Laser(pg.sprite.Sprite):
    def __init__(self, game, x, y, img, colormask=LIME):
        super(Laser, self).__init__()
        self.game = game
        self.x = x
        self.y = y
        self.image = img
        self.image = pg.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.colorImage = pg.Surface(self.image.get_size()).convert_alpha()
        self.colorImage.fill(colormask)
        self.image.blit(self.colorImage, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.velocity = 7
        self.is_player = False
        self.is_AI = False
        self.power_level = 0
        self.damage = 0

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.y -= self.velocity

    def detonate(self, _target):
        if _target.shield_points > 0:
            _target.shield_points -= 100
        elif _target.shield_points <= 0:
            _target.hull_points -= 10
        self.kill()
