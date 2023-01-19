from django.db.models import Count
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField
from anime.models import *


class GenreSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = 'number'.split()


class ThemeSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Theme
        exclude = 'number'.split()


class ProducerSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Producer
        exclude = 'number'.split()


class VoiceActingSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = VoiceActing
        exclude = 'number'.split()


class StatusAnimeSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = StatusAnime
        exclude = 'number'.split()


class AnimeSerializers(serializers.ModelSerializer):
    genre_anime = GenreSerializer(many=True, queryset=Genre.objects.all())
    theme_anime = ThemeSerializer(many=True, queryset=Theme.objects.all())
    producer_anime = ProducerSerializer(many=True, queryset=Producer.objects.all())
    status_anime = StatusAnimeSerializer(many=False, queryset=StatusAnime.objects.all())

    class Meta:
        model = Anime
        fields = ('id', 'author', 'title_anime',
                  'cover_anime', 'original_anime_name',
                  'description_anime', 'producer_anime',
                  'genre_anime', 'theme_anime', 'status_anime',
                  'release_date_anime', 'creation_date',)


class AnimeValidateSerializer(serializers.Serializer):
    author = serializers.IntegerField(min_value=1)
    title_anime = serializers.CharField(max_length=255)
    original_anime_name = serializers.SlugField(max_length=20)
    cover_anime = serializers.ImageField()
    description_anime = serializers.CharField()
    producer_anime = serializers.ListField(child=serializers.IntegerField(min_value=1))
    genre_anime = serializers.ListField(child=serializers.IntegerField(min_value=1))
    theme_anime = serializers.ListField(child=serializers.IntegerField(min_value=1))
    status_anime = serializers.IntegerField(min_value=1, max_value=3)
    release_date_anime = serializers.DateField()

    def validate_author(self, author):
        try:
            User.objects.get(pk=author)
        except User.DoesNotExist:
            raise ValidationError('User not found!')
        return author

    def validate_producer_anime(self, producer_anime):
        filtered_producers_anime = Producer.objects.filter(id__in=producer_anime)
        if len(filtered_producers_anime) != len(producer_anime):
            raise ValidationError('Producer anime not found!')
        return producer_anime

    def validate_genre_anime(self, genre_anime):
        filtered_genres_anime = Genre.objects.filter(id__in=genre_anime)
        if len(filtered_genres_anime) != len(genre_anime):
            raise ValidationError('Genre anime not found!')
        return genre_anime

    def validate_theme_anime(self, theme_anime):
        filtered_themes_anime = Theme.objects.filter(id__in=theme_anime)
        if len(filtered_themes_anime) != len(theme_anime):
            raise ValidationError('Producer anime not found!')
        return theme_anime


class AnimeCreateSerializer(AnimeValidateSerializer):
    def validate_title(self, title):
        if Anime.objects.filter(title=title).count() > 0:
            raise ValidationError('Title must be unique')
        return title

    def validate_original_anime_name(self, original_anime_name):
        if Anime.objects.filter(original_anime_name=original_anime_name).count() > 0:
            raise ValidationError('Original anime name must be unique')
        return original_anime_name


class AnimeUpdateSerializer(AnimeValidateSerializer):
    def validate_title(self, title):
        if Anime.objects.filter(title=title).exclude(id=self.context.get('id')).count() > 0:
            raise ValidationError('Title must be unique')
        return title

    def validate_original_anime_name(self, original_anime_name):
        if Anime.objects.filter(original_anime_name=original_anime_name).exclude(id=self.context.get('id')).count() > 0:
            raise ValidationError('Original anime name must be unique')
        return original_anime_name
