from GUI.button import Button
from settings import *


class FusionPreview(Button):
    def __init__(self, id_num, pos, img, scale=(1, 1), col=1, max_col=3, row=1, max_row=3):
        super().__init__(id_num, pos, img)
        self.image = pg.transform.scale(self.image, (int(128 * scale[0]), int(128 * scale[1])))
        self.rect = self.image.get_rect()
        self.column = col
        self.row = row
        self.max_column = max_col
        self.max_row = max_row
        self.fusion = None
        self.img = None
        self.info = None
        self.selected = False
        self.submission_id = id_num

    def set_img(self, newImg):
        self.img = newImg

    def set_info(self, newImg):
        self.info = newImg

    def update_image(self, newImg):
        super(FusionPreview, self).update_image(newImg)

    def events(self):
        pass

    def update(self):
        super(FusionPreview, self).update()

    def draw(self, window):
        super(FusionPreview, self).draw(window)
        if self.selected:
            pg.draw.rect(window, GREY50, self.rect, 2)

    def draw_selection_outline(self):
        pg.draw.rect(self.image, GOLDENROD, self.rect)

    def flip_to_info(self):
        self.image = self.info

    def flip_to_img(self):
        self.image = self.img
