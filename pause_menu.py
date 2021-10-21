from button import Button
from menu import Menu
import pygame as pg
from settings import *
from text import Text
from text_button import TextButton


class PauseMenu(Menu):
    def __init__(self):
        super(PauseMenu, self).__init__()
        self.dead_menu_label = Text("Dead menu for spaceDits",
                                    (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT * 3 // 22), DARK_SLATE_BLUE)
        self.all_buttons = []
        self.return_to_game_button = TextButton(0, DISPLAY_CENTER, "blank", text="Return to Game", textcolor=LIGHT_PINK,
                                                optiontype="Game", optioncolor=RANDOM_GREEN,
                                                fontsize=16, col=1, max_col=2, row=16, max_row=22)

        self.text_edit_button = TextButton(1, DISPLAY_CENTER, "blank", text="Change my Text", textcolor=LIGHT_PINK,
                                           optiontype="False", optioncolor=RANDOM_GREEN,
                                           fontsize=16, col=1, max_col=2, row=13, max_row=22)

        self.text_edit_button_2 = TextButton(2, DISPLAY_CENTER, "blank", text="Change my Text 2", textcolor=LIGHT_PINK,
                                             optiontype="False", optioncolor=RANDOM_GREEN,
                                             fontsize=16, col=1, max_col=2, row=14, max_row=22, canEdit=True)

        self.text_edit_button_3 = TextButton(3, DISPLAY_CENTER, "blank", text="Change my Text 3", textcolor=LIGHT_PINK,
                                             optiontype="False", optioncolor=RANDOM_GREEN,
                                             fontsize=16, col=1, max_col=2, row=15, max_row=22, canEdit=True)
        self.paused_player = None
        self.paused_enemy = None
        self.all_buttons.append(self.return_to_game_button)
        self.all_buttons.append(self.text_edit_button)
        self.all_buttons.append(self.text_edit_button_2)
        self.all_buttons.append(self.text_edit_button_3)

    def startup(self, persistent):
        self.paused_player = persistent["Player"]
        self.paused_enemy = persistent["Enemy"]

    def get_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            for b in self.all_buttons:
                if b.optiontype != "Game":
                    b.active = False
                    if b.rect.collidepoint(self.mouse_pos):
                        b.active = True
                    b.set_button_option(DARK_BLUE, str(b.active))
                    b.render()
                print(b.text + str(b.active))
            if self.return_to_game_button.rect.collidepoint(self.mouse_pos):
                self.persist = {
                    "Player": self.paused_player,
                    "Enemy": self.paused_enemy
                }
                self.next_state_name = "DOG_FIGHT"
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
                    "Enemy": self.paused_enemy
                }
                self.next_state_name = "DOG_FIGHT"
                self.done = True


    def update(self, dt):
        super(PauseMenu, self).update(dt)
        for b in self.all_buttons:
            b.update()
        # self.return_to_game_button.update()
        # self.text_edit_button.update()
        # self.text_edit_button_2.update()

    def draw(self, screen):
        screen.fill(FIREBRICK)
        for b in self.all_buttons:
            b.draw(screen)
        # self.return_to_game_button.draw(screen)
        # self.text_edit_button.draw(screen)
        # self.text_edit_button_2.draw(screen)
        # pg.display.flip()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
