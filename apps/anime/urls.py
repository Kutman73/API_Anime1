from django.urls import path, include
from rest_framework import routers
from .api.viewsets import *

anime_router = routers.DefaultRouter()
anime_router.register(r'anime', AnimeModelViewSet)

urlpatterns = (
    path('', include(anime_router.urls)),
    path('anime/<slug:slug>/seasons/',
         SeasonModelViewSet.as_view({'get': 'list',
                                     'post': 'create'})),
    path('anime/<slug:slug>/season-<int:pk>/',
         SeasonModelViewSet.as_view({'get': 'retrieve',
                                     'put': 'update',
                                     'delete': 'destroy'})),
    path('anime/<slug:slug>/season-<int:pk>/episodes/',
         EpisodeModelViewSet.as_view({'get': 'list',
                                     'post': 'create'})),
    path('anime/<slug:slug>/season-<int:pk>/episode-<int:id>/',
         EpisodeModelViewSet.as_view({'get': 'retrieve',
                                      'put': 'update',
                                      'delete': 'destroy'})),
    path('anime/<slug:slug>/season-<int:season>'
         '/episode-<int:episode>/download/',
         DownloadEpisodeViewSet.as_view({'get': 'list',
                                         'post': 'create'})),
    path('anime/<slug:slug>/season-<int:season>'
         '/episode-<int:episode>/download/<str:filename>/',
         DownloadEpisodeViewSet.as_view({'get': 'retrieve'})),
    path('anime/<slug:slug>/movies/',
         AnimeMovieModelViewSet.as_view({'get': 'list',
                                         'post': 'create'})),
    path('anime/<slug:slug>/movie-<int:pk>/',
         AnimeMovieModelViewSet.as_view({'get': 'retrieve',
                                         'delete': 'destroy',
                                         'put': 'update'})),
    path('anime/<slug:slug>/reviews/',
         ReviewModelViewSet.as_view({'get': 'list',
                                     'post': 'create'})),
    path('anime/<slug:slug>/review-<int:pk>/',
         ReviewModelViewSet.as_view({'get': 'retrieve',
                                     'delete': 'destroy',
                                     'put': 'update'})),
)
