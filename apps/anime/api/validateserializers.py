from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.anime.models import *


class AuthorValidateSerializer(serializers.Serializer):
    author = serializers.IntegerField(min_value=1)

    @staticmethod
    def validate_author(author):
        try:
            User.objects.get(pk=author)
        except User.DoesNotExist:
            raise ValidationError('User not found!')
        return author


class AnimeValidateSerializer(AuthorValidateSerializer):
    title_anime = serializers.CharField(max_length=255)
    original_anime_name = serializers.SlugField(max_length=20)
    cover_anime = serializers.ImageField()
    description_anime = serializers.CharField()
    producer_anime = serializers.ListField(child=serializers.IntegerField(min_value=1))
    genre_anime = serializers.ListField(child=serializers.IntegerField(min_value=1))
    theme_anime = serializers.ListField(child=serializers.IntegerField(min_value=1))
    status_anime = serializers.IntegerField(min_value=1, max_value=3)
    release_date_anime = serializers.DateField()

    @staticmethod
    def validate_producer_anime(producer_anime):
        filtered_producers_anime = Producer.objects.filter(id__in=producer_anime)
        if len(filtered_producers_anime) != len(producer_anime):
            raise ValidationError('Producer anime not found!')
        return producer_anime

    @staticmethod
    def validate_genre_anime(genre_anime):
        filtered_genres_anime = Genre.objects.filter(id__in=genre_anime)
        if len(filtered_genres_anime) != len(genre_anime):
            raise ValidationError('Genre anime not found!')
        return genre_anime

    @staticmethod
    def validate_theme_anime(theme_anime):
        filtered_themes_anime = Theme.objects.filter(id__in=theme_anime)
        if len(filtered_themes_anime) != len(theme_anime):
            raise ValidationError('Producer anime not found!')
        return theme_anime


class AnimeCreateSerializer(AnimeValidateSerializer):
    @staticmethod
    def validate_title(title):
        if Anime.objects.filter(title=title).count() > 0:
            raise ValidationError('Title must be unique')
        return title

    @staticmethod
    def validate_original_anime_name(original_anime_name):
        if Anime.objects.filter(original_anime_name=original_anime_name).count() > 0:
            raise ValidationError('Original anime name must be unique')
        return original_anime_name


class AnimeUpdateSerializer(AnimeValidateSerializer):
    @staticmethod
    def validate_title(self, title):
        if Anime.objects.filter(
                title=title
        ).exclude(id=self.context.get('id')).count() > 0:
            raise ValidationError('Title must be unique')
        return title

    @staticmethod
    def validate_original_anime_name(self, original_anime_name):
        if Anime.objects.filter(
                original_anime_name=original_anime_name
        ).exclude(id=self.context.get('id')).count() > 0:
            raise ValidationError('Original anime name must be unique')
        return original_anime_name


class SeasonValidateSerializer(AuthorValidateSerializer):
    season_anime = serializers.IntegerField(min_value=1)
    season_number = serializers.IntegerField(min_value=1)
    voiceover_of_the_season = serializers.ListField(child=serializers.IntegerField(min_value=1))
    producer_of_the_season = serializers.ListField(child=serializers.IntegerField(min_value=1))
    season_title = serializers.CharField(max_length=100)
    release_date_of_the_season = serializers.DateField()

    @staticmethod
    def validate_season_anime(season_anime):
        try:
            Anime.objects.get(pk=season_anime)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return season_anime

    @staticmethod
    def validate_voiceover_of_the_season(voiceover_of_the_season):
        filtered_voice_actings = VoiceActing.objects.filter(id__in=voiceover_of_the_season)
        if len(filtered_voice_actings) != len(voiceover_of_the_season):
            raise ValidationError('Voice acting not found!')
        return voiceover_of_the_season

    @staticmethod
    def validate_producer_of_the_season(producer_of_the_season):
        filtered_voice_actings = VoiceActing.objects.filter(id__in=producer_of_the_season)
        if len(filtered_voice_actings) != len(producer_of_the_season):
            raise ValidationError('Producer not found!')
        return producer_of_the_season


class SeasonCreateSerializer(SeasonValidateSerializer):
    @staticmethod
    def validate_season_title(season_title):
        if AnimeSeason.objects.filter(season_title=season_title).count() > 0:
            raise ValidationError('Season title must be unique')
        return season_title

    @staticmethod
    def validate_season_number(season_number):
        if AnimeSeason.objects.filter(season_number=season_number).count() > 0:
            raise ValidationError('Season number must be unique')
        return season_number


class SeasonUpdateSerializer(SeasonValidateSerializer):
    @staticmethod
    def validate_season_title(self, season_title):
        if AnimeSeason.objects.filter(
                season_title=season_title).exclude(
                    id=self.context.get('id')
        ).count() > 0:
            raise ValidationError('Season title must be unique')
        return season_title

    @staticmethod
    def validate_season_number(self, season_number):
        if AnimeSeason.objects.filter(
                anime_season__anime__number=season_number).exclude(
                    id=self.context.get('id')).count() > 0:
            raise ValidationError('Season number must be unique')
        return season_number


class EpisodeValidateSerializer(AuthorValidateSerializer):
    title_episode = serializers.CharField(max_length=55)
    anime = serializers.IntegerField(min_value=1)
    anime_video = serializers.FileField()
    episode_duration = serializers.DurationField()
    voice_acting_of_the_episode = serializers.IntegerField(min_value=1)
    anime_season = serializers.IntegerField(min_value=1)
    episode_number = serializers.IntegerField(min_value=1)
    release_date_of_the_episode = serializers.DateField()

    @staticmethod
    def validate_voice_acting_anime_of_the_episode(voice_acting_anime_of_the_episode):
        try:
            VoiceActing.objects.get(pk=voice_acting_anime_of_the_episode)
        except VoiceActing.DoesNotExist:
            raise ValidationError('Voice acting not found!')
        return voice_acting_anime_of_the_episode

    @staticmethod
    def validate_anime(anime):
        try:
            Anime.objects.get(pk=anime)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return anime


class EpisodeCreateSerializer(EpisodeValidateSerializer):
    @staticmethod
    def validate_title_episode(title_episode):
        if AnimeEpisode.objects.filter(title_episode=title_episode).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title_episode


class EpisodeUpdateSerializer(EpisodeValidateSerializer):
    @staticmethod
    def validate_title_episode(self, title_episode):
        if AnimeEpisode.objects.filter(
                title_episode=title_episode).exclude(
                    id=self.context.get('id')
        ).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title_episode


class MovieValidateSerializer(AuthorValidateSerializer):
    title_movie = serializers.CharField(max_length=255)
    voice_acting_anime_of_the_movie = serializers.IntegerField(min_value=1)
    anime_movie = serializers.IntegerField(min_value=1)
    anime_movie_video = serializers.FileField()
    movie_duration = serializers.DurationField()
    producer_anime_of_the_movie = serializers.ListField(child=serializers.IntegerField(min_value=1))
    movie_number = serializers.IntegerField(min_value=1)
    release_date_of_the_movie = serializers.DateField()

    @staticmethod
    def validate_voice_acting_anime_of_the_movie(voice_acting_anime_of_the_movie):
        try:
            VoiceActing.objects.get(pk=voice_acting_anime_of_the_movie)
        except VoiceActing.DoesNotExist:
            raise ValidationError('Voice acting not found!')
        return voice_acting_anime_of_the_movie

    @staticmethod
    def validate_anime_movie(anime_movie):
        try:
            Anime.objects.get(pk=anime_movie)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return anime_movie

    @staticmethod
    def validate_producer_anime_of_the_movie(producer_anime_of_the_movie):
        filtered_producers_anime = Producer.objects.filter(id__in=producer_anime_of_the_movie)
        if len(filtered_producers_anime) != len(producer_anime_of_the_movie):
            raise ValidationError('Producer not found!')
        return producer_anime_of_the_movie


class MovieCreateSerializer(MovieValidateSerializer):
    @staticmethod
    def validate_title_movie(title_movie):
        if AnimeMovie.objects.filter(title_movie=title_movie).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title_movie


class MovieUpdateSerializer(MovieValidateSerializer):
    @staticmethod
    def validate_title_movie(self, title_movie):
        if AnimeMovie.objects.filter(
                title_movie=title_movie).exclude(
                    id=self.context.get('id')
        ).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title_movie


class ReviewValidateSerializer(AuthorValidateSerializer):
    review_text = serializers.CharField()
    rating_for_anime = serializers.ChoiceField(choices=ANIME_RATING, allow_blank=False,
                                               default=5.0)
    anime = serializers.IntegerField(min_value=1)

    @staticmethod
    def validate_anime(anime):
        try:
            Anime.objects.get(pk=anime)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return anime
