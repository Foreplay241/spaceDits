from dataclasses import dataclass

from pygame.math import Vector2

from RedditFusions.create_fusion import Fusion
from settings import *
import pygame as pg
import praw


@dataclass
class Enement(Fusion):
    """
    An enement is an enemy fused with a comment. It is an AI powered drone or an alien.
    """

    def __init__(self, creation_time=1474201111, id_string="r4nd0m"):
        super().__init__("Comment", "Enemy", creation_time=creation_time, id_string=id_string)
        self.fusion_name = "Enement"
        self.image = pg.Surface((128, 128))
        self.rect = self.image.get_rect()
        self.redbit_dict = self.comment_dict
        self.arms_part_num = 0
        self.body_part_num = 0
        self.eye_part_num = 0
        self.mouth_part_num = 0
        self.max_health = 10
        self.health = self.max_health

        # MOVEMENT VARIABLES
        self.direction = Vector2(0, -1)
        self.position = Vector2(60, 90)
        self.angle_speed = 0
        self.speed = 0
        self.angle = 0

    def add_arms(self, comment=None):
        if comment:
            x = 0
            for c in map(int, str(int(comment.created_utc))):
                if x == 6:
                    self.arms_part_num = c
                x += 1

    def add_body(self, comment=None):
        x = 0
        for c in map(int, str(self.cake_day)):
            if x == 7:
                self.speed = c * .1
            x += 1

    def add_eye(self, comment=None):
        if comment:
            x = 0
            for c in map(int, str(int(comment.created_utc))):
                if x == 8:
                    self.eye_part_num = c
                x += 1

    def add_mouth(self, comment=None):
        if comment:
            x = 0
            for c in map(int, str(int(comment.created_utc))):
                if x == 9:
                    self.mouth_part_num = c
                x += 1

    def generate_alien_img(self):
        alien_img = pg.Surface((128, 128))
        alien_img.set_colorkey(BLACK)
        sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        redditFusionAssetsPath = os.path.join(sourceFileDir, "assets")
        alienPartPath = os.path.join(redditFusionAssetsPath, "alien")
        arms_image = pg.image.load(os.path.join(alienPartPath, f"arms{self.arms_part_num}.png")).convert_alpha()
        body_image = pg.image.load(os.path.join(alienPartPath, f"body{self.body_part_num}.png")).convert_alpha()
        eye_image = pg.image.load(os.path.join(alienPartPath, f"eye{self.eye_part_num}.png")).convert_alpha()
        mouth_image = pg.image.load(os.path.join(alienPartPath, f"mouth{self.mouth_part_num}.png")).convert_alpha()
        parts_list = [arms_image, body_image, eye_image, mouth_image]
        for part in parts_list:
            alien_img.blit(part, (0, 0))
        return alien_img
