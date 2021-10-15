from dataclasses import dataclass
import pygame as pg
import random
import praw
import os

redditor_list = ["Foreplay241", "Big-mac_sauce", "Camel-of_Chicken", "Camel_this_Chicken",
                 "Camel_and_Chicken", "Camel_of_Chicken", "3MuchLikeLA", "ACC15ORD", "antianit",
                 "bot_neen", "BlurrZ8", "coby----", "atobitt", "Gena1548"]

expertise_list = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces"
]
expertise_dict = {
    "Aries": ["Health", "Ram Dash.", "Fire"],
    "Taurus": ["Health", "Stronger Hull.", "Earth"],
    "Gemini": ["Shield", "Twin for a min.", "Air"],
    "Cancer": ["Shield", "Tidal wave blast.", "Water"],
    "Leo": ["Health", "Sonic boom stun.", "Fire"],
    "Virgo": ["Health", "Life after Death.", "Earth"],
    "Libra": ["Shield", "Set hull_points equal to shield.", "Air"],
    "Scorpio": ["Shield", "Medium Arrow angled.", "Water"],
    "Sagittarius": ["Health", "Giant Arrow.", "Fire"],
    "Capricorn": ["Health", "Drop Bombs.", "Earth"],
    "Aquarius": ["Shield", "Extra Shields.", "Air"],
    "Pisces": ["Shield", "Jet stream.", "Water"]
}


@dataclass
class Redilot:
    """A redilot is a redditor pilot for a shidpit from reddit."""
    name: str
    reddit: praw.Reddit
    cake_day: int
    pilot_rank: int
    square_num: int
    triangle_num: int
    circle_num: int
    lines_num: int
    max_hull_points: int
    max_shield_points: int
    medal_img: pg.Surface((128, 128))

    def __init__(self, name="TestPilot", from_reddit=False, pilot_rank=1):
        self.cake_day = 0
        self.name = name
        self.from_reddit = from_reddit
        self.pilot_rank = pilot_rank
        self.medal_img = pg.Surface((128, 128))
        if self.from_reddit:
            self.generate_from_reddit()
        else:
            self.generate_from_random()
        self.statistics = {
            "Name": name,
            "Cake Day": self.cake_day,
            "Square Number": self.square_num,
            "Triangle Number": self.triangle_num,
            "Circle Number": self.circle_num,
            "Lines Number": self.lines_num
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

    def add_square_part(self, redditor=None):
        self.square_num = random.randint(0, 9)
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

    def generate_medal_image(self):
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
        redditor = reddit.redditor(self.name)
        self.cake_day = redditor.created_utc
        self.set_hull_points(redditor)
        self.set_shield_points(redditor)
        self.add_square_part(redditor)
        self.add_triangle_part(redditor)
        self.add_circle_part(redditor)
        self.add_lines_part(redditor)
        self.medal_img = self.generate_medal_image()

    def generate_from_random(self):
        # GENERATE A REDILOT FROM RANDOM INPUT.
        self.cake_day = random.randint(1119553200, 1633120253)
        self.set_hull_points()
        self.set_shield_points()
        self.add_square_part()
        self.add_triangle_part()
        self.add_circle_part()
        self.add_lines_part()
        self.medal_img = self.generate_medal_image()
