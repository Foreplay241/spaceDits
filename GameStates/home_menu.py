from GUI.button import Button
from settings import *
from GameStates.menu import Menu
# from button import Button
from GUI.text_button import TextButton
from GUI.text import Text
from GUI.fusion_preview import FusionPreview
from RedditFusions.create_shidpit import Shidpit
from RedditFusions.create_redilot import Redilot
import json


class HomeMenu(Menu):
    def __init__(self):
        super(HomeMenu, self).__init__()
        self.third_pilot_img = None
        self.second_pilot_img = None
        self.first_pilot_img = None
        self.redilot_dict = {}
        self.shidpit_dict = {}
        self.pilots_path = os.path.join("assets", "pilots")
        self.all_pilots = [os.path.join(self.pilots_path, f) for f in os.listdir(self.pilots_path) if
                           f.endswith("_pilot.jpeg")]

        self.selected_redditor_name = ""
        self.player_redilot = None

        self.all_buttons = []
        self.text_buttons = []
        self.choice_buttons = []
        self.pilot_buttons = []
        self.max_row = 22

        # INITIALIZE THE HOME MENU BUTTONS AND ADD TO APPROPRIATE LISTS
        self.player_redilot_name_button = TextButton("H0", (0, 0), (0, 0), (0, 0), text=random.choice(redditor_list),
                                                     textcolor=WHITE_SMOKE, bgColor=SPACE_GREY,
                                                     optiontext="Redditor", optioncolor=LIGHT_SLATE_BLUE, fontsize=22,
                                                     col=1, max_col=2, row=2, max_row=self.max_row, canEdit=True,
                                                     maxWidth=420)
        self.gather_player_redditor = TextButton("H1", (0, 0), (1, 1), "frame", text="Gather Redditor Info",
                                                 textcolor=WHITE_SMOKE, bgColor=SPACE_GREY,
                                                 optiontext=None, fontsize=18,
                                                 col=1, max_col=2, row=3, max_row=self.max_row,
                                                 maxWidth=210)
        self.player_redilot_preview = FusionPreview("H2", (0, 0), "fusionBG", "fusionFG",
                                                    col=1, max_col=2, row=5, max_row=self.max_row)

        self.first_redilot_preview = FusionPreview("H3", (0, 0), "fusionBG", "fusionFG",
                                                   col=1, max_col=4, row=9, max_row=self.max_row)
        self.second_redilot_preview = FusionPreview("H4", (0, 0), "fusionBG", "fusionFG",
                                                    col=2, max_col=4, row=9, max_row=self.max_row)
        self.third_redilot_preview = FusionPreview("H5", (0, 0), "fusionBG", "fusionFG",
                                                   col=3, max_col=4, row=9, max_row=self.max_row)
        self.first_redilot_preview.fusion = "Redilot"
        self.second_redilot_preview.fusion = "Redilot"
        self.third_redilot_preview.fusion = "Redilot"

        self.choose_miner_ship_button = TextButton("H6", (0, 0), (20, 10), "frame", text="Miner Ship",
                                                   textcolor=ANTIQUE_WHITE, bgColor=SPACE_GREY,
                                                   col=1, max_col=4, row=20, max_row=self.max_row, maxWidth=110)
        self.choose_fighter_ship_button = TextButton("H7", (0, 0), "blank", (10, 30), text="Fighter Ship",
                                                     textcolor=ANTIQUE_WHITE, bgColor=SPACE_GREY,
                                                     col=2, max_col=4, row=20, max_row=self.max_row, maxWidth=110)
        self.choose_racing_ship_button = TextButton("H8", (0, 0), "blank", (1, 1), text="Racer Ship",
                                                    textcolor=ANTIQUE_WHITE, bgColor=SPACE_GREY,
                                                    col=3, max_col=4, row=20, max_row=self.max_row, maxWidth=110)

        self.choice_buttons.append(self.choose_miner_ship_button)
        self.choice_buttons.append(self.choose_fighter_ship_button)
        self.choice_buttons.append(self.choose_racing_ship_button)

        self.text_buttons.append(self.player_redilot_name_button)
        self.text_buttons.append(self.gather_player_redditor)

        self.pilot_buttons.append(self.player_redilot_preview)
        self.pilot_buttons.append(self.first_redilot_preview)
        self.pilot_buttons.append(self.second_redilot_preview)
        self.pilot_buttons.append(self.third_redilot_preview)

        self.all_buttons.append(self.player_redilot_name_button)
        self.all_buttons.append(self.gather_player_redditor)
        self.all_buttons.append(self.player_redilot_preview)
        self.all_buttons.append(self.first_redilot_preview)
        self.all_buttons.append(self.second_redilot_preview)
        self.all_buttons.append(self.third_redilot_preview)
        self.all_buttons.append(self.choose_miner_ship_button)
        self.all_buttons.append(self.choose_fighter_ship_button)
        self.all_buttons.append(self.choose_racing_ship_button)
        self.screen = pg.display.set_mode(DISPLAY_SIZE)
        self.clock = pg.time.Clock()
        self.is_active = True

    def startup(self, persistent):
        pilot_list = []
        for pilot_path in self.all_pilots:
            redilot_time = pilot_path.split("_")[0][14:24]
            redilot_id = pilot_path.split("_")[1]
            newRedilot = Redilot(creation_time=redilot_time, id_string=redilot_id)
            newRedilot.medal_img = newRedilot.generate_img_img()
            pilot_list.append(newRedilot)
            self.redilot_dict[redilot_id] = newRedilot
        self.first_redilot_preview.update_image(newBGimg=pg.Surface((128, 128)), newFGimg=pilot_list[0].medal_img)
        self.second_redilot_preview.update_image(newBGimg=pg.Surface((128, 128)), newFGimg=pilot_list[1].medal_img)
        self.third_redilot_preview.update_image(newBGimg=pg.Surface((128, 128)), newFGimg=pilot_list[2].medal_img)

    def get_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEMOTION:
            self.mouse_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            for ab in self.all_buttons:
                ab.active = False
                if ab.rect.collidepoint(self.mouse_pos):
                    ab.active = True
            for pb in self.pilot_buttons:
                pb.selected = False
                if pb.rect.collidepoint(self.mouse_pos):
                    pb.selected = True
                    self.player_redilot = Redilot()
            for cb in self.choice_buttons:
                # DETERMINE WHICH SHIP WAS CHOSEN
                if cb.rect.collidepoint(self.mouse_pos):
                    if self.player_redilot:
                        self.persist = {
                            "Player Redilot": self.player_redilot,
                            "Ship Type": cb.text
                        }
                        self.next_state_name = "HOME_MENU2"
                        self.done = True

            # TYPE THE NAME OF THE REDDITOR TO GATHER INFORMATION
            if self.player_redilot_name_button.rect.collidepoint(self.mouse_pos):
                self.player_redilot_name_button.update_button_text("")

            # GATHER INFORMATION FROM THE REDDITOR NAME.
            if self.gather_player_redditor.rect.collidepoint(self.mouse_pos):
                if self.player_redilot_name_button.text != "Type a redditor name":
                    if self.player_redilot_name_button.text != "":
                        self.selected_redditor_name = self.player_redilot_name_button.text
                        self.player_redilot = Redilot(name=self.selected_redditor_name)
                        self.player_redilot_preview.update_image(self.player_redilot.medal_img,
                                                                 pg.Surface((0, 0)))
                        self.player_redilot_preview.fusion = self.player_redilot
                        self.display_player_redilot_stats()

            if self.first_redilot_preview.rect.collidepoint(self.mouse_pos):
                self.display_player_redilot_stats()

            if self.second_redilot_preview.rect.collidepoint(self.mouse_pos):
                self.display_player_redilot_stats()

            if self.third_redilot_preview.rect.collidepoint(self.mouse_pos):
                self.display_player_redilot_stats()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
            for atb in self.text_buttons:
                if atb.active:
                    if event.key == pg.K_BACKSPACE:
                        if len(atb.text) > 0:
                            atb.text = atb.text[:-1]
                            atb.update_button_text(atb.text)
                    else:
                        atb.text += event.unicode
                        atb.update_button_text(atb.text)

    def update(self, dt):
        super(HomeMenu, self).update(dt)
        for ab in self.all_buttons:
            ab.update()

    def draw(self, screen):
        super(HomeMenu, self).draw(screen)
        screen.blit(self.background_image, (self.BGx, 0))
        for ab in self.all_buttons:
            ab.draw(screen)
        pg.display.flip()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def display_player_redilot_stats(self):
        c = 1
        r = 14
        if self.player_redilot:
            for key in self.player_redilot.save_data_dict:
                if key.endswith("Dictionary"):
                    dictbtn = TextButton(0, (0, 0), (1, 1), "frame", text=key.split(" ")[0], textcolor=GHOST_WHITE,
                                         col=c, max_col=5, row=14, max_row=self.max_row,
                                         maxWidth=120)
                    self.all_buttons.append(dictbtn)
                    self.text_buttons.append(dictbtn)
                    r2 = 1
                    for key2 in self.player_redilot.save_data_dict[key]:
                        txtbtn = TextButton(0, (0, 0), (1, 1), "frame", text="",
                                            valuetext=str(self.player_redilot.save_data_dict[key][key2]),
                                            valuecolor=NAVAJO_WHITE,
                                            optiontext=key2, optioncolor=NAVAJO_WHITE,
                                            col=c, max_col=5, row=r + r2, max_row=self.max_row,
                                            maxWidth=120)
                        self.all_buttons.append(txtbtn)
                        self.text_buttons.append(txtbtn)
                        r2 += 1
                    c += 1

    def collect_top_submission_from_redditor(self, num_submission):
        if self.player_redilot:
            self.player_redilot.submissions.top(limit=num_submission)
