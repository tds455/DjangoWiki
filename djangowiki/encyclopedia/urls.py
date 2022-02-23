from django.urls import path

from . import views

urlpatterns = [
    # Path to show index page
    path("", views.index, name="index"),
    # Path to show a certain page
    # <str:title> allows the GET request to match to a path
    path("wiki/<str:title>", views.display, name="display"),
    # Path to process search input
    path("search", views.search, name="search")

]
