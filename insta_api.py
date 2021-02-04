import os
from pathlib import Path

import requests
from pathvalidate import sanitize_filename, sanitize_filepath
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def get_data_from_link(link: str) -> requests.models.Response:
    link_response = requests.get(link, verify=False, allow_redirects=False)
    link_response.raise_for_status()
    return link_response


def write_image_to_file(data: bytes, full_path_file: str) -> str:
    with open(full_path_file, "wb") as file:
        file.write(data)
    return full_path_file


def download_image(link: str, filename: str, folder: str = "./") -> str:
    checked_folder = sanitize_filepath(folder)
    checked_filename = sanitize_filename(filename)
    Path(f"./{ folder }").mkdir(parents=True, exist_ok=True)
    string_filepath = f"{ os.path.join(checked_folder, checked_filename) }"
    image_data = get_data_from_link(link)
    file_with_data_filepath = write_image_to_file(image_data.content, string_filepath)
    return file_with_data_filepath


def fetch_spacex_last_launch(link_api: str) -> list:
    image_folder = "./images"
    images_filepaths = []
    spacex_api_conten = get_data_from_link(link_api)
    spacex_image_links = spacex_api_conten.json().get("links").get("flickr_images")
    for image_number, image_link in enumerate(spacex_image_links):
        image_filename = f"spacex{ image_number }.jpg"
        image_filepath = download_image(image_link, image_filename, image_folder)
        images_filepaths.append(image_filepath)
    return images_filepaths


def fetch_hable_photo(link_api: str, image_id: int) -> list:
    image_folder = "./images_hable"
    images_filepaths = []
    hable_api_conten = get_data_from_link(f"{link_api}{image_id}")
    hable_image_links = [
        f'https:{image_info.get("file_url")}'
        for image_info in hable_api_conten.json().get("image_files")
    ]
    for image_number, image_link in enumerate(hable_image_links):
        image_extension = get_image_extension(image_link)
        image_filename = f"hable{ image_number}.{ image_extension }"
        image_filepath = download_image(image_link, image_filename, image_folder)
        images_filepaths.append(image_filepath)
    return images_filepaths


def get_image_extension(link: str) -> str:
    link_extension = link.split(".")[-1]
    return link_extension


def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    spacex_link_api = "https://api.spacexdata.com/v3/launches/67"
    hable_link_api = "http://hubblesite.org//api/v3/image/"
    hable_image_id = 1
    print(fetch_hable_photo(hable_link_api, hable_image_id))


if __name__ == "__main__":
    main()
