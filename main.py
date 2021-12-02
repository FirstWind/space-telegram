import requests
from requests.exceptions import HTTPError
from pathlib import Path
from os import path as os_path, environ
from dotenv import load_dotenv


def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except HTTPError:
        response.ok


def create_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_extension(url):
    ext = os_path.splitext(url)[1]
    return ext.split("?")[0]


def download_img(url, path_image):
    filename = path_image + os_path.basename(url)
    filename = filename.split("?")[0]
    response = get_response(url)
    if not os_path.isdir(path_image):
        create_dir(path_image)
    if response:
        try:
            with open(filename, 'wb') as file_img:
                file_img.write(response.content)
            print(f"картинку {filename} cкачали успешно")
        except IOError as error:
            print(f"Ошибка: {error}")


def fetch_spacex_last_launch(response, path_image):
    for container_img in response.json():
        urls_img = container_img["links"]["flickr_images"]
        if urls_img:
            for url in urls_img:
                download_img(url, path_image)
            exit()


def fetch_nasa(response, path_image):
    for container_img in response.json():
        if container_img["url"]:
            download_img(container_img["url"], path_image)


def fetch_nasa_epic(response, path_image):
    for container_img in response.json():
        if container_img["image"]:
            image = container_img["image"]
        if container_img["date"]:
            date = container_img["date"]
            date = date[:10]
            date = "/".join(date.rsplit("-"))
        url = f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image}.png?api_key={TOKEN_NASA}"
        download_img(url, path_image)


def initial_space_x(url, json_filter):
    save_path = "images/SpaceX/"
    response = get_response(url)
    if response:
        fetch_spacex_last_launch(response, save_path)
    else:
        space_x_query = os_path.split(url)[0] + json_filter
        response = get_response(space_x_query)
        if response:
            fetch_spacex_last_launch(response, save_path)


def initial_nasa(url):
    save_path = "images/NASA/"
    response = get_response(url)
    if response:
        fetch_nasa(response, save_path)


def initial_nasa_epic(url):
    save_path = "images/NASA_EPIC/"
    response = get_response(url)
    if response:
        fetch_nasa_epic(response, save_path)


if __name__ == "__main__":
    load_dotenv()
    TOKEN_NASA = environ.get('TOKEN_NASA')
    space_x_query = "https://api.spacexdata.com/v3/launches/latest?pretty=true"
    nasa_query = f"https://api.nasa.gov/planetary/apod?start_date=2021-11-15&end_date=2021-12-02&api_key={TOKEN_NASA}"
    nasa_query_epic = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={TOKEN_NASA}"
    json_filter = "?pretty=true&filter=links(flickr_images)"
    # initial_space_x(space_x_query, json_filter)
    initial_nasa(nasa_query)
    # initial_nasa_epic(nasa_query_epic)

    print("Закончили")
