import os
from pathlib import Path
from PIL import Image

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
    string_filepath = os.path.join(checked_folder, checked_filename)
    image_data = get_data_from_link(link)
    file_with_data_filepath = write_image_to_file(image_data.content, string_filepath)
    return file_with_data_filepath


def fetch_spacex_last_launch(image_link_api: str) -> list:
    image_folder = "./images"
    images_filepaths = []
    spacex_api_conten = get_data_from_link(image_link_api)
    spacex_image_links = spacex_api_conten.json().get("links").get("flickr_images")
    for image_number, image_link in enumerate(spacex_image_links):
        image_filename = f"spacex{ image_number }.jpg"
        image_filepath = download_image(image_link, image_filename, image_folder)
        images_filepaths.append(image_filepath)
    return images_filepaths


def fetch_hable_photo(
    image_link_api: str, image_id: int, image_folder: str = "./images"
) -> list:
    images_filepaths = []
    hable_api_content = get_data_from_link(f"{image_link_api}{image_id}")
    hable_image_links = [
        f'https:{image_info.get("file_url")}'
        for image_info in hable_api_content.json().get("image_files")
    ]
    print(hable_image_links)
    for image_number, image_link in enumerate(hable_image_links):
        image_extension = get_image_extension(image_link)
        image_filename = f"{ image_id }hable{ image_number}.{ image_extension }"
        image_filepath = download_image(image_link, image_filename, image_folder)
        change_image_size_proportions(image_filepath)
        image_filepath_jpg = convert_image_to_jpg(image_filepath)
        print(image_filepath_jpg)
        images_filepaths.append(image_filepath_jpg)
    return images_filepaths


def convert_image_to_jpg(image_filepath: str) -> str:
    image = Image.open(image_filepath)
    image_full_filename = os.path.basename(image_filepath)
    image_extension = os.path.splitext(image_full_filename)[1]
    if image_extension == ".jpg":
        return image_filepath
    image_full_dirpath = os.path.dirname(image_filepath)
    image_filename = os.path.splitext(image_full_filename)[0]
    image_filename_jpg = f"{ image_filename }.jpg"
    image_full_filepath_jpg = os.path.join(image_full_dirpath, image_filename_jpg)
    image.save(image_full_filepath_jpg, format="JPEG")
    if os.path.exists(image_full_filepath_jpg):
        os.remove(image_filepath)
    return image_full_filepath_jpg


def change_image_size_proportions(image_filepath: str):
    image = Image.open(image_filepath)
    height, width = image.size
    if height > 1080 or width > 1080:
        image.thumbnail((1080, 1080))
        image.save(image_filepath)
        return image_filepath
    return image_filepath


def get_image_extension(link: str) -> str:
    link_extension = link.split(".")[-1]
    return link_extension


def fetch_hable_image_id(collection_link_api: str, collection_name: str) -> list:
    hable_api_content = get_data_from_link(f"{collection_link_api}{collection_name}")
    hable_images_id = [image_id.get("id") for image_id in hable_api_content.json()]
    return hable_images_id


def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    spacex_image_link_api = "https://api.spacexdata.com/v3/launches/67"
    hable_image_link_api = "http://hubblesite.org//api/v3/image/"
    hable_collection_link_api = "http://hubblesite.org//api/v3/images/"
    hable_collection_name = "stsci_gallery"
    hable_image_range_id = fetch_hable_image_id(
        hable_collection_link_api, hable_collection_name
    )
    for hable_image_id in hable_image_range_id:
        fetch_hable_photo(hable_image_link_api, hable_image_id)


if __name__ == "__main__":
    main()
