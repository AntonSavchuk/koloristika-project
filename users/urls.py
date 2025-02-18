from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path("profile/", views.profile_view, name="account_profile"),
]

