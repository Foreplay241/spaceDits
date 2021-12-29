from GUI.text import Text
from Player.HUD import HUD
from settings import *


class FHUD(HUD):
    def __init__(self, game, ship):
        super(FHUD, self).__init__(game, ship)
        self.color_list = [RED, DARK_RED, LIGHT_RED, RANDOM_RED, PALE_VIOLET_RED, FREE_SPEECH_RED]

    def update(self):
        super(FHUD, self).update()

    def draw(self, window, pos):
        super(FHUD, self).draw(window, pos)
        self.draw_weapons_display(self.image)
        self.draw_target_crosshair()
        window.blit(self.image, (pos[0], pos[1]))

    def draw_target_crosshair(self):
        for e in self.ship.target_list:
            if e.isTarget:
                self.ship.game.screen.blit(self.target_crosshair, (e.position[0] - 32,
                                                                   e.position[1] - 32))

    def draw_weapons_display(self, HUD_display):
        """
        Draw Blaster L, M, R and Pods L, R and Bomb Bay weapon statuses.
        :param HUD_display:
        :return:
        """
        max_height = 48
        i = 0
        b = 0
        # blaster_color = LIGHT_GOLDENROD_YELLOW
        if "Weapons" in self.list_to_display:
            for weapon in self.ship.weapons_dict:
                if weapon.endswith("Blaster"):
                    pg.draw.rect(HUD_display, GREY50,
                                 ((HUD_display.get_width() - 96) + (i * 32), 5, 22, max_height))
                    pg.draw.rect(HUD_display, self.ship.weapons_dict[weapon].HUD_bar_color,
                                 ((HUD_display.get_width() - 96) + (i * 32), 5,
                                  22, (self.ship.weapons_dict[weapon].current_charge * max_height //
                                       self.ship.weapons_dict[weapon].max_charge * max_height) // max_height))

                    i += 1
                elif weapon.endswith("Pod"):
                    self.pod_label = Text(f"Pod:{b + 1}",
                                          (0, 0), DARK_PURPLE, size=16)
                    self.podr_label = Text(f"{self.ship.weapons_dict[weapon].current_missiles}",
                                           (0, 0), DARK_PURPLE, size=16)
                    HUD_display.blit(self.pod_label.img, ((HUD_display.get_width() - 96) + (b * 32), 54))
                    HUD_display.blit(self.podr_label.img, ((HUD_display.get_width() - 96) + (b * 32), 64))
                    b += 1
                elif weapon.endswith("Bay"):
                    self.bay_label = Text(f"BAY: ",
                                          (0, 0), DARK_PURPLE, size=16)
                    self.bayr_label = Text(f"{self.ship.weapons_dict[weapon].current_bombs}",
                                           (0, 0), DARK_PURPLE, size=16)
                    HUD_display.blit(self.bay_label.img, ((HUD_display.get_width() - 96) + (2 * 32), 54))
                    HUD_display.blit(self.bayr_label.img, (HUD_display.get_width() - 32, 64))
