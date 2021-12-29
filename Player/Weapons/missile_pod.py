from settings import *
import pygame as pg
from Player.Weapons.missile import Missile


class MissilePod(pg.sprite.Sprite):
    def __init__(self, shidpit, pos, img):
        super(MissilePod, self).__init__()
        self.shidpit = shidpit
        self.x, self.y = pos
        self.image = img
        sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        assetsPath = os.path.join(sourceFileDir, "assets")
        self.missile_image = pg.image.load(os.path.join(assetsPath, 'missile.png'))
        self.is_player = False
        self.canDeploy = True

        self.max_missiles = 1
        self.current_missiles = 1
        self.power_hull = 1
        self.power_shield = 1
        self.deploy_rate = 1

        self.missiles = []
        self.prev_shot_time = 0
        self.missile_velocity = -7

    def fire(self, game):
        now = pg.time.get_ticks()
        if now - self.prev_shot_time > self.deploy_rate and \
                self.current_missiles > 0 and self.canDeploy:
            self.prev_shot_time = pg.time.get_ticks()
            missile = Missile(self.shidpit, (self.x + game.player.rect.x,
                                             self.y + game.player.rect.y),
                              self.missile_image, colormask=LIGHT_BLUE)
            missile.velocity = self.missile_velocity + self.shidpit.ship_properties["y velocity"]
            self.missiles.append(missile)
            game.all_sprites.add(missile)

    def generate_pod(self):
        self.max_missiles = self.shidpit.wings_dict["Max Missiles"]
        self.current_missiles = self.shidpit.wings_dict["Max Missiles"]
        self.power_hull = 1
        self.power_shield = 1
        self.deploy_rate = self.shidpit.wings_dict["Deploy Rate"]
