from settings import *


class Bomb(pg.sprite.Sprite):
    def __init__(self, game, pos, img, colormask=DARK_GREEN):
        super(Bomb, self).__init__()
        self.game = game
        self.x, self.y = pos
        self.image = img
        self.image = pg.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))
        self.colorImage = pg.Surface(self.image.get_size()).convert_alpha()
        self.colorImage.fill(colormask)
        self.image.blit(self.colorImage, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.is_player = False
        self.is_AI = False
        self.power_level = 0

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def detonate(self, _target):
        if _target.shield_points > 0:
            _target.shield_points -= 10
        elif _target.shield_points <= 0:
            _target.hull_points -= 100
        self.kill()
