import os
from urllib.parse import unquote, urlsplit

import requests
from pathvalidate import sanitize_filename, sanitize_filepath
from PIL import Image


def get_data_from_link(link: str) -> requests.models.Response:
    link_response = requests.get(link, verify=False, allow_redirects=False)
    link_response.raise_for_status()
    return link_response


def write_image_to_file(data: bytes, filepath: str) -> str:
    with open(filepath, "wb") as file:
        file.write(data)


def download_image(
    image_link: str, image_filename: str, image_folder: str = "./"
) -> str:
    sanitized_folder = sanitize_filepath(image_folder)
    sanitized_filename = sanitize_filename(image_filename)
    filepath = os.path.join(sanitized_folder, sanitized_filename)
    image_data = get_data_from_link(image_link)
    write_image_to_file(image_data.content, filepath)
    return filepath


def convert_image_to_jpg(image_filepath: str) -> str:
    image = Image.open(image_filepath)
    image_filepath_without_extension, image_extension = os.path.splitext(image_filepath)
    if image_extension == ".jpg":
        return image_filepath
    try:
        image_filepath_with_jpg_extension = f"{ image_filepath_without_extension }.jpg"
        image.save(image_filepath_with_jpg_extension, format="JPEG")
    finally:
        os.remove(image_filepath)
    return image_filepath_with_jpg_extension


def change_image_size_proportions(image_filepath: str):
    image = Image.open(image_filepath)
    image_height, image_width = image.size
    image_height_limit = 1080
    image_width_limit = 1080
    if image_height > image_height_limit or image_width > image_width_limit:
        image.thumbnail((image_height_limit, image_width_limit))
        image.save(image_filepath)


def get_image_extension(image_link: str) -> str:
    image_link_parse = urlsplit(image_link)
    image_path = unquote(image_link_parse.path)
    image_extension = os.path.splitext(image_path)[1]
    return image_extension
