import hashlib
import os
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from api_anime01 import settings


def file_hashing(instance, filename: str, fieldname: str) -> str:
    """
    Receives 'instance', is a class model
        type: class(model class instance), 'filename' is a filename,
        type: str(filename), 'fieldname' is a 'instance' field,
        type: str(instance fieldname).
    Return path renamed the filename to its hash(hashlib.sha256),
        type: str.
    """
    hash256 = hashlib.sha256()
    format_file = os.path.splitext(filename)[1].lower()
    field_file = getattr(instance, fieldname)
    for byte_chunk in field_file.chunks():
        hash256.update(byte_chunk)
    encrypted_name_of_the_anime = hash256.hexdigest()
    return f"{encrypted_name_of_the_anime + format_file}"


def file_exist_check(path: str) -> bool or int:
    """
    Receives 'path',
        type: str.
    Return False if a file exists at this 'path',
        else return 'path'.
    Note!!!
        This function checks files exactly by hash.
    """
    if os.path.isfile(path):
        return False
    return path


def check_file_anime_cover_size(file_object) -> ValidationError or None:
    """
    Receives 'file_object',
        type: django.db.models.fields.files.ImageFieldFile.
    Checking data size.
    Return ValidationError if file size in excess of 'file_limit'
    """
    file_limit = 3  # field is a Byte
    if file_object.size > file_limit * 1024 * 1024:
        raise ValidationError(f"Max size file {file_limit}MB")


def get_path_to_cover_anime(instance, filename) -> str:
    """
    Receives 'instance' is a class model,
        type: class(model class instance),
    'filename' is the name of the uploaded file with extension,
        type: str(filename).
    Return path, renamed file name,
        type: str.
    """
    path_to_cover_anime = f"{instance.original_anime_name}/cover/"
    hashed_filename = file_hashing(instance, filename, 'cover_anime')
    path = os.path.join(path_to_cover_anime, hashed_filename)
    end_path = file_exist_check(path)
    if end_path:
        return end_path
    return ''


def get_path_to_movie(instance, filename) -> str:
    """
    Receives 'instance' is a class model,
        type: class(model class instance),
    'filename' is the name of the uploaded file with extension,
        type: str(filename).
    Return path, renamed file name,
        type: str.
    """
    path_to_movie = f"{instance.anime_movie.original_anime_name}/movie/"
    hashed_filename = file_hashing(instance, filename, 'anime_movie_video')
    path = os.path.join(path_to_movie, hashed_filename)
    end_path = file_exist_check(path)
    if end_path:
        return end_path
    return ''


def get_path_to_episode(instance, filename) -> str:
    """
    Receives 'instance' is a class model,
        type: class(model class instance),
    'filename' is the name of the uploaded file with extension,
        type: str(filename).
    Return path, renamed file name,
        type: str.
    """
    path_to_episode = f"{instance.anime.original_anime_name}/season-" \
                      f"{instance.anime_season.season_number}/"
    hashed_filename = file_hashing(instance, filename, 'anime_video')
    path = os.path.join(path_to_episode, hashed_filename)
    end_path = file_exist_check(path)
    if end_path:
        return end_path
    return ''


class OverWriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=100):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
