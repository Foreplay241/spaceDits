from button import Button
from settings import *
from text import Text


class RedilotPreview(Button):
    def __init__(self, id_num, pos, img, col=1, max_col=3, row=1, max_row=3):
        super().__init__(id_num, pos, img)
        self.column = col
        self.row = row
        self.max_column = max_col
        self.max_row = max_row
        self.medal_img = pg.Surface((128, 128))
        self.medal_info_img = pg.Surface((128, 128))
        self.medal_img.fill(GOLDENROD)
        self.medal_info_img.fill(ROYAL_BLUE)

    def set_medal_img(self, newImg):
        self.medal_img = newImg

    def set_medal_info_img(self, newImg):
        self.medal_info_img = newImg

    def update_image(self, newImg):
        super(RedilotPreview, self).update_image(newImg)

    def events(self):
        pass

    def update(self):
        super(RedilotPreview, self).update()
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)

    def draw_selection_outline(self):
        pg.draw.rect(self.image, GOLDENROD, self.rect)

    def flip_to_info(self):
        self.image = self.medal_info_img

    def flip_to_img(self):
        self.image = self.medal_img

