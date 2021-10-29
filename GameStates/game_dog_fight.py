from GameStates.game import Game
import pygame as pg
from enemy import Enemy


class DogFight(Game):
    def __init__(self):
        super(DogFight, self).__init__()
        self.enemy = None
        self.enemy_lasers = pg.sprite.Group()
        self.enemy_missiles = pg.sprite.Group()
        self.enemy_bombs = pg.sprite.Group()

    def startup(self, persistent):
        super(DogFight, self).startup(persistent)
        if "Enemy" in persistent:
            self.enemy = persistent["Enemy"]
        else:
            self.enemy = Enemy(self, persistent["Enemy Redilot"], persistent["Enemy Shidpit"])
        self.all_sprites.add(self.enemy)

    def get_event(self, event):
        super(DogFight, self).get_event(event)

    def update(self, dt):
        super(DogFight, self).update(dt)

    def draw(self, screen):
        super(DogFight, self).draw(screen)
