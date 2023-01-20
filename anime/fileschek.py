import os
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from api_anime01 import settings


def check_file_anime_cover_size(file_object) -> None:
    file_limit = 3  # field is a Byte
    if file_object.size > file_limit * 1024 * 1024:
        raise ValidationError(f"Max size file {file_limit}MB")


def get_path_to_cover_anime(instance, file) -> str:
    """ The path to the file
        Path format: media/(original_anime_name)/cover/(photo).png
    """
    return f"{instance.original_anime_name}/cover/{file}"


def get_path_to_movie(instance, file) -> str:
    return f"{instance.anime_movie.original_anime_name}/movie/{file}"


def get_path_to_episode(instance, file) -> str:
    return f"{instance.anime.original_anime_name}" \
           f"/season-{instance.anime_season.season_number}/episode/{file}"


class OverWriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=100):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
