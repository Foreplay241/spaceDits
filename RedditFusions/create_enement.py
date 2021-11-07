from dataclasses import dataclass

from RedditFusions.create_fusion import Fusion
from settings import *
import pygame as pg
import praw


@dataclass
class Enement(Fusion):
    """
    An enement is an enemy fused with a comment. It is an AI powered drone.
    """
    submission_id: str
    creation_date: int
    upvote_ratio: float
