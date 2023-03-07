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
    title = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=20)
    cover = serializers.ImageField()
    description = serializers.CharField()
    producer = serializers.ListField(child=serializers.IntegerField(min_value=1))
    genre = serializers.ListField(child=serializers.IntegerField(min_value=1))
    theme = serializers.ListField(child=serializers.IntegerField(min_value=1))
    status = serializers.IntegerField(min_value=1, max_value=3)
    release_date = serializers.DateField()

    @staticmethod
    def validate_producer(producer):
        filtered_producers_anime = Producer.objects.filter(id__in=producer)
        if len(filtered_producers_anime) != len(producer):
            raise ValidationError('Producer not found!')
        return producer

    @staticmethod
    def validate_genre(genre):
        filtered_genres_anime = Genre.objects.filter(id__in=genre)
        if len(filtered_genres_anime) != len(genre):
            raise ValidationError('Genre not found!')
        return genre

    @staticmethod
    def validate_theme(theme):
        filtered_themes_anime = Theme.objects.filter(id__in=theme)
        if len(filtered_themes_anime) != len(theme):
            raise ValidationError('Producer not found!')
        return theme


class AnimeCreateSerializer(AnimeValidateSerializer):
    @staticmethod
    def validate_title(title):
        if Anime.objects.filter(title=title).count() > 0:
            raise ValidationError('Title must be unique')
        return title

    @staticmethod
    def validate_slug(slug):
        if Anime.objects.filter(original_anime_name=slug).count() > 0:
            raise ValidationError('Slug must be unique')
        return slug


class AnimeUpdateSerializer(AnimeValidateSerializer):
    @staticmethod
    def validate_title(self, title):
        if Anime.objects.filter(
                title=title
        ).exclude(id=self.context.get('id')).count() > 0:
            raise ValidationError('Title must be unique')
        return title

    @staticmethod
    def validate_slug(self, slug):
        if Anime.objects.filter(
                original_anime_name=slug
        ).exclude(id=self.context.get('id')).count() > 0:
            raise ValidationError('Original anime name must be unique')
        return slug


class SeasonValidateSerializer(AuthorValidateSerializer):
    season = serializers.IntegerField(min_value=1)
    season_number = serializers.IntegerField(min_value=1)
    voice_acting = serializers.ListField(child=serializers.IntegerField(min_value=1))
    producer = serializers.ListField(
        child=serializers.IntegerField(min_value=1))
    title = serializers.CharField(max_length=100)
    release_date = serializers.DateField()

    @staticmethod
    def validate_season(season):
        try:
            Anime.objects.get(pk=season)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return season

    @staticmethod
    def validate_voice_acting(voice_acting):
        filtered_voice_actings = VoiceActing.objects.filter(id__in=voice_acting)
        if len(filtered_voice_actings) != len(voice_acting):
            raise ValidationError('Voice acting not found!')
        return voice_acting

    @staticmethod
    def validate_producer(producer):
        filtered_voice_actings = VoiceActing.objects.filter(id__in=producer)
        if len(filtered_voice_actings) != len(producer):
            raise ValidationError('Producer not found!')
        return producer


class SeasonCreateSerializer(SeasonValidateSerializer):
    @staticmethod
    def validate_title(title):
        if AnimeSeason.objects.filter(season_title=title).count() > 0:
            raise ValidationError('Season title must be unique')
        return title

    @staticmethod
    def validate_season_number(season_number):
        if AnimeSeason.objects.filter(season_number=season_number).count() > 0:
            raise ValidationError('Season number must be unique')
        return season_number


class SeasonUpdateSerializer(SeasonValidateSerializer):
    @staticmethod
    def validate_season_title(self, title):
        if AnimeSeason.objects.filter(
                season_title=title).exclude(
                    id=self.context.get('id')
        ).count() > 0:
            raise ValidationError('Season title must be unique')
        return title

    @staticmethod
    def validate_season_number(self, season_number):
        if AnimeSeason.objects.filter(
                anime_season__anime__number=season_number).exclude(
                    id=self.context.get('id')).count() > 0:
            raise ValidationError('Season number must be unique')
        return season_number


class EpisodeValidateSerializer(AuthorValidateSerializer):
    title = serializers.CharField(max_length=55)
    season = serializers.IntegerField(min_value=1)
    video = serializers.FileField()
    duration = serializers.DurationField()
    voice_acting = serializers.IntegerField(min_value=1)
    episode_number = serializers.IntegerField(min_value=1)
    release_date = serializers.DateField()

    @staticmethod
    def validate_voice_acting(voice_acting):
        try:
            VoiceActing.objects.get(pk=voice_acting)
        except VoiceActing.DoesNotExist:
            raise ValidationError('Voice acting not found!')
        return voice_acting

    @staticmethod
    def validate_season(season):
        try:
            AnimeSeason.objects.get(pk=season)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return season


class EpisodeCreateSerializer(EpisodeValidateSerializer):
    @staticmethod
    def validate_title(title):
        if AnimeEpisode.objects.filter(title_episode=title).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title


class EpisodeUpdateSerializer(EpisodeValidateSerializer):
    @staticmethod
    def validate_title(self, title):
        if AnimeEpisode.objects.filter(
                title_episode=title).exclude(
                    id=self.context.get('id')
        ).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title


class MovieValidateSerializer(AuthorValidateSerializer):
    title = serializers.CharField(max_length=255)
    voice_acting = serializers.IntegerField(min_value=1)
    anime = serializers.IntegerField(min_value=1)
    video = serializers.FileField()
    duration = serializers.DurationField()
    producer = serializers.ListField(child=serializers.IntegerField(min_value=1))
    movie_number = serializers.IntegerField(min_value=1)
    release_date = serializers.DateField()

    @staticmethod
    def validate_voice_acting(voice_acting):
        try:
            VoiceActing.objects.get(pk=voice_acting)
        except VoiceActing.DoesNotExist:
            raise ValidationError('Voice acting not found!')
        return voice_acting

    @staticmethod
    def validate_anime(anime):
        try:
            Anime.objects.get(pk=anime)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return anime

    @staticmethod
    def validate_producer(producer):
        filtered_producers_anime = Producer.objects.filter(id__in=producer)
        if len(filtered_producers_anime) != len(producer):
            raise ValidationError('Producer not found!')
        return producer


class MovieCreateSerializer(MovieValidateSerializer):
    @staticmethod
    def validate_title(title):
        if AnimeMovie.objects.filter(title_movie=title).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title


class MovieUpdateSerializer(MovieValidateSerializer):
    @staticmethod
    def validate_title(self, title):
        if AnimeMovie.objects.filter(
                title_movie=title).exclude(
                    id=self.context.get('id')
        ).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title


class ReviewValidateSerializer(AuthorValidateSerializer):
    comment = serializers.CharField()
    rating = serializers.ChoiceField(choices=ANIME_RATING, allow_blank=False)
    anime = serializers.IntegerField(min_value=1)

    @staticmethod
    def validate_anime(anime):
        try:
            Anime.objects.get(pk=anime)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return anime
