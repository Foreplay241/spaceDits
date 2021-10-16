from ship import *
from text import Text


class Player(Ship):
    def __init__(self, game, x, y, redilot, shidpit):
        super().__init__(game, x, y, redilot, shidpit)
        self.HUD = HUD(self.game, self)
        self.HUD.scale_display_size((1, 1))
        self.target_HUD = HUD(self.game, self)
        self.target_HUD.scale_display_size((1, 1))
        self.target_HUD.can_see_name = False
        self.target_HUD.can_see_shield_points = False
        self.image = shidpit.img
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (50, 45))
        self.colorImage = pg.Surface(self.image.get_size()).convert_alpha()
        self.colorImage.fill(RANDOM_BLUE)
        self.image.blit(self.colorImage, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.redilot = redilot
        self.shidpit = shidpit
        self.prev_target = None
        self.target = None

    def update(self):
        super(Player, self).update()
        self.HUD.update()
        self.HUD.x = self.rect.x
        self.HUD.y = self.rect.y

    def draw(self, window):
        super().draw(window)
        self.HUD.draw(window, self.rect)
        if self.target:
            self.target_HUD.draw(window, self.target.rect)
            print("drawing target HUD")

    def switch_target(self, new_target):
        self.prev_target = self.target
        self.target = new_target

    def shoot(self, blaster):
        # SHOOT A LASBAT BLASTER OR A CHAIN GUN
        now = pg.time.get_ticks()
        if now - self.prev_laser_time > self.laser_cool_down:
            self.prev_laser_time = pg.time.get_ticks()
            laser = Laser(self.game, self.rect.x + (self.image.get_width() / 2),
                          self.rect.y + ((self.image.get_height()) / 3), self.laser_img, colormask=LIGHT_BLUE)
            laser.is_player = True
            laser.velocity -= self.y_vel
            self.lasers.append(laser)
            self.game.all_sprites.add(laser)
            self.game.player_lasers.add(laser)

    def deploy(self, podbay):
        # DEPLOY AN EXPLOSIVE FROM A MISSLE POD BAY OR BOMB BAY.
        now = pg.time.get_ticks()
        if now - self.prev_missle_time > self.missle_cool_down:
            self.prev_missle_time = pg.time.get_ticks()
            missle = Missle(self.game, self.rect.x + (self.image.get_width() / 2),
                            self.rect.y + (self.image.get_height() / 3), self.missle_img, colormask=NEON_BLUE)
            missle.is_player = True
            missle.velocity -= self.y_vel
            self.missles.append(missle)
            self.game.all_sprites.add(missle)
            self.game.player_missles.add(missle)

    def release(self, bombay):
        pass

    def death(self):
        super(Player, self).death()
        self.outcome = "loser"


class HUD(pg.sprite.Sprite):
    def __init__(self, game, ship):
        super().__init__()
        self.game = game
        self.ship = ship
        self.name_label = Text("", (0, 0), BLACK, 11)
        self.x, self.y = (0, 0)
        self.image = pg.Surface((64, 48))
        self.image.fill(GREY25)
        self.image.set_colorkey(GREY25)
        self.rect = self.image.get_rect()
        self.can_see_hull_points = True
        self.can_see_shield_points = True
        self.can_see_fuel = True
        self.can_see_name = True
        self.scale = (1, 1)

    def scale_display_size(self, scale):
        self.scale = scale
        self.image = pg.transform.scale(self.image, (int(64 * scale[0]), int(48 * scale[1])))
        self.rect = self.image.get_rect()

    def update(self):
        super(HUD, self).update()

    def draw(self, window, pos):
        if self.can_see_name:
            self.draw_name(self.image)
        if self.can_see_fuel:
            self.draw_fuel_bar(self.image)
        if self.can_see_hull_points:
            self.draw_hullbar(self.image)
        if self.can_see_shield_points:
            self.draw_shieldbar(self.image)
        window.blit(self.image, (pos[0] - (self.rect.width // 2 - self.ship.rect.width // 2),
                                 pos[1] + self.ship.rect.height))

    def draw_name(self, HUD_display):
        """
        Draw the enemy name near the hull_points and shield_points bar.
        :param HUD_display:
        :return:
        """
        self.name_label = Text(self.ship.name, ((self.rect.width // 2),
                                                5 * self.scale[1]), GREY99, int(13 * self.scale[0]))
        self.name_label.draw(HUD_display)

    def draw_hullbar(self, HUD_display):
        """
        Draw a bar that displays the remaining hull_points out of the maximum hull_points based on submission karma
        :param HUD_display:
        :return: None
        """
        max_width = 60 * self.scale[0]
        pg.draw.rect(HUD_display, GREY50, (HUD_display.get_width() // 2 - max_width // 2, 15 * self.scale[1],
                                           max_width, 5 * self.scale[1]))
        pg.draw.rect(HUD_display, RANDOM_GREEN, (HUD_display.get_width() // 2 - max_width // 2, 15 * self.scale[1],
                                                 ((self.ship.hull_points * max_width //
                                                   self.ship.max_hull_points * max_width)
                                                  / max_width), 5 * self.scale[1]))

    def draw_shieldbar(self, HUD_display):
        """
        Draw a shield_points that displays the remaining shield_points out of max shields based on comment karma
        :param HUD_display:
        :return: None
        """
        max_width = 60 * self.scale[0]
        pg.draw.rect(HUD_display, GREY50, (HUD_display.get_width() // 2 - max_width // 2, 25 * self.scale[1],
                                           max_width, 5 * self.scale[1]))
        pg.draw.rect(HUD_display, RANDOM_BLUE, (HUD_display.get_width() // 2 - max_width // 2, 25 * self.scale[1],
                                                ((self.ship.shield_points * max_width //
                                                  self.ship.max_shield_points * max_width)
                                                 / max_width), 5 * self.scale[1]))

    def draw_fuel_bar(self, HUD_display):
        """

        :param HUD_display:
        :return:
        """
        max_width = 60 * self.scale[0]
        pg.draw.rect(HUD_display, GREY50, (HUD_display.get_width() // 2 - max_width // 2, 35 * self.scale[1],
                                           max_width, 5 * self.scale[1]))
        pg.draw.rect(HUD_display, LIME, (HUD_display.get_width() // 2 - max_width // 2, 35 * self.scale[1],
                                         (self.ship.current_fuel * max_width //
                                          self.ship.max_fuel * max_width)
                                         / max_width, 5 * self.scale[1]))
