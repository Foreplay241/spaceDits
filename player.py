from GUI.button import Button
from GUI.hud_button import HUDbutton
from ship import *
from GUI.text import Text


class Player(Ship):
    def __init__(self, game, redilot, shidpit):
        super().__init__(game, redilot, shidpit)
        self.HUD = HUD(self.game, self)
        self.image = shidpit.ship_img
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (64, 64))
        self.colorImage = pg.Surface(self.image.get_size()).convert_alpha()
        self.colorImage.fill(RANDOM_BLUE)
        self.image.blit(self.colorImage, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.redilot = redilot
        self.shidpit = shidpit
        self.weapons_dict = self.shidpit.weapons_dict
        self.prev_target = None
        self.target = None

    def update(self):
        super(Player, self).update()
        self.HUD.update()
        self.HUD.x = 0
        self.HUD.y = (DISPLAY_HEIGHT * 8) // 10

    def draw(self, window):
        super().draw(window)
        self.HUD.draw(window, (0, DISPLAY_HEIGHT - 90))
        if self.target:
            print(self.target)

    def switch_target(self, new_target):
        self.prev_target = self.target
        self.target = new_target

    def shoot(self, blaster):
        super(Player, self).shoot(blaster)
        blaster.current_charge -= 10

    def deploy(self, podbay):
        super(Player, self).deploy(podbay)
        podbay.current_missiles -= 1

    def release(self, bombay):
        bombay.current_bombs -= 1

    def death(self):
        super(Player, self).death()
        self.outcome = "loser"


class HUD(pg.sprite.Sprite):
    name_HUDbutton: HUDbutton

    def __init__(self, game, ship):
        super().__init__()
        self.game = game
        self.ship = ship

        self.name_label = Text("Name", (0, 0), WHITE, 11)
        self.velocity_label = Text("Speed", (0, 0), WHITE, 11)
        self.speed_label = Text("Speed", (0, 0), WHITE, 11)
        self.pod1_label = Text("Pod1", (0, 0), WHITE, 11)
        self.p1r_label = Text("remaining", (0, 0), WHITE, 11)
        self.pod2_label = Text("Pod2", (0, 0), WHITE, 11)
        self.p2r_label = Text("remaining", (0, 0), WHITE, 11)
        self.bay_label = Text("Bay", (0, 0), WHITE, 11)
        self.x, self.y = (0, 0)
        self.image = pg.Surface((DISPLAY_WIDTH, 128))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.list_to_display = [
            "Name", "Hull Points", "Shield Points",
            "Fuel", "Speed", "Weapons"
        ]
        self.weapon_module_btns = []
        self.HUD_display_btns = []

    def update(self):
        super(HUD, self).update()

    def draw(self, window, pos):
        self.image.fill(GREY)
        for wpn in self.weapon_module_btns:
            wpn.draw(self.image)
        self.draw_name(self.image)
        self.draw_fuel_display(self.image)
        self.draw_hullbar(self.image)
        self.draw_shieldbar(self.image)
        self.draw_weapons_display(self.image)
        self.draw_speed_display(self.image)

        window.blit(self.image, (pos[0],  # - (self.rect.width // 2 - self.ship.rect.width // 2),
                                 pos[1]))  # self.ship.rect.height))

    def draw_name(self, HUD_display):
        """
        Draw the enemy name near the hull_points and shield_points bar.
        :param HUD_display:
        :return:
        """
        if "Name" in self.list_to_display:
            self.name_label = Text(self.ship.name, (0, 0), DARK_PURPLE, 32)
            HUD_display.blit(self.name_label.img, (64, 8))

    def draw_hullbar(self, HUD_display):
        """
        Draw a bar that displays the remaining hull_points out of the maximum hull_points based on submission karma
        :param HUD_display:
        :return: None
        """
        max_width = self.image.get_width() // 3
        pg.draw.rect(HUD_display, GREY50, (10, 32,
                                           max_width, 22))
        pg.draw.rect(HUD_display, RANDOM_GREEN, (10, 32,
                                                 ((self.ship.hull_points * max_width //
                                                   self.ship.max_hull_points * max_width)
                                                  / max_width), 22))

    def draw_shieldbar(self, HUD_display):
        """
        Draw a shield_points that displays the remaining shield_points out of max shields based on comment karma
        :param HUD_display:
        :return: None
        """
        max_width = self.image.get_width() // 3
        pg.draw.rect(HUD_display, GREY50, (10, 64,
                                           max_width, 22))
        pg.draw.rect(HUD_display, RANDOM_BLUE, (10, 64,
                                                ((self.ship.shield_points * max_width //
                                                  self.ship.max_shield_points * max_width)
                                                 / max_width), 22))

    def draw_speed_display(self, HUD_display):
        """

        :param HUD_display:
        :return:
        """
        self.velocity_label = Text(f"Velocity: ({self.ship.x_velocity}, {self.ship.y_velocity})"
                                   , (0, 0), DARK_BLUE, size=16)
        self.speed_label = Text(f"Speed: {self.ship.min_y_velocity}", (0, 0), DARK_BLUE, size=16)
        HUD_display.blit(self.velocity_label.img, ((self.image.get_width() // 3) + 64, 32))
        HUD_display.blit(self.speed_label.img, ((self.image.get_width() // 3) + 64, 64))

    def draw_fuel_display(self, HUD_display):
        """

        :param HUD_display:
        :return:
        """
        max_height = 64
        pg.draw.rect(HUD_display, GREY50, ((self.image.get_width() * 4) // 6, 16,
                                           32, max_height))
        pg.draw.rect(HUD_display, LIME, ((HUD_display.get_width() * 4) // 6, 16,
                                         32,
                                         (self.ship.current_fuel * max_height //
                                          self.ship.max_fuel * max_height)
                                         / max_height))

    def draw_weapons_display(self, HUD_display):
        """
        Draw Blaster L, M, R and Pods L, R and Bomb Bay weapon statuses.
        :param HUD_display:
        :return:
        """
        max_height = 48
        i = 0
        for weapon in self.ship.weapons_dict:
            if weapon.endswith("Blaster"):
                pg.draw.rect(HUD_display, GREY50,
                             ((HUD_display.get_width() - 96) + (i * 32), 5, 22, max_height))
                pg.draw.rect(HUD_display, LIGHT_YELLOW,
                             ((HUD_display.get_width() - 96) + (i * 32), 5,
                              22, (self.ship.weapons_dict[weapon].current_charge * max_height //
                                   self.ship.weapons_dict[weapon].max_charge * max_height) // max_height))

                i += 1
            elif weapon.endswith("Pod"):
                self.pod1_label = Text(f"Pod1:",
                                       (0, 0), DARK_PURPLE, size=16)
                self.pod2_label = Text(f"Pod2:",
                                       (0, 0), DARK_PURPLE, size=16)
                self.p1r_label = Text(f"{self.ship.weapons_dict[weapon].current_missiles}",
                                      (0, 0), DARK_PURPLE, size=16)
                self.p2r_label = Text(f"{self.ship.weapons_dict[weapon].current_missiles}",
                                      (0, 0), DARK_PURPLE, size=16)
                HUD_display.blit(self.pod1_label.img, ((HUD_display.get_width() - 96) + (0 * 32), 54))
                HUD_display.blit(self.pod2_label.img, ((HUD_display.get_width() - 96) + (1 * 32), 54))
                HUD_display.blit(self.p1r_label.img, ((HUD_display.get_width() - 96) + (0 * 32), 64))
                HUD_display.blit(self.p2r_label.img, ((HUD_display.get_width() - 96) + (1 * 32), 64))
            elif weapon.endswith("Bay"):
                self.bay_label = Text(f"BAY: ",
                                      (0, 0), DARK_PURPLE, size=16)
                self.bayr_label = Text(f"{self.ship.weapons_dict[weapon].current_bombs}",
                                       (0, 0), DARK_PURPLE, size=16)
                HUD_display.blit(self.bay_label.img, ((HUD_display.get_width() - 96) + (2 * 32), 54))
