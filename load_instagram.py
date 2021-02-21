import os

from dotenv import load_dotenv
from instabot import Bot
from PIL import Image

from handler import reduce_photo_size_preserving_proportions, convert_image_to_jpg


def check_ratio(image_filepath: str) -> bool:
    image = Image.open(image_filepath)
    height, width = image.size
    ratio = height / width
    ratio_limit = 0.9
    return ratio > ratio_limit


def main():
    load_dotenv()
    bot = Bot()
    image_folder = os.environ["IMAGE_FOLDER"]
    images = os.listdir(image_folder)
    bot.login(
        username=os.environ["INSTAGRAM_USERNAME"],
        password=os.environ["INSTAGRAM_PASSWORD"],
    )
    for image in images:
        filepath = os.path.join(image_folder, image)
        reduce_photo_size_preserving_proportions(filepath)
        image_jpg_filepath = convert_image_to_jpg(filepath)
        if not check_ratio(image_jpg_filepath):
            print(f"Неверное соотношение сторон: { image }")
            continue
        bot.upload_photo(image_jpg_filepath, caption=filepath)


if __name__ == "__main__":
    main()
