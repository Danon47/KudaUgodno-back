from django.urls import path

from users.apps import UsersConfig

from .views import (UserDestroyView, UserListCreateView, UserRetrieveView,
                    UserUpdateView)

app_name = UsersConfig.name

urlpatterns = [
    path("users/", UserListCreateView.as_view(), name="user_list_create"),
    path("users/<int:pk>/", UserRetrieveView.as_view(), name="user_retrieve"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", UserDestroyView.as_view(), name="user_delete"),
]
