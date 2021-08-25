import os
from PIL import ImageFile, Image, ImageDraw, ImageFilter


class ImageEditor:
    def __init__(self, input_img_path):
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        self.input_img_path = input_img_path
        self.img = Image.open(input_img_path)
        self.width, self.height = self.img.size
        self.should_save_as_png = False

    def trim_square(self):
        square_side = min(self.width, self.height)

        # landscape
        if self.width > self.height:
            left = (self.width - square_side) / 2
            top = 0
            right = left + square_side
            bottom = top + square_side
        # portrait
        else:
            left = 0
            top = (self.height - square_side) / 2
            right = left + square_side
            bottom = top + square_side
        self.img = self.img.crop((left, top, right, bottom))
        self.width, self.height = self.img.size

    def mask_circle_transparent(self, blur_radius=4, offset=0):
        offset = blur_radius * 2 + offset
        mask = Image.new("L", self.img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, self.width - offset, self.height - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        result = self.img.copy()
        result.putalpha(mask)

        self.img = result
        self.should_save_as_png = True

    def save(self, output_folder_path = None):
        if output_folder_path is None:
            root, ext = os.path.splitext(self.input_img_path)
            _ext = ".png" if self.should_save_as_png else ext
            output_img_path = "".join([root, _ext])
        else:
            file_name = os.path.basename(self.input_img_path)
            file_name_exclude_ext, ext = os.path.splitext(file_name)
            _ext = ".png" if self.should_save_as_png else ext
            _file_name = "".join([file_name_exclude_ext, _ext])
            output_img_path = os.path.join(output_folder_path, _file_name)
        self.img.save(output_img_path)
