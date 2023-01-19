from rest_framework import status
from rest_framework.response import Response
from anime.serializers import *
from anime.models import *
from rest_framework.viewsets import *
from rest_framework.decorators import action


class AnimeModelViewSet(ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializers
    lookup_field = 'original_anime_name'

    def create(self, request, **kwargs):
        serializer = AnimeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.validated_data.get('author')
        title_anime = serializer.validated_data.get('title_anime')
        original_anime_name = serializer.validated_data.get('original_anime_name')
        cover_anime = serializer.validated_data.get('cover_anime')
        description_anime = serializer.validated_data.get('description_anime')
        producer_anime = serializer.validated_data.get('producer_anime')
        genre_anime = serializer.validated_data.get('genre_anime')
        theme_anime = serializer.validated_data.get('theme_anime')
        status_anime = serializer.validated_data.get('status_anime')
        release_date_anime = serializer.validated_data.get('release_date_anime')
        new_anime = Anime.objects.create(author_id=author,
                                         title_anime=title_anime,
                                         original_anime_name=original_anime_name,
                                         cover_anime=cover_anime,
                                         description_anime=description_anime,
                                         status_anime_id=status_anime,
                                         release_date_anime=release_date_anime)
        new_anime.producer_anime.set(producer_anime)
        new_anime.genre_anime.set(genre_anime)
        new_anime.theme_anime.set(theme_anime)
        new_anime.save()
        return Response(data={'message': 'Data received!',
                              'anime': AnimeSerializers(new_anime).data},
                        status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        anime = self.get_object()
        serializer = AnimeUpdateSerializer(data=request.data, context={'id': anime.id})
        serializer.is_valid(raise_exception=True)
        anime.author_id = serializer.validated_data.get('author')
        anime.title = serializer.validated_data.get('title')
        anime.original_anime_name = serializer.validated_data.get('original_anime_name')
        anime.cover_anime = serializer.validated_data.get('cover_anime')
        anime.description_anime = serializer.validated_data.get('description_anime')
        anime.producer_anime.set(serializer.validated_data.get('producer_anime'))
        anime.genre_anime.set(serializer.validated_data.get('genre_anime'))
        anime.theme_anime.set(serializer.validated_data.get('theme_anime'))
        anime.status_anime_id = serializer.validated_data.get('status_anime')
        anime.release_date_anime = serializer.validated_data.get('release_date_anime')
        anime.save()
        return Response(data={'message': 'Data received!',
                              'anime': AnimeSerializers(anime).data},
                        status=status.HTTP_201_CREATED)


class SeasonModelViewSet(ModelViewSet):
    queryset = AnimeSeason.objects.all()
    serializer_class = SeasonSerializers
    lookup_field = 'pk'

    def list(self, request, **kwargs):
        anime_season = self.queryset.filter(
            season_anime__original_anime_name=kwargs['original_anime_name']
        )
        serializer = self.serializer_class(anime_season, many=True)
        return Response(data=serializer.data)

    def create(self, request, **kwargs):
        anime = self.queryset.filter(
            season_anime__original_anime_name=kwargs['original_anime_name']
        )
        serializer = SeasonCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        anime.author = serializer.validated_data.get('author')
        anime.season_anime = serializer.validated_data.get('season_anime')
        anime.season_number = serializer.validated_data.get('season_number')
        anime.voiceover_of_the_season = serializer.validated_data.get('voiceover_of_the_season')
        anime.producer_of_the_season = serializer.validated_data.get('producer_of_the_season')
        anime.season_title = serializer.validated_data.get('season_title')
        anime.release_date_of_the_season = serializer.validated_data.get('release_date_of_the_season')
        new_season = AnimeSeason.objects.create(
            author_id=anime.author,
            season_anime_id=anime.season_anime,
            season_number=anime.season_number,
            season_title=anime.season_title,
            release_date_of_the_season=anime.release_date_of_the_season
        )
        new_season.voiceover_of_the_season.set(anime.voiceover_of_the_season)
        new_season.producer_of_the_season.set(anime.producer_of_the_season)
        new_season.save()
        return Response(data={'message': 'Data received!',
                              'anime': SeasonSerializers(new_season).data},
                        status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        season = self.get_object()
        serializer = SeasonUpdateSerializer(data=request.data, context={'id': season.id})
        serializer.is_valid(raise_exception=True)
        season.author_id = serializer.validated_data.get('author')
        season.season_anime_id = serializer.validated_data.get('season_anime')
        season.season_number_id = serializer.validated_data.get('season_number')
        season.voiceover_of_the_season.set(serializer.validated_data.get('voiceover_of_the_season'))
        season.producer_of_the_season.set(serializer.validated_data.get('producer_of_the_season'))
        season.season_title = serializer.validated_data.get('season_title')
        season.release_date_of_the_season = serializer.validated_data.get('release_date_of_the_season')
        season.save()
        return Response(data={'message': 'Data received!',
                              'anime': SeasonSerializers(season).data},
                        status=status.HTTP_201_CREATED)


class EpisodeModelViewSet(ModelViewSet):
    queryset = AnimeEpisode.objects.all()
    serializer_class = EpisodeSerializers
    lookup_field = 'id'

    def list(self, request, **kwargs):
        anime_episode = self.queryset.filter(
            anime_season_id=kwargs['pk']
        )
        serializer = self.serializer_class(anime_episode, many=True)
        return Response(data=serializer.data)

    def create(self, request, **kwargs):
        anime = self.queryset.filter(
            anime__original_anime_name=kwargs['original_anime_name']
        )
        serializer = EpisodeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        anime.author = serializer.validated_data.get('author')
        anime.title_episode = serializer.validated_data.get('title_episode')
        anime.anime = serializer.validated_data.get('anime')
        anime.anime_video = serializer.validated_data.get('anime_video')
        anime.voice_acting_anime_of_the_episode = serializer.validated_data.get('voice_acting_anime_of_the_episode')
        anime.anime_season = serializer.validated_data.get('anime_season')
        anime.episode_number = serializer.validated_data.get('episode_number')
        anime.release_date_of_the_episode = serializer.validated_data.get('release_date_of_the_episode')
        new_episode = AnimeEpisode.objects.create(
            author_id=anime.author,
            title_episode=anime.title_episode,
            anime_id=anime.anime,
            anime_video=anime.anime_video,
            voice_acting_of_the_episode_id=anime.voice_acting_anime_of_the_episode,
            anime_season_id=anime.anime_season,
            episode_number=anime.episode_number,
            release_date_of_the_episode=anime.release_date_of_the_episode
        )
        new_episode.save()
        return Response(data={'message': 'Data received!',
                              'episode': EpisodeSerializers(new_episode).data},
                        status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        episode = self.get_object()
        serializer = EpisodeUpdateSerializer(data=request.data, context={'id': episode.id})
        serializer.is_valid(raise_exception=True)
        episode.author_id = serializer.validated_data.get('author')
        episode.title_episode = serializer.validated_data.get('title_episode')
        episode.anime_id = serializer.validated_data.get('anime')
        episode.anime_video = serializer.validated_data.get('anime_video')
        episode.voice_acting_anime_of_the_episode_id = serializer.validated_data.get('voice_acting_anime_of_the_episode')
        episode.anime_season_id = serializer.validated_data.get('anime_season')
        episode.episode_number = serializer.validated_data.get('episode_number')
        episode.release_date_of_the_episode = serializer.validated_data.get('release_date_of_the_episode')
        episode.save()
        return Response(data={'message': 'Data received!',
                              'episode': EpisodeSerializers(episode).data},
                        status=status.HTTP_201_CREATED)


class ReviewAPIView(ViewSet):
    def list(self, request, **kwargs):
        anime_review = Review.objects.filter(
            anime__original_anime_name=kwargs['original_anime_name']
        )
        serializer = ReviewsSerializers(anime_review, many=True)
        return Response(data=serializer.data)

    def create(self, request):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.validated_data.get('author')
        review_text = serializer.validated_data.get('review_text')
        rating_for_anime = serializer.validated_data.get('rating_for_anime')
        anime = serializer.validated_data.get('anime')
        new_review = Review.objects.create(
            author_id=author,
            review_text=review_text,
            rating_for_anime=rating_for_anime,
            anime_id=anime
        )
        new_review.save()
        return Response(data={'message': 'Data received!',
                              'review': ReviewsSerializers(new_review).data},
                        status=status.HTTP_201_CREATED)


class AnimeMovieModelViewSet(ModelViewSet):
    queryset = AnimeMovie.objects.all()
    serializer_class = AnimeMovieSerializers
    lookup_field = 'pk'

    def list(self, request, **kwargs):
        anime_movie = self.queryset.filter(
            anime_movie__original_anime_name=kwargs['original_anime_name']
        )
        serializer = self.serializer_class(anime_movie, many=True)
        return Response(data=serializer.data)

    def create(self, request, **kwargs):
        serializer = MovieCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        anime = self.queryset.filter(
            anime_movie__original_anime_name=kwargs['original_anime_name']
        )
        anime.author = serializer.validated_data.get('author')
        anime.title_movie = serializer.validated_data.get('title_movie')
        anime.voice_acting_anime_of_the_movie = serializer.validated_data.get('voice_acting_anime_of_the_movie')
        anime.anime_movie = serializer.validated_data.get('anime_movie')
        anime.movie_duration = serializer.validated_data.get('movie_duration')
        anime.producer_anime_of_the_movie = serializer.validated_data.get('producer_anime_of_the_movie')
        anime.anime_movie_video = serializer.validated_data.get('anime_movie_video')
        anime.release_date_of_the_movie = serializer.validated_data.get('release_date_of_the_movie')
        new_movie = AnimeMovie.objects.create(
            author_id=anime.author,
            title_movie=anime.title_movie,
            voice_acting_anime_of_the_movie_id=anime.voice_acting_anime_of_the_movie,
            anime_movie_id=anime.anime_movie,
            movie_duration=anime.movie_duration,
            anime_movie_video=anime.anime_movie_video,
            release_date_of_the_movie=anime.release_date_of_the_movie
        )
        new_movie.producer_anime_of_the_movie.set(anime.producer_anime_of_the_movie)
        new_movie.save()
        return Response(data={'message': 'Data received!',
                              'anime_movie': AnimeMovieSerializers(new_movie).data},
                        status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        movie = self.get_object()
        serializer = MovieUpdateSerializer(data=request.data, context={'id': movie.id})
        serializer.is_valid(raise_exception=True)
        movie.author_id = serializer.validated_data.get('author')
        movie.title_movie = serializer.validated_data.get('title_movie')
        movie.voice_acting_anime_of_the_movie_id = serializer.validated_data.get('voice_acting_anime_of_the_movie')
        movie.anime_movie_id = serializer.validated_data.get('anime_movie')
        movie.anime_movie_video = serializer.validated_data.get('anime_movie_video')
        movie.movie_duration = serializer.validated_data.get('movie_duration')
        movie.producer_anime_of_the_movie.set(serializer.validated_data.get('producer_anime_of_the_movie'))
        movie.movie_number = serializer.validated_data.get('movie_number')
        movie.release_date_of_the_movie = serializer.validated_data.get('release_date_of_the_movie')
        movie.save()
        return Response(data={'message': 'Data received!',
                              'anime': AnimeMovieSerializers(movie).data},
                        status=status.HTTP_201_CREATED)


class ReviewModelViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializers
    lookup_field = 'pk'

    def list(self, request, **kwargs):
        anime_review = self.queryset.filter(
            anime__original_anime_name=kwargs['original_anime_name']
        )
        serializer = ReviewsSerializers(anime_review, many=True)
        return Response(data=serializer.data)

    def create(self, request, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.validated_data.get('author')
        review_text = serializer.validated_data.get('review_text')
        rating_for_anime = serializer.validated_data.get('rating_for_anime')
        anime = serializer.validated_data.get('anime')
        new_review = Review.objects.create(
            author_id=author,
            review_text=review_text,
            rating_for_anime=rating_for_anime,
            anime_id=anime
        )
        new_review.save()
        return Response(data={'message': 'Data received!',
                              'review': ReviewsSerializers(new_review).data},
                        status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        updating_review = self.queryset.filter(
            anime__original_anime_name=kwargs['original_anime_name']
        )
        serializer = ReviewValidateSerializer(data=request.data, context={'id': updating_review.id})
        serializer.is_valid(raise_exception=True)
        updating_review.author_id = serializer.validated_data.get('author')
        updating_review.review_text = serializer.validated_data.get('review_text')
        updating_review.rating_for_anime = serializer.validated_data.get('rating_for_anime')
        updating_review.anime_id = serializer.validated_data.get('anime')
        updating_review.save()
        return Response(data={'message': 'Data received!',
                              'review': ReviewsSerializers(updating_review).data},
                        status=status.HTTP_201_CREATED)
