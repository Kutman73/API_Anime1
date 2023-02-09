from django.urls import path, include
from rest_framework import routers
from .views import *

anime_router = routers.DefaultRouter()
anime_router.register(r'', AnimeModelViewSet)

urlpatterns = (
    path('', include(anime_router.urls)),
    path('<slug:original_anime_name>/seasons/',
         SeasonModelViewSet.as_view({'get': 'list',
                                     'post': 'create'})),
    path('<slug:original_anime_name>/season-<int:pk>/',
         SeasonModelViewSet.as_view({'get': 'retrieve',
                                     'put': 'update',
                                     'delete': 'destroy'})),
    path('<slug:original_anime_name>/season-<int:pk>/episodes/',
         EpisodeModelViewSet.as_view({'get': 'list',
                                     'post': 'create'})),
    path('<slug:original_anime_name>/season-<int:pk>/episode-<int:id>/',
         EpisodeModelViewSet.as_view({'get': 'retrieve',
                                      'put': 'update',
                                      'delete': 'destroy'})),
    path('<slug:original_anime_name>/season-<int:season>'
         '/episode-<int:episode>/download/',
         DownloadEpisodeViewSet.as_view({'get': 'list',
                                         'post': 'create'})),
    path('<slug:original_anime_name>/season-<int:season>'
         '/episode-<int:episode>/download/<str:filename>/',
         DownloadEpisodeViewSet.as_view({'get': 'retrieve'})),
    path('', include(anime_router.urls)),
    path('<slug:original_anime_name>/movies/',
         AnimeMovieModelViewSet.as_view({'get': 'list',
                                         'post': 'create'})),
    path('<slug:original_anime_name>/movie-<int:pk>/',
         AnimeMovieModelViewSet.as_view({'get': 'retrieve',
                                         'delete': 'destroy',
                                         'put': 'update'})),
    path('<slug:original_anime_name>/reviews/',
         ReviewModelViewSet.as_view({'get': 'list',
                                     'post': 'create'})),
    path('<slug:original_anime_name>/review-<int:pk>/',
         ReviewModelViewSet.as_view({'get': 'retrieve',
                                     'delete': 'destroy',
                                     'put': 'update'})),
)
