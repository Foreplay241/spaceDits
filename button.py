import pygame as pg
from settings import *


class Button(pg.sprite.Sprite):

    def __init__(self, pos, img, col=1, max_col=3, row=1, max_row=3):
        super(Button, self).__init__()
        self.x, self.y = pos
        self.image = pg.image.load(f'assets/buttons/{img}.png').convert()
        self.rect = self.image.get_rect()
        self.column = col
        self.row = row
        self.max_column = max_col
        self.max_row = max_row
        self.clicked = False
        self.active = False

    def update_image(self, newImg):
        self.image = newImg
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def events(self):
        pass

    def update(self):
        super(Button, self).update()
        self.rect.x = (DISPLAY_WIDTH * self.column) // self.max_column - (self.image.get_width() // 2)
        self.rect.y = (DISPLAY_HEIGHT * self.row) // self.max_row

    def draw(self, window):
        window.blit(self.image, self.rect)

    def draw_selection_outline(self):
        pg.draw.rect(self.image, GOLDENROD, self.rect)
