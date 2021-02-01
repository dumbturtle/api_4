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
    folder = "./images"
    images_filepaths = []
    try:
        spacex_api_conten = get_data_from_link(link_api)
        spacex_image_links = spacex_api_conten.json().get("links").get("flickr_images")
        for image_number, link in enumerate(spacex_image_links):
            filename = f"spacex{ image_number }.jpg"
            image_filepath = download_image(link, filename, folder)
            images_filepaths.append(image_filepath)
    except (requests.ConnectionError, requests.HTTPError):
        images_filepaths = ["Что-то пошло не так:( Проверьте подключение к интернету!"]
    return images_filepaths


def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    spacex_link_api = "https://api.spacexdata.com/v3/launches/67"
    print(fetch_spacex_last_launch(spacex_link_api))


if __name__ == "__main__":
    main()
