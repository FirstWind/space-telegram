from os import environ
from os import path as os_path

from additional import download_img, get_response
from dotenv import load_dotenv


def fetch_spacex_last_launch(response, path_images):
    for container_img in response.json():
        urls_img = container_img["links"]["flickr_images"]
        if urls_img:
            for url in urls_img:
                download_img(url, path_images)
            exit()


def initial_space_x(url, json_filter, path_images):
    response = get_response(url)
    if response:
        fetch_spacex_last_launch(response, f"{path_images}SpaceX/")
    else:
        space_x_query = os_path.split(url)[0] + json_filter
        response = get_response(space_x_query)
        if response:
            fetch_spacex_last_launch(response, f"{path_images}SpaceX/")


if __name__ == "__main__":
    load_dotenv()
    path_images = environ.get('PATH_IMAGES')
    space_x_query = "https://api.spacexdata.com/v3/launches/latest?pretty=true"
    json_filter = "?pretty=true&filter=links(flickr_images)"
    initial_space_x(space_x_query, json_filter, path_images)
