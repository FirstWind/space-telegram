from datetime import date, timedelta
from os import environ

from additional import download_img, get_response
from dotenv import load_dotenv


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
    DELTA_DATE = int(environ.get('DELTA_DATE'))
    TOKEN_NASA = environ.get('TOKEN_NASA')
    path_images = environ.get('PATH_IMAGES')
    now = date.today() - timedelta(days=1)
    delta_date = now - timedelta(days=DELTA_DATE)
    nasa_query = f"https://api.nasa.gov/planetary/apod?start_date={delta_date}&end_date={now}&api_key={TOKEN_NASA}"
    initial_nasa(nasa_query, path_images)
