from settings import *


class Text:
    """Create a text object."""
    fontname = None
    fontsize = 36
    fontcolor = BLANCHED_ALMOND
    background = None
    italic = False
    bold = False
    underline = False

    def __init__(self, text, pos, color=BLACK, size=36):
        super().__init__()
        self.text = text
        self.pos = pos
        self.font_color = color
        self.font = None
        self.img = None
        self.rect = None
        self.fontname = None
        self.font_size = size
        self.set_font()
        self.render()

    def set_font(self):
        """Set the Font object from name and size."""
        self.font = pg.font.Font(self.fontname, self.font_size)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.font_color)
        self.rect = self.img.get_rect()
        self.rect.center = self.pos

    def draw(self, window):
        """Draw the text image to the screen."""
        window.blit(self.img, self.rect)
