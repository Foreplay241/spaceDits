from dataclasses import dataclass

from GUI.text import Text
from settings import *
import pygame as pg
import praw
import os


@dataclass
class Fusion:
    """
    A fusion is a combination of a Redditor, Subreddit, Submission, or Comment combined with a space object.
    """
    fusion_name: str
    id_str: str
    cake_day: int
    img_img: pg.Surface((128, 128))
    info_img: pg.Surface((128, 128))
    alpha_part_num: int
    beta_part_num: int
    gamma_part_num: int
    delta_part_num: int
    redbit_dict: {}
    redditor_dict: {}
    subreddit_dict: {}
    submission_dict: {}
    comment_dict: {}

    def __init__(self, redbit, spacebit, creation_time=1474200000, id_string="r4nd0m"):
        """        
        :param redbit: A bit from reddit. (Redditor, Subreddit, Submission, Comment)
        :param spacebit: A bit from space. (Alien, Ship, Asteroid, Galaxy)
        """
        self.redbit = redbit
        self.spacebit = spacebit
        self.fusion_name = "None"

        # REDBIT INFORMATION
        self.id_str = id_string
        self.cake_day = int(creation_time)
        self.redbit_dict = {}
        self.redditor_dict = {
            "Creation Date": self.cake_day,
            "ID": self.id_str,
            "Comment Karma": 0,
            "Link Karma": 0,
            "Comments List": [],
            "Submissions List": [],
        }

        self.subreddit_dict = {
            "Creation Date": self.cake_day,
            "ID": self.id_str,
            "Subscriber Count": 0,
        }

        self.submission_dict = {
            "Creation Date": self.cake_day,
            "ID": self.id_str,
            "Score": 0,
            "Number of Comments": 0,
            "Upvote Ratio": 0.0
        }

        self.comment_dict = {
            "Creation Date": self.cake_day,
            "ID": self.id_str,
            "Creator": "",
            "Comment Body": "",
            "Score": 0
        }

        # SPACEBIT INFORMATION
        self.img_img = pg.Surface((128, 128))
        self.info_img = pg.Surface((128, 128))
        self.img_img.set_colorkey(BLACK)
        self.info_img.set_colorkey(BLACK)
        sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        redditFusionAssetsPath = os.path.join(sourceFileDir, "assets")
        self.partPath = os.path.join(redditFusionAssetsPath, spacebit)

        self.alpha_part_num = 0
        self.beta_part_num = 0
        self.gamma_part_num = 0
        self.delta_part_num = 0

    def add_alpha_part(self, redbit=None):
        x = 0
        r, g, b = 0, 0, 0
        for c in map(int, str(self.cake_day)):
            if x == 9:
                r = c * 22
            if x == 8:
                g = c * 22
            if x == 7:
                b = c * 22
            if x == 6:
                self.alpha_part_num = c
            x += 1
        # print(os.path.join(self.partPath, f"alpha{self.alpha_part_num}.png"))
        alpha_image = pg.image.load(os.path.join(self.partPath, f"alpha{self.alpha_part_num}.png")).convert_alpha()
        alpha_color = pg.Surface((128, 128))
        alpha_color.fill(pg.Color(r, g, b, 200))
        alpha_image.blit(alpha_color, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        return alpha_image

    def add_beta_part(self, redbit=None):
        x = 0
        r, g, b = 0, 0, 0
        for c in map(int, str(self.cake_day)):
            if x == 6:
                r = c * 22
            if x == 8:
                g = c * 22
            if x == 7:
                self.beta_part_num = c
            if x == 9:
                b = c * 22
            x += 1
        beta_image = pg.image.load(os.path.join(self.partPath, f"beta{self.beta_part_num}.png")).convert_alpha()
        beta_color = pg.Surface((128, 128))
        # print(r, g, b)
        beta_color.fill(pg.Color(r, g, b))
        beta_image.blit(beta_color, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        return beta_image

    def add_gamma_part(self, redbit=None):
        x = 0
        r, g, b = 0, 0, 0
        for c in map(int, str(self.cake_day)):
            if x == 9:
                r = c * 22
            if x == 6:
                g = c * 22
            if x == 7:
                b = c * 22
            if x == 8:
                self.gamma_part_num = c
            x += 1
        gamma_image = pg.image.load(os.path.join(self.partPath, f"gamma{self.gamma_part_num}.png")).convert_alpha()
        gamma_color = pg.Surface((128, 128))
        gamma_color.fill(pg.Color(r, g, b))
        gamma_image.blit(gamma_color, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        return gamma_image

    def add_delta_part(self, redbit=None):
        x = 0
        r, g, b = 0, 0, 0
        for c in map(int, str(self.cake_day)):
            if x == 8:
                r = c * 22
            if x == 7:
                g = c * 22
            if x == 6:
                b = c * 22
            if x == 9:
                self.delta_part_num = c
            x += 1
        delta_image = pg.image.load(os.path.join(self.partPath, f"delta{self.delta_part_num}.png")).convert_alpha()
        delta_color = pg.Surface((128, 128))
        delta_color.fill(pg.Color(r, g, b))
        delta_image.blit(delta_color, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        return delta_image

    def generate_info_img(self, redbit=None):
        info_img = pg.Surface((128, 128))
        name_label = Text(str(self.fusion_name), (0, 0), GREY50, 20)
        id_label = Text(str(self.id_str), (0, 0), GREY50, 20)
        if redbit:
            name_label = Text(redbit.name, (0, 0), GREY50, 22)
            id_label = Text(redbit.id, (0, 0), GREY50, 22)

        labels_list = [name_label, id_label]
        y = 0
        for label in labels_list:
            info_img.blit(label.img, (0, y * 22))
            y += 1
        return info_img

    def generate_img_img(self):
        alpha_image = self.add_alpha_part()
        beta_image = self.add_beta_part()
        gamma_image = self.add_gamma_part()
        delta_image = self.add_delta_part()
        parts_list = [alpha_image, beta_image, gamma_image, delta_image]
        for part in parts_list:
            self.img_img.blit(part, (0, 0))
        return self.img_img
