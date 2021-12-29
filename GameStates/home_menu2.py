import praw

from GUI.fusion_preview import FusionPreview
# from GUI.text import Text
from GUI.text import Text
from GameStates.menu import Menu
# from GUI.redilot_preview import RedilotPreview
from settings import *
# from GUI.shidpit_preview import ShidpitPreview
from GUI.text_button import TextButton
# from RedditFusions.create_redilot import Redilot
from RedditFusions.create_shidpit import Shidpit


class HomeMenu2(Menu):
    def __init__(self):
        super(HomeMenu2, self).__init__()
        self.all_buttons = []
        self.shidpit_preview_buttons = []
        self.text_buttons = []
        self.shidpit_dict = {}
        self.num_of_posts = 4
        self.nop = self.num_of_posts
        self.true_max_row = 24
        self.max_preview_scale = 1.4
        self.min_preview_scale = .4
        self.selected_shidpit_sub_id = None
        self.player_redilot = None
        self.player_shidpit = None
        self.ships_path = os.path.join("assets", "ships")
        self.ship_path_strings = [os.path.join(self.ships_path, f) for f in os.listdir(self.ships_path) if
                                  f.endswith("_ship.jpeg")]

        self.title_label = Text("", (DISPLAY_WIDTH // 2, 50), FLORAL_WHITE, 42)
        self.go_back_button = TextButton("H20", (0, 0), (1, 1), "frame", text="Choose different Redilot.",
                                         textcolor=FLORAL_WHITE,
                                         col=1, max_col=3, row=22, max_row=self.true_max_row)

        self.start_game_button = TextButton("H21", (0, 0), (1, 1), "frame", text="Start Game", textcolor=FLORAL_WHITE,
                                            col=2, max_col=3, row=22, max_row=self.true_max_row)

        self.collect_top_posts_button = TextButton("H22", (0, 0), (1, 1), "frame",
                                                   text=f"Collect top {self.num_of_posts} posts",
                                                   textcolor=FLORAL_WHITE, maxWidth=200,
                                                   col=1, max_col=4, row=20, max_row=self.true_max_row)
        self.collect_hot_posts_button = TextButton("H23", (0, 0), (1, 1), "frame",
                                                   text=f"Collect {self.num_of_posts} hot posts",
                                                   textcolor=FLORAL_WHITE, maxWidth=200,
                                                   col=2, max_col=4, row=19, max_row=self.true_max_row)
        self.collect_new_posts_button = TextButton("H24", (0, 0), (1, 1), "frame",
                                                   text=f"Collect {self.num_of_posts} new posts",
                                                   textcolor=FLORAL_WHITE, maxWidth=200,
                                                   col=3, max_col=4, row=20, max_row=self.true_max_row)
        for r in range(3):
            for c in range(4):
                if self.nop >= 1:
                    shidpit_button = FusionPreview(f"NoP{self.nop}", (0, 0), "fusionBG", "fusionFG",
                                                   col=c + 1, max_col=5, row=(r + 1) * 4,
                                                   max_row=self.true_max_row)
                    self.shidpit_preview_buttons.append(shidpit_button)
                    self.nop -= 1

        self.text_buttons.append(self.go_back_button)
        self.text_buttons.append(self.start_game_button)
        self.text_buttons.append(self.collect_top_posts_button)
        self.text_buttons.append(self.collect_hot_posts_button)
        self.text_buttons.append(self.collect_new_posts_button)
        self.all_buttons.append(self.text_buttons)
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
            st = persistent["Ship Type"].split(' ')[0]
            if st == "Miner":
                self.next_state_name = "MINING"
                self.title_label.text = "Miner ships"
                self.title_label.render()
            elif st == "Fighter":
                self.next_state_name = "FIGHTING"
                self.title_label.text = "Fighter ships"
                self.title_label.render()
            elif st == "Racer":
                self.next_state_name = "RACING"
                self.title_label.text = "Racing ships"
                self.title_label.render()

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
                    if b.rect.collidepoint(self.mouse_pos):
                        b.active = True
            # CLICKING ON A SHIDPIT PREVIEW WILL SELECT ONLY THAT SHIDPIT.
            for spb in self.shidpit_preview_buttons:
                if spb.rect.collidepoint(self.mouse_pos):
                    for spb2 in self.shidpit_preview_buttons:
                        spb2.selected = False
                    spb.selected = True
                    self.display_shidpit_stats(spb.fusion)

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
                for spb in self.shidpit_preview_buttons:
                    if spb.fusion and spb.selected:
                        self.set_player_shidpit()
                        self.persist = {
                            "Player Redilot": self.player_redilot,
                            "Player Shidpit": self.player_shidpit,
                            "Game Type": self.next_state_name,
                            "Num of Comments": 10
                        }
                        self.done = True

    def update(self, dt):
        super(HomeMenu2, self).update(dt)
        for spb in self.shidpit_preview_buttons:
            spb.update()
        for tb in self.text_buttons:
            tb.update()

    def draw(self, screen):
        screen.blit(self.background_image, (self.BGx, 0))
        for spb in self.shidpit_preview_buttons:
            spb.draw(screen)
        for tb in self.text_buttons:
            tb.draw(screen)
        self.title_label.draw(screen)
        pg.display.flip()

    def display_shidpit_stats(self, selected_shidpit=None):
        c = 1
        r = 11
        if selected_shidpit:
            for key in selected_shidpit.statistics:
                if key.endswith("Dictionary"):
                    dictbtn = TextButton(0, (0, 0), (1, 1), "frame", text=key.split(" ")[0], textcolor=GHOST_WHITE,
                                         col=c, max_col=5, row=11, max_row=24,
                                         maxWidth=120)
                    self.text_buttons.append(dictbtn)
                    r2 = 1
                    for key2 in selected_shidpit.statistics[key]:
                        txtbtn = TextButton(0, (0, 0), (1, 1), "frame", text="",
                                            valuetext=str(selected_shidpit.statistics[key][key2]),
                                            valuecolor=NAVAJO_WHITE,
                                            optiontext=key2, optioncolor=NAVAJO_WHITE,
                                            col=c, max_col=5, row=r + r2, max_row=24,
                                            maxWidth=120)
                        self.text_buttons.append(txtbtn)
                        r2 += 1
                    c += 1

    def set_player_shidpit(self):
        for spb in self.shidpit_preview_buttons:
            if spb.selected:
                self.player_shidpit = self.shidpit_dict[spb.submission_id]

    def collect_redilot_top_posts(self, num_of_posts):
        # for submission in self.player_redilot.redditor.submissions.top(limit=num_of_posts):
        #     self.shidpit_dict[submission.id] = Shidpit(sub_id=submission.id, from_reddit=True)
        pass

    def collect_redilot_hot_posts(self, num_of_posts):
        x = num_of_posts
        for ship_path in self.ship_path_strings:
            shidpit_time = ship_path.split("_")[0][13:-1]
            shidpit_id = ship_path.split("_")[1]
            newShidpit = Shidpit(creation_time=shidpit_time, id_string=shidpit_id)
            newShidpit.ship_img = newShidpit.generate_img_img()
            # newShidpit.ship_img = ship_img
            self.shidpit_dict[shidpit_id] = newShidpit
            x -= 1
        # self.update_shidpit_previews()

    def collect_redilot_new_posts(self, num_of_posts):
        # for submission in self.player_redilot.redditor.submissions.new(limit=num_of_posts):
        #     self.shidpit_dict[submission.id] = Shidpit(sub_id=submission.id, from_reddit=True)
        pass

    def update_shidpit_previews(self):
        s = 0
        for shidpit in self.shidpit_dict:
            self.shidpit_dict[shidpit].type = self.next_state_name
            self.shidpit_preview_buttons[s].set_img(self.shidpit_dict[shidpit].ship_img)
            self.shidpit_preview_buttons[s].set_info(self.shidpit_dict[shidpit].generate_info_img())
            self.shidpit_preview_buttons[s].flip_to_img()
            self.shidpit_preview_buttons[s].submission_id = self.shidpit_dict[shidpit].submission_id
            self.shidpit_preview_buttons[s].fusion = self.shidpit_dict[shidpit]
            s += 1
