from button import Button
from settings import *


class TextButton(Button):

    def __init__(self, id_num, pos, img, text="TEXT", textcolor=BLACK, optiontype=None, optioncolor=RANDOM_GREEN,
                 fontsize=16, col=1, max_col=3, row=1, max_row=3, canEdit=False, maxWidth=200):
        super().__init__(id_num, pos, img)
        self.id = id_num
        self.x, self.y = pos
        self.font_size = fontsize
        self.fontname = pg.font.match_font('ariel')
        self.text = text
        self.textcolor = textcolor
        self.optioncolor = optioncolor
        self.optiontype = optiontype
        self.txt_img = None
        self.opt_img = None
        self.txt_rect = None
        self.opt_rect = None
        self.font = None
        self.column = col
        self.row = row
        self.max_column = max_col
        self.max_row = max_row
        self.canEdit = canEdit
        self.max_width = maxWidth
        self.set_button_option(optioncolor, optiontype)
        self.set_font()
        self.render()

    def update(self):
        super(TextButton, self).update()
        self.rect.x = (DISPLAY_WIDTH * self.column) // self.max_column - (self.image.get_width() // 2)
        self.rect.y = (DISPLAY_HEIGHT * self.row) // self.max_row

    def set_font(self):
        self.font = pg.font.Font(self.fontname, self.font_size)

    def set_button_option(self, optioncolor, optiontype):
        self.optioncolor = optioncolor
        self.optiontype = optiontype
        if self.optiontype == "True":
            self.optioncolor = LIGHT_SLATE_BLUE
        elif self.optiontype == "False":
            self.optioncolor = DARK_SLATE_BLUE

    def render(self):
        """Render the text onto the image."""
        self.txt_img = self.font.render(self.text, True, self.textcolor)
        self.opt_img = self.font.render(self.optiontype, True, self.optioncolor)
        self.txt_rect = self.txt_img.get_rect()
        self.opt_rect = self.opt_img.get_rect()
        self.image = pg.transform.scale(self.image, (self.max_width, 22))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.image.blit(self.txt_img,
                        ((self.image.get_width() // 2) - (self.txt_rect.width // 2),
                         self.txt_rect.height * 2 // 4))
        self.image.blit(self.opt_img, (8, self.opt_rect.height // 2))
        # if self.active:
        #     pg.draw.rect(self.image, FREE_SPEECH_GREEN, self.rect, 2)
        # if not self.active:
        #     pg.draw.rect(self.image, DARK_SEA_GREEN, self.rect, 2)

    def update_button_text(self, text):
        self.text = str(text)
        self.image.fill(BLACK)
        self.render()
