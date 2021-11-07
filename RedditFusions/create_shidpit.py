# import random
from dataclasses import dataclass

from RedditFusions.create_fusion import Fusion
from settings import *
from Weapons.lasbat_blaster import Blaster
from Weapons.missile_pod import MissilePod
from Weapons.bomb_bay import BombBay
import pygame as pg
import praw

from GUI.text import Text

submission_list = ["pt7pca", "ptgmem", "ptk8gf", "psf4kh",
                   "pruf23", "prsn97", "prizqk", "pqpq93", "pqqlqh",
                   "pq6fff", "ppz69h", "pok3ti", "povobm", "pnsoe2"]

alpha_name_list = ["Fast", "Quick", "Smooth", "Quiet", "Blitz", "Speedy", "Lonely", "Crusty", "Screaming", "Delta"]
beta_name_list = ["Spotless", "Clean", "Bumpy", "Dirty", "Smooth", "Blue", "Brown", "Quartz", "Jade", "Angel"]
gamma_name_list = ["Eagle", "Crow", "Hawk", "Falcon", "Hummingbird", "Owl", "Tiger", "Panther", "Jaguar", "Demon"]


@dataclass
class Shidpit(Fusion):
    """A shidpit is a space ship from a reddit post, to be piloted by a redilot."""
    alpha_name: str
    beta_name: str
    gamma_name: str
    name: str
    submission_id: str

    creation_date: int
    upvote_ratio: float

    ship_dict: {}

    nose_dict: {}
    nose_part_num: int
    firePower: int
    fireRate: int
    deployRate: int
    dropRate: int
    maxCharge: int

    body_dict: {}
    body_part_num: int
    chargeRate: int
    max_hull_points: int
    max_shield_points: int
    max_bombs: int
    alpha_num: int

    wings_dict: {}
    wings_part_num: int
    min_x_speed: int
    max_x_speed: int
    max_missiles: int
    beta_num: int

    engine_dict: {}
    engine_part_num: int
    min_y_speed: int
    max_y_speed: int
    zodiac: str
    zodiac_timer: int
    gamma_num: int

    ship_img: pg.Surface((128, 128))
    info_img: pg.Surface((128, 128))

    weapons_dict: {}
    switch_dict: {}
    ship_properties = {}
    ship_coords = (0, 0)
    ship_rank: int

    def __init__(self, sub_id="pry1bu", from_reddit=False):
        super().__init__(sub_id)
        self.from_reddit = from_reddit
        self.submission = None
        self.submission_id = sub_id
        self.creation_date = 1433553253

        self.nose_part_num = random.randint(0, 9)
        self.firePower = random.randint(15, 222)
        self.fireRate = int(random.random()) * 200
        self.deployRate = random.randint(22, 133) * 23
        self.dropRate = (int(random.random()) + 5) * 241
        self.max_charge = random.randint(250, 415)

        self.body_part_num = random.randint(0, 9)
        self.chargeRate = random.randint(50, 132)
        self.max_hull_points = random.randint(413, 1694)
        self.max_shield_points = random.randint(643, 1294)
        self.max_bombs = random.randint(0, 9)
        self.alpha_num = random.randint(0, 9)
        self.alpha_name = sub_id[0:2].upper()

        self.wings_part_num = random.randint(0, 9)
        self.min_x_speed = random.randint(-9, -6)
        self.max_x_speed = random.randint(6, 9)
        self.max_missiles = random.randint(0, 9)
        self.beta_num = random.randint(0, 9)
        self.beta_name = sub_id[2:4].upper()

        self.engine_part_num = random.randint(0, 9)
        self.min_y_speed = random.randint(-4, -2)
        self.max_y_speed = random.randint(-10, -7)
        self.zodiac = "Gemini"
        self.zodiac_timer = random.randint(0, 9)
        self.gamma_num = random.randint(0, 9)
        self.gamma_name = sub_id[4:6].upper()

        self.left_blaster = Blaster(self, (24, 12), pg.Surface((10, 10)))
        self.middle_blaster = Blaster(self, (32, 12), pg.Surface((10, 10)))
        self.right_blaster = Blaster(self, (40, 12), pg.Surface((10, 10)))
        self.left_missle_pod = MissilePod(self, (14, 48), pg.Surface((10, 10)))
        self.right_missle_pod = MissilePod(self, (50, 48), pg.Surface((10, 10)))
        self.bomb_bay = BombBay(self, (32, 60), pg.Surface((10, 10)))

        self.ship_coords = (random.randint(0, DISPLAY_WIDTH), random.randint(0, DISPLAY_HEIGHT))
        self.ship_properties = {
            "position": self.ship_coords,
            "y velocity": -3,

        }
        self.name = self.alpha_name + self.beta_name + self.gamma_name
        self.ship_img = pg.Surface((128, 128))
        self.info_img = pg.Surface((128, 128))

        if self.from_reddit:
            self.generate_reddit_shidpit()

        self.nose_dict = {
            "Fire Power": self.firePower,
            "Charge Rate": self.chargeRate,
            "Fire Rate": self.fireRate,
            "Max Charge": self.max_charge
        }
        self.body_dict = {
            "Hull Points": self.max_hull_points,
            "Shield Points": self.max_shield_points,
            "Drop Rate": self.dropRate,
            "Max Bombs": self.max_bombs,
            "Alpha": self.alpha_name,
        }
        self.wings_dict = {
            "Min X Speed": self.min_x_speed,
            "Max X Speed": self.max_x_speed,
            "Deploy Rate": self.deployRate,
            "Max Missiles": self.max_missiles,
            "Beta": self.beta_name
        }
        self.engine_dict = {
            "Min Y Speed": self.min_y_speed,
            "Max Y Speed": self.max_y_speed,
            "Zodirok": self.zodiac,
            "Zodirok Timer": self.zodiac_timer,
            "Gamma": self.gamma_name,
        }

        self.weapons_dict = {
            "Left Blaster": self.left_blaster,
            "Middle Blaster": self.middle_blaster,
            "Right Blaster": self.right_blaster,
            "Left Pod": self.left_missle_pod,
            "Right Pod": self.right_missle_pod,
            "Bomb Bay": self.bomb_bay
        }
        self.statistics = {
            "Name": self.name,
            "Creation Date": self.creation_date,
            "Nose Dictionary": self.nose_dict,
            "Body Dictionary": self.body_dict,
            "Wings Dictionary": self.wings_dict,
            "Engine Dictionary": self.engine_dict,
            "Weapons Dict": self.weapons_dict,
        }

    def add_nose_ship_part(self, submission=None):
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 1:
                    self.max_charge = submission.score * c
                if x == 2:
                    self.dropRate = c
                if x == 3:
                    self.fireRate = round(submission.upvote_ratio * 100 + (c * 22))
                if x == 4:
                    self.chargeRate = random.randint(50, 132)
                if x == 6:
                    self.nose_part_num = c
                if x == 8:
                    self.firePower = submission.num_comments + (c ** 3)
                x += 1

    def add_body_ship_part(self, submission=None):
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 2:
                    self.max_hull_points = submission.score + round(submission.score * self.upvote_ratio * c)
                if x == 5:
                    self.max_shield_points = submission.score * round(self.upvote_ratio * c)
                if x == 7:
                    self.body_part_num = c
                if x == 8:
                    self.alpha_num = c
                if x == 9:
                    self.max_bombs = random.randint(0, 9)
                x += 1

    def add_wings_ship_part(self, submission=None):
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 0:
                    self.min_x_speed = -c
                if x == 5 and not (c == 1 or c == 0):
                    self.max_x_speed = -c
                if x == 6:
                    self.max_missiles = submission.num_comments ** 2
                if x == 8:
                    self.wings_part_num = c
                if x == 9:
                    self.beta_num = c
                x += 1

    def add_engine_ship_part(self, submission=None):
        if submission:
            x = 0
            for c in map(int, str(int(submission.created_utc))):
                if x == 0:
                    self.min_y_speed = -c
                if x == 4 and not (c == 1 or c == 0):
                    self.max_y_speed = -c
                if x == 6:
                    self.zodiac = "Gemini"
                if x == 5:
                    self.zodiac_timer = c + 22
                if x == 7:
                    self.gamma_num = c
                if x == 9:
                    self.engine_part_num = random.randint(0, 9)
                x += 1

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
        self.ship_rank = 1
        self.name = self.alpha_name + " " + self.beta_name + "-" + self.gamma_name
        self.left_blaster = Blaster(self, (24, 12), pg.Surface((10, 10)), maxCharge=self.max_charge,
                                    power=self.firePower, fire_rate=self.fireRate)
        self.middle_blaster = Blaster(self, (32, 12), pg.Surface((10, 10)), maxCharge=self.max_charge,
                                      power=self.firePower, fire_rate=self.fireRate)
        self.right_blaster = Blaster(self, (40, 12), pg.Surface((10, 10)), maxCharge=self.max_charge,
                                     power=self.firePower, fire_rate=self.fireRate)
        self.left_missle_pod = MissilePod(self, (14, 48), pg.Surface((10, 10)), maxMissiles=self.max_missiles,
                                          power=self.firePower, fire_rate=self.fireRate)
        self.right_missle_pod = MissilePod(self, (50, 48), pg.Surface((10, 10)), maxMissiles=self.max_missiles,
                                           power=self.firePower, fire_rate=self.fireRate)
        self.bomb_bay = BombBay(self, (32, 60), pg.Surface((10, 10)), maxBombs=self.max_bombs, drop_rate=self.fireRate)
        self.info_img = self.generate_info_img(self.submission)
        self.ship_img = self.generate_ship_img()

    def generate_info_img(self, submission=None):
        info_img = pg.Surface((128, 128))
        name_label = Text(str(self.name), (0, 0), GREY50, 20)
        if submission:
            name_label = Text(submission.name, (0, 0), GREY50, 22)

        labels_list = [name_label]
        y = 0
        for label in labels_list:
            info_img.blit(label.img, (0, y * 22))
            y += 1
        return info_img

    def generate_ship_img(self):
        # LAYERS THE LAYERS ON THE MEDAL IMAGE
        ship_img = pg.Surface((128, 128))
        ship_img.set_colorkey(BLACK)
        sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        redditFusionAssetsPath = os.path.join(sourceFileDir, "assets")
        shipPartPath = os.path.join(redditFusionAssetsPath, "ship_parts")
        nose_image = pg.image.load(os.path.join(shipPartPath, f"nose{self.nose_part_num}.png"))
        body_image = pg.image.load(os.path.join(shipPartPath, f"body{self.body_part_num}.png"))
        wings_image = pg.image.load(os.path.join(shipPartPath, f"wings{self.wings_part_num}.png"))
        engine_image = pg.image.load(os.path.join(shipPartPath, f"engine{self.engine_part_num}.png"))
        parts_list = [nose_image, body_image, wings_image, engine_image]
        for part in parts_list:
            ship_img.blit(part, (0, 0))
        return ship_img


def roundpartial(value, resolution):
    return round(float(value) / resolution) * resolution
