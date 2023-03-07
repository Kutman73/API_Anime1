from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from api_anime01 import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('', include('api_anime01.swagger')),
    path('api/v1/', include('apps.anime.urls')),
    path('api/v1/users/', include('apps.users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
