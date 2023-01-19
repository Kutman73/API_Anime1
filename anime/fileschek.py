import hashlib
import os
from django.core.files.storage import FileSystemStorage
from api_anime01 import settings
from django.http import Http404


def upload_cover(instance, filename, fieldname):
    format_file = os.path.splitext(filename)[1].lower()
    if format_file != '.png':
        return Http404()

    name_of_the_anime = instance.original_anime_name.lower()
    hash256 = hashlib.sha256()
    file = getattr(instance, fieldname)
    path = f"/home/kutu/PycharmProjects/api_anime/media/cover/{name_of_the_anime}/{file}"

    if os.path.exists(path):
        print("file is already")  # if such file already exists it will not add this file

    for byte_chunk in file.chunks():
        hash256.update(byte_chunk)

    encrypted_name_of_the_anime = hash256.hexdigest()
    file_address = os.path.join(
        name_of_the_anime,
        encrypted_name_of_the_anime + format_file,
    )
    return file_address


def upload_movie(instance, filename, fieldname):
    format_file = os.path.splitext(filename)[1].lower()
    if format_file != '.mp4':
        return Http404()

    name_of_the_anime = instance.anime_movie.original_anime_name.lower()
    hash256 = hashlib.sha256()
    file = getattr(instance, fieldname)
    path = f"/home/kutu/PycharmProjects/api_anime/media/movie/{name_of_the_anime}/{file}"

    if os.path.exists(path):
        print("file is already")  # if such file already exists it will not add this file

    for byte_chunk in file.chunks():
        hash256.update(byte_chunk)

    encrypted_name_of_the_anime = hash256.hexdigest()
    file_address = os.path.join(
        name_of_the_anime,
        encrypted_name_of_the_anime + format_file,
    )
    return file_address


def upload_episode(instance, filename, fieldname):
    format_file = os.path.splitext(filename)[1].lower()
    if format_file != '.mp4':
        return Http404()

    name_of_the_anime = instance.anime.original_anime_name.lower()
    season_number = instance.anime_season.season_number
    hash256 = hashlib.sha256()
    file = getattr(instance, fieldname)
    path = f"/home/kutu/PycharmProjects/api_anime/media/" \
           f"{name_of_the_anime}/season-{season_number}/{file}"

    if os.path.exists(path):
        print("file is already")  # if such file already exists it will not add

    for byte_chunk in file.chunks():
        hash256.update(byte_chunk)

    encrypted_name_of_the_anime = hash256.hexdigest()
    file_address = os.path.join(
        name_of_the_anime,
        str(season_number),
        encrypted_name_of_the_anime + format_file,
    )
    return file_address


class OverWriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=100):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
