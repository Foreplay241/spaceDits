# import random
from dataclasses import dataclass

from RedditFusions.create_fusion import Fusion
from settings import *
from Player.Weapons.lasbat_blaster import Blaster
from Player.Weapons.missile_pod import MissilePod
from Player.Weapons.bomb_bay import BombBay
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
    """A shidpit is a spaceship from a reddit post, to be piloted by a redilot."""
    alpha_name: str
    beta_name: str
    gamma_name: str
    name: str
    submission_id: str
    type: str

    creation_date: int
    upvote_ratio: float

    ship_dict: {}

    nose_dict: {}
    nose_part_num: int

    body_dict: {}
    body_part_num: int
    charge_rate: int
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

    info_img: pg.Surface((128, 128))
    ship_img: pg.Surface((128, 128))

    weapons_dict: {}
    switch_dict: {}
    statistics: {}
    ship_properties = {}
    ship_coords = (0, 0)
    ship_rank: int

    def __init__(self, creation_time=1474200000, id_string="r4nd0m"):
        super().__init__("Submission", "ship", creation_time=creation_time, id_string=id_string)
        self.fusion_name = "Shidpit"
        self.submission = None
        self.submission_id = id_string
        self.creation_time = creation_time
        self.statistics = {}
        self.type = "None"
        self.upvote_scale = .72

        self.nose_part_num = random.randint(0, 9)
        self.fire_power = 1
        self.fire_rate = 2
        self.charge_cost = 3
        self.blaster_max_charge = 40
        self.blaster_charge_rate = 5
        self.add_nose_ship_part()

        self.body_part_num = random.randint(0, 9)
        self.shield_charge_rate = 1
        self.max_hull_points = 2
        self.max_shield_points = 3
        self.max_bombs = 4
        self.drop_rate = 5
        self.alpha_num = 6
        self.alpha_name = self.submission_id[0:2].upper()
        self.add_body_ship_part()

        self.wings_part_num = random.randint(0, 9)
        self.min_x_speed = 1
        self.max_x_speed = 2
        self.max_missiles = 3
        self.deploy_rate = 4
        self.beta_num = 5
        self.beta_name = self.submission_id[2:4].upper()
        self.add_wings_ship_part()

        self.engine_part_num = random.randint(0, 9)
        self.min_y_speed = 1
        self.max_y_speed = 2
        self.zodirok_inset = "Gemini"
        self.gamma_num = random.randint(0, 9)
        self.gamma_name = self.submission_id[4:6].upper()
        self.add_engine_ship_part()

        self.ship_coords = (random.randint(0, DISPLAY_WIDTH), random.randint(0, DISPLAY_HEIGHT))
        self.ship_properties = {
            "position": self.ship_coords,
            "y velocity": -3,

        }
        self.name = self.beta_name + self.gamma_name
        self.ship_img = pg.Surface((128, 128))
        self.info_img = pg.Surface((128, 128))

        self.nose_dict = {
            "Fire Power": self.fire_power,
            "Fire Rate": self.fire_rate,
            "Charge Cost": self.charge_cost,
            "Max Charge": self.blaster_max_charge,
            "Charge Rate": self.blaster_charge_rate
        }
        self.body_dict = {
            "Charge Rate": self.shield_charge_rate,
            "Hull Points": self.max_hull_points,
            "Shield Points": self.max_shield_points,
            "Max Bombs": self.max_bombs,
            "Drop Rate": self.drop_rate
        }
        self.wings_dict = {
            "Min X Speed": self.min_x_speed,
            "Max X Speed": self.max_x_speed,
            "Max Missiles": self.max_missiles,
            "Deploy Rate": self.deploy_rate,
            "Beta": self.beta_name
        }
        self.engine_dict = {
            "Min Y Speed": self.min_y_speed,
            "Max Y Speed": self.max_y_speed,
            "Zodirok Inset": self.zodirok_inset,
            "Gamma": self.gamma_name,
        }

        # INITIALIZE WEAPONRY AND GENERATE
        self.left_blaster = Blaster(self, (24, 12), pg.Surface((5, 10)))
        self.middle_blaster = Blaster(self, (32, 12), pg.Surface((5, 10)))
        self.right_blaster = Blaster(self, (40, 12), pg.Surface((5, 10)))
        self.left_missle_pod = MissilePod(self, (14, 48), pg.Surface((10, 5)))
        self.right_missle_pod = MissilePod(self, (50, 48), pg.Surface((10, 5)))
        self.bomb_bay = BombBay(self, (32, 60), pg.Surface((10, 10)))

        self.left_blaster.generate_blaster()
        self.middle_blaster.generate_blaster()
        self.right_blaster.generate_blaster()
        self.left_missle_pod.generate_pod()
        self.right_missle_pod.generate_pod()
        self.bomb_bay.generate_bay()

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
            "Creation Date": self.creation_time,
            "Nose Dictionary": self.nose_dict,
            "Body Dictionary": self.body_dict,
            "Wings Dictionary": self.wings_dict,
            "Engine Dictionary": self.engine_dict,
            "Weapons Dict": self.weapons_dict,
        }

    def add_nose_ship_part(self, submission=None):
        x = 0
        for c in map(int, str(int(self.cake_day))):
            if x == 4:
                self.fire_power = c
            if x == 5:
                self.blaster_charge_rate = c
            if x == 6:
                self.nose_part_num = c
            if x == 7:
                self.charge_cost = c
            if x == 8:
                self.fire_rate = c
            if x == 9:
                self.blaster_max_charge = c
            x += 1

    def add_body_ship_part(self, submission=None):
        x = 0
        for c in map(int, str(int(self.cake_day))):
            if x == 4:
                self.shield_charge_rate = c
            if x == 5:
                self.max_hull_points = c + 10
            if x == 6:
                self.max_shield_points = c + 10
            if x == 7:
                self.max_bombs = c
            if x == 8:
                self.body_part_num = c
            if x == 9:
                self.drop_rate = c
            x += 1

    def add_wings_ship_part(self, submission=None):
        x = 0
        for c in map(int, str(int(self.cake_day))):
            if x == 6:
                self.max_missiles = c
            if x == 7:
                self.deploy_rate = c
            if x == 5 and c != 1 and c != 0:
                self.max_x_speed = -c
                self.min_x_speed = -c
            if x == 8:
                self.wings_part_num = c
            x += 1

    def add_engine_ship_part(self, submission=None):
        if submission:
            x = 0
            for c in map(int, str(int(self.cake_day))):
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


def roundpartial(value, resolution):
    return round(float(value) / resolution) * resolution
