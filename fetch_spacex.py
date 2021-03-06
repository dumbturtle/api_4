import os
from pathlib import Path

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from dotenv import load_dotenv
from handler import (
    download_image,
    get_response_from_link,
    get_image_extension,
)


def fetch_spacex_launch(
    image_api_link: str, launch_id: str, image_folder: str = "./images"
) -> list:
    image_filepaths = []
    image_launch_link = f"{ image_api_link }/{ launch_id }"
    spacex_api_content = get_response_from_link(image_launch_link)
    spacex_image_links = spacex_api_content.json().get("links").get("flickr_images")
    for image_number, image_link in enumerate(spacex_image_links):
        image_extension = get_image_extension(image_link)
        image_filename = f"{ launch_id }spacex{ image_number}{ image_extension }"
        image_filepath = download_image(image_link, image_filename, image_folder)
        image_filepaths.append(image_filepath)
    return image_filepaths


def main():
    load_dotenv()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    spacex_image_api_link = os.environ["SPACEX_IMAGE_API_LINK"]
    launch_id = os.environ["LAUNCH_ID"]
    image_folder = os.environ["IMAGE_FOLDER"]
    Path(f"./{ image_folder }").mkdir(parents=True, exist_ok=True)
    try:
        fetch_spacex_launch(spacex_image_api_link, launch_id, image_folder)
    except (requests.ConnectionError, requests.HTTPError):
        print("Что-то пошло не так. Проверьте соединение с интернетом.")


if __name__ == "__main__":
    main()
