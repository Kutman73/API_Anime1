from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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

    def get_anime_rating(self, ob):
        return ob.reviews.all().aggregate(Avg('rating_for_anime'))['rating_for_anime__avg']

    def get_total_amount_seasons(self, ob):
        return ob.seasons.all().aggregate(Sum('number'))['number__sum']

    def get_total_amount_reviews(self, ob):
        return ob.reviews.all().aggregate(Sum('number'))['number__sum']


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
        if Anime.objects.filter(
                title=title
        ).exclude(id=self.context.get('id')).count() > 0:
            raise ValidationError('Title must be unique')
        return title

    def validate_original_anime_name(self, original_anime_name):
        if Anime.objects.filter(
                original_anime_name=original_anime_name
        ).exclude(id=self.context.get('id')).count() > 0:
            raise ValidationError('Original anime name must be unique')
        return original_anime_name


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

    def get_amount_episodes(self, ob):
        return ob.anime_season.all().aggregate(Sum('number'))['number__sum']


class SeasonValidateSerializer(serializers.Serializer):
    author = serializers.IntegerField(min_value=1)
    season_anime = serializers.IntegerField(min_value=1)
    season_number = serializers.IntegerField(min_value=1)
    voiceover_of_the_season = serializers.ListField(child=serializers.IntegerField(min_value=1))
    producer_of_the_season = serializers.ListField(child=serializers.IntegerField(min_value=1))
    season_title = serializers.CharField(max_length=100)
    release_date_of_the_season = serializers.DateField()

    def validate_author(self, author):
        try:
            User.objects.get(pk=author)
        except User.DoesNotExist:
            raise ValidationError('User not found!')
        return author

    def validate_season_anime(self, season_anime):
        try:
            Anime.objects.get(pk=season_anime)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return season_anime

    def validate_voiceover_of_the_season(self, voiceover_of_the_season):
        filtered_voice_actings = VoiceActing.objects.filter(id__in=voiceover_of_the_season)
        if len(filtered_voice_actings) != len(voiceover_of_the_season):
            raise ValidationError('Voice acting not found!')
        return voiceover_of_the_season

    def validate_producer_of_the_season(self, producer_of_the_season):
        filtered_voice_actings = VoiceActing.objects.filter(id__in=producer_of_the_season)
        if len(filtered_voice_actings) != len(producer_of_the_season):
            raise ValidationError('Producer not found!')
        return producer_of_the_season


class SeasonCreateSerializer(SeasonValidateSerializer):
    def validate_season_title(self, season_title):
        if AnimeSeason.objects.filter(season_title=season_title).count() > 0:
            raise ValidationError('Season title must be unique')
        return season_title

    def validate_season_number(self, season_number):
        if AnimeSeason.objects.filter(season_number=season_number).count() > 0:
            raise ValidationError('Season number must be unique')
        return season_number


class SeasonUpdateSerializer(SeasonValidateSerializer):
    def validate_season_title(self, season_title):
        if AnimeSeason.objects.filter(
                season_title=season_title).exclude(
                    id=self.context.get('id')
        ).count() > 0:
            raise ValidationError('Season title must be unique')
        return season_title

    def validate_season_number(self, season_number):
        if AnimeSeason.objects.filter(
                anime_season__anime__number=season_number).exclude(
                    id=self.context.get('id')).count() > 0:
            raise ValidationError('Season number must be unique')
        return season_number


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


class EpisodeValidateSerializer(serializers.Serializer):
    author = serializers.IntegerField(min_value=1)
    title_episode = serializers.CharField(max_length=55)
    anime = serializers.IntegerField(min_value=1)
    anime_video = serializers.FileField()
    episode_duration = serializers.DurationField()
    voice_acting_of_the_episode = serializers.IntegerField(min_value=1)
    anime_season = serializers.IntegerField(min_value=1)
    episode_number = serializers.IntegerField(min_value=1)
    release_date_of_the_episode = serializers.DateField()

    def validate_author(self, author):
        try:
            User.objects.get(pk=author)
        except User.DoesNotExist:
            raise ValidationError('User not found!')
        return author

    def validate_voice_acting_anime_of_the_episode(self, voice_acting_anime_of_the_episode):
        try:
            VoiceActing.objects.get(pk=voice_acting_anime_of_the_episode)
        except VoiceActing.DoesNotExist:
            raise ValidationError('Voice acting not found!')
        return voice_acting_anime_of_the_episode

    def validate_anime(self, anime):
        try:
            Anime.objects.get(pk=anime)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return anime


class EpisodeCreateSerializer(EpisodeValidateSerializer):
    def validate_title_episode(self, title_episode):
        if AnimeEpisode.objects.filter(title_episode=title_episode).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title_episode


class EpisodeUpdateSerializer(EpisodeValidateSerializer):
    def validate_title_episode(self, title_episode):
        if AnimeEpisode.objects.filter(
                title_episode=title_episode).exclude(
                    id=self.context.get('id')
        ).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title_episode


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


class MovieValidateSerializer(serializers.Serializer):
    author = serializers.IntegerField(min_value=1)
    title_movie = serializers.CharField(max_length=255)
    voice_acting_anime_of_the_movie = serializers.IntegerField(min_value=1)
    anime_movie = serializers.IntegerField(min_value=1)
    anime_movie_video = serializers.FileField()
    movie_duration = serializers.DurationField()
    producer_anime_of_the_movie = serializers.ListField(child=serializers.IntegerField(min_value=1))
    movie_number = serializers.IntegerField(min_value=1)
    release_date_of_the_movie = serializers.DateField()

    def validate_author(self, author):
        try:
            User.objects.get(pk=author)
        except User.DoesNotExist:
            raise ValidationError('User not found!')
        return author

    def validate_voice_acting_anime_of_the_movie(self, voice_acting_anime_of_the_movie):
        try:
            VoiceActing.objects.get(pk=voice_acting_anime_of_the_movie)
        except VoiceActing.DoesNotExist:
            raise ValidationError('Voice acting not found!')
        return voice_acting_anime_of_the_movie

    def validate_anime_movie(self, anime_movie):
        try:
            Anime.objects.get(pk=anime_movie)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return anime_movie

    def validate_producer_anime_of_the_movie(self, producer_anime_of_the_movie):
        filtered_producers_anime = Producer.objects.filter(id__in=producer_anime_of_the_movie)
        if len(filtered_producers_anime) != len(producer_anime_of_the_movie):
            raise ValidationError('Producer not found!')
        return producer_anime_of_the_movie


class MovieCreateSerializer(MovieValidateSerializer):
    def validate_title_movie(self, title_movie):
        if AnimeMovie.objects.filter(title_movie=title_movie).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title_movie


class MovieUpdateSerializer(MovieValidateSerializer):
    def validate_title_movie(self, title_movie):
        if AnimeMovie.objects.filter(
                title_movie=title_movie).exclude(
                    id=self.context.get('id')
        ).count() > 0:
            raise ValidationError('Title movie must be unique')
        return title_movie


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


class ReviewValidateSerializer(serializers.Serializer):
    author = serializers.IntegerField(min_value=1)
    review_text = serializers.CharField()
    rating_for_anime = serializers.ChoiceField(choices=ANIME_RATING, allow_blank=False,
                                               default=5.0)
    anime = serializers.IntegerField(min_value=1)

    def validate_author(self, author):
        try:
            User.objects.get(pk=author)
        except User.DoesNotExist:
            raise ValidationError('User not found!')
        return author

    def validate_anime(self, anime):
        try:
            Anime.objects.get(pk=anime)
        except Anime.DoesNotExist:
            raise ValidationError('Anime not found!')
        return anime
