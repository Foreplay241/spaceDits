from dataclasses import dataclass
from settings import *
import pygame as pg
import praw


@dataclass
class Subteroid:
    """
    A subtroid is an asteroid created from a reddit submission
    """
    submission_id: str
    creation_date: int
    upvote_ratio: float
