from django.urls import path
from django.contrib import admin

import wiki

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("wiki/<str:title>/", views.link_page, name="wiki"),
    path("wiki/", views.SearchPage, name="wiki_search") 
]
