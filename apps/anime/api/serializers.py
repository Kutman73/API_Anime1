from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from apps.anime.models import *


class GenreSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ThemeSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'


class ProducerSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'


class VoiceActingSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = VoiceActing
        fields = '__all__'


class StatusAnimeSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = StatusAnime
        fields = '__all__'


class AnimeSerializers(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, queryset=Genre.objects.all())
    theme = ThemeSerializer(many=True, queryset=Theme.objects.all())
    producer = ProducerSerializer(many=True, queryset=Producer.objects.all())
    status = StatusAnimeSerializer(many=False, queryset=StatusAnime.objects.all())

    class Meta:
        model = Anime
        fields = (
            'author',
            'title',
            'cover',
            'slug',
            'description',
            'producer',
            'genre',
            'theme',
            'status',
            'release_date',
            'amount_seasons',
            'amount_reviews',
            'anime_rating',
        )

    amount_seasons = serializers.SerializerMethodField()
    amount_reviews = serializers.SerializerMethodField()
    anime_rating = serializers.SerializerMethodField()

    @staticmethod
    def get_anime_rating(ob):
        return ob.review.all().aggregate(Avg('rating'))['rating__avg']

    @staticmethod
    def get_amount_seasons(ob):
        return ob.season_anime.all().aggregate(Sum('number'))['number__sum']

    @staticmethod
    def get_amount_reviews(ob):
        return ob.review.all().aggregate(Sum('number'))['number__sum']


class SeasonSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnimeSeason
        fields = (
            'author',
            'anime',
            'season_number',
            'producer',
            'voice_acting',
            'title',
            'amount_episodes',
            'release_date',
            'amount_episodes',
        )

    amount_episodes = serializers.SerializerMethodField()

    @staticmethod
    def get_amount_episodes(ob):
        return ob.episode_season.all().aggregate(Sum('number'))['number__sum']


class EpisodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnimeEpisode
        fields = (
            'author',
            'title',
            'season',
            'video',
            'duration',
            'voice_acting',
            'episode_number',
            'release_date',
        )


class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnimeMovie
        fields = (
            'author',
            'anime',
            'title',
            'voice_acting',
            'video',
            'producer',
            'movie_number',
            'duration',
            'release_date',
        )


class ReviewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'author',
            'anime',
            'rating',
            'comment',
        )
