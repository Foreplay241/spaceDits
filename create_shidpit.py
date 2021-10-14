# import random
from dataclasses import dataclass
from settings import *
from blaster import Blaster
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
    sub_id: str
    creation_date: int
    ship_rank: int
    upvote_ratio: float
    nose_num: int
    body_num: int
    wings_num: int
    engine_num: int
    img: pg.Surface((128, 128))
    weapons_dict: {}
    switch_dict: {}
    max_hull_points: int
    max_shield_points: int

    def __init__(self, sub_id="pry1bu", from_reddit=False):
        self.from_reddit = from_reddit
        self.name = "name" + sub_id
        self.alpha_name = "alpha" + sub_id
        self.beta_name = "beta" + sub_id
        self.gamma_name = "gamma" + sub_id
        self.sub_id = sub_id
        self.weapons_dict = {}
        self.img = pg.Surface((128, 128))
        if self.from_reddit:
            self.generate_reddit_shidpit()
        else:
            self.generate_random_shidpit()
        self.statistics = {
            "Name": self.name,
            "Creation Date": self.creation_date,
            "Nose Number": self.nose_num,
            "Body Number": self.body_num,
            "Wings Number": self.wings_num,
            "Engine Number": self.engine_num,
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

    def print_ship_stats(self):
        print((self.name + ' == ' + self.sub_id))
        # for key in self.switch_dict:
        #     if len(key) == 1:
        #         print(key + ":  " + str(self.switch_dict[key]))
        #     if len(key) == 2:
        #         print(key + ": " + str(self.switch_dict[key]))

    def add_nose_ship_part(self, min_blasters=2, max_blasters=6, submission=None):
        self.nose_num = random.randint(0, 9)
        num_blasters = random.randint(min_blasters, max_blasters)
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 5:
                    if 5 >= c > 0:
                        num_blasters = c
                    else:
                        num_blasters = c - 5
                if x == 6:
                    self.nose_num = c
                x += 1
        for i in range(num_blasters):
            blaster = self.add_lasbat_blaster((0, 0), name="blaster"+str(i+1))
            self.weapons_dict[blaster["Name"]] = blaster
        nose_image = pg.image.load(os.path.join("assets/ship_parts", "nose" + str(self.nose_num) + ".png"))
        self.img.blit(nose_image, (0, 0))

    def add_body_ship_part(self, submission=None):
        self.body_num = random.randint(0, 9)
        self.max_hull_points = random.randint(50, 150)
        self.max_shield_points = random.randint(50, 150)
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 7:
                    self.body_num = c
                    self.alpha_name = alpha_name_list[c]
                x += 1
            self.max_hull_points = submission.score
            self.max_shield_points = submission.score * submission.upvote_ratio
        body_image = pg.image.load(os.path.join("assets/ship_parts", "body" + str(self.body_num) + ".png"))
        self.img.blit(body_image, (0, 0))

    def add_wings_ship_part(self, submission=None):
        self.wings_num = random.randint(0, 9)
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 8:
                    self.wings_num = c
                    self.beta_name = beta_name_list[c]
                x += 1
        for i in range(2):
            pod = self.add_missle_pod((0, (i+10)*3), name="pod"+str(i+1))
            self.weapons_dict[pod["Name"]] = pod
        wings_image = pg.image.load(os.path.join("assets/ship_parts", "wings" + str(self.wings_num) + ".png"))
        self.img.blit(wings_image, (0, 0))

    def add_engine_ship_part(self, submission=None):
        self.engine_num = random.randint(0, 9)
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 9:
                    self.engine_num = c
                    self.gamma_name = gamma_name_list[c]
                x += 1
        engine_image = pg.image.load(os.path.join("assets/ship_parts", "engine" + str(self.engine_num) + ".png"))
        self.img.blit(engine_image, (0, 0))

    def add_lasbat_blaster(self, pos, name="blaster", max_charge=random.randint(45, 90), power=random.randint(15, 22)):
        lasbat_stats_dict = {
            "Position": pos,
            "Name": name,
            "Max Charge": max_charge,
            "Current Charge": max_charge,
            "Power": power
        }
        self.weapons_dict[lasbat_stats_dict["Name"]] = lasbat_stats_dict
        return lasbat_stats_dict

    def add_missle_pod(self, pos, name="pod",
                       max_num_missles=random.randint(45, 90), missle_power=random.randint(26, 38)):
        missle_stats_dict = {
            "Position": pos,
            "Name": name,
            "Max Number Missles": max_num_missles,
            "Current Missles": max_num_missles,
            "Missle Power": missle_power
        }
        self.weapons_dict[missle_stats_dict["Name"]] = missle_stats_dict
        return missle_stats_dict

    def generate_reddit_shidpit(self):
        reddit = praw.Reddit(
            user_agent="(by u/Foreplay241)",
            client_id="kbIP5RKylq0_0AgP_9hFYg",
            client_secret="BU_jfFaK2lwHampEjJtoDzieWNxDyw",
            username="Camel_this_Chicken",
            password="1Fuckfuck!!"
        )
        submission = reddit.submission(self.sub_id)
        print(submission)
        print(submission.shortlink)
        self.upvote_ratio = roundpartial(submission.upvote_ratio, 0.02)
        self.creation_date = int(submission.created_utc)
        self.add_nose_ship_part(submission=submission)
        self.add_body_ship_part(submission=submission)
        self.add_engine_ship_part(submission=submission)
        self.add_wings_ship_part(submission=submission)
        # self.img = self.generate_ship_image(self.nose_num,
        #                                self.body_num,
        #                                self.wings_num,
        #                                self.engine_num)
        self.switch_dict = {
            "C": submission.clicked,
            "E": submission.edited,
            "I1": submission.is_original_content,
            "I2": submission.is_self,
            "L": submission.locked,
            "O": submission.over_18,
            "S1": submission.saved,
            "S2": submission.spoiler,
            "S3": submission.stickied
        }
        self.print_ship_stats()
        self.ship_rank = 1
        self.name = self.alpha_name + " " + self.beta_name + "-" + self.gamma_name
        self.fuel_usage = 2
        self.max_fuel = 100
        self.current_fuel = 100

    def generate_random_shidpit(self):
        self.creation_date = random.randint(1119553200, 1633120253)
        self.upvote_ratio = roundpartial(random.random(), 0.02)
        # self.ship_rank = 1
        self.add_nose_ship_part()
        self.add_body_ship_part()
        self.add_engine_ship_part()
        self.add_wings_ship_part()
        # self.img = generate_ship_image(self.nose_num,
        #                                self.body_num,
        #                                self.wings_num,
        #                                self.engine_num)
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
        self.print_ship_stats()
        self.name = self.alpha_name + " " + self.beta_name + "-" + self.gamma_name
        self.fuel_usage = 2
        self.max_fuel = 100
        self.current_fuel = 100


def roundpartial(value, resolution):
    return round(float(value) / resolution) * resolution
