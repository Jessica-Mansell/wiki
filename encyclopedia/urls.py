from django.urls import path
from django.contrib import admin

import wiki

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("wiki/<str:title>/", views.link_page, name="entries"),
    path("search_page/", views.search, name="search_query"),
    path("edit_page/", views.edit_entry, name="edit"),
    path("new_page/", views.new_entry, name="new")
]
