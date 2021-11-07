import os

import pygame as pg
from settings import *


class Button(pg.sprite.Sprite):

    def __init__(self, id_num, pos, BGimg, FGimg, col=1, max_col=3, row=1, max_row=3):
        super(Button, self).__init__()
        self.id_num = id_num
        self.pos = pos
        self.sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        self.GUIAssetsPath = os.path.join(self.sourceFileDir, "assets")
        self.BGimage = pg.Surface((35, 35))
        self.FGimage = pg.Surface((15, 15))
        if type(BGimg) is tuple:
            self.BGimage = pg.Surface(BGimg)
        elif type(BGimg) is str:
            self.BGimage = pg.image.load(os.path.join(self.GUIAssetsPath, BGimg + ".png")).convert_alpha()

        if type(FGimg) is tuple:
            self.BGimage = pg.Surface(FGimg)
        elif type(FGimg) is str:
            self.FGimage = pg.image.load(os.path.join(self.GUIAssetsPath, FGimg + ".png")).convert_alpha()

        self.column = col
        self.row = row
        self.max_column = max_col
        self.max_row = max_row
        self.image = self.BGimage
        # self.image.set_colorkey(BLACK)
        # self.image.blit(self.FGimage, (0, 0))
        self.rect = self.image.get_rect()
        self.clicked = False
        self.active = False

    def update_image(self, newBGimg, newFGimg):
        self.BGimage = newBGimg
        self.FGimage = newFGimg
        self.image.fill(BLACK)
        self.image.blit(self.BGimage, (0, 0))
        self.image.blit(self.FGimage, (0, 0))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def events(self):
        pass

    def update(self):
        super(Button, self).update()
        # IF ROW/COL ARE ALL 0, IGNORE THE GRID
        if self.column == 0 and self.row == 0:
            if self.max_row == 0 and self.max_column == 0:
                pass
        else:
            self.pos = ((DISPLAY_WIDTH * self.column) // self.max_column - (self.image.get_width() // 2),
                        (DISPLAY_HEIGHT * self.row) // self.max_row)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw(self, window):
        window.blit(self.image, self.rect)
        if self.active:
            pg.draw.rect(self.image, MIDNIGHT_BLUE, self.rect, 4)

    def draw_selection_outline(self):
        pg.draw.rect(self.image, MIDNIGHT_BLUE, self.rect, 4)
