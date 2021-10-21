from button import Button
from settings import *


class ShidpitPreview(Button):
    def __init__(self, id_num, pos, img, col=1, max_col=3, row=1, max_row=3):
        super().__init__(id_num, pos, img)
        self.column = col
        self.row = row
        self.max_column = max_col
        self.max_row = max_row
        self.shidpit = None
        self.ship_img = pg.Surface((128, 128))
        self.ship_info_img = pg.Surface((128, 128))
        self.ship_img.fill(DARK_SEA_GREEN)
        self.ship_info_img.fill(SEASHELL)

    def set_ship_img(self, newImg):
        self.ship_img = newImg

    def set_ship_info_img(self, newImg):
        self.ship_info_img = newImg

    def update_image(self, newImg):
        super(ShidpitPreview, self).update_image(newImg)

    def events(self):
        pass

    def update(self):
        super(ShidpitPreview, self).update()

    def draw(self, window):
        window.blit(self.image, self.rect)

    def draw_selection_outline(self):
        pg.draw.rect(self.image, GOLDENROD, self.rect)

    def flip_to_info(self):
        self.image = self.ship_info_img

    def flip_to_img(self):
        self.image = self.ship_img
