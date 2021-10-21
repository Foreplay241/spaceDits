from dataclasses import dataclass
from settings import *
import time
import pygame as pg
import random
import praw
import os

from text import Text

redditor_name_list = ["Foreplay241", "Big-mac_sauce", "Camel-of_Chicken", "Camel_this_Chicken",
                 "Camel_and_Chicken", "Camel_of_Chicken", "3MuchLikeLA", "ACC15ORD", "antianit",
                 "bot_neen", "BlurrZ8", "coby----", "atobitt", "Gena1548"]

MONTH_LIST = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

ZODIAC_DICT = {
    "Aquarius": ["Shield", "Extra Shields.", "Air", "Garnet", (1, 20), (2, 18)],
    "Pisces": ["Shield", "Jet stream.", "Water", "Amethyst", (2, 19), (3, 20)],
    "Aries": ["Health", "Ram Dash.", "Fire", "Bloodstone", (3, 21), (4, 19)],
    "Taurus": ["Health", "Stronger Hull.", "Earth", "Sapphire", (4, 20), (5, 20)],
    "Gemini": ["Shield", "Twin for a min.", "Air", "Agate", (5, 21), (6, 20)],
    "Cancer": ["Shield", "Tidal wave blast.", "Water", "Emerald", (6, 21), (7, 22)],
    "Leo": ["Health", "Sonic boom stun.", "Fire", "Onyx", (7, 23), (8, 22)],
    "Virgo": ["Health", "Life after Death.", "Earth", "Carnelian", (8, 23), (9, 22)],
    "Libra": ["Shield", "Set hull_points equal to shield.", "Air", "Chrysolite", (9, 23), (10, 22)],
    "Scorpio": ["Shield", "Medium Arrow angled.", "Water", "Beryl", (10, 23), (11, 21)],
    "Sagittarius": ["Health", "Giant Arrow.", "Fire", "Topaz", (11, 22), (12, 21)],
    "Capricorn": ["Health", "Drop Bombs.", "Earth", "Ruby", (12, 22), (1, 19)]
}


@dataclass
class Redilot:
    """A redilot is a redditor pilot for a shidpit from reddit."""
    name: str
    cake_day: int
    constellation: str
    pilot_rank: int
    square_num: int
    triangle_num: int
    circle_num: int
    lines_num: int
    max_hull_points: int
    max_shield_points: int
    medal_img: pg.Surface((128, 128))
    info_img: pg.Surface((128, 128))

    def __init__(self, name=random.choice(redditor_name_list), from_reddit=False, pilot_rank=1):
        self.cake_day = random.randint(1119553200, 1633120253)
        self.redditor = None
        self.name = name
        self.from_reddit = from_reddit
        self.pilot_rank = pilot_rank
        self.medal_img = pg.Surface((128, 128))
        self.info_img = pg.Surface((128, 128))
        self.set_constellation()
        if self.from_reddit:
            self.generate_from_reddit()
        else:
            self.generate_from_random()
        self.statistics = {
            "power": 0,
            "fire rate": 0,
            "maxCharge": 0,
            "hull points": 0,
            "shield points": 0,
        }

    def set_hull_points(self, redditor=None):
        self.max_hull_points = random.randint(42, 69)
        if redditor:
            x = 0
            self.max_hull_points = 0
            for c in map(int, str(int(redditor.created_utc))):
                self.max_hull_points += c
                x += 1

    def set_shield_points(self, redditor=None):
        self.max_shield_points = random.randint(42, 69)
        if redditor:
            x = 0
            self.max_shield_points = 0
            for c in map(int, str(int(redditor.created_utc))):
                self.max_hull_points += c
                x += 1

    def set_constellation(self, redditor=None):
        print("Name: " + str(self.name))
        print("Cake Day: " + str(MONTH_LIST[time.gmtime(self.cake_day).tm_mon - 1])
              + " " + str(time.gmtime(self.cake_day).tm_mday)
              + " " + str(time.gmtime(self.cake_day).tm_year))
        chosen_constellation = []
        for constellation in ZODIAC_DICT:
            start_month, start_day = ZODIAC_DICT[constellation][4]
            end_month, end_day = ZODIAC_DICT[constellation][5]
            if start_month == time.gmtime(self.cake_day).tm_mon:
                if time.gmtime(self.cake_day).tm_mday >= start_day:
                    chosen_constellation = constellation

            elif end_month == time.gmtime(self.cake_day).tm_mon:
                if time.gmtime(self.cake_day).tm_mday <= end_day:
                    chosen_constellation = constellation
        self.constellation = chosen_constellation

    def add_square_part(self, redditor=None):
        self.square_num = random.randint(0, 9)
        firePower = self.get_average_top_comment_score(num_of_posts=10)
        fireRate = 0
        maxCharge = self.get_sum_top_comment_score(num_of_comments=3)
        if redditor:
            x = 0
            for c in map(int, str(int(redditor.created_utc))):
                if x == 9:
                    self.square_num = c
                x += 1

    def add_triangle_part(self, redditor=None):
        self.triangle_num = random.randint(0, 9)
        if redditor:
            x = 0
            for c in map(int, str(int(redditor.created_utc))):
                if x == 8:
                    self.triangle_num = c
                x += 1

    def add_circle_part(self, redditor=None):
        self.circle_num = random.randint(0, 9)
        if redditor:
            x = 0
            for c in map(int, str(int(redditor.created_utc))):
                if x == 7:
                    self.circle_num = c
                x += 1

    def add_lines_part(self, redditor=None):
        self.lines_num = random.randint(0, 9)
        if redditor:
            x = 0
            for c in map(int, str(int(redditor.created_utc))):
                if x == 6:
                    self.lines_num = c
                x += 1

    def generate_info_image(self, redditor=None):
        info_img = pg.Surface((128, 128))
        name_label = Text(str(self.name), (0, 0), GREY50, 20)
        score_label = Text(str(self.circle_num), (0, 22), GREY50, 20)
        constellation_label = Text(str(self.triangle_num), (0, 22), GREY50, 20)
        if redditor:
            name_label = Text(redditor.name, (0, 0), GREY50, 22)
            score_label = Text(str(redditor.comment_karma), (0, 22), GREY50, 22)
            constellation_label = Text(str(self.constellation), (0, 22), GREY50, 20)

        labels_list = [name_label, score_label, constellation_label]
        y = 0
        for label in labels_list:
            info_img.blit(label.img, (0, y * 22))
            y += 1
        return info_img

    def generate_medal_image(self, redditor=None):
        # LAYERS THE LAYERS ON THE MEDAL IMAGE
        medal_img = pg.Surface((128, 128))
        square_image = pg.image.load(os.path.join("assets/medallion_parts", "square" + str(self.square_num) + ".png"))
        triangle_image = pg.image.load(os.path.join("assets/medallion_parts", "triangle"
                                                    + str(self.triangle_num) + ".png"))
        circle_image = pg.image.load(os.path.join("assets/medallion_parts", "circle" + str(self.circle_num) + ".png"))
        lines_image = pg.image.load(os.path.join("assets/medallion_parts", "lines" + str(self.lines_num) + ".png"))
        parts_list = [square_image, triangle_image, circle_image, lines_image]
        for part in parts_list:
            medal_img.blit(part, (0, 0))
        return medal_img

    def generate_from_reddit(self):
        reddit = praw.Reddit(
            user_agent="(by u/Foreplay241)",
            client_id="kbIP5RKylq0_0AgP_9hFYg",
            client_secret="BU_jfFaK2lwHampEjJtoDzieWNxDyw",
            username="Camel_this_Chicken",
            password="1Fuckfuck!!"
        )
        self.redditor = reddit.redditor(self.name)
        self.cake_day = self.redditor.created_utc
        self.set_hull_points(self.redditor)
        self.set_shield_points(self.redditor)
        self.add_square_part(self.redditor)
        self.add_triangle_part(self.redditor)
        self.add_circle_part(self.redditor)
        self.add_lines_part(self.redditor)
        self.medal_img = self.generate_medal_image(self.redditor)
        self.info_img = self.generate_info_image(self.redditor)

    def generate_from_random(self):
        # GENERATE A REDILOT FROM RANDOM INPUT.
        self.set_hull_points()
        self.set_shield_points()
        self.add_square_part()
        self.add_triangle_part()
        self.add_circle_part()
        self.add_lines_part()
        self.medal_img = self.generate_medal_image()
        self.info_img = self.generate_info_image()

    def get_average_top_comment_score(self, num_of_comments=5):
        total_comment_score = 0
        for c in self.redditor.comments.top(limit=num_of_comments):
            total_comment_score += c.score
        return total_comment_score // num_of_comments

    def get_sum_top_comment_score(self, num_of_comments=5):
        total_comment_score = 0
        for c in self.redditor.comments.top(limit=num_of_comments):
            total_comment_score += c.score
        return total_comment_score
