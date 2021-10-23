from button import Button
from settings import *
from text import Text


class RedilotPreview(Button):
    def __init__(self, id_num, pos, img, scale=(1, 1), col=1, max_col=3, row=1, max_row=3):
        super().__init__(id_num, pos, img)
        self.image = pg.transform.scale(self.image, (int(128 * scale[0]), int(128 * scale[1])))
        self.rect = self.image.get_rect()
        self.column = col
        self.row = row
        self.max_column = max_col
        self.max_row = max_row
        self.medal_img = pg.Surface((int(128 * scale[0]), int(128 * scale[1])))
        self.medal_info_img = pg.Surface((int(128 * scale[0]), int(128 * scale[1])))
        self.medal_img.fill(SAGE_GREEN)
        self.medal_info_img.fill(ROYAL_BLUE)
        self.selected = False
        self.redilot_name = "none"

    def set_medal_img(self, newImg):
        self.medal_img = newImg

    def set_medal_info_img(self, newImg):
        self.medal_info_img = newImg

    def set_selected(self, isSelected):
        self.selected = isSelected

    def update_image(self, newImg):
        super(RedilotPreview, self).update_image(newImg)

    def events(self):
        pass

    def update(self):
        super(RedilotPreview, self).update()

    def draw(self, window):
        super(RedilotPreview, self).draw(window)
        if self.selected:
            pg.draw.rect(window, YELLOW, self.rect, 2)

    def flip_to_info(self):
        self.image = self.medal_info_img

    def flip_to_img(self):
        self.image = self.medal_img

