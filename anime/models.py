from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Avg
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from .fileschek import *


class Genre(models.Model):
    """Creation a genre model"""
    genre_name = models.CharField(max_length=50,
                                  unique=True)

    def __str__(self):
        return self.genre_name


class Theme(models.Model):
    """Creation a theme model"""
    theme_name = models.CharField(max_length=55,
                                  unique=True)

    def __str__(self):
        return self.theme_name


class Producer(models.Model):
    """Creation a producer model"""
    producer_name = models.CharField(max_length=100,
                                     unique=True)

    def __str__(self):
        return self.producer_name


class VoiceActing(models.Model):
    """Creation a voice acting model"""
    voice_acting = models.CharField(max_length=100,
                                    unique=True)

    def __str__(self):
        return self.voice_acting


class StatusAnime(models.Model):
    status = models.CharField(max_length=50,
                              unique=True)

    def __str__(self):
        return self.status


class Anime(models.Model):
    """Creation a anime model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    title_anime = models.CharField(max_length=255,
                                   unique=True)
    original_anime_name = models.SlugField(unique=True)  # this field must be filled exclusively
    cover_anime = models.ImageField(
        storage=OverWriteStorage(),
        validators=[FileExtensionValidator(allowed_extensions=['png']), check_file_anime_cover_size],
        upload_to=get_path_to_cover_anime,
        unique=True
    )
    description_anime = models.TextField()
    producer_anime = models.ManyToManyField(Producer)
    genre_anime = models.ManyToManyField(Genre)
    theme_anime = models.ManyToManyField(Theme)
    status_anime = models.ForeignKey(StatusAnime,
                                     on_delete=models.CASCADE)
    release_date_anime = models.DateField()
    creation_date = models.DateField(auto_now=True)
    number = models.PositiveSmallIntegerField(default=1)  # это поле нужно для подсчета всех аниме

    def save(self, *args, **kwargs):
        self.original_anime_name = slugify(self.title_anime)
        super(Anime, self).save(*args, **kwargs)

    @property
    def average_rating(self):
        """This method is needed to calculate the average rating value"""
        if hasattr(self, '_average_rating'):
            return self._average_rating
        return self.reviews.aggregate(Avg('rating_for_anime'))

    @property
    def average_season(self):
        if hasattr(self, '_average_season'):
            return self._average_season
        return self.seasons.aggregate(Sum('season'))

    @property
    def average_review(self):
        if hasattr(self, '_average_review'):
            return self._average_review
        return self.seasons.aggregate(Sum('reviews'))

    def __str__(self):
        return self.title_anime


class AnimeSeason(models.Model):
    """Creation an anime season model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    season_anime = models.ForeignKey(Anime,
                                     on_delete=models.CASCADE,
                                     related_name='seasons')
    season_number = models.PositiveIntegerField(unique=True)
    voiceover_of_the_season = models.ManyToManyField(VoiceActing)
    producer_of_the_season = models.ManyToManyField(Producer)
    season_title = models.CharField(max_length=100,
                                    unique=True)
    release_date_of_the_season = models.DateField()
    creation_date = models.DateField(auto_now=True)
    number = models.PositiveSmallIntegerField(default=1)

    @property
    def average_episode(self):
        if hasattr(self, '_average_episode'):
            return self._average_episode
        return self.anime_season.aggregate(Sum('episode'))

    def __str__(self):
        return f'{self.season_anime}_season{self.season_number}'


class AnimeEpisode(models.Model):
    """Creation a anime episode model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    title_episode = models.CharField(max_length=255,
                                     unique=True)
    anime = models.ForeignKey(Anime,
                              on_delete=models.CASCADE)
    anime_video = models.FileField(
        storage=OverWriteStorage(),
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        upload_to=get_path_to_episode,
        unique=True
    )
    episode_duration = models.DurationField()
    voice_acting_of_the_episode = models.ForeignKey(VoiceActing,
                                                    on_delete=models.CASCADE)
    anime_season = models.ForeignKey(AnimeSeason,
                                     on_delete=models.CASCADE,
                                     related_name='anime_season')
    episode_number = models.PositiveIntegerField(unique=True)
    release_date_of_the_episode = models.DateField()
    creation_date = models.DateField(auto_now=True)
    number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.anime_season}-{self.episode_number}-{self.title_episode}'


class AnimeMovie(models.Model):
    """Creation a anime movie model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    title_movie = models.CharField(max_length=255,
                                   unique=True)
    voice_acting_anime_of_the_movie = models.ForeignKey(VoiceActing,
                                                        on_delete=models.CASCADE)
    anime_movie = models.ForeignKey(Anime, on_delete=models.CASCADE)
    anime_movie_video = models.FileField(
        storage=OverWriteStorage(),
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        upload_to=get_path_to_movie,
        unique=True
        )
    movie_duration = models.DurationField()
    producer_anime_of_the_movie = models.ManyToManyField(Producer)
    movie_number = models.PositiveIntegerField(unique=True)
    release_date_of_the_movie = models.DateField()
    creation_date = models.DateField(auto_now=True)
    number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.title_movie


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
    """Creation a review model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    review_text = models.TextField()
    rating_for_anime = models.DecimalField(max_digits=3,
                                           decimal_places=1,
                                           choices=ANIME_RATING,
                                           default=5.0)
    anime = models.ForeignKey(Anime,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    creation_date = models.DateField(auto_now=True)
    number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.review_text
