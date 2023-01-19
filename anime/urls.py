from django.urls import path
from .views import *


urlpatterns = (
    path('', AnimeModelViewSet.as_view({'get': 'list',
                                        'post': 'create'})),
    path('<slug:original_anime_name>/', AnimeModelViewSet.as_view({'get': 'retrieve',
                                                                   'delete': 'destroy'})),
)
