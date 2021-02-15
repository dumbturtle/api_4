import os

from dotenv import load_dotenv
from instabot import Bot
from PIL import Image


def check_ratio(image_filepath: str) -> bool:
    image = Image.open(image_filepath)
    height, width = image.size
    ratio = height / width
    ratio_limit = 0.9
    if ratio < ratio_limit:
        return False
    return True


def main():
    load_dotenv()
    bot = Bot()
    images_folder = os.environ["IMAGES_FOLDER"]
    images = os.listdir(images_folder)
    bot.login(
        username=os.environ["INSTAGRAM_USERNAME"],
        password=os.environ["INSTAGRAM_PASSWORD"],
    )
    for image in images:
        string_filepath = os.path.join(images_folder, image)
        if check_ratio(string_filepath):
            bot.upload_photo(string_filepath, caption=string_filepath)
            print(f"{ image }: { bot.api.last_response.status_code }")
            continue
        print(f"Неверное соотношение сторон: { image }")


if __name__ == "__main__":
    main()
