import os

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


def download_image(
    image_link: str, image_filename: str, image_folder: str = "./"
) -> str:
    checked_folder = sanitize_filepath(image_folder)
    checked_filename = sanitize_filename(image_filename)
    filepath = os.path.join(checked_folder, checked_filename)
    image_data = get_data_from_link(image_link)
    write_image_to_file(image_data.content, filepath)
    return filepath


def convert_image_to_jpg(image_filepath: str) -> str:
    image = Image.open(image_filepath)
    image_filepath_without_extension, image_extension = os.path.splitext(image_filepath)
    if image_extension == ".jpg":
        return image_filepath
    image_filepath_jpg = f"{ image_filepath_without_extension }.jpg"
    image.save(image_filepath_jpg, format="JPEG")
    if os.path.exists(image_filepath_jpg):
        os.remove(image_filepath)
    return image_filepath_jpg


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
