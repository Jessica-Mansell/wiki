from fileinput import filename
from multiprocessing import context
from turtle import title
from urllib import response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2

from markdown2 import Markdown

import encyclopedia

markdowner = Markdown()

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def link_page(request, title):
    return render(request, "encyclopedia/info_page.html", {
        "title" : title
    })

class SearchForm(forms.Form):
    query = forms.CharField(label='New Search', max_length=50)

    def search(request):
        # populate the form
        form = SearchForm()
        # prepare for substring search with empty list for possible matches
        queries_list = []
        # check for GET request method and run request
        if request.method == "GET":
            form = SearchForm(request.GET)
            # check for valid input and clean up the data to query
            if form.is_valid():
                # loop through list of entries
                for entry in util.list_entries():
                    # put query through a cleaned_data, returns as string and makes all lowercase
                    match_same = form.cleaned_data["query"].casefold() == entry.casefold()
                    # if substring query matches anything, clean entry as well
                    substring_match = form.cleaned_data["query"].casefold() in entry.casefold()
                    # query match shows user the matching page
                    if match_same:
                        return HttpResponseRedirect(reverse("wiki",
                        kwargs={"title": entry}))
                    # shows list of possible matches
                    elif substring_match:
                        substring_match.append(entry)

        context = {
            "form": SearchForm(),
            "substring_match": substring_match
        }

        response = render(request, "encyclopedia/search_page.html", context)
        return response


