import math

from GUI.hud_button import HUDbutton
from GUI.text import Text
from settings import *


class HUD(pg.sprite.Sprite):
    name_HUDbutton: HUDbutton

    def __init__(self, game, ship):
        super().__init__()
        self.game = game
        self.ship = ship
        self.sourceFileDir = os.path.dirname(os.path.abspath(__file__))
        self.assetsPath = os.path.join(self.sourceFileDir, "assets")
        self.HUDPath = os.path.join(self.assetsPath, "HUD")
        self.edge_indicator_arrow = pg.image.load(os.path.join(self.HUDPath, "ship_edge_indicator.png"))
        self.target_crosshair = pg.image.load(os.path.join(self.HUDPath, "target_indicator.png"))
        self.arrow_rect = self.edge_indicator_arrow.get_rect()
        self.crosshair_rect = self.target_crosshair.get_rect()
        self.orig_arrow = self.edge_indicator_arrow
        self.orig_crosshair = self.target_crosshair
        self.color_list = [GREY, BLACK, WHITE, RANDOM_COLOR, RANDOM_COLOR2, RANDOM_COLOR3]
        self.image = pg.Surface((DISPLAY_WIDTH, 128))
        self.image.fill(self.color_list[0])
        self.rect = self.image.get_rect()

        self.name_label = Text("Name", (0, 0), WHITE, 11)
        self.position_label = Text("Position", (0, 0), WHITE, 11)
        self.speed_label = Text("Speed", (0, 0), WHITE, 11)

        # self.velocity_label = Text("Velocity", (0, 0), WHITE, 11)
        self.direction_label = Text("Direction", (0, 0), WHITE, 11)
        self.pod_label = Text("Pod1", (0, 0), WHITE, 11)
        self.podr_label = Text("remaining", (0, 0), WHITE, 11)
        self.bay_label = Text("Bay", (0, 0), WHITE, 11)
        self.bayr_label = Text("remaining", (0, 0), WHITE, 11)
        self.x, self.y = (0, 0)
        self.list_to_display = [
            "Name", "Hull Points", "Shield Points",
            "Fuel", "Speed", "Weapons", "Edge Arrow",
            "TargetSys"
        ]
        self.weapon_module_btns = []
        self.HUD_display_btns = []

    def update(self):
        super(HUD, self).update()

    def draw(self, window, pos):
        self.image.fill(self.color_list[0])
        self.draw_name(self.image)
        self.draw_fuel_display(self.image)
        self.draw_hullbar(self.image)
        self.draw_shieldbar(self.image)
        self.draw_speed_display(self.image)
        self.draw_edge_arrow()

        window.blit(self.image, (pos[0], pos[1]))

    def draw_edge_arrow(self):
        angleRad = math.atan2(DISPLAY_CENTER[1] - self.ship.position[1], self.ship.position[0] - DISPLAY_CENTER[0])
        arrow_surface = pg.transform.rotate(self.orig_arrow, math.degrees(angleRad))

        # PLAYER GOES OFF RIGHT SIDE OF THE SCREEN
        if self.ship.position[0] > DISPLAY_RIGHT:
            self.ship.isOffScreen = True
            self.ship.game.screen.blit(arrow_surface, (DISPLAY_RIGHT - 32,
                                                       clamp(self.ship.position[1], 0, DISPLAY_BOTTOM)))
        # PLAYER GOES OFF LEFT SIDE OF THE SCREEN
        if self.ship.position[0] < DISPLAY_LEFT:
            self.ship.isOffScreen = True
            self.ship.game.screen.blit(arrow_surface, (DISPLAY_LEFT,
                                                       clamp(self.ship.position[1], 0, DISPLAY_BOTTOM)))
        # PLAYER GOES OFF BOTTOM OF THE SCREEN
        if self.ship.position[1] > DISPLAY_BOTTOM - 90:
            self.ship.isOffScreen = True
            self.ship.game.screen.blit(arrow_surface, (clamp(self.ship.position[0], 0, DISPLAY_RIGHT - 32),
                                                       DISPLAY_BOTTOM - 128))
        # PLAYER GOES OFF THE TOP OF THE SCREEN
        if self.ship.position[1] < DISPLAY_TOP:
            self.ship.isOffScreen = True
            self.ship.game.screen.blit(arrow_surface, (clamp(self.ship.position[0], 0, DISPLAY_RIGHT - 32),
                                                       DISPLAY_TOP))
        else:
            self.ship.isOffScreen = False

    def draw_name(self, HUD_display):
        """
        Draw the enemy name near the hull_points and shield_points bar.
        :param HUD_display:
        :return:
        """
        if "Name" in self.list_to_display:
            self.name_label = Text(self.ship.name, (0, 0), self.color_list[1], 32)
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
        pg.draw.rect(HUD_display, self.color_list[3], (10, 32,
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
        pg.draw.rect(HUD_display, self.color_list[4], (10, 64,
                                                       ((self.ship.shield_points * max_width //
                                                         self.ship.max_shield_points * max_width)
                                                        / max_width), 22))

    def draw_speed_display(self, HUD_display):
        """
        Draw the speed display on the HUD_display
        :param HUD_display: shows most stats of your shidpit.
        :return:
        """
        # self.velocity_label = Text(f"Velocity: ({round(self.ship.x_velocity)}, {round(self.ship.y_velocity)})",
        #                            (0, 0), self.color_list[2], size=16)
        self.position_label = Text(f"Position: ({int(self.ship.position[0])}, {int(self.ship.position[1])})",
                                   (0, 0), self.color_list[2], size=16)
        self.speed_label = Text(f"Speed: {round(self.ship.speed, 2)}", (0, 0), self.color_list[2], size=16)
        self.direction_label = Text(f"Direction: ({round(self.ship.direction[0])}, {round(self.ship.direction[1])})",
                                    (0, 0), self.color_list[2], size=16)

        # HUD_display.blit(self.velocity_label.img, ((self.image.get_width() // 3) + 64, 32))
        HUD_display.blit(self.position_label.img, ((self.image.get_width() // 3) + 64, 32))
        HUD_display.blit(self.speed_label.img, ((self.image.get_width() // 3) + 64, 48))
        HUD_display.blit(self.direction_label.img, ((self.image.get_width() // 3) + 64, 64))

    def draw_fuel_display(self, HUD_display):
        """
        Draws the fuel portion of your shidpit stats.
        :param HUD_display:
        :return:
        """
        max_height = 64
        pg.draw.rect(HUD_display, GREY50, ((self.image.get_width() * 4) // 6, 16,
                                           32, max_height))
        pg.draw.rect(HUD_display, self.color_list[5], ((HUD_display.get_width() * 4) // 6, 16,
                                                       32,
                                                       (self.ship.current_fuel * max_height //
                                                        self.ship.max_fuel * max_height)
                                                       / max_height))
        