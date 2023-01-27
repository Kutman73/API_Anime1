from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from anime.models import *


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
    genre_anime = GenreSerializer(many=True, queryset=Genre.objects.all())
    theme_anime = ThemeSerializer(many=True, queryset=Theme.objects.all())
    producer_anime = ProducerSerializer(many=True, queryset=Producer.objects.all())
    status_anime = StatusAnimeSerializer(many=False, queryset=StatusAnime.objects.all())

    class Meta:
        model = Anime
        fields = (
            'id',
            'author',
            'title_anime',
            'cover_anime',
            'original_anime_name',
            'description_anime',
            'producer_anime',
            'genre_anime',
            'theme_anime',
            'status_anime',
            'release_date_anime',
            'creation_date',
            'total_amount_seasons',
            'total_amount_reviews',
            'anime_rating',
        )

    total_amount_seasons = serializers.SerializerMethodField()
    total_amount_reviews = serializers.SerializerMethodField()
    anime_rating = serializers.SerializerMethodField()

    @staticmethod
    def get_anime_rating(ob):
        return ob.reviews.all().aggregate(Avg('rating_for_anime'))['rating_for_anime__avg']

    @staticmethod
    def get_total_amount_seasons(ob):
        return ob.seasons.all().aggregate(Sum('number'))['number__sum']

    @staticmethod
    def get_total_amount_reviews(ob):
        return ob.reviews.all().aggregate(Sum('number'))['number__sum']


class SeasonSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnimeSeason
        fields = (
            'id',
            'author',
            'season_anime',
            'season_number',
            'producer_of_the_season',
            'voiceover_of_the_season',
            'season_title',
            'amount_episodes',
            'release_date_of_the_season',
            'creation_date',
            'amount_episodes',
        )

    amount_episodes = serializers.SerializerMethodField()

    @staticmethod
    def get_amount_episodes(ob):
        return ob.anime_season.all().aggregate(Sum('number'))['number__sum']


class EpisodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnimeEpisode
        fields = (
            'id',
            'author',
            'title_episode',
            'anime',
            'anime_video',
            'episode_duration',
            'voice_acting_of_the_episode',
            'anime_season',
            'episode_number',
            'release_date_of_the_episode',
            'creation_date',
        )


class AnimeMovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnimeMovie
        fields = (
            'id',
            'author',
            'title_movie',
            'voice_acting_anime_of_the_movie',
            'anime_movie',
            'anime_movie_video',
            'producer_anime_of_the_movie',
            'movie_number',
            'movie_duration',
            'release_date_of_the_movie',
            'creation_date',
        )


class ReviewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'anime',
            'rating_for_anime',
            'review_text',
            'creation_date',
        )
