from button import Button
from settings import *


class ShidpitPreview(Button):
    def __init__(self, id_num, pos, img, scale=(1, 1), col=1, max_col=3, row=1, max_row=3):
        super().__init__(id_num, pos, img)
        self.image = pg.transform.scale(self.image, (int(128 * scale[0]), int(128 * scale[1])))
        self.rect = self.image.get_rect()
        self.column = col
        self.row = row
        self.max_column = max_col
        self.max_row = max_row
        self.shidpit = None
        self.ship_img = pg.Surface((int(128 * scale[0]), int(128 * scale[1])))
        self.ship_info_img = pg.Surface((int(128 * scale[0]), int(128 * scale[1])))
        self.ship_img.fill(DARK_GREEN)
        self.ship_info_img.fill(SEASHELL)
        self.selected = False
        self.sub_id = "none"

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
        super(ShidpitPreview, self).draw(window)
        if self.selected:
            pg.draw.rect(window, GREY50, self.rect, 2)

    def draw_selection_outline(self):
        pg.draw.rect(self.image, GOLDENROD, self.rect)

    def flip_to_info(self):
        self.image = self.ship_info_img

    def flip_to_img(self):
        self.image = self.ship_img
