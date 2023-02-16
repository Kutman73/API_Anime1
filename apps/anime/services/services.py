from api_anime01 import settings
import os


def get_file(path) -> list:
    file_list = []
    prefix_length = str(settings.MEDIA_ROOT)
    project_url = "http://127.0.0.1:8000/media/"
    for file in os.scandir(path):
        if file.is_file():
            file_list.append(project_url + file.path[prefix_length:])
    return file_list
