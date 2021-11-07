from GUI.button import Button
import pygame as pg

from GUI.text_button import TextButton


class HUDbutton(TextButton):
    id_num: int
    HUDsize: tuple
    pos: (0, 0)
    BGimg: pg.Surface
    FGimg: pg.Surface
    dispMod: str

    def __init__(self, id_num, HUDsize, pos, BGimg, FGimg, dispMod, weapon=None,
                 col=1, max_col=3, row=1, max_row=3, text="TEXT"):
        super(HUDbutton, self).__init__(id_num, pos, BGimg, FGimg)
        self.display_module = dispMod
        self.HUDsize = HUDsize

    def update(self):
        super(HUDbutton, self).update()
        if self.column == 0 and self.row == 0 \
                and self.max_row == 0 and self.max_column == 0:
            pass
        else:
            self.pos = ((self.HUDsize[0] * self.column) // self.max_column - (self.image.get_width() // 2),
                        (self.HUDsize[1] * self.row) // self.max_row)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw(self, window):
        window.blit(self.image, self.rect)
