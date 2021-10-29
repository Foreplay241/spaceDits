from settings import *
from GameStates.menu import Menu
from GUI.text import Text
from GUI.text_button import TextButton


class DeadMenu(Menu):
    def __init__(self):
        super(DeadMenu, self).__init__()
        self.dead_menu_label = Text("Dead menu for spaceDits",
                                    (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT * 3 // 22), DARK_SLATE_BLUE)
        self.player_label = Text("Player", (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT * 8 // 22), DARK_PURPLE)
        self.enemy_label = Text("Enemy", (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT * 9 // 22), DARK_PURPLE)
        self.home_menu_button = TextButton(0, (0, DISPLAY_HEIGHT * 13 // 22), "blank",
                                           text="Home Menu", textcolor=LIGHT_GOLDENROD_YELLOW,
                                           optioncolor=MEDIUM_PURPLE, optiontext="Menu",
                                           col=1, max_col=2, row=22, max_row=24)
        self.retry_button = TextButton(1, (0, DISPLAY_HEIGHT * 14 // 22),
                                       "blank", text="Retry", textcolor=LIGHT_GOLDENROD_YELLOW,
                                       optioncolor=GAINSBORO, optiontext="Game",
                                       col=1, max_col=2, row=23, max_row=24)

    def startup(self, persistent):
        self.persist = {
            "Player Redilot": persistent["Player"].redilot,
            "Enemy Redilot": persistent["Enemy"].redilot,
            "Player Ship": persistent["Player"].shidpit,
            "Enemy Ship": persistent["Enemy"].shidpit
        }
        self.player_label = Text(f'{persistent["Player"].redilot.name} is the {persistent["Player"].outcome}!!!',
                                 (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT * 8 // 22), DARK_BLUE)
        self.enemy_label = Text(f'{persistent["Enemy"].redilot.name} is the {persistent["Enemy"].outcome}!',
                                (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT * 9 // 22), DARK_RED)

    def get_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.retry_button.rect.collidepoint(self.mouse_pos):
                self.persist = {
                    "Player Redilot": self.persist["Player Redilot"],
                    "Enemy Redilot": self.persist["Enemy Redilot"],
                    "Player Ship": self.persist["Player Ship"],
                    "Enemy Ship": self.persist["Enemy Ship"]
                }
                self.next_state_name = "DOG_FIGHT"
                self.done = True
            if self.home_menu_button.rect.collidepoint(self.mouse_pos):
                self.persist = {
                    "Player Redilot": self.persist["Player Redilot"],
                    "Enemy Redilot": self.persist["Enemy Redilot"],
                    "Player Ship": self.persist["Player Ship"],
                    "Enemy Ship": self.persist["Enemy Ship"]
                }
                self.next_state_name = "HOME_MENU"
                self.done = True

    def update(self, dt):
        self.retry_button.update()
        self.home_menu_button.update()

    def draw(self, screen):
        screen.fill(DARK_OLIVE_GREEN)
        self.dead_menu_label.draw(screen)
        self.player_label.draw(screen)
        self.enemy_label.draw(screen)
        self.home_menu_button.draw(screen)
        self.retry_button.draw(screen)
        pg.display.flip()
