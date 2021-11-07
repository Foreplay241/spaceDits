from GUI.button import Button
from settings import *


class TextButton(Button):

    def __init__(self, id_num, pos, BGimg, FGimg,
                 text="TEXT", textcolor=BLACK, bgColor=SPACE_GREY,
                 optiontext=None, optioncolor=RANDOM_GREEN,
                 valuetext=None, valuecolor=FREE_SPEECH_GREEN,
                 fontsize=16, col=1, max_col=3, row=1, max_row=3, canEdit=False, maxWidth=200):
        """

        :param id_num: unique id number per button
        :param pos: keeps track of position of button
        :param img: image of the button
        :param text: text on top of image of the button
        :param textcolor: color of that text
        :param optiontext: if button has an option text
        :param optioncolor: the color of that text
        :param valuetext: if the button has an option text, it probably has a value
        :param valuecolor: the color of that text
        :param fontsize: the size of the font of text
        :param col: column position
        :param max_col: max columns on the screen
        :param row: row position
        :param max_row: mac rows on the screen
        :param canEdit: if the text is editable
        :param maxWidth: width of the button
        """
        super().__init__(id_num, pos, BGimg, FGimg)
        self.id = id_num
        self.x, self.y = pos
        self.font_size = fontsize
        self.fontname = pg.font.match_font('ariel')
        self.text = text
        self.textcolor = textcolor
        self.bgColor = bgColor
        self.BGimage.fill(bgColor)
        self.FGimage.fill(HOT_PINK)
        self.optioncolor = optioncolor
        self.optiontext = optiontext
        self.valuetext = valuetext
        self.valuecolor = valuecolor
        self.txt_img = None
        self.opt_img = None
        self.val_img = None
        self.txt_rect = None
        self.opt_rect = None
        self.val_rect = None
        self.font = None
        self.column = col
        self.row = row
        self.max_column = max_col
        self.max_row = max_row
        self.canEdit = canEdit
        self.max_width = maxWidth
        self.set_button_option(optioncolor, optiontext)
        self.set_font()
        self.render()

    def update(self):
        super(TextButton, self).update()
        self.rect.x = (DISPLAY_WIDTH * self.column) // self.max_column - (self.image.get_width() // 2)
        self.rect.y = (DISPLAY_HEIGHT * self.row) // self.max_row

    def set_font(self):
        self.font = pg.font.Font(self.fontname, self.font_size)

    def set_button_option(self, optioncolor, optiontext):
        self.optioncolor = optioncolor
        self.optiontext = optiontext
        if self.optiontext == "True":
            self.optioncolor = LIGHT_SLATE_BLUE
        elif self.optiontext == "False":
            self.optioncolor = DARK_SLATE_BLUE

    def render(self):
        """Render the text onto the image."""
        self.txt_img = self.font.render(self.text, True, self.textcolor)
        self.opt_img = self.font.render(self.optiontext, True, self.optioncolor)
        self.val_img = self.font.render(self.valuetext, True, self.valuecolor)
        self.txt_rect = self.txt_img.get_rect()
        self.opt_rect = self.opt_img.get_rect()
        self.val_rect = self.val_img.get_rect()
        self.image = pg.transform.scale(self.image, (self.max_width, 32))
        self.BGimage = pg.transform.scale(self.BGimage, (self.max_width, 32))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.image.blit(self.txt_img,
                        ((self.image.get_width() // 2) - (self.txt_rect.width // 2),
                         self.txt_rect.height // 2))
        self.image.blit(self.opt_img, (5, self.opt_rect.height // 2))
        self.image.blit(self.val_img, (self.image.get_width() - (self.val_rect.width + 5), self.val_rect.height // 2))

    def update_button_text(self, text):
        self.text = str(text)
        self.image.fill(self.bgColor)
        self.render()
