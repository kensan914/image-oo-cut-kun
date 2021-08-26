from ImageEditor import ImageEditor


def round_image(input_img_path, output_folder_path = None, resize_px=300):
    image_editor = ImageEditor(input_img_path)
    image_editor.compress(resize_px=resize_px)
    image_editor.trim_square()
    image_editor.mask_circle_transparent()
    image_editor.save(output_folder_path)
