from button import Button
from settings import *
from menu import Menu
# from button import Button
from text_button import TextButton
from text import Text
from create_shidpit import Shidpit
from create_redilot import Redilot
import json


class HomeMenu(Menu):
    def __init__(self):
        super(HomeMenu, self).__init__()
        self.redilot_dict = {}
        self.shidpit_dict = {}
        self.home_menu_label = Text("Home Menu for spaceDits", (DISPLAY_WIDTH // 2, 64))
        # SETUP TEXT BUTTONS ON HOME MENU.
        self.save_redilot_button = TextButton((0, 0), "blank", text="Redilots",
                                              textcolor=VERY_LIGHT_GREY, optiontype="Save", optioncolor=MEDIUM_WOOD,
                                              col=1, max_col=3, row=4, max_row=22)
        self.save_shidpit_button = TextButton((0, 0), "blank", text="Shidpits",
                                              textcolor=VERY_LIGHT_GREY, optiontype="Save", optioncolor=MEDIUM_WOOD,
                                              col=2, max_col=3, row=4, max_row=22)
        self.start_reddit_game_button = TextButton((0, 0), "blank", text="Start Game",
                                                   textcolor=SEASHELL, optiontype="Reddit", optioncolor=MEDIUM_PURPLE,
                                                   col=2, max_col=3, row=17, max_row=22)
        self.player_redilot_button = TextButton((0, 0), "blank", text="Player Redilot", canEdit=True,
                                                textcolor=PAPAYA_WHIP, optiontype="Redilot",
                                                optioncolor=RANDOM_BLUE, col=1, max_col=3, row=11, max_row=22)
        self.enemy_redilot_button = TextButton((0, 0), "blank", text="Enemy Redilot", canEdit=True,
                                               textcolor=FLORAL_WHITE, optiontype="Redilot",
                                               optioncolor=RANDOM_RED, col=2, max_col=3, row=11, max_row=22)
        self.player_shidpit_button = TextButton((0, 0), "blank", text="Player ship", canEdit=True,
                                                textcolor=PAPAYA_WHIP, optiontype="Shidpit",
                                                optioncolor=RANDOM_BLUE, col=1, max_col=3, row=12, max_row=22)
        self.enemy_shidpit_button = TextButton((0, 0), "blank", text="Enemy ship", canEdit=True,
                                               textcolor=FLORAL_WHITE, optiontype="Shidpit",
                                               optioncolor=RANDOM_RED, col=2, max_col=3, row=12, max_row=22)
        self.start_random_game_button = TextButton((0, 0), "blank", text="Start Game",
                                                   textcolor=SEASHELL, optiontype="Random", optioncolor=RANDOM_GREEN,
                                                   col=1, max_col=3, row=17, max_row=22)
        self.start_reddit_game_button = TextButton((0, 0), "blank", text="Start Game",
                                                   textcolor=SEASHELL, optiontype="Reddit", optioncolor=MEDIUM_PURPLE,
                                                   col=2, max_col=3, row=17, max_row=22)
        # SETUP BUTTONS ON HOME MENU
        self.player_redilot_preview = Button((0, 0), "blank", col=1, max_col=3, row=8, max_row=22)
        self.enemy_redilot_preview = Button((0, 0), "blank", col=2, max_col=3, row=8, max_row=22)
        self.player_shidpit_preview = Button((0, 0), "blank", col=1, max_col=3, row=13, max_row=22)
        self.enemy_shidpit_preview = Button((0, 0), "blank", col=2, max_col=3, row=13, max_row=22)

        # PUT BUTTONS IN A LIST FOR EASY EXECUTION
        self.all_buttons = []
        self.all_text_buttons = []
        self.all_buttons.append(self.player_redilot_preview)
        self.all_buttons.append(self.enemy_redilot_preview)
        self.all_buttons.append(self.player_shidpit_preview)
        self.all_buttons.append(self.enemy_shidpit_preview)
        self.all_text_buttons.append(self.start_random_game_button)
        self.all_text_buttons.append(self.start_reddit_game_button)
        self.all_text_buttons.append(self.player_redilot_button)
        self.all_text_buttons.append(self.enemy_redilot_button)
        self.all_text_buttons.append(self.player_shidpit_button)
        self.all_text_buttons.append(self.enemy_shidpit_button)
        self.all_text_buttons.append(self.save_redilot_button)
        self.all_text_buttons.append(self.save_shidpit_button)
        self.all_buttons += self.all_text_buttons

        self.screen = pg.display.set_mode(DISPLAY_SIZE)
        self.clock = pg.time.Clock()
        self.is_active = True
        self.player_redilot = None
        self.player_ship = None
        self.enemy_redilot = None
        self.enemy_ship = None

    def startup(self, persistent):
        self.load_redilots()
        self.load_shidpits()

    def get_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            # CLICKED INSIDE SAVE REDILOTS.
            if self.save_redilot_button.rect.collidepoint(self.mouse_pos)\
                    and self.player_redilot_button.text != "Player Redilot"\
                    and self.enemy_redilot_button.text != "Enemy Redilot":
                self.player_redilot = Redilot(name=self.player_redilot_button.text, from_reddit=True)
                self.enemy_redilot = Redilot(name=self.enemy_redilot_button.text, from_reddit=True)
                self.redilot_dict[self.player_redilot.name] = [self.player_redilot.statistics]
                self.redilot_dict[self.enemy_redilot.name] = [self.enemy_redilot.statistics]
                self.save_redilots()

            # CLICKED INSIDE SAVE SHIDPITS.
            if self.save_shidpit_button.rect.collidepoint(self.mouse_pos)\
                    and self.player_shidpit_button.text != "Player ship"\
                    and self.enemy_shidpit_button.text != "Enemy ship":
                self.player_ship = Shidpit(sub_id=self.player_shidpit_button.text, from_reddit=True)
                self.enemy_ship = Shidpit(sub_id=self.enemy_shidpit_button.text, from_reddit=True)
                self.shidpit_dict[self.player_ship.sub_id] = self.player_ship.statistics
                self.shidpit_dict[self.enemy_ship.sub_id] = self.enemy_ship.statistics
                self.save_shidpits()

            # CLICKED INSIDE REDILOT PREVIEW.
            if self.player_redilot_preview.rect.collidepoint(self.mouse_pos):
                self.player_redilot_button.update_button_text(random.choice(redditor_list))
                self.player_redilot = Redilot(name=self.player_redilot_button.text)
                self.player_redilot_preview.update_image(self.player_redilot.medal_img)

            # CLICKED INSIDE ENEMY REDILOT PREVIEW.
            if self.enemy_redilot_preview.rect.collidepoint(self.mouse_pos):
                self.enemy_redilot_button.update_button_text(random.choice(redditor_list))
                self.enemy_redilot = Redilot(name=self.enemy_redilot_button.text)
                self.enemy_redilot_preview.update_image(self.enemy_redilot.generate_medal_image())

            # CLICKED INSIDE PLAYER SHIDPIT PREVIEW.
            if self.player_shidpit_preview.rect.collidepoint(self.mouse_pos):
                self.player_shidpit_button.update_button_text(random.choice(submission_list))
                self.player_ship = Shidpit(sub_id=self.player_shidpit_button.text)
                self.player_shidpit_preview.update_image(self.player_ship.img)

            # CLICKED INSIDE ENEMY SHIDPIT PREVIEW.
            if self.enemy_shidpit_preview.rect.collidepoint(self.mouse_pos):
                self.enemy_shidpit_button.update_button_text(random.choice(submission_list))
                self.enemy_ship = Shidpit(sub_id=self.enemy_shidpit_button.text)
                self.enemy_shidpit_preview.update_image(self.enemy_ship.img)

            # CLICKED INSIDE PLAYER REDILOT BUTTONS.
            if self.player_redilot_button.rect.collidepoint(self.mouse_pos):
                self.player_redilot_button.update_button_text("")
                for b in self.all_text_buttons:
                    b.active = False
                self.player_redilot_button.active = True

            # CLICKED INSIDE ENEMY REDILOT BUTTONS.
            if self.enemy_redilot_button.rect.collidepoint(self.mouse_pos):
                self.enemy_redilot_button.update_button_text("")
                for b in self.all_text_buttons:
                    b.active = False
                self.enemy_redilot_button.active = True

            # CLICKED INSIDE PLAYER SHIPDIT BUTTON.
            if self.player_shidpit_button.rect.collidepoint(self.mouse_pos):
                self.player_shidpit_button.update_button_text("")
                for b in self.all_text_buttons:
                    b.active = False
                self.player_shidpit_button.active = True

            # CLICKED INSIDE ENEMY SHIDPIT BUTTON.
            if self.enemy_shidpit_button.rect.collidepoint(self.mouse_pos):
                self.enemy_shidpit_button.update_button_text("")
                for b in self.all_text_buttons:
                    b.active = False
                self.enemy_shidpit_button.active = True

            # START RANDOM GAME.
            if self.start_random_game_button.rect.collidepoint(self.mouse_pos):
                self.enemy_redilot = Redilot(name=self.enemy_redilot_button.text)
                self.player_ship = Shidpit()
                self.enemy_ship = Shidpit()
                self.persist = {
                    "Player Redilot": self.player_redilot,
                    "Player Ship": self.player_ship,
                    "Enemy Redilot": self.enemy_redilot,
                    "Enemy Ship": self.enemy_ship
                }
                self.next_state_name = "DOG_FIGHT"
                self.done = True

            # START REDDIT GAME.
            if self.start_reddit_game_button.rect.collidepoint(self.mouse_pos):
                self.player_redilot = Redilot(name=self.player_redilot_button.text, from_reddit=True)
                self.enemy_redilot = Redilot(name=self.enemy_redilot_button.text, from_reddit=True)
                self.player_ship = Shidpit(sub_id=self.player_shidpit_button.text, from_reddit=True)
                self.enemy_ship = Shidpit(sub_id=self.enemy_shidpit_button.text, from_reddit=True)
                self.persist = {
                    "Player Redilot": self.player_redilot,
                    "Player Ship": self.player_ship,
                    "Enemy Redilot": self.enemy_redilot,
                    "Enemy Ship": self.enemy_ship
                }
                self.next_state_name = "DOG_FIGHT"
                self.done = True
        if event.type == pg.KEYDOWN:
            for b in self.all_text_buttons:
                if b.active:
                    if event.key == pg.K_BACKSPACE:
                        if len(b.text) > 0:
                            b.text = b.text[:-1]
                            b.update_button_text(b.text)
                    if event.key == pg.K_RETURN:
                        pass
                    else:
                        b.text += event.unicode
                        b.update_button_text(b.text)

    def update(self, dt):
        super(HomeMenu, self).update(dt)
        for b in self.all_buttons:
            b.update()

    def draw(self, screen):
        screen.fill(FIREBRICK)
        for b in self.all_buttons:
            b.draw(screen)
        pg.display.flip()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def save_redilots(self):
        try:
            with open('assets/pilots/' + self.player_redilot.name + '.json', 'w') as write_file:
                json.dump(self.player_redilot.statistics, write_file, indent=3)
            with open('assets/pilots/' + self.enemy_redilot.name + '.json', 'w') as write_file:
                json.dump(self.enemy_redilot.statistics, write_file, indent=3)
            pg.image.save(self.player_redilot.medal_img, 'assets/pilots/' + self.player_redilot.name + '.png')
            pg.image.save(self.enemy_redilot.medal_img, 'assets/pilots/' + self.enemy_redilot.name + '.png')
            print("======== Saved Redilots ========")
        except:
            print("Sorry, couldn't load redilots.")

    def save_shidpits(self):
        try:
            with open('assets/ships/' + self.player_ship.sub_id + '.json', 'w') as write_file:
                json.dump(self.player_ship.statistics, write_file, indent=3)
            with open('assets/ships/' + self.enemy_ship.sub_id + '.json', 'w') as write_file:
                json.dump(self.enemy_ship.statistics, write_file, indent=3)
            pg.image.save(self.player_ship.img, 'assets/ships/' + self.player_ship.name + '.png')
            pg.image.save(self.enemy_ship.img, 'assets/ships/' + self.enemy_ship.name + '.png')
            print("======== Saved Shidpits ========")
        except:
            print("Sorry, couldn't load shidpits.")

    def load_redilots(self):
        try:
            with open('pilots.json', ) as load_file:
                self.redilot_dict = json.load(load_file)
            print("======== Loaded Redilots ========")
            for key in self.redilot_dict:
                print(key)
        except:
            print("Sorry, couldn't load redilots.")

    def load_shidpits(self):
        try:
            with open('ships.json', ) as load_file:
                self.shidpit_dict = json.load(load_file)
            print("======== Loaded Shidpits ========")
            for key in self.shidpit_dict:
                print(key)
        except:
            print("Sorry, couldn't load shidpits.")
