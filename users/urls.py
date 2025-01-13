from django.urls import path

from users.apps import UsersConfig

from .views import UserListCreateView, UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path("", UserListCreateView.as_view(), name="user_list_create"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_name_detail")
]
