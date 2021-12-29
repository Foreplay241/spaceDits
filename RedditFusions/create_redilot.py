from dataclasses import dataclass

from RedditFusions.create_fusion import Fusion
from settings import *
import time
import pygame as pg
import random
import praw
import os

from GUI.text import Text

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
    "Aquarius": ["Shield", "Extra Shields", "Air", "Garnet", (1, 20), (2, 18)],
    "Pisces": ["Shield", "Jet stream", "Water", "Amethyst", (2, 19), (3, 20)],
    "Aries": ["Health", "Ram Dash", "Fire", "Bloodstone", (3, 21), (4, 19)],
    "Taurus": ["Health", "Stronger Hull", "Earth", "Sapphire", (4, 20), (5, 20)],
    "Gemini": ["Shield", "Twin for a min", "Air", "Agate", (5, 21), (6, 20)],
    "Cancer": ["Shield", "Tidal wave blast", "Water", "Emerald", (6, 21), (7, 22)],
    "Leo": ["Health", "Sonic boom stun", "Fire", "Onyx", (7, 23), (8, 22)],
    "Virgo": ["Health", "Life after Death", "Earth", "Carnelian", (8, 23), (9, 22)],
    "Libra": ["Shield", "Set hull_points equal to shield", "Air", "Chrysolite", (9, 23), (10, 22)],
    "Scorpio": ["Shield", "Medium Arrow angled", "Water", "Beryl", (10, 23), (11, 21)],
    "Sagittarius": ["Health", "Giant Arrow", "Fire", "Topaz", (11, 22), (12, 21)],
    "Capricorn": ["Health", "Drop Bombs", "Earth", "Ruby", (12, 22), (1, 19)]
}


@dataclass
class Redilot(Fusion):
    """A redilot is a redditor pilot for a shidpit from reddit."""
    name: str
    redditor: None
    cake_day: int
    constellation: str
    pilot_rank: int
    medallion_dict: {}
    square_dict: {}
    triangle_dict: {}
    circle_dict: {}
    lines_dict: {}
    medal_img: pg.Surface((128, 128))
    info_img: pg.Surface((128, 128))

    def __init__(self, name=random.choice(redditor_name_list), creation_time=1474200000, id_string="r4nd0m"):
        super().__init__("Redditor", "pilot", creation_time=creation_time, id_string=id_string)
        self.fusion_name = "Redilot"
        self.redbit_dict = self.redditor_dict
        self.creation_date = creation_time
        self.redditor = None
        self.redditor_name = name

        self.square_num = random.randint(0, 9)
        self.zodiac_sign = "Gemini"
        self.zodiac_rock = "Agate"
        self.constellation = self.zodiac_sign
        self.pilot_rank = 1
        self.add_square_part()

        self.triangle_num = random.randint(0, 9)
        self.max_hull_points = random.randint(1, 10)
        self.max_shield_points = random.randint(1, 10)
        self.add_triangle_part()

        self.circle_num = random.randint(0, 9)
        self.min_x_velocity = random.randint(-9, -6)
        self.max_x_velocity = -self.min_x_velocity
        self.add_circle_part()

        self.lines_num = random.randint(0, 9)
        self.min_y_velocity = random.randint(-4, -2)
        self.max_y_velocity = random.randint(-10, -7)
        self.add_lines_part()

        self.medal_img = pg.Surface((128, 128))
        self.info_img = pg.Surface((128, 128))

        self.square_dict = {
            "Star Sign": self.constellation,
            "Zodirok": ZODIAC_DICT[self.constellation][3]
        }

        self.triangle_dict = {
            "Hull Points": self.max_hull_points,
            "Shield Points": self.max_shield_points,
        }

        self.circle_dict = {
            "Min X Velocity": self.min_x_velocity,
            "Max X Velocity": self.max_x_velocity,
        }

        self.lines_dict = {
            "Min Y Velocity": self.min_y_velocity,
            "Max Y Velocity": self.max_y_velocity,
        }

        self.save_data_dict = {
            "Name": self.redditor_name,
            "Cake Day": self.cake_day,
            "Square Dictionary": self.square_dict,
            "Triangle Dictionary": self.triangle_dict,
            "Circle Dictionary": self.circle_dict,
            "Lines Dictionary": self.lines_dict,
        }

    def set_constellation(self, redditor=None):
        # print("Cake Day: " + str(MONTH_LIST[time.gmtime(self.cake_day).tm_mon - 1])
        #       + " " + str(time.gmtime(self.cake_day).tm_mday)
        #       + " " + str(time.gmtime(self.cake_day).tm_year))
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
        self.set_constellation()
        x = 0
        for c in map(int, str(self.cake_day)):
            if x == 9:
                self.square_num = c
            x += 1

    def add_triangle_part(self, redditor=None):
        x = 0
        for c in map(int, str(self.cake_day)):
            if x == 6:
                self.max_hull_points = c + 10
            if x == 7:
                self.max_shield_points = c + 10
            if x == 8:
                self.triangle_num = c
            x += 1

    def add_circle_part(self, redditor=None):
        x = 0
        for c in map(int, str(self.cake_day)):
            if x == 0:
                self.min_y_velocity = -c
            if x == 1 and not (c == 1 or c == 0):
                self.max_y_velocity = -c
            if x == 4:
                pass
            if x == 7:
                self.circle_num = c
            x += 1

    def add_lines_part(self, redditor=None):
        if redditor:
            x = 0
            for c in map(int, str(self.cake_day)):
                if x == 3 and c != 0:
                    self.min_x_velocity = -c
                    self.max_x_velocity = c
                if x == 5:
                    pass
                if x == 6:
                    self.lines_num = c
                x += 1
