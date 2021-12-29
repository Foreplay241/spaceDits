from GameStates.menu import Menu
from settings import *
from GUI.text import Text
from GUI.text_button import TextButton


class PauseMenu(Menu):
    def __init__(self):
        super(PauseMenu, self).__init__()
        self.pause_menu_label = Text("Pause menu for spaceDits",
                                     (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT * 3 // 22), DARK_SLATE_BLUE)
        self.all_buttons = []

        self.return_to_home_menu = TextButton(3, DISPLAY_CENTER, "blank", "frame",
                                              text="Home Menu", textcolor=LIGHT_PINK,
                                              optiontext="Game", optioncolor=RANDOM_GREEN,
                                              fontsize=16, col=1, max_col=2, row=13, max_row=22)
        self.return_to_game_button = TextButton(0, DISPLAY_CENTER, "blank", "frame",
                                                text="Return to Game", textcolor=LIGHT_PINK,
                                                optiontext="Game", optioncolor=RANDOM_GREEN,
                                                fontsize=16, col=1, max_col=2, row=14, max_row=22)

        self.paused_player = None
        self.paused_game_type = None
        self.all_buttons.append(self.return_to_game_button)
        self.all_buttons.append(self.return_to_home_menu)

    def startup(self, persistent):
        self.paused_player = persistent["Player"]
        self.paused_game_type = persistent["Game Type"]

    def get_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            for b in self.all_buttons:
                if b.optiontext != "Game":
                    b.active = False
                    if b.rect.collidepoint(self.mouse_pos):
                        b.active = True
                    b.set_button_option(DARK_BLUE, str(b.active))
                    b.render()
            if self.return_to_home_menu.rect.collidepoint(self.mouse_pos):
                self.persist = {}
                self.paused_player.hull_points = 0
                self.next_state_name = "HOME_MENU"
                self.done = True

            if self.return_to_game_button.rect.collidepoint(self.mouse_pos):
                self.persist = {
                    "Player": self.paused_player,
                    "Game Type": self.paused_game_type,
                    "Num of Comments": 0
                }
                self.next_state_name = self.paused_game_type
                self.done = True
        if event.type == pg.KEYDOWN:
            for b in self.all_buttons:
                if b.active:
                    if b.canEdit:
                        if event.key == pg.K_BACKSPACE:
                            if len(b.text) > 0:
                                b.text = b.text[:-1]
                                b.update_button_text(b.text)
                        else:
                            b.text += event.unicode
                            b.update_button_text(b.text)
            if event.key == pg.K_ESCAPE:
                pg.quit()
            if event.key == pg.K_p:
                self.persist = {
                    "Player": self.paused_player,
                    "Game Type": self.paused_game_type,
                    "Num of Comments": 0
                }
                self.next_state_name = self.paused_game_type
                self.done = True

    def update(self, dt):
        super(PauseMenu, self).update(dt)
        for b in self.all_buttons:
            b.update()

    def draw(self, screen):
        screen.fill(DARK_RED)
        for b in self.all_buttons:
            b.draw(screen)

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
