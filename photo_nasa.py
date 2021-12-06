from dotenv import load_dotenv
from os import environ

from additional import download_img
from additional import get_response


def fetch_nasa(response, path_images):
    for container_img in response.json():
        if container_img["url"]:
            download_img(container_img["url"], path_images)


def initial_nasa(url, path_images):
    response = get_response(url)
    if response:
        fetch_nasa(response, f"{path_images}NASA/")


if __name__ == "__main__":
    load_dotenv()
    TOKEN_NASA = environ.get('TOKEN_NASA')
    path_images = environ.get('PATH_IMAGES')
    nasa_query = f"https://api.nasa.gov/planetary/apod?start_date=2021-11-15&end_date=2021-12-02&api_key={TOKEN_NASA}"
    initial_nasa(nasa_query, path_images)
