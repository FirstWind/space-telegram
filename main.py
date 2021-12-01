import requests
from requests.exceptions import HTTPError
from pathlib import Path

def get_response(url):
    response = requests.get(url_img)
    response.raise_for_status()
    return response


def create_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def download_img(url_img, filename):
    try:
        response = get_response(url_img)
        with open(filename, 'wb') as file:
             file.write(response.content)
        print(f"картинку {Path(url_img).name} cкачали успешно")
    except HTTPError as http_err:
        print(f'произошла ошибка HTTP: {http_err}')
        exit()


if __name__ == "__main__":
    url_img = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    save_path = "images/"
    try:
        create_dir(save_path)
        filename = save_path+Path(url_img).name
        download_img(url_img, filename)
    except IOError:
        print("Ошибка в скачивании картинки")
