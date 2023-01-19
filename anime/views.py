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

    @action(detail=False, methods=['post'])
    def create(self, request, **kwargs):
        serializer = AnimeCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
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
