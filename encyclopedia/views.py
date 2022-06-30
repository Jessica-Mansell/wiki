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
        "entries":util.save_entry(filename)
    })

class SearchPage(forms.Form):
    query = forms.CharField(label="New Item",
    hint_text="Search the Wiki")

    def search_wiki(request):
        form = SearchPage()
        context = { 
            "form": form
        }

        response = render(request, "encyclopedia/layout.html", context)
        return response

class EditEntryPage(forms.Form):
    title= forms.CharField(widget=forms.HiddenInput, label="title")
    content = forms.CharField(widget=forms.Textarea, label="content")

    def edit_page(request):
        if request.method == "POST":
            form = SearchPage(request.POST)

            if form.is_valid():
                title = form.scrubbed_data["title"]
                content = util.get_entry(title)
                form = EditEntryPage(initial={
                    "title": title,
                    "content": content
                })
                return render(request, "encyclopedia/edit_page.html", {
                    "title":title,
                    "form": form
                })
