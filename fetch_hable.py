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
    get_image_extension,
)


def fetch_hable_photo(
    image_link_api: str, image_id: int, image_folder: str = "./images"
) -> list:
    images_filepaths = []
    hable_api_content = get_data_from_link(f"{image_link_api}{image_id}")
    hable_image_links = [
        f'https:{image_info.get("file_url")}'
        for image_info in hable_api_content.json().get("image_files")
    ]
    for image_number, image_link in enumerate(hable_image_links):
        image_extension = get_image_extension(image_link)
        image_filename = f"{ image_id }hable{ image_number}.{ image_extension }"
        image_filepath = download_image(image_link, image_filename, image_folder)
        change_image_size_proportions(image_filepath)
        image_filepath_jpg = convert_image_to_jpg(image_filepath)
        images_filepaths.append(image_filepath_jpg)
    return images_filepaths


def fetch_hable_image_id(collection_link_api: str, collection_name: str) -> list:
    hable_api_content = get_data_from_link(f"{collection_link_api}{collection_name}")
    hable_images_id = [image_id.get("id") for image_id in hable_api_content.json()]
    return hable_images_id


def main():
    load_dotenv()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    hable_image_link_api = os.environ["HABLE_IMAGE_LINK_API"]
    hable_collection_link_api = os.environ["HABLE_COLLECTION_LINK_API"]
    hable_collection_name = os.environ["HABLE_COLLECTION_NAME"]
    image_folder = os.environ["IMAGE_FOLDER"]
    Path(f"./{ image_folder }").mkdir(parents=True, exist_ok=True)
    try:
        hable_image_range_id = fetch_hable_image_id(
            hable_collection_link_api, hable_collection_name
        )
        for hable_image_id in hable_image_range_id:
            fetched_images = fetch_hable_photo(
                hable_image_link_api, hable_image_id, image_folder
            )
            print(fetched_images)
    except (requests.ConnectionError, requests.HTTPError):
        print("Что-то пошло не так. Проверьте соединение с интернетом.")


if __name__ == "__main__":
    main()
