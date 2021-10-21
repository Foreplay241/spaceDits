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

ZODIAC_LIST = ["Aquarius", "Pisces", "Aries", "Taurus", "Gemini", "Cancer",
               "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn"]
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
    square_dict: {}
    triangle_dict: {}
    circle_dict: {}
    lines_dict: {}
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
        self.square_dict = {}
        self.triangle_dict = {}
        self.circle_dict = {}
        self.lines_dict = {}

        if self.from_reddit:
            self.generate_from_reddit()
        else:
            self.generate_from_random()
        self.statistics = {
            "Name": self.name,
            "Cake Day": self.cake_day,
            "Square Dictionary": self.square_dict,
            "Triangle Dictionary": self.triangle_dict,
            "Circle Dictionary": self.circle_dict,
            "Lines Dictionary": self.lines_dict,
        }

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
        img_num = random.randint(0, 9)
        max_hull_points = random.randint(600, 1009)
        max_shield_points = random.randint(721, 1396)
        max_bombs = random.randint(0, 9)
        if redditor:
            x = 0
            for c in map(int, str(self.cake_day)):
                if x == 1:
                    max_bombs += c
                if x == 3:
                    max_shield_points += redditor.comment_karma * c
                if x == 6:
                    max_hull_points += redditor.link_karma * c
                if x == 9:
                    img_num = c
                x += 1
        self.square_dict["image number"] = img_num
        self.square_dict["health"] = max_hull_points
        self.square_dict["shield"] = max_shield_points
        self.square_dict["max bombs"] = max_bombs

    def add_triangle_part(self, redditor=None):
        img_num = random.randint(0, 9)
        firePower = random.randint(39, 129)
        fireRate = random.randint(230, 741)
        maxCharge = random.randint(60, 99)
        if redditor:
            x = 0
            for c in map(int, str(self.cake_day)):
                if x == 1:
                    fireRate += c
                if x == 2:
                    maxCharge += self.get_sum_top_comment_score(num_of_comments=3) * c
                if x == 4:
                    firePower += self.get_average_top_comment_score(num_of_comments=10) + c
                if x == 8:
                    img_num = c
                x += 1
        self.triangle_dict["image number"] = img_num
        self.triangle_dict["fire power"] = firePower
        self.triangle_dict["fire rate"] = fireRate
        self.triangle_dict["max charge"] = maxCharge

    def add_circle_part(self, redditor=None):
        img_num = random.randint(0, 9)
        min_y_velocity = random.randint(-4, -1)
        max_y_velocity = random.randint(-9, -6)
        zodiac_sign = ZODIAC_DICT[self.constellation]
        if redditor:
            x = 0
            for c in map(int, str(self.cake_day)):
                if x == 0:
                    min_y_velocity = -c
                if x == 1 and not (c == 1 or c == 0):
                    max_y_velocity = -c
                if x == 4:
                    zodiac_sign = ZODIAC_DICT[self.constellation]
                if x == 7:
                    img_num = c
                x += 1
        self.circle_dict["image number"] = img_num
        self.circle_dict["min y velocity"] = min_y_velocity
        self.circle_dict["max y velocity"] = max_y_velocity
        self.circle_dict["zodiac sign"] = zodiac_sign

    def add_lines_part(self, redditor=None):
        img_num = random.randint(0, 9)
        min_x_velocity = random.randint(-4, -1)
        max_x_velocity = random.randint(-9, -6)
        max_missles = random.randint(6, 9)
        if redditor:
            x = 0
            for c in map(int, str(self.cake_day)):
                if x == 0:
                    min_x_velocity = -c
                if x == 3 and not (c == min_x_velocity or c == 0):
                    max_x_velocity = -c
                if x == 5:
                    max_missles = c * (4 + c)
                if x == 6:
                    img_num = c
                x += 1
        self.lines_dict["image number"] = img_num
        self.lines_dict["min x velocity"] = min_x_velocity
        self.lines_dict["max x velocity"] = max_x_velocity
        self.lines_dict["max missles"] = max_missles

    def generate_info_image(self, redditor=None):
        info_img = pg.Surface((128, 128))
        name_label = Text(str(self.name), (0, 0), GREY50, 20)
        score_label = Text(str(self.circle_dict["image number"]), (0, 22), GREY50, 20)
        constellation_label = Text(str(self.triangle_dict["image number"]), (0, 22), GREY50, 20)
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
        square_image = pg.image.load(os.path.join("assets/medallion_parts", "square" +
                                                  str(self.square_dict["image number"]) + ".png"))
        triangle_image = pg.image.load(os.path.join("assets/medallion_parts", "triangle" +
                                                    str(self.triangle_dict["image number"]) + ".png"))
        circle_image = pg.image.load(os.path.join("assets/medallion_parts", "circle" +
                                                  str(self.circle_dict["image number"]) + ".png"))
        lines_image = pg.image.load(os.path.join("assets/medallion_parts", "lines" +
                                                 str(self.lines_dict["image number"]) + ".png"))
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
        self.cake_day = int(self.redditor.created_utc)
        self.set_constellation(self.redditor)
        self.add_square_part(self.redditor)
        self.add_triangle_part(self.redditor)
        self.add_circle_part(self.redditor)
        self.add_lines_part(self.redditor)
        self.medal_img = self.generate_medal_image(self.redditor)
        self.info_img = self.generate_info_image(self.redditor)

    def generate_from_random(self):
        # GENERATE A REDILOT FROM RANDOM INPUT.
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
