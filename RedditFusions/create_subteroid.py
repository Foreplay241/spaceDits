from dataclasses import dataclass
from RedditFusions.create_fusion import Fusion
from settings import *
import pygame as pg
import prawSubteroid


@dataclass
class Subteroid(Fusion):
    """
    A subtroid is an asteroid created from a reddit submission
    """

    def __init__(self, creation_time=1474200000, id_string="r4nd0m"):
        super().__init__("Comment", "asteroid", creation_time=creation_time, id_string=id_string)
        self.fusion_name = "Asterment"
        self.image = pg.Surface((128, 128))
