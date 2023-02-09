from api_anime01 import settings
import os


def base(**kwargs) -> list:
    file_path = settings.BASE_DIR / f"media/{kwargs['original_anime_name']}" \
                                    f"/season-{kwargs['season']}" \
                                    f"/episode-{kwargs['episode']}/"
    file_list = []
    prefix_length = len("/home/kutu/PycharmProjects/api_anime01/media/")
    for file in os.scandir(file_path):
        if file.is_file():
            file_list.append("http://127.0.0.1:8000/media/" + file.path[prefix_length:])
    return file_list
