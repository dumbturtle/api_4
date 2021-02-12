import os
from pathlib import Path

import requests
from pathvalidate import sanitize_filename, sanitize_filepath
from PIL import Image


def get_data_from_link(link: str) -> requests.models.Response:
    link_response = requests.get(link, verify=False, allow_redirects=False)
    link_response.raise_for_status()
    return link_response


def write_image_to_file(data: bytes, full_path_file: str) -> str:
    with open(full_path_file, "wb") as file:
        file.write(data)
    return full_path_file


def download_image(
    image_link: str, image_filename: str, image_folder: str = "./"
) -> str:
    checked_folder = sanitize_filepath(image_folder)
    checked_filename = sanitize_filename(image_filename)
    Path(f"./{ image_folder }").mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(checked_folder, checked_filename)
    image_data = get_data_from_link(image_link)
    file_with_data_filepath = write_image_to_file(image_data.content, filepath)
    return file_with_data_filepath


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


def get_image_extension(image_link: str) -> str:
    link_image_extension = image_link.split(".")[-1]
    return link_image_extension
