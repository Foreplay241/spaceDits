import praw

from GUI.fusion_preview import FusionPreview
from GUI.text import Text
from GameStates.menu import Menu
from GUI.redilot_preview import RedilotPreview
from settings import *
from GUI.shidpit_preview import ShidpitPreview
from GUI.text_button import TextButton
from RedditFusions.create_redilot import Redilot
from RedditFusions.create_shidpit import Shidpit


class HomeMenu2(Menu):
    def __init__(self):
        super(HomeMenu2, self).__init__()
        self.all_buttons = []
        self.shidpit_preview_buttons = []
        self.all_text_buttons = []
        self.shidpit_dict = {}
        self.num_of_posts = 4
        self.nop = self.num_of_posts
        self.true_max_row = 24
        self.max_preview_scale = 1.4
        self.min_preview_scale = .4
        self.selected_shidpit_sub_id = None
        self.player_redilot = None
        self.player_shidpit = None

        self.title_label = None
        self.go_back_button = TextButton(0, (0, 0), "blank", text="Choose different Redilot.", textcolor=FLORAL_WHITE,
                                         col=1, max_col=3, row=22, max_row=self.true_max_row)

        self.start_game_button = TextButton(0, (0, 0), "blank", text="Start Game", textcolor=FLORAL_WHITE,
                                            col=2, max_col=3, row=22, max_row=self.true_max_row)

        self.collect_top_posts_button = TextButton(0, (0, 0), "blank",
                                                   text=f"Collect top {self.num_of_posts}"
                                                        f" posts by {self.player_redilot}",
                                                   textcolor=FLORAL_WHITE, maxWidth=200,
                                                   col=1, max_col=4, row=20, max_row=self.true_max_row)
        self.collect_hot_posts_button = TextButton(0, (0, 0), "blank",
                                                   text=f"Collect hot {self.num_of_posts}"
                                                        f" post by {self.player_redilot}",
                                                   textcolor=FLORAL_WHITE, maxWidth=200,
                                                   col=2, max_col=4, row=19, max_row=self.true_max_row)
        self.collect_new_posts_button = TextButton(0, (0, 0), "blank",
                                                   text=f"Collect new {self.num_of_posts}"
                                                        f" post by {self.player_redilot}",
                                                   textcolor=FLORAL_WHITE, maxWidth=200,
                                                   col=3, max_col=4, row=20, max_row=self.true_max_row)
        for r in range(3):
            for c in range(4):
                if self.nop >= 1:
                    shidpit_button = FusionPreview(0, (0, 0), "click_here",
                                                   col=c + 1, max_col=5, row=(r + 1) * 4,
                                                   max_row=self.true_max_row)
                    self.shidpit_preview_buttons.append(shidpit_button)
                    self.nop -= 1
        self.all_text_buttons.append(self.go_back_button)
        self.all_text_buttons.append(self.start_game_button)
        self.all_text_buttons.append(self.collect_top_posts_button)
        self.all_text_buttons.append(self.collect_hot_posts_button)
        self.all_text_buttons.append(self.collect_new_posts_button)
        self.all_buttons.append(self.all_text_buttons)
        self.all_buttons.append(self.shidpit_preview_buttons)
        self.reddit = praw.Reddit(
            user_agent="(by u/Foreplay241)",
            client_id="kbIP5RKylq0_0AgP_9hFYg",
            client_secret="BU_jfFaK2lwHampEjJtoDzieWNxDyw",
            username="Camel_this_Chicken",
            password="1Fuckfuck!!"
        )

    def startup(self, persistent):
        if "Player Redilot" in persistent:
            self.player_redilot = persistent["Player Redilot"]
        if "Ship Type" in persistent:
            self.title_label = Text(persistent["Ship Type"], (40, 40), BLACK)

        self.collect_top_posts_button.update_button_text(f"Collect top {self.num_of_posts}"
                                                         f" post by {self.player_redilot.name}")
        self.collect_hot_posts_button.update_button_text(f"Collect hot {self.num_of_posts}"
                                                         f" post by {self.player_redilot.name}")
        self.collect_new_posts_button.update_button_text(f"Collect new {self.num_of_posts}"
                                                         f" post by {self.player_redilot.name}")

    def get_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = pg.mouse.get_pos()
            # CREATE THE MOUSE HOVER EFFECT
            for ssb in self.shidpit_preview_buttons:
                if ssb.rect.collidepoint(self.mouse_pos) and ssb.info:
                    ssb.flip_to_info()
                elif ssb.img:
                    ssb.flip_to_img()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()

        if event.type == pg.MOUSEBUTTONDOWN:
            # CLICKING ANYWHERE DEACTIVATES ALL BUTTONS
            for i in range(len(self.all_buttons)):
                for b in self.all_buttons[i]:
                    b.active = False
            # CLICKING ON A SHIDPIT PREVIEW WILL SELECT ONLY THAT SHIDPIT.
            for spb in self.shidpit_preview_buttons:
                if spb.rect.collidepoint(self.mouse_pos):
                    for spb2 in self.shidpit_preview_buttons:
                        spb2.selected = False
                    spb.selected = True

            # CHOOSE TOP POSTS TO FLY
            if self.collect_top_posts_button.rect.collidepoint(self.mouse_pos):
                self.shidpit_dict = {}
                self.collect_redilot_top_posts(self.num_of_posts)
                self.update_shidpit_previews()
            # CHOOSE HOT POSTS TO FLY
            if self.collect_hot_posts_button.rect.collidepoint(self.mouse_pos):
                self.shidpit_dict = {}
                self.collect_redilot_hot_posts(self.num_of_posts)
                self.update_shidpit_previews()
            # CHOOSE NEW POSTS TO FLY
            if self.collect_new_posts_button.rect.collidepoint(self.mouse_pos):
                self.shidpit_dict = {}
                self.collect_redilot_new_posts(self.num_of_posts)
                self.update_shidpit_previews()

            # GO BACK TO REDILOT SELECTION
            if self.go_back_button.rect.collidepoint(self.mouse_pos):
                self.next_state_name = "HOME_MENU"
                self.done = True

            # START A GAME WITH THE REDILOT AND SHIDPIT
            if self.start_game_button.rect.collidepoint(self.mouse_pos):
                self.set_player_shidpit()
                self.persist = {
                    "Player Redilot": self.player_redilot,
                    "Player Shidpit": self.player_shidpit,
                }
                self.next_state_name = "MINE ASTROIDING"

    def update(self, dt):
        super(HomeMenu2, self).update(dt)
        for spb in self.shidpit_preview_buttons:
            spb.update()
        for tb in self.all_text_buttons:
            tb.update()

    def draw(self, screen):
        screen.fill(DARK_BLUE)
        for spb in self.shidpit_preview_buttons:
            spb.draw(screen)
        for tb in self.all_text_buttons:
            tb.draw(screen)
        pg.display.flip()

    def set_player_shidpit(self):
        for ssb in self.shidpit_preview_buttons:
            if ssb.selected:
                self.player_shidpit = self.shidpit_dict[ssb.submission_id]

    def collect_redilot_top_posts(self, num_of_posts):
        for submission in self.player_redilot.redditor.submissions.top(limit=num_of_posts):
            self.shidpit_dict[submission.id] = Shidpit(sub_id=submission.id, from_reddit=True)

    def collect_redilot_hot_posts(self, num_of_posts):
        for submission in self.player_redilot.redditor.submissions.hot(limit=num_of_posts):
            self.shidpit_dict[submission.id] = Shidpit(sub_id=submission.id, from_reddit=True)

    def collect_redilot_new_posts(self, num_of_posts):
        for submission in self.player_redilot.redditor.submissions.new(limit=num_of_posts):
            self.shidpit_dict[submission.id] = Shidpit(sub_id=submission.id, from_reddit=True)

    def update_shidpit_previews(self):
        s = 0
        for shidpit in self.shidpit_dict:
            self.shidpit_preview_buttons[s].set_img(self.shidpit_dict[shidpit].generate_ship_img())
            self.shidpit_preview_buttons[s].set_info(self.shidpit_dict[shidpit].generate_info_img())
            self.shidpit_preview_buttons[s].flip_to_img()
            self.shidpit_preview_buttons[s].submission_id = self.shidpit_dict[shidpit].submission_id
            s += 1
