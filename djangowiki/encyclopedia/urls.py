from django.urls import path

from . import views

urlpatterns = [
    # Path to show index page
    path("", views.index, name="index"),
    # Path to show a certain page
    path("<str:title>", views.display, name="display")
]
