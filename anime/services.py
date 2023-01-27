from api_anime01 import settings
import os


def base(**kwargs):
    file_path = settings.BASE_DIR / f"media/{kwargs['original_anime_name']}" \
                                    f"/season-{kwargs['season']}" \
                                    f"/episode-{kwargs['episode']}/"
    file_list = []
    for files in os.listdir(file_path):
        file = f"{file_path}/{files}"
        if os.path.isfile(file):
            file_list.append(f"http://127.0.0.1:8000/media/{file[45:]}")
    return file_list
