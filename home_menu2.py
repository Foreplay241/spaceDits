import json

import praw
from menu import Menu
from redilot_preview import RedilotPreview
from settings import *
from button import Button
from shidpit_preview import ShidpitPreview
from text_button import TextButton
from create_redilot import Redilot
from create_shidpit import Shidpit


class HomeMenu2(Menu):
    def __init__(self):
        super(HomeMenu2, self).__init__()
        self.redilot_dict = {}
        self.shidpit_dict = {}
        self.all_buttons = []
        self.redilot_slot_buttons = []
        self.shidpit_slot_buttons = []
        self.all_text_buttons = []
        self.num_of_posts = 2
        self.generate_redilot_button = TextButton(0, (0, 0), "blank",
                                                  text=f"Grab {self.num_of_posts} new posts", textcolor=SEA_GREEN,
                                                  optiontype=None, optioncolor=KHAKI,
                                                  col=1, max_col=2, row=2, max_row=15)
        self.save_redilot_dict_button = TextButton(1, (0, 0), "blank", text="Save Redilots", textcolor=SEA_GREEN,
                                                   optiontype=None, optioncolor=KHAKI,
                                                   col=1, max_col=3, row=3, max_row=15)
        self.save_shidpit_dict_button = TextButton(2, (0, 0), "blank", text="Save Shidpits", textcolor=SEA_GREEN,
                                                   optiontype=None, optioncolor=KHAKI,
                                                   col=2, max_col=3, row=3, max_row=15)
        self.start_game_button = TextButton(8, (0, 0), "blank", text="Start Game",
                                            textcolor=SEASHELL, optiontype=None, optioncolor=MEDIUM_PURPLE,
                                            col=1, max_col=2, row=17, max_row=22)

        for i in range(self.num_of_posts):
            redilot_slot_button = RedilotPreview(i, (0, 0), "click_here",
                                                 col=1, max_col=3, row=4 + (i * 2.5), max_row=15)
            self.redilot_slot_buttons.append(redilot_slot_button)
        for i in range(self.num_of_posts):
            shidpit_slot_button = ShidpitPreview(i, (0, 0), "click_here",
                                                 col=2, max_col=3, row=4 + (i * 2.5), max_row=15)
            self.shidpit_slot_buttons.append(shidpit_slot_button)

        self.all_text_buttons.append(self.generate_redilot_button)
        self.all_text_buttons.append(self.save_redilot_dict_button)
        self.all_text_buttons.append(self.save_shidpit_dict_button)
        self.all_text_buttons.append(self.start_game_button)
        self.reddit = praw.Reddit(
            user_agent="(by u/Foreplay241)",
            client_id="kbIP5RKylq0_0AgP_9hFYg",
            client_secret="BU_jfFaK2lwHampEjJtoDzieWNxDyw",
            username="Camel_this_Chicken",
            password="1Fuckfuck!!"
        )

    def startup(self, persistent):
        pass

    def get_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = pg.mouse.get_pos()
            for rsb in self.redilot_slot_buttons:
                if rsb.rect.collidepoint(self.mouse_pos):
                    rsb.flip_to_info()
                else:
                    rsb.flip_to_img()
            for ssb in self.shidpit_slot_buttons:
                if ssb.rect.collidepoint(self.mouse_pos):
                    ssb.flip_to_info()
                else:
                    ssb.flip_to_img()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.start_game_button.rect.collidepoint(self.mouse_pos):
                pass

            if self.generate_redilot_button.rect.collidepoint(self.mouse_pos):
                self.collect_new_reddit_posts(num_of_posts=self.num_of_posts, subreddit_name="all")
                # self.update_shidpit_previews()
                # self.update_redilot_previews()
                pass

            # if self.save_redilot_dict_button.rect.collidepoint(self.mouse_pos):
            #     self.save_redilot_dict()

    def update(self, dt):
        super(HomeMenu2, self).update(dt)
        for rsb in self.redilot_slot_buttons:
            rsb.update()
        for ssb in self.shidpit_slot_buttons:
            ssb.update()
        for tb in self.all_text_buttons:
            tb.update()

    def draw(self, screen):
        screen.fill(DARK_BLUE)
        # player_draw_text(screen, "H2mEnu", LIGHT_WOOD, 36, DISPLAY_TOP_CENTER)
        for rsb in self.redilot_slot_buttons:
            rsb.draw(screen)
        for ssb in self.shidpit_slot_buttons:
            ssb.draw(screen)
        for tb in self.all_text_buttons:
            tb.draw(screen)
        pg.display.flip()

    def load_redilots(self):
        pass

    def load_shidpits(self):
        pass

    def collect_new_reddit_posts(self, num_of_posts=5, subreddit_name="AskReddit"):
        subreddit = self.reddit.subreddit(subreddit_name)
        for submission in subreddit.new(limit=num_of_posts):
            self.redilot_dict[submission.author.name] = Redilot(name=submission.author, from_reddit=True)
            self.shidpit_dict[submission.id] = Shidpit(sub_id=submission.id, from_reddit=True)

    def update_shidpit_previews(self):
        s = 0
        for shidpit in self.shidpit_dict:
            self.shidpit_slot_buttons[s].set_ship_img(self.shidpit_dict[shidpit].ship_img)
            self.shidpit_slot_buttons[s].set_ship_info_img(self.shidpit_dict[shidpit].info_img)
            s += 1

    def update_redilot_previews(self):
        r = 0
        for redilot in self.redilot_dict:
            self.redilot_slot_buttons[r].set_medal_img(self.redilot_dict[redilot].medal_img)
            self.redilot_slot_buttons[r].set_medal_info_img(self.redilot_dict[redilot].info_img)
            r += 1

    def save_redilot_dict(self):
        for redilot in self.redilot_dict:
            print(self.redilot_dict[redilot])
            # with open('assets/pilots/' + str(self.redilot_dict[redilot].name) + '.json', 'w') as write_file:
        #         json.dump(self.redilot_dict[redilot].statistics, write_file, indent=4)
