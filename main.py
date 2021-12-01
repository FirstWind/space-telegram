import requests
from requests.exceptions import HTTPError
from pathlib import Path


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def create_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def get_file_ext(url):
    ext = url.split(".")[-1]
    return ext.split("?")[0]


def download_img(url, path):
    try:
        filename = path + Path(url).name
        response = get_response(url)
        with open(filename, 'wb') as file_img:
            file_img.write(response.content)
        print(f"картинку {Path(url).name} cкачали успешно")
    except HTTPError as http_err:
        print(f'произошла ошибка HTTP: {http_err}')
        exit()


def fetch_spacex_last_launch(url, path):
    try:
        response = get_response(url)
        for container_img in response.json():
            urls = container_img["links"]["flickr_images"]
            if urls:
                for url in urls:
                    download_img(url, path)
                exit()
    except HTTPError as http_err:
        print(f'произошла ошибка HTTP: {http_err}')
        exit()


if __name__ == "__main__":
    url_space_x_latest = "https://api.spacexdata.com/v3/launches/latest?pretty=true"
    json_filter = "?pretty=true&filter=links(flickr_images)"
    save_path = "images/SpaceX/"
    try:
        create_dir(save_path)
        try:
            get_response(url_space_x_latest)
            fetch_spacex_last_launch(url_space_x_latest, save_path)
        except:
            url_space_x = "/".join(["/".join(url_space_x_latest.split("/")[0:-1]), json_filter])
            fetch_spacex_last_launch(url_space_x, save_path)
        print("Успешно закончили")
    except IOError:
        print("Ошибка в скачивании картинки")
