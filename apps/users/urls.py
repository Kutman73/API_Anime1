from django.urls import path
from apps.users.api.apiviews import *

urlpatterns = (
    path('authorization/', UserAuthorizationAPIView.as_view()),
    path('registration/', UserRegistrationAPIView.as_view())
)
