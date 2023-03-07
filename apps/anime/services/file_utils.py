from api_anime01 import settings
import hashlib
import os
import pymediainfo
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage


class SearchFiles:
    @staticmethod
    def get_local_files(path: str) -> list:
        file_list = []
        prefix_length = len(str(settings.MEDIA_ROOT))
        project_url = "http://127.0.0.1:8000/media"
        for file in os.scandir(path):
            if file.is_file():
                file_list.append(project_url + file.path[prefix_length:])
        return file_list


class FileCheck:
    @staticmethod
    def check_local_file_exist(path: str) -> bool | str:
        if os.path.isfile(path):
            return False
        return path

    @staticmethod
    def check_file_size(file) -> ValidationError or None:
        byte_limit = 3
        if file.size > byte_limit * 1024 * 1024:
            raise ValidationError(f"Max size file {byte_limit}MB")


class FileModify:
    @staticmethod
    def get_video_quality(instance, unique_id: int, fieldname: str) -> str:
        video_file = getattr(instance, fieldname)
        media_info = pymediainfo.MediaInfo.parse(video_file)
        video_track = media_info.tracks[1]
        resolution = video_track.height
        bitrate = video_track.bit_rate

        if resolution >= 1080 and bitrate >= 4000:
            return f"{unique_id}-1080p-"
        elif resolution >= 720 and bitrate >= 2000:
            return f"{unique_id}-720p-"
        elif resolution >= 480 and bitrate >= 1300:
            return f"{unique_id}-480p-"
        elif resolution >= 360 and bitrate >= 1000:
            return f"{unique_id}-360p-"
        elif resolution >= 240 and bitrate >= 500:
            return f"{unique_id}-240p-"
        else:
            return "other"

    @staticmethod
    def get_filename_hash(instance, fieldname: str) -> str:
        hash256 = hashlib.sha256()
        field_file = getattr(instance, fieldname)
        for byte_chunk in field_file.chunks():
            hash256.update(byte_chunk)
        hashed_name_of_the_anime = hash256.hexdigest()
        return f"{hashed_name_of_the_anime}"


class FilePath:
    @staticmethod
    def get_path_to_cover_anime(instance, filename) -> str:
        format_file = os.path.splitext(filename)[1].lower()
        path_to_cover_anime = f"{instance.slug}/cover/"
        hashed_filename = FileModify.get_filename_hash(instance, 'cover')
        path = os.path.join(path_to_cover_anime, hashed_filename)
        end_path = FileCheck.check_local_file_exist(path + format_file)
        if end_path:
            return end_path
        return ''

    @staticmethod
    def get_path_to_movie(instance, filename) -> str:
        format_file = os.path.splitext(filename)[1].lower()
        path_to_movie = f"{instance.anime.slug}/movie/"
        hashed_filename = FileModify.get_filename_hash(
            instance, 'video'
        )
        video_quality = FileModify.get_video_quality(
            instance, instance.movie_number, 'video'
        )
        end_path = FileCheck.check_local_file_exist(
            os.path.join(
                path_to_movie, video_quality + hashed_filename + format_file
            )
        )
        if end_path:
            return end_path
        return ''

    @staticmethod
    def get_path_to_episode(instance, filename) -> str:
        format_file = os.path.splitext(filename)[1].lower()
        path_to_episode = f"{instance.season.anime.slug}" \
                          f"/season-{instance.season.season_number}/episode-" \
                          f"{instance.episode_number}/"
        hashed_filename = FileModify.get_filename_hash(instance, 'video')
        video_quality = FileModify.get_video_quality(
            instance, instance.episode_number, 'video'
        )
        check_file = FileCheck.check_local_file_exist(
            os.path.join(
                path_to_episode, video_quality + hashed_filename + format_file
            )
        )
        if check_file:
            return check_file
        return ''


class OverWriteStorage(FileSystemStorage):
    def __init__(self):
        super(OverWriteStorage, self).__init__()

    def get_available_name(self, name: str, max_length: int = 100) -> str:
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name
