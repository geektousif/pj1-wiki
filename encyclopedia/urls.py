from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wikipage, name="wikipage"),
    path("search", views.new_search, name="search"),
    path("add_entry", views.add_view, name='add_entry'),
    path("edit_entry/<str:title>", views.edit_entry, name='edit'),
    path("random", views.random_wiki, name="random_wiki")
]
