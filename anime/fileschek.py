import hashlib
import os
import pymediainfo
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from typing import Union
from django.db.models.fields.files import ImageFieldFile


class FileCheck:
    @staticmethod
    def file_exist_check(path: str) -> Union[bool, str]:
        """
        Check if a file already exists in the given path.

        Parameters:
            path (str): The file path.

        Returns:
            bool : False if the file already exists at the given path,
            str : The path if the file does not exist.
        """
        if os.path.isfile(path):
            return False
        return path

    @staticmethod
    def check_file_anime_cover_size(file_object: ImageFieldFile) -> ValidationError or None:
        """
        Check if the file size of the file_object is within the limit.

        Parameters:
            file_object: django.db.models.fields.files.ImageFieldFile.

        Returns:
            ValidationError: if file size exceeds the file_limit
            None: if file size is within limit
        """
        print(type(file_object))
        file_limit = 3  # field is a Byte
        if file_object.size > file_limit * 1024 * 1024:
            raise ValidationError(f"Max size file {file_limit}MB")


class FileModify:
    @staticmethod
    def adding_video_quality(instance, fieldname: str) -> str:
        """
        Checking_video_quality is a method of the FileStorage class that is used to check the
        video quality of a file.
        The method takes in two arguments:
        - instance: an instance of a class model that contains the file.
        - fieldname: a string representing the name of the field on the class model instance that
        contains the file.
        The method uses the pymediainfo library to parse the file and extract information about
        the video track. It then checks the height (resolution) and bitrate of the video track and
        compares it to predefined values to determine the video quality.
        """
        video_file = getattr(instance, fieldname)
        media_info = pymediainfo.MediaInfo.parse(video_file)
        video_track = media_info.tracks[1]
        resolution = video_track.height
        bitrate = video_track.bit_rate

        if resolution >= 1080 and bitrate >= 4000:
            return f"{instance.episode_number}-1080p-"
        elif resolution >= 720 and bitrate >= 2000:
            return f"{instance.episode_number}-720p-"
        elif resolution >= 480 and bitrate >= 1300:
            return f"{instance.episode_number}-480p-"
        elif resolution >= 360 and bitrate >= 1000:
            return f"{instance.episode_number}-360p-"
        elif resolution >= 240 and bitrate >= 500:
            return f"{instance.episode_number}-240p-"
        else:
            return "other"

    @staticmethod
    def file_hashing(instance, fieldname: str) -> str:
        """
        Hashes a file's name and returns the hash as a string.
        Parameters:
            instance (class): A class model instance.
            fieldname (str): The field name on the class model instance.
        Returns:
            str: The hashed file name.
        """
        hash256 = hashlib.sha256()
        field_file = getattr(instance, fieldname)
        for byte_chunk in field_file.chunks():
            hash256.update(byte_chunk)
        hashed_name_of_the_anime = hash256.hexdigest()
        return f"{hashed_name_of_the_anime}"


class FilePath:
    @staticmethod
    def get_path_to_cover_anime(instance, filename) -> str:
        """
        Returns the path for storing the anime movie.

        Parameters:
            instance (class): A class model instance.
            filename (str): The file's name.

        Returns:
            str: The path where the anime movie should be stored.
        """
        format_file = os.path.splitext(filename)[1].lower()
        path_to_cover_anime = f"{instance.original_anime_name}/cover/"
        hashed_filename = FileModify.file_hashing(instance, 'cover_anime')
        path = os.path.join(path_to_cover_anime, hashed_filename)
        end_path = FileCheck.file_exist_check(path + format_file)
        if end_path:
            return end_path
        return ''

    @staticmethod
    def get_path_to_movie(instance, filename) -> str:
        """
        Returns the path for storing the anime movie.

        Parameters:
            instance (class): A class model instance.
            filename (str): The file's name.

        Returns:
            str: The path where the anime movie should be stored.
        """
        format_file = os.path.splitext(filename)[1].lower()
        path_to_movie = f"{instance.anime_movie.original_anime_name}/movie/"
        hashed_filename = FileModify.file_hashing(instance, 'anime_movie_video')
        video_quality = FileModify.adding_video_quality(instance, 'anime_movie_video')
        path = os.path.join(path_to_movie, hashed_filename + video_quality + format_file)
        end_path = FileCheck.file_exist_check(path)
        if end_path:
            return end_path
        return ''

    @staticmethod
    def get_path_to_episode(instance, filename) -> str:
        """
        Returns the path for storing the anime episode.

        Parameters:
            instance (class): A class model instance.
            filename (str): The file's name.

        Returns:
            str: The path where the anime episode should be stored.
        """
        format_file = os.path.splitext(filename)[1].lower()
        path_to_episode = f"{instance.anime.original_anime_name}/season-" \
                          f"{instance.anime_season.season_number}/episode-" \
                          f"{instance.episode_number}/"
        hashed_filename = FileModify.file_hashing(instance, 'anime_video')
        video_quality = FileModify.adding_video_quality(instance, 'anime_video')
        check_path_to_episode = FileCheck.file_exist_check(
            os.path.join(path_to_episode, video_quality + hashed_filename + format_file)
        )
        if check_path_to_episode:
            return check_path_to_episode
        return ''


class OverWriteStorage(FileSystemStorage):
    """
    A storage class that overwrites files with the same name when uploading new files.
    """
    def __init__(self):
        """
        Initializes the storage by calling the parent class's __init__ method.
        """
        super(OverWriteStorage, self).__init__()

    def get_available_name(self, name: str, max_length: int = 100) -> str:
        """
        Determines the available name for a file being stored.

        Parameters:
            - name (str): The desired name of the file being stored.
            - max_length (int): The maximum length of the file name. Defaults to 100.

        Returns:
            str: The final name of the file.
        """
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name
