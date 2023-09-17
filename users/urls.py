from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import SignUpAPIView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name="signup"),
    path('login/', obtain_auth_token, name='login'),
]