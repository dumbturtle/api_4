import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from handler import (
    change_image_size_proportions,
    convert_image_to_jpg,
    download_image,
    get_data_from_link,
)


def fetch_spacex_launch(
    image_link_api: str, launch_id: str, image_folder: str = "./images"
) -> list:
    image_filepaths = []
    image_link_api = f"{ image_link_api }/{ launch_id }"
    spacex_api_content = get_data_from_link(image_link_api)
    spacex_image_links = spacex_api_content.json().get("links").get("flickr_images")
    for image_number, image_link in enumerate(spacex_image_links):
        image_filename = f"{ launch_id }spacex{ image_number }.jpg"
        image_filepath = download_image(image_link, image_filename, image_folder)
        change_image_size_proportions(image_filepath)
        image_jpg_filepath = convert_image_to_jpg(image_filepath)
        image_filepaths.append(image_jpg_filepath)
    return image_filepaths


def main():
    load_dotenv()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    spacex_image_link_api = os.environ["SPACEX_IMAGE_LINK_API"]
    launch_id = os.environ["LAUNCH_ID"]
    image_folder = os.environ["IMAGE_FOLDER"]
    Path(f"./{ image_folder }").mkdir(parents=True, exist_ok=True)
    try:
        fetched_images = fetch_spacex_launch(
            spacex_image_link_api, launch_id, image_folder
        )
        print(fetched_images)
    except (requests.ConnectionError, requests.HTTPError):
        print("Что-то пошло не так. Проверьте соединение с интернетом.")


if __name__ == "__main__":
    main()
