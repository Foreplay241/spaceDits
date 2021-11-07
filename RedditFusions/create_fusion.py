from dataclasses import dataclass
from settings import *
import pygame as pg
import praw
import os


@dataclass
class Fusion:
    """
    A fusion is a combination of a Redditor, Subreddit, Submission, or Comment combined with a space object.
    """
    fusion_name: str
    id_str: str
    creation_date: int
    img_img: pg.Surface((128, 128))
    info_img: pg.Surface((128, 128))
    redbit_dict: {}

    def __init__(self, _ID):
        self.name = "None"
        self.id_str = _ID
        self.creation_date = random.randint(1119553200, 1633120253)
        self.img_img = pg.Surface((128, 128))
        self.info_img = pg.Surface((128, 128))
        self.redbit_dict = {}
        self.redditor_dict = {
            "Creation Date": self.creation_date,
            "ID": _ID,
            "Name": self.name,
            "Comment Karma": 0,
            "Link Karma": 0,
            "Comments List": [],
            "Submissions List": [],
            }

        self.subreddit_dict = {
            "Creation Date": self.creation_date,
            "ID": _ID,
            "Name": "",
            "Subscriber Count": 0,
            }

        self.submission_dict = {
            "Creation Date": self.creation_date,
            "ID": _ID,
            "Name": "",
            "Creator": "",
            "Score": 0,
            "Number of Comments": 0,
            "Upvote Ratio": 0.0
            }

        self.comment_dict = {
            "Creation Date": self.creation_date,
            "ID": _ID,
            "Creator": "",
            "Comment Body": "",
            "Score": 0
            }
