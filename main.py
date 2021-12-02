import requests
from requests.exceptions import HTTPError
from pathlib import Path
from os import path as os_path


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def create_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_extension(url):
    ext = os_path.splitext(url)[1]
    return ext.split("?")[0]


def download_img(url, path_image):
    try:
        filename = path_image + os_path.basename(url)
        response = get_response(url)
        with open(filename, 'wb') as file_img:
            file_img.write(response.content)
        print(f"картинку {os_path.basename(url)} cкачали успешно")
    except HTTPError as http_err:
        print(f'произошла ошибка HTTP: {http_err}')
        exit()


def fetch_spacex_last_launch(url, path_image):
    try:
        response = get_response(url)
        for container_img in response.json():
            urls = container_img["links"]["flickr_images"]
            if urls:
                for url in urls:
                    download_img(url, path_image)
                exit()
    except HTTPError as http_err:
        print(f'произошла ошибка HTTP: {http_err}')
        exit()


if __name__ == "__main__":
    url_space_x_latest = "https://api.spacexdata.com/v3/launches/latest?pretty=true"
    json_filter = "?pretty=true&filter=links(flickr_images)"
    nasa_query = "https://api.nasa.gov/planetary/apod?api_key=NkcWH3O7Q7oL5bNRKGN21Q5CXJfH7yDcEHR7mWXw"
    save_path = "images/Nasa/"
    try:
        # get_response(url_space_x_latest)
        # fetch_spacex_last_launch(url_space_x_latest, save_path)
        get_response(nasa_query)
        fetch_spacex_last_launch(nasa_query, save_path)
    except HTTPError:
        url_space_x = os_path.split(url_space_x_latest)[0] + json_filter
        fetch_spacex_last_launch(url_space_x, save_path)
        print("Успешно закончили")

