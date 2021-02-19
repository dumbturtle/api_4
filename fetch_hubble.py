import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from handler import (
    change_image_size_proportions,
    convert_image_to_jpg,
    download_image,
    get_response_from_link,
    get_image_extension,
)


def fetch_hubble_photo(
    image_link_api: str, image_id: int, image_folder: str = "./images"
) -> str:
    image_filepaths = []
    hubble_api_content = get_response_from_link(f"{image_link_api}{image_id}")
    hubble_api_image_link = hubble_api_content.json().get(
        "image_files")[-1].get("file_url")
    image_link = f'https:{ hubble_api_image_link }'
    image_extension = get_image_extension(image_link)
    image_filename = f"{ image_id }hubble{ image_extension }"
    image_filepath = download_image(image_link, image_filename, image_folder)
    return image_filepath


def fetch_hubble_image_ids(collection_api_link: str, collection_name: str) -> list:
    hubble_api_content = get_response_from_link(
        f"{ collection_api_link }{ collection_name }"
    )
    hubble_image_ids = [
        image_information.get("id") for image_information in hubble_api_content.json()
    ]
    return hubble_image_ids


def main():
    load_dotenv()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    hubble_image_api_link = os.environ["HUBBLE_IMAGE_API_LINK"]
    hubble_collection_api_link = os.environ["HUBBLE_COLLECTION_API_LINK"]
    hubble_collection_name = os.environ["HUBBLE_COLLECTION_NAME"]
    image_folder = os.environ["IMAGE_FOLDER"]
    Path(f"./{ image_folder }").mkdir(parents=True, exist_ok=True)
    try:
        hubble_image_ids = fetch_hubble_image_ids(
            hubble_collection_api_link, hubble_collection_name
        )
        for hubble_image_id in hubble_image_ids:
            fetched_images = fetch_hubble_photo(
                hubble_image_api_link, hubble_image_id, image_folder
            )
    except (requests.ConnectionError, requests.HTTPError):
        print("Что-то пошло не так. Проверьте соединение с интернетом.")


if __name__ == "__main__":
    main()
