from ship import *
from text import Text


class Player(Ship):
    def __init__(self, game, x, y, redilot, shidpit):
        super().__init__(game, x, y, redilot, shidpit)
        self.HUD = HUD(self.game, self.redilot)
        self.image = shidpit.img
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (50, 45))
        self.colorImage = pg.Surface(self.image.get_size()).convert_alpha()
        self.colorImage.fill(RANDOM_BLUE)
        self.image.blit(self.colorImage, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.redilot = redilot
        self.shidpit = shidpit
        self.fuel_usage = self.shidpit.fuel_usage
        self.current_fuel = self.shidpit.current_fuel
        self.max_shield = self.shidpit.max_fuel

    def update(self):
        super(Player, self).update()
        print(self.fuel_usage)

    def draw(self, window):
        super().draw(window)
        self.HUD.draw_player_name(window, self.redilot.name)
        self.HUD.draw_hullbar(window, self.health, self.max_health)
        self.HUD.draw_shieldbar(window, self.shield, self.max_shield)
        self.HUD.draw_fuel_bar(window, self.fuel_usage, self.current_fuel, self.max_fuel)
        if self.HUD.can_see_enemy_name:
            self.HUD.draw_enemy_name(window, self.game.enemy.redilot.name)
        if self.HUD.can_see_enemy_health:
            self.HUD.draw_enemy_hullbar(window, self.game.enemy.health, self.game.enemy.max_health)
        if self.HUD.can_see_enemy_shield:
            self.HUD.draw_enemy_shieldbar(window, self.game.enemy.shield, self.game.enemy.max_shield)

    def shoot(self, blaster):
        now = pg.time.get_ticks()
        if now - self.prev_laser_time > self.laser_cool_down:
            self.prev_laser_time = pg.time.get_ticks()
            laser = Laser(self.game, self.rect.x + (self.image.get_width() / 2),
                          self.rect.y + ((self.image.get_height()) / 3), self.laser_img, colormask=LIGHT_BLUE)
            laser.is_player = True
            self.lasers.append(laser)
            self.game.all_sprites.add(laser)
            self.game.player_lasers.add(laser)

    def fire_missle(self, podbay):
        now = pg.time.get_ticks()
        if now - self.prev_missle_time > self.missle_cool_down:
            self.prev_missle_time = pg.time.get_ticks()
            missle = Missle(self.game, self.rect.x + (self.image.get_width() / 2),
                            self.rect.y + (self.image.get_height() / 3), self.missle_img, colormask=NEON_BLUE)
            missle.is_player = True
            self.missles.append(missle)
            self.game.all_sprites.add(missle)
            self.game.player_missles.add(missle)
            
    def death(self):
        super(Player, self).death()
        self.outcome = "loser"


class HUD:
    def __init__(self, game, _redilot):
        self.game = game
        self.redilot = _redilot
        self.enemy_name_label = Text("EneMY nAme", DISPLAY_CENTER)
        self.can_see_enemy_health = True
        self.can_see_enemy_shield = True
        self.can_see_enemy_name = True

    @staticmethod
    def draw_player_name(window, name):
        """
        Draw the enemy name near the health and shield bar.
        :param window:
        :param name:
        :return:
        """
        player_draw_text(window, name, RANDOM_BLUE, 42, (DISPLAY_WIDTH // 2 + 200, DISPLAY_BOTTOM - 25))

    @staticmethod
    def draw_hullbar(window, health, max_health):
        """
        Draw a bar that displays the remaining health out of the maximum health based on submission karma
        :param window:
        :param health: int
        :param max_health: int
        :return: None
        """
        max_width = 400
        pg.draw.rect(window, GREY50, ((DISPLAY_WIDTH // 2) - max_width // 2, DISPLAY_HEIGHT - 68, max_width, 12))
        pg.draw.rect(window, RANDOM_GREEN, ((DISPLAY_WIDTH // 2) - max_width // 2, DISPLAY_HEIGHT - 68,
                                            (health * max_width // max_health * max_width) / max_width, 20))
        pass

    @staticmethod
    def draw_shieldbar(window, shield, max_shield):
        """
        Draw a shield that displays the remaining shield out of max shields based on comment karma
        :param window:
        :param shield: int
        :param max_shield: int
        :return: None
        """
        max_width = 400
        pg.draw.rect(window, GREY50, ((DISPLAY_WIDTH // 2) - max_width // 2, DISPLAY_HEIGHT - 45, max_width, 12))
        pg.draw.rect(window, RANDOM_BLUE, ((DISPLAY_WIDTH // 2) - max_width // 2, DISPLAY_HEIGHT - 45,
                                           (shield * max_width // max_shield * max_width) / max_width, 20))

    @staticmethod
    def draw_fuel_bar(window, usage_rate, current_fuel, max_fuel):
        max_height = 300
        pg.draw.rect(window, GREY50, (DISPLAY_WIDTH - 75, DISPLAY_HEIGHT - 80, 25, 75))
        pg.draw.rect(window, LIME, (DISPLAY_WIDTH - 75, DISPLAY_HEIGHT - 80,
                                    25, (current_fuel * max_height // max_fuel * max_height) / max_height))

    @staticmethod
    def draw_enemy_name(window, name):
        """
        Draw the enemy name near the health and shield bar.
        :param window:
        :param name:
        :return:
        """
        enemy_draw_text(window, name, RANDOM_RED, 42, (DISPLAY_WIDTH // 2 - 200, DISPLAY_TOP))
        # enemy_name_label.draw(window)

    @staticmethod
    def draw_enemy_hullbar(window, health, max_health):
        """
        Draw a bar that displays the remaining health out of the maximum health based on submission karma
        :param window:
        :param health: int
        :param max_health: int
        :return: None
        """
        max_width = 400
        pg.draw.rect(window, GREY50, ((DISPLAY_WIDTH // 2) - max_width // 2, 45, max_width, 12))
        pg.draw.rect(window, RANDOM_GREEN, ((DISPLAY_WIDTH // 2) - max_width // 2, 45,
                                            (health * max_width // max_health * max_width) / max_width, 20))

    @staticmethod
    def draw_enemy_shieldbar(window, shield, max_shield):
        """
        Draw a shield that displays the remaining shield out of max shields based on comment karma
        :param window:
        :param shield: int
        :param max_shield: int
        :return: None
        """
        max_width = 400
        pg.draw.rect(window, GREY50, ((DISPLAY_WIDTH // 2) - max_width // 2, 22, max_width, 12))
        pg.draw.rect(window, RANDOM_BLUE, ((DISPLAY_WIDTH // 2) - max_width // 2, 22,
                                           (shield * max_width // max_shield * max_width) / max_width, 20))
