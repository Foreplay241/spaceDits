import time

from pygame.time import wait

from Player.fighterHUD import FHUD
from Player.ship import *


class Fighter(Ship):
    def __init__(self, game, redilot, shidpit):
        super().__init__(game, redilot, shidpit)
        self.HUD = FHUD(self.game, self)

        # WEAPON STUFF
        self.weapons_dict = self.shidpit.weapons_dict
        self.sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        self.weaponAssetsPath = os.path.join(self.sourceFileDir, "Weapons/assets")
        self.target_range = 241
        self.target_list = []

        self.laser = None
        self.laser_img = pg.image.load(os.path.join(self.weaponAssetsPath, "laser.png"))
        self.lasers = []
        self.laser_fire_rate = 0
        self.laser_power_hull = 1 - self.shidpit.upvote_scale
        self.laser_power_shield = self.shidpit.upvote_scale
        self.prev_laser_time = pg.time.get_ticks()

        self.missile = None
        self.missile_img = pg.image.load(os.path.join(self.weaponAssetsPath, "missile.png"))
        self.missiles = []
        self.missiles_remaining = 22
        self.missile_cool_down = 250
        self.missile_power_hull = .65
        self.missile_power_shield = .15
        self.prev_missile_time = pg.time.get_ticks()

        self.bomb = None
        self.bomb_img = pg.image.load(os.path.join(self.weaponAssetsPath, "bomb.png"))
        self.bombs = []
        self.bombs_remaining = 2
        self.bomb_cool_down = 300
        self.bomb_power_hull = .90
        self.bomb_power_shield = .07

        self.can_shoot = True
        self.is_player = False
        self.redilot_age = self.redilot.cake_day - datetime.utcnow().timestamp()
        self.redilot_age = abs(int(self.redilot_age))

    def update(self):
        super(Fighter, self).update()
        pass

    def shoot(self, blaster):
        if blaster.current_charge > 0 and blaster.canShoot:
            if len(self.target_list) >= 1:
                blaster.fire(self.game, self.target_list[0])
        elif blaster.current_charge <= 0:
            blaster.current_charge += 1

    def deploy(self, pod):
        if pod.current_missiles > 0 and pod.canDeploy:
            pod.current_missiles -= 0
            print(pod.current_missiles)
            pod.fire(self.game)

    def release(self, bay):
        if bay.current_bombs > 0 and bay.canDrop:
            bay.current_bombs -= 1
            bay.fire(self.game)

    def draw(self, window):
        super(Fighter, self).draw(window)
        self.HUD.draw(window, (0, DISPLAY_HEIGHT - 90))

    def u_turn(self):
        pass

    def barrel_roll(self, roll_left=True):
        if roll_left:
            self.direction.rotate_ip(-90)
        else:
            self.direction.rotate_ip(90)

    def acquire_target(self):
        for alien in self.game.alien_list:
            if alien.position[0] <= self.position[0]\
                    and alien.position[1] >= self.position[1]:
                alien.isTarget = True
                self.target_list.append(alien)
