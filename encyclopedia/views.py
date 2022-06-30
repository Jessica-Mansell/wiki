from fileinput import filename
from turtle import title
from django import forms
from django.shortcuts import render
import markdown2

from markdown2 import Markdown

import encyclopedia

markdowner = Markdown()

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def link_page(request):
    return render(request, "encyclopedia/info_page.html", {
        "title" : title
    })

