from dotenv import load_dotenv
from os import environ

from additional import download_img
from additional import get_response


def fetch_nasa_epic(response, path_images):
    for container_img in response.json():
        if container_img["image"]:
            image = container_img["image"]
        if container_img["date"]:
            date = container_img["date"]
            date = date[:10]
            date = "/".join(date.rsplit("-"))
        url = f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image}.png?api_key={TOKEN_NASA}"
        download_img(url, path_images)


def initial_nasa_epic(url, path_images):
    response = get_response(url)
    if response:
        fetch_nasa_epic(response, f"{path_images}SpaceX/")


if __name__ == "__main__":
    load_dotenv()
    path_images = environ.get('PATH_IMAGES')
    TOKEN_NASA = environ.get('TOKEN_NASA')
    nasa_query_epic = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={TOKEN_NASA}"
    initial_nasa_epic(nasa_query_epic, path_images)