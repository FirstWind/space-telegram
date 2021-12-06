import requests
from requests.exceptions import HTTPError
from pathlib import Path
from os import path as os_path, environ, walk
from dotenv import load_dotenv

from telegram.ext import Updater, CommandHandler
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


def get_random_photo():
    return open(choice(get_local_pictures("images/")), "rb")


def send_photo(updater, CHAT_ID):
    updater.bot.send_photo(
        chat_id=CHAT_ID,
        photo=get_random_photo()
        )
    print("Фотография отправлена")


def main(token, chat_id) -> None:
    updater = Updater(token)
    updater.start_polling()
    print("Бот запущен")
    send_photo(updater, chat_id)
    updater.idle()


if __name__ == "__main__":
    select_image_type = int(
        input(
            "Какие картинки будем загружать? Выберите цифру:\n NASA(1)\n NASA EPIC(2)\n SpaceX(3)\n Или не качаем(0)\n >> "
            )
        )
    load_dotenv()
    if select_image_type == 1:
        TOKEN_NASA = environ.get('TOKEN_NASA')
        nasa_query = f"https://api.nasa.gov/planetary/apod?start_date=2021-11-15&end_date=2021-12-02&api_key={TOKEN_NASA}"
        initial_nasa(nasa_query)
    elif select_image_type == 2:
        TOKEN_NASA = environ.get('TOKEN_NASA')
        nasa_query_epic = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={TOKEN_NASA}"
        initial_nasa_epic(nasa_query_epic)
    elif select_image_type == 3:
        space_x_query = "https://api.spacexdata.com/v3/launches/latest?pretty=true"
        json_filter = "?pretty=true&filter=links(flickr_images)"
        initial_space_x(space_x_query, json_filter)

    TOKEN_TELEGRAM = environ.get('TOKEN_TELEGRAM')
    CHAT_ID = environ.get('CHANNEL_TELEGRAM_ID')

    main(TOKEN_TELEGRAM, CHAT_ID)
    send_photo()
    # print(choice(get_local_pictures("images/NASA_EPIC/")))

    print("Закончили")
