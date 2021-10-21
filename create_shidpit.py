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
    sub_id: str
    creation_date: int
    ship_rank: int
    upvote_ratio: float
    nose_num: int
    body_num: int
    wings_num: int
    engine_num: int
    ship_img: pg.Surface((128, 128))
    info_img: pg.Surface((128, 128))
    weapons_dict: {}
    switch_dict: {}
    ship_properties = {}
    ship_coords = (0, 0)
    max_hull_points: int
    max_shield_points: int

    def __init__(self, sub_id="pry1bu", from_reddit=False):
        self.from_reddit = from_reddit
        self.name = sub_id
        self.submission = None
        self.alpha_name = "alpha" + sub_id[:2]
        self.beta_name = "beta" + sub_id[:4]
        self.gamma_name = "gamma" + sub_id[:6]
        self.sub_id = sub_id
        self.weapons_dict = {}
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

    # def print_ship_stats(self):
    #     print((self.name + ' == ' + self.sub_id))
        # for key in self.switch_dict:
        #     if len(key) == 1:
        #         print(key + ":  " + str(self.switch_dict[key]))
        #     if len(key) == 2:
        #         print(key + ": " + str(self.switch_dict[key]))

    def add_nose_ship_part(self, submission=None):
        self.nose_num = random.randint(0, 9)
        firePower = random.randint(15, 222)
        fireRate = self.upvote_ratio * 100
        maxCharge = random.randint(50, 1245)
        if submission:
            x = 0
            firePower = submission.num_comments
            fireRate = submission.upvote_ratio*100
            maxCharge = submission.score
            for c in map(int, str(int(submission.created_utc))):
                if x == 6:
                    self.nose_num = c
                x += 1
        for i in range(3):
            blaster = self.add_lasbat_blaster(((i + 3) * 8, 12), name="blaster" + str(i + 1),
                                              max_charge=maxCharge, fire_rate=fireRate,
                                              fire_power=firePower)
            self.weapons_dict[blaster.name] = blaster
        nose_image = pg.image.load(os.path.join("assets/ship_parts", "nose" + str(self.nose_num) + ".png"))
        self.ship_img.blit(nose_image, (0, 0))

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
            self.max_hull_points = submission.score + (submission.score * submission.upvote_ratio)
            self.max_shield_points = submission.score * submission.upvote_ratio
            bay = self.add_bomb_bay((32, 64), name="bay" + str(1))
            self.weapons_dict[bay["Name"]] = bay
        body_image = pg.image.load(os.path.join("assets/ship_parts", "body" + str(self.body_num) + ".png"))
        self.ship_img.blit(body_image, (0, 0))

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
            pod = self.add_missle_pod((14 + (i * 36), 48), name="pod" + str(i + 1))
            self.weapons_dict[pod.name] = pod
        wings_image = pg.image.load(os.path.join("assets/ship_parts", "wings" + str(self.wings_num) + ".png"))
        self.ship_img.blit(wings_image, (0, 0))

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
        self.ship_img.blit(engine_image, (0, 0))

    def add_lasbat_blaster(self, pos, name="blaster", max_charge=random.randint(45, 90),
                           fire_power=random.randint(15, 22),
                           fire_rate=random.randint(150, 320)):
        lasbat_stats_dict = {
            "Position": pos,
            "Name": name,
            "Max Charge": max_charge,
            "Power": fire_power,
            "Fire Rate": fire_rate
        }
        lasbat_blaster = Blaster(self, pos, pg.Surface((10, 10)), max_charge, fire_power, fire_rate)
        lasbat_blaster.name = name
        self.weapons_dict[lasbat_stats_dict["Name"]] = lasbat_blaster
        return lasbat_blaster

    def add_missle_pod(self, pos, name="pod",
                       max_num_missles=random.randint(45, 90), power=random.randint(26, 38),
                       fire_rate=random.randint(150, 320)):
        missle_stats_dict = {
            "Position": pos,
            "Name": name,
            "Max Missles": max_num_missles,
            "Power": power,
            "Fire Rate": fire_rate
        }
        missle_pod = MisslePod(self, pos, pg.Surface((10, 10)), max_num_missles, power, fire_rate)
        missle_pod.name = name
        self.weapons_dict[missle_stats_dict["Name"]] = missle_pod
        return missle_pod

    def add_bomb_bay(self, pos, name="bay", max_num_bombs=random.randint(3, 8), bomb_power=random.randint(78, 89)):
        bomb_stats_dict = {
            "Position": pos,
            "Name": name,
            "Max Number Bombs": max_num_bombs,
            "Current Bombs": max_num_bombs,
            "Bomb Power": bomb_power
        }
        self.weapons_dict[bomb_stats_dict["Name"]] = bomb_stats_dict
        return bomb_stats_dict

    def generate_reddit_shidpit(self):
        reddit = praw.Reddit(
            user_agent="(by u/Foreplay241)",
            client_id="kbIP5RKylq0_0AgP_9hFYg",
            client_secret="BU_jfFaK2lwHampEjJtoDzieWNxDyw",
            username="Camel_this_Chicken",
            password="1Fuckfuck!!"
        )
        self.submission = reddit.submission(self.sub_id)
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
