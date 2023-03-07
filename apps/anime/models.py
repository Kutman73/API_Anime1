from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Avg
from django.core.validators import FileExtensionValidator
from apps.anime.services.file_utils import *


class Genre(models.Model):
    """Creation a genre model"""
    genre_name = models.CharField(max_length=50,
                                  unique=True)

    def __str__(self):
        return self.genre_name


class Theme(models.Model):
    """Creation a theme model"""
    theme_name = models.CharField(max_length=50,
                                  unique=True)

    def __str__(self):
        return self.theme_name


class Producer(models.Model):
    """Producer model"""
    producer_name = models.CharField(max_length=100,
                                     unique=True)

    def __str__(self):
        return self.producer_name


class VoiceActing(models.Model):
    """Voice acting model"""
    voice_acting = models.CharField(max_length=100,
                                    unique=True)

    def __str__(self):
        return self.voice_acting


class StatusAnime(models.Model):
    """Status anime model"""
    status = models.CharField(max_length=50,
                              unique=True)

    def __str__(self):
        return self.status


class Anime(models.Model):
    """Anime model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=50)
    cover = models.ImageField(
        storage=OverWriteStorage(),
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg']),
                    FileCheck.check_file_size],
        upload_to=FilePath.get_path_to_cover_anime,
        max_length=255
    )
    description = models.TextField()
    producer = models.ManyToManyField(Producer)
    genre = models.ManyToManyField(Genre)
    theme = models.ManyToManyField(Theme)
    status = models.ForeignKey(StatusAnime,
                               on_delete=models.CASCADE)
    release_date = models.DateField()
    updating_at = models.DateField(auto_now=True)
    creating_at = models.DateField(auto_now_add=True)
    number = models.PositiveSmallIntegerField(default=1)

    @property
    def average_rating(self):
        if hasattr(self, '_average_rating'):
            return self._average_rating
        return self.review.aggregate(Avg('rating'))

    @property
    def average_season(self):
        if hasattr(self, '_average_season'):
            return self._average_season
        return self.season_anime.aggregate(Sum('season'))

    @property
    def average_review(self):
        if hasattr(self, '_average_review'):
            return self._average_review
        return self.season_anime.aggregate(Sum('review'))

    def __str__(self):
        return self.title


class AnimeSeason(models.Model):
    """Anime season model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime,
                              on_delete=models.CASCADE,
                              related_name='season_anime')
    season_number = models.PositiveIntegerField()
    voice_acting = models.ManyToManyField(VoiceActing)
    producer = models.ManyToManyField(Producer)
    title = models.CharField(max_length=100,
                             null=True,
                             blank=True)
    release_date = models.DateField()
    updating_at = models.DateField(auto_now=True)
    creating_at = models.DateField(auto_now_add=True)
    number = models.PositiveSmallIntegerField(default=1)

    @property
    def average_episode(self):
        if hasattr(self, '_average_episode'):
            return self._average_episode
        return self.episode_season.aggregate(Sum('episode'))

    def __str__(self):
        return f'{self.anime}_season{self.season_number}'


class AnimeEpisode(models.Model):
    """Anime episode model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    season = models.ForeignKey(AnimeSeason,
                               on_delete=models.CASCADE,
                               related_name='episode_season')
    video = models.FileField(
        storage=OverWriteStorage(),
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        upload_to=FilePath.get_path_to_episode,
        max_length=255
    )
    duration = models.DurationField()
    voice_acting = models.ForeignKey(VoiceActing,
                                     on_delete=models.CASCADE)
    episode_number = models.PositiveIntegerField()
    release_date = models.DateField()
    updating_at = models.DateField(auto_now=True)
    creating_at = models.DateField(auto_now_add=True)
    number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.season}-{self.episode_number}-{self.title}'


class AnimeMovie(models.Model):
    """Anime movie model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=255,
                             unique=True)
    voice_acting = models.ForeignKey(VoiceActing,
                                     on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    video = models.FileField(
        storage=OverWriteStorage(),
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        upload_to=FilePath.get_path_to_movie,
        max_length=255
        )
    duration = models.DurationField()
    producer = models.ManyToManyField(Producer)
    movie_number = models.PositiveIntegerField()
    release_date = models.DateField()
    creating_at = models.DateField(auto_now_add=True)
    number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.title


ANIME_RATING = (
        (Decimal("1.0"), "★☆☆☆☆☆☆☆☆☆ (1/10)"),
        (Decimal("2.0"), "★★☆☆☆☆☆☆☆☆ (2/10)"),
        (Decimal("3.0"), "★★★☆☆☆☆☆☆☆ (3/10)"),
        (Decimal("4.0"), "★★★★☆☆☆☆☆☆ (4/10)"),
        (Decimal("5.0"), "★★★★★☆☆☆☆☆ (5/10)"),
        (Decimal("6.0"), "★★★★★★☆☆☆☆ (6/10)"),
        (Decimal("7.0"), "★★★★★★★☆☆☆ (7/10)"),
        (Decimal("8.0"), "★★★★★★★★☆☆ (8/10)"),
        (Decimal("9.0"), "★★★★★★★★★☆ (9/10)"),
        (Decimal("10.0"), "★★★★★★★★★★ (10/10)"),
)


class Review(models.Model):
    """Review model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.DecimalField(max_digits=3,
                                 decimal_places=1,
                                 choices=ANIME_RATING)
    anime = models.ForeignKey(Anime,
                              on_delete=models.CASCADE,
                              related_name='review')
    creating_at = models.DateField(auto_now_add=True)
    number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.comment
