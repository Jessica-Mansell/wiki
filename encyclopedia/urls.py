from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("wiki/<str:title>/", views.link_page, name="entries"),
]
