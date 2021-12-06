import requests
from requests.exceptions import HTTPError
from pathlib import Path
from os import path as os_path, walk
from random import choice


def get_local_pictures(path_img):
    local_pictures = []
    for files in walk(path_img):
        for file in files[2]:
            if file:
                local_pictures.append(os_path.join(files[0], file))
    return local_pictures


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


def get_random_photo():
    return open(choice(get_local_pictures("images/")), "rb")
