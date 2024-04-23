from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, CustomTokenObtainPairView, UserRetrieveAPIView, InvitationActivate

app_name = UsersConfig.name


urlpatterns = [
    path('users/', UserCreateAPIView.as_view(), name='users_create'),
    path('users/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='users_retrieve'),
    path('users/activate_invite/', InvitationActivate.as_view(), name='activate_invite')
]
