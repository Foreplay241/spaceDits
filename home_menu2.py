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
        self.true_max_row = 24
        self.max_scale = 1.4
        self.min_scale = .4
        self.player_redilot = None
        self.player_shidpit = None
        self.enemy_redilot = None
        self.enemy_shidpit = None

        self.generate_redilot_button = TextButton(0, (0, 0), "blank",
                                                  text=f"Grab {self.num_of_posts} new posts", textcolor=SEA_GREEN,
                                                  optiontype=None, optioncolor=KHAKI,
                                                  col=1, max_col=2, row=1, max_row=self.true_max_row)
        self.save_redilot_dict_button = TextButton(1, (0, 0), "blank", text="Save Redilots", textcolor=SEA_GREEN,
                                                   optiontype=None, optioncolor=KHAKI,
                                                   col=1, max_col=3, row=20, max_row=self.true_max_row)
        self.save_shidpit_dict_button = TextButton(2, (0, 0), "blank", text="Save Shidpits", textcolor=SEA_GREEN,
                                                   optiontype=None, optioncolor=KHAKI,
                                                   col=2, max_col=3, row=20, max_row=self.true_max_row)
        self.start_game_button = TextButton(8, (0, 0), "blank", text="Start Game",
                                            textcolor=SEASHELL, optiontype=None, optioncolor=MEDIUM_PURPLE,
                                            col=1, max_col=2, row=22, max_row=self.true_max_row)

        for i in range(self.num_of_posts):
            scale = (8-self.num_of_posts)*.2
            if scale <= self.min_scale:
                scale = self.min_scale
            if scale >= self.max_scale:
                scale = self.max_scale
            redilot_slot_button = RedilotPreview(i, (0, 0), "click_here",
                                                 scale=(scale, scale),
                                                 col=1, max_col=3, row=4 + (i*(8-self.num_of_posts)),
                                                 max_row=self.true_max_row)
            self.redilot_slot_buttons.append(redilot_slot_button)
        for i in range(self.num_of_posts):
            shidpit_slot_button = ShidpitPreview(i, (0, 0), "click_here",
                                                 scale=(scale, scale),
                                                 col=2, max_col=3, row=4 + (i*(8-self.num_of_posts)),
                                                 max_row=self.true_max_row)
            self.shidpit_slot_buttons.append(shidpit_slot_button)

        self.all_text_buttons.append(self.generate_redilot_button)
        self.all_text_buttons.append(self.save_redilot_dict_button)
        self.all_text_buttons.append(self.save_shidpit_dict_button)
        self.all_text_buttons.append(self.start_game_button)
        self.all_buttons.append(self.all_text_buttons)
        self.all_buttons.append(self.redilot_slot_buttons)
        self.all_buttons.append(self.shidpit_slot_buttons)
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
            # CREATE THE MOUSE HOVER EFFECT
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
            for i in range(len(self.all_buttons)):
                for b in self.all_buttons[i]:
                    b.active = False
            for rsb in self.redilot_slot_buttons:
                if rsb.rect.collidepoint(self.mouse_pos):
                    for rsb2 in self.redilot_slot_buttons:
                        rsb2.selected = False
                    rsb.selected = True
            for ssb in self.shidpit_slot_buttons:
                if ssb.rect.collidepoint(self.mouse_pos):
                    for ssb2 in self.shidpit_slot_buttons:
                        ssb2.selected = False
                    ssb.selected = True

            if self.start_game_button.rect.collidepoint(self.mouse_pos):
                for rsb in self.redilot_slot_buttons:
                    if rsb.selected:
                        self.player_redilot = Redilot(name=rsb.redilot_name, from_reddit=True)
                for ssb in self.shidpit_slot_buttons:
                    if ssb.selected:
                        self.player_shidpit = Shidpit(sub_id=ssb.sub_id, from_reddit=True)

                self.enemy_redilot = Redilot(name=random.choice(redditor_list), from_reddit=True)
                self.enemy_shidpit = Shidpit(sub_id=random.choice(submission_list), from_reddit=True)
                self.persist = {
                    "Player Redilot": self.player_redilot,
                    "Player Ship": self.player_shidpit,
                    "Enemy Redilot": self.enemy_redilot,
                    "Enemy Ship": self.enemy_shidpit
                }
                self.next_state_name = "DOG_FIGHT"
                self.done = True

            if self.save_shidpit_dict_button.rect.collidepoint(self.mouse_pos):
                # self.save_shidpit_dict_button.active = True
                pass

            if self.save_redilot_dict_button.rect.collidepoint(self.mouse_pos):
                # self.save_redilot_dict_button.active = True
                pass

            if self.generate_redilot_button.rect.collidepoint(self.mouse_pos):
                self.collect_hot_reddit_posts(num_of_posts=self.num_of_posts, subreddit_name="all")
                self.update_shidpit_previews()
                self.update_redilot_previews()

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

    def collect_hot_reddit_posts(self, num_of_posts=5, subreddit_name="AskReddit"):
        subreddit = self.reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=num_of_posts):
            self.redilot_dict[submission.author.name] = Redilot(name=submission.author.name, from_reddit=True)
            self.shidpit_dict[submission.id] = Shidpit(sub_id=submission.id, from_reddit=True)

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
            self.shidpit_slot_buttons[s].sub_id = self.shidpit_dict[shidpit].submission_id
            s += 1

    def update_redilot_previews(self):
        r = 0
        for redilot in self.redilot_dict:
            self.redilot_slot_buttons[r].set_medal_img(self.redilot_dict[redilot].medal_img)
            self.redilot_slot_buttons[r].set_medal_info_img(self.redilot_dict[redilot].info_img)
            self.redilot_slot_buttons[r].redilot_name = self.redilot_dict[redilot].name
            r += 1

    def save_redilot_dict(self):
        for redilot in self.redilot_dict:
            print(self.redilot_dict[redilot])
            # with open('assets/pilots/' + str(self.redilot_dict[redilot].name) + '.json', 'w') as write_file:
        #         json.dump(self.redilot_dict[redilot].statistics, write_file, indent=4)
