from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from apps.anime.services.services import get_local_files
from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework import permissions
from apps.anime.models import (
    Anime,
    AnimeSeason,
    AnimeEpisode,
    AnimeMovie,
    Review,
)
from apps.anime.api.validateserializers import (
    AnimeCreateSerializer,
    AnimeUpdateSerializer,
    SeasonCreateSerializer,
    SeasonUpdateSerializer,
    EpisodeCreateSerializer,
    EpisodeUpdateSerializer,
    MovieCreateSerializer,
    MovieUpdateSerializer,
    ReviewValidateSerializer,
)
from apps.anime.api.serializers import (
    AnimeSerializers,
    SeasonSerializers,
    EpisodeSerializers,
    MovieSerializers,
    ReviewsSerializers,
)
from api_anime01 import settings
import glob
import os


class DownloadEpisodeViewSet(ViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    project_url = "http://127.0.0.1:8000/media"

    @staticmethod
    def get_folder(**kwargs: dict) -> str:
        folder_to_files_for_download = \
            f"{settings.MEDIA_ROOT}/" \
            f"{kwargs['slug']}/season-" \
            f"{kwargs['season']}/episode-{kwargs['episode']}/"
        return folder_to_files_for_download

    @action(detail=False, methods=['get'])
    def list(self, request, **kwargs: dict) -> Response:
        files_to_download = self.get_folder(**kwargs)
        return Response(get_local_files(files_to_download))

    @action(detail=True, methods=['get'])
    def retrieve(self, request, **kwargs):
        files_to_download = self.get_folder(**kwargs)
        file_list = get_local_files(files_to_download)
        if len(file_list) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT,
                            data={'detail': 'No file(s) were for this episode'})
        files = glob.glob(files_to_download + '*' + kwargs['filename'] + '*')
        if len(files) == 1:
            file_location = files[0]
            file_name = kwargs['slug'] + '-episode-' + file_location[75:81]
            file_response = FileResponse(open(file_location, 'rb'))
            file_response['content_type'] = 'application/force-download'
            file_response['Content-Disposition'] = 'attachment; filename=%s' % file_name
            return file_response
        elif len(files) > 1:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'detail': 'Several such files were found according to the search '
                                            'results, please enter a more accurate file name'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'detail': "you didn't enter the file name "
                                            "sequentially(in order from left to right"})

    @action(detail=False, methods=['post'])
    def create(self, request):
        project_base_directory = str(settings.BASE_DIR)
        requesttable_file = request.data['file']
        file_path = project_base_directory + requesttable_file[21:]
        if os.path.isfile(file_path):
            file_response = FileResponse(open(file_path, 'rb'))
            file_response['content_type'] = 'application/force-download'
            file_response['Content-Disposition'] = 'attachment; filename=%s' % file_path[67:]
            return file_response
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'detail': 'File not exists'})


class AnimeModelViewSet(ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializers
    lookup_field = 'slug'

    def create(self, request, **kwargs):
        serializer = AnimeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.validated_data.get('author')
        title = serializer.validated_data.get('title')
        slug = serializer.validated_data.get('slug')
        cover = serializer.validated_data.get('cover')
        description = serializer.validated_data.get('description')
        producer = serializer.validated_data.get('producer')
        genre = serializer.validated_data.get('genre')
        theme = serializer.validated_data.get('theme')
        anime_status = serializer.validated_data.get('status')
        release_date = serializer.validated_data.get('release_date')
        new_anime = Anime.objects.create(author_id=author,
                                         title=title,
                                         slug=slug,
                                         cover=cover,
                                         description=description,
                                         status_id=anime_status,
                                         release_date=release_date)
        new_anime.producer.set(producer)
        new_anime.genre.set(genre)
        new_anime.theme.set(theme)
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
        anime.slug = serializer.validated_data.get('slug')
        anime.cover = serializer.validated_data.get('cover')
        anime.description = serializer.validated_data.get('description')
        anime.producer.set(serializer.validated_data.get('producer'))
        anime.genre.set(serializer.validated_data.get('genre'))
        anime.theme.set(serializer.validated_data.get('theme'))
        anime.status_id = serializer.validated_data.get('status')
        anime.release_date = serializer.validated_data.get('release_date')
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
            anime__slug=kwargs['slug']
        )
        serializer = self.serializer_class(anime_season, many=True)
        return Response(data=serializer.data)

    def create(self, request, **kwargs):
        anime = self.queryset.filter(
            anime__slug=kwargs['slug']
        )
        serializer = SeasonCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        anime.author = serializer.validated_data.get('author')
        anime.anime = serializer.validated_data.get('anime')
        anime.season_number = serializer.validated_data.get('season_number')
        anime.voice_acting = serializer.validated_data.get('voice_acting')
        anime.producer = serializer.validated_data.get('producer')
        anime.title = serializer.validated_data.get('title')
        anime.release_date = serializer.validated_data.get('release_date')
        new_season = AnimeSeason.objects.create(
            author_id=anime.author,
            anime_id=anime.anime,
            season_number=anime.season_number,
            title=anime.title,
            release_date=anime.release_date
        )
        new_season.voice_acting.set(anime.voice_acting)
        new_season.producer.set(anime.producer)
        new_season.save()
        return Response(data={'message': 'Data received!',
                              'anime': SeasonSerializers(new_season).data},
                        status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        season = self.get_object()
        serializer = SeasonUpdateSerializer(data=request.data, context={'id': season.id})
        serializer.is_valid(raise_exception=True)
        season.author_id = serializer.validated_data.get('author')
        season.anime_id = serializer.validated_data.get('anime')
        season.season_number_id = serializer.validated_data.get('season_number')
        season.voice_acting.set(serializer.validated_data.get('voice_acting'))
        season.producer.set(serializer.validated_data.get('producer'))
        season.title = serializer.validated_data.get('title')
        season.release_date = serializer.validated_data.get('release_date')
        season.save()
        return Response(data={'message': 'Data received!',
                              'anime': SeasonSerializers(season).data},
                        status=status.HTTP_201_CREATED)


class EpisodeModelViewSet(ModelViewSet):
    queryset = AnimeEpisode.objects.all()
    serializer_class = EpisodeSerializers
    lookup_field = 'id'

    def list(self, request, **kwargs):
        episode = self.queryset.filter(
            season_id=kwargs['pk']
        )
        serializer = self.serializer_class(episode, many=True)
        return Response(data=serializer.data)

    def create(self, request, **kwargs):
        anime = self.queryset.filter(
            season__anime__slug=kwargs['slug']
        )
        serializer = EpisodeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        anime.author = serializer.validated_data.get('author')
        anime.title = serializer.validated_data.get('title')
        anime.season = serializer.validated_data.get('season')
        anime.video = serializer.validated_data.get('video')
        anime.voice_acting = serializer.validated_data.get('voice_acting')
        anime.episode_number = serializer.validated_data.get('episode_number')
        anime.release_date = serializer.validated_data.get('release_date')
        new_episode = AnimeEpisode.objects.create(
            author_id=anime.author,
            title=anime.title,
            season_id=anime.anime,
            video=anime.video,
            voice_acting_id=anime.voice_acting,
            episode_number=anime.episode_number,
            release_date=anime.release_date
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
        episode.title = serializer.validated_data.get('title')
        episode.season_id = serializer.validated_data.get('season')
        episode.video = serializer.validated_data.get('video')
        episode.voice_acting = serializer.validated_data.get('voice_acting')
        episode.episode_number = serializer.validated_data.get('episode_number')
        episode.release_date = serializer.validated_data.get('release_date')
        episode.save()
        return Response(data={'message': 'Data received!',
                              'episode': EpisodeSerializers(episode).data},
                        status=status.HTTP_201_CREATED)


class AnimeMovieModelViewSet(ModelViewSet):
    queryset = AnimeMovie.objects.all()
    serializer_class = MovieSerializers
    lookup_field = 'pk'

    def list(self, request, **kwargs):
        movie = self.queryset.filter(
            anime__slug=kwargs['slug']
        )
        serializer = self.serializer_class(movie, many=True)
        return Response(data=serializer.data)

    def create(self, request, **kwargs):
        serializer = MovieCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        anime = self.queryset.filter(anime__slug=kwargs['slug'])
        anime.author = serializer.validated_data.get('author')
        anime.title = serializer.validated_data.get('title')
        anime.voice_acting = serializer.validated_data.get('voice_acting')
        anime.anime = serializer.validated_data.get('anime')
        anime.duration = serializer.validated_data.get('duration')
        anime.producer = serializer.validated_data.get('producer')
        anime.video = serializer.validated_data.get('video')
        anime.release_date = serializer.validated_data.get('release_date')
        new_movie = AnimeMovie.objects.create(
            author_id=anime.author,
            title=anime.title,
            voice_acting_id=anime.voice_acting_anime_of_the_movie,
            anime_id=anime.anime,
            duration=anime.duration,
            video=anime.video,
            release_date=anime.release_date
        )
        new_movie.producer.set(anime.producer)
        new_movie.save()
        return Response(data={'message': 'Data received!',
                              'anime_movie': MovieSerializers(new_movie).data},
                        status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        movie = self.get_object()
        serializer = MovieUpdateSerializer(data=request.data, context={'id': movie.id})
        serializer.is_valid(raise_exception=True)
        movie.author_id = serializer.validated_data.get('author')
        movie.title = serializer.validated_data.get('title')
        movie.voice_acting = serializer.validated_data.get('voice_acting')
        movie.anime_id = serializer.validated_data.get('anime')
        movie.video = serializer.validated_data.get('video')
        movie.duration = serializer.validated_data.get('duration')
        movie.producer.set(serializer.validated_data.get('producer'))
        movie.movie_number = serializer.validated_data.get('movie_number')
        movie.release_date = serializer.validated_data.get('release_date')
        movie.save()
        return Response(data={'message': 'Data received!',
                              'anime': MovieSerializers(movie).data},
                        status=status.HTTP_201_CREATED)


class ReviewModelViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializers
    lookup_field = 'pk'

    def list(self, request, **kwargs):
        anime_review = self.queryset.filter(
            anime__slug=kwargs['slug']
        )
        serializer = ReviewsSerializers(anime_review, many=True)
        return Response(data=serializer.data)

    def create(self, request, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.validated_data.get('author')
        comment = serializer.validated_data.get('comment')
        rating = serializer.validated_data.get('rating')
        anime = serializer.validated_data.get('anime')
        new_review = Review.objects.create(
            author_id=author,
            comment=comment,
            rating=rating,
            anime_id=anime
        )
        new_review.save()
        return Response(data={'message': 'Data received!',
                              'review': ReviewsSerializers(new_review).data},
                        status=status.HTTP_201_CREATED)

    def update(self, request, **kwargs):
        review = self.queryset.get(
            anime__slug=kwargs['slug']
        )
        serializer = ReviewValidateSerializer(
            data=request.data, context={'id': review.id}
        )
        serializer.is_valid(raise_exception=True)
        review.author_id = serializer.validated_data.get('author')
        review.comment = serializer.validated_data.get('comment')
        review.rating = serializer.validated_data.get('rating')
        review.anime_id = serializer.validated_data.get('anime')
        review.save()
        return Response(data={'message': 'Data received!',
                              'review': ReviewsSerializers(review).data},
                        status=status.HTTP_201_CREATED)
