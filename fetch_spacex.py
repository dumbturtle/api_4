import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from handler import (
    change_image_size_proportions,
    convert_image_to_jpg,
    download_image,
    get_data_from_link,
)


def fetch_spacex_launch(
    image_link_api: str, launche_id: str, image_folder: str = "./images"
) -> list:
    images_filepaths = []
    image_link_api = f"{ image_link_api }/{ launche_id }"
    spacex_api_conten = get_data_from_link(image_link_api)
    spacex_image_links = spacex_api_conten.json().get("links").get("flickr_images")
    for image_number, image_link in enumerate(spacex_image_links):
        image_filename = f"{ launche_id }spacex{ image_number }.jpg"
        image_filepath = download_image(image_link, image_filename, image_folder)
        change_image_size_proportions(image_filepath)
        image_filepath_jpg = convert_image_to_jpg(image_filepath)
        images_filepaths.append(image_filepath_jpg)
    return images_filepaths


def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    spacex_image_link_api = "https://api.spacexdata.com/v3/launches"
    launche_id = "67"
    try:
        fetched_images = fetch_spacex_launch(spacex_image_link_api, launche_id)
        print(fetched_images)
    except (requests.ConnectionError, requests.HTTPError):
        print("Что-то пошло не так. Проверьте соединение с интернетом.")


if __name__ == "__main__":
    main()
