# import random
from dataclasses import dataclass
from settings import *
from blaster import Blaster
from missle_pod import MisslePod
from bomb_bay import BombBay
import pygame as pg
import praw

submission_list = ["pt7pca", "ptgmem", "ptk8gf", "psf4kh",
                   "pruf23", "prsn97", "prizqk", "pqpq93", "pqqlqh",
                   "pq6fff", "ppz69h", "pok3ti", "povobm", "pnsoe2"]

alpha_name_list = ["Fast", "Quick", "Smooth", "Quiet", "Blitz", "Speedy", "Lonely", "Crusty", "Screaming", "Delta"]
beta_name_list = ["Spotless", "Clean", "Bumpy", "Dirty", "Filthy", "Blue", "Brown", "Quartz", "Jade", "Angel"]
gamma_name_list = ["Eagle", "Crow", "Hawk", "Falcon", "Hummingbird", "Owl", "Tiger", "Panther", "Jaguar", "Demon"]


@dataclass
class Shidpit:
    """A shidpit is a space ship from a reddit post, to be piloted by a redilot."""
    alpha_name: str
    beta_name: str
    gamma_name: str
    name: str
    submission_id: str
    creation_date: int
    upvote_ratio: float
    nose_dict: {}
    body_dict: {}
    wings_dict: {}
    engine_dict: {}
    ship_img: pg.Surface((128, 128))
    info_img: pg.Surface((128, 128))

    weapons_dict: {}
    switch_dict: {}
    ship_properties = {}
    ship_coords = (0, 0)
    ship_rank: int

    def __init__(self, sub_id="pry1bu", from_reddit=False):
        self.from_reddit = from_reddit
        self.submission = None
        self.submission_id = sub_id
        self.alpha_name = "alpha-" + sub_id[2].upper()
        self.beta_name = "beta-" + sub_id[4].upper()
        self.gamma_name = "gamma-" + sub_id[1].upper()
        self.name = self.alpha_name + self.beta_name + self.gamma_name
        self.nose_dict = {}
        self.body_dict = {}
        self.wings_dict = {}
        self.engine_dict = {}

        self.left_blaster = Blaster(self, (24, 12), pg.Surface((10, 10)))
        self.middle_blaster = Blaster(self, (32, 12), pg.Surface((10, 10)))
        self.right_blaster = Blaster(self, (40, 12), pg.Surface((10, 10)))
        self.left_missle_pod = MisslePod(self, (14, 48), pg.Surface((10, 10)))
        self.right_missle_pod = MisslePod(self, (50, 48), pg.Surface((10, 10)))
        self.bomb_bay = BombBay(self, (32, 60), pg.Surface((10, 10)))
        self.weapons_dict = {
            "Left Blaster": self.left_blaster,
            "Middle Blaster": self.middle_blaster,
            "Right Blaster": self.right_blaster,
            "Left Pod": self.left_missle_pod,
            "Right Pod": self.right_missle_pod,
            "Bomb Bay": self.bomb_bay
        }

        self.ship_coords = (random.randint(0, DISPLAY_WIDTH), random.randint(0, DISPLAY_HEIGHT))
        self.ship_properties = {
            "position": self.ship_coords,
            "y velocity": -3,

        }
        self.ship_img = pg.Surface((128, 128))
        self.info_img = pg.Surface((128, 128))
        self.ship_img.fill(DARK_BLUE)
        self.info_img.fill(LIGHT_BLUE)
        if self.from_reddit:
            self.generate_reddit_shidpit()
        else:
            self.generate_random_shidpit()
        self.statistics = {
            "Name": self.name,
            "Creation Date": self.creation_date,
            "Nose Dictionary": self.nose_dict,
            "Body Dictionary": self.body_dict,
            "Wings Dictionary": self.wings_dict,
            "Engine Dictionary": self.engine_dict,
            "Weapons Dict": self.weapons_dict,
        }

    @staticmethod
    def get_average_comment_score(sub=None):
        total_score = 0
        x = 0
        if sub:
            while x <= 100:
                for c in sub.comments:
                    total_score += c.score
                    x += 1
        else:
            while x <= 100:
                for i in range(random.randint(85, 110)):
                    total_score += random.randint(-15, 142)
                    x += 1
        return total_score // x

    def add_nose_ship_part(self, submission=None):
        img_num = random.randint(0, 9)
        firePower = random.randint(15, 222)
        fireRate = random.random() * 200
        maxCharge = random.randint(250, 415)
        chargeRate = random.randint(50, 132)
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 1:
                    maxCharge = submission.score * c
                if x == 3:
                    fireRate = submission.upvote_ratio * 100 + (c * 22)
                if x == 4:
                    chargeRate = random.randint(50, 132)
                if x == 6:
                    img_num = c
                if x == 8:
                    firePower = submission.num_comments + (c ** 3)

                x += 1
        self.nose_dict["image number"] = img_num
        self.nose_dict["fire power"] = firePower
        self.nose_dict["fire rate"] = fireRate
        self.nose_dict["max charge"] = maxCharge
        self.nose_dict["charge rate"] = chargeRate

    def add_body_ship_part(self, submission=None):
        img_num = random.randint(0, 9)
        max_hull_points = random.randint(413, 1694)
        max_shield_points = random.randint(643, 1294)
        max_bombs = random.randint(0, 9)
        alpha_num = random.randint(0, 9)
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 2:
                    max_hull_points = submission.score + (submission.score * self.upvote_ratio)
                if x == 5:
                    max_shield_points = submission.score * self.upvote_ratio
                if x == 7:
                    img_num = random.randint(0, 9)
                if x == 8:
                    alpha_num = c
                if x == 9:
                    max_bombs = random.randint(0, 9)
                x += 1
        self.body_dict["image number"] = img_num
        self.body_dict["hull points"] = max_hull_points
        self.body_dict["shield points"] = max_shield_points
        self.body_dict["max bombs"] = max_bombs
        self.body_dict["alpha name"] = alpha_name_list[alpha_num]

    def add_wings_ship_part(self, submission=None):
        img_num = random.randint(0, 9)
        min_x_speed = random.randint(-9, -6)
        max_x_speed = random.randint(6, 9)
        max_missles = random.randint(0, 9)
        beta_num = random.randint(0, 9)
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 0:
                    min_x_speed = -c
                if x == 5 and not (c == 1 or c == 0):
                    max_x_speed = -c
                if x == 6:
                    max_missles = submission.num_comments ** 2
                if x == 8:
                    img_num = c
                if x == 9:
                    beta_num = c
                x += 1
        self.wings_dict["image number"] = img_num
        self.wings_dict["min x speed"] = min_x_speed
        self.wings_dict["max x speed"] = max_x_speed
        self.wings_dict["max missles"] = max_missles
        self.wings_dict["beta name"] = beta_name_list[beta_num]

    def add_engine_ship_part(self, submission=None):
        img_num = random.randint(0, 9)
        min_y_speed = random.randint(-4, -2)
        max_y_speed = random.randint(-10, -7)
        zodiac_strength = random.randint(0, 9)
        gamma_num = random.randint(0, 9)
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 0:
                    min_y_speed = -c
                if x == 4 and not (c == 1 or c == 0):
                    max_y_speed = -c
                if x == 6:
                    zodiac_strength = c + 11
                if x == 7:
                    gamma_num = c
                if x == 9:
                    img_num = random.randint(0, 9)
                x += 1
        self.engine_dict["image number"] = img_num
        self.engine_dict["min y speed"] = min_y_speed
        self.engine_dict["max y speed"] = max_y_speed
        self.engine_dict["zodiac strength"] = zodiac_strength
        self.engine_dict["gamma name"] = gamma_name_list[gamma_num]

    def generate_reddit_shidpit(self):
        reddit = praw.Reddit(
            user_agent="(by u/Foreplay241)",
            client_id="kbIP5RKylq0_0AgP_9hFYg",
            client_secret="BU_jfFaK2lwHampEjJtoDzieWNxDyw",
            username="Camel_this_Chicken",
            password="1Fuckfuck!!"
        )
        self.submission = reddit.submission(self.submission_id)
        print(self.submission.shortlink)
        self.upvote_ratio = roundpartial(self.submission.upvote_ratio, 0.02)
        self.creation_date = int(self.submission.created_utc)
        self.add_nose_ship_part(submission=self.submission)
        self.add_body_ship_part(submission=self.submission)
        self.add_engine_ship_part(submission=self.submission)
        self.add_wings_ship_part(submission=self.submission)
        self.switch_dict = {
            "C": self.submission.clicked,
            "E": self.submission.edited,
            "I1": self.submission.is_original_content,
            "I2": self.submission.is_self,
            "L": self.submission.locked,
            "O": self.submission.over_18,
            "S1": self.submission.saved,
            "S2": self.submission.spoiler,
            "S3": self.submission.stickied
        }
        # self.print_ship_stats()
        self.ship_rank = 1
        self.name = self.alpha_name + " " + self.beta_name + "-" + self.gamma_name
        # self.fuel_usage = 2
        # self.max_fuel = 100
        # self.current_fuel = 100

    def generate_random_shidpit(self):
        self.creation_date = random.randint(1119553200, 1633120253)
        self.upvote_ratio = roundpartial(random.random(), 0.02)
        # self.ship_rank = 1
        self.add_nose_ship_part()
        self.add_body_ship_part()
        self.add_engine_ship_part()
        self.add_wings_ship_part()
        self.switch_dict = {
            "C": bool(random.getrandbits(1)),
            "E": bool(random.getrandbits(1)),
            "I1": bool(random.getrandbits(1)),
            "I2": bool(random.getrandbits(1)),
            "L": bool(random.getrandbits(1)),
            "O": bool(random.getrandbits(1)),
            "S1": bool(random.getrandbits(1)),
            "S2": bool(random.getrandbits(1)),
            "S3": bool(random.getrandbits(1))
        }
        # self.print_ship_stats()
        self.name = self.alpha_name + " " + self.beta_name + "-" + self.gamma_name
        # self.fuel_usage = 2
        # self.max_fuel = 100
        # self.current_fuel = 100


def roundpartial(value, resolution):
    return round(float(value) / resolution) * resolution
