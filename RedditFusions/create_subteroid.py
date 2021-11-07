from dataclasses import dataclass
from RedditFusions.create_fusion import Fusion
from settings import *
import pygame as pg
import praw


@dataclass
class Subteroid(Fusion):
    """
    A subtroid is an asteroid created from a reddit submission
    """
    submission_id: str
    creation_date: int
    upvote_ratio: float
    rock_dict: {}
    metal_dict: {}

    def __init__(self):
        super(Subteroid, self).__init__("r4nd0m")
    