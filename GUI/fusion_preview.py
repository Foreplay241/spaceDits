from GUI.button import Button
from settings import *


class FusionPreview(Button):
    def __init__(self, id_num, pos, BGimg, FGimg, scale=(1, 1), col=1, max_col=3, row=1, max_row=3):
        super().__init__(id_num, pos, BGimg, FGimg)
        self.id_num = id_num
        self.pos = pos
        self.image = pg.transform.scale(self.image, (int(128 * scale[0]), int(128 * scale[1])))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.orig_image = self.image
        self.orig_rect = self.rect

        self.column = col
        self.row = row
        self.max_column = max_col
        self.max_row = max_row

        self.fusion = None
        self.img = None
        self.info = None
        self.selected = False
        self.submission_id = id_num
        self.fusion_angle = 0

    def rotate_center(self, surf, image, pos, originPos, angle):
        img_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
        offset_center_to_pivot = pg.math.Vector2(pos) - img_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = pg.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
        surf.blit(rotated_image, rotated_image_rect)

    def set_img(self, newImg):
        """
        Sets the image for the preview.
        :param newImg:
        :return:
        """
        self.img = newImg

    def set_info(self, newImg):
        """
        Sets the info image for the preview.
        :param newImg:
        :return:
        """
        self.info = newImg

    def update_image(self, newBGimg, newFGimg):
        super(FusionPreview, self).update_image(newBGimg, newFGimg)

    def events(self):
        pass

    def update(self):
        super(FusionPreview, self).update()

    def draw(self, window):
        super(FusionPreview, self).draw(window)
        if not self.fusion:
            self.rotate_center(window, self.FGimage, (self.pos[0] + 64, self.pos[1] + 64), (64, 64), self.fusion_angle)
            self.fusion_angle += 1
        if self.selected:
            pg.draw.rect(window, GREY50, self.rect, 2)

    def draw_selection_outline(self):
        pg.draw.rect(self.image, GOLDENROD, self.rect)

    def flip_to_info(self):
        self.image = self.info

    def flip_to_img(self):
        self.image = self.img
