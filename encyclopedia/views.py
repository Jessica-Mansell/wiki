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
                    return HttpResponseRedirect(reverse("entries",
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

# setup for editing entries with textarea
class EntryForm(forms.Form):
    content = forms.CharField(required = True, widget = forms.Textarea, label = "Text")
# calling the request for HttpResponse and title to activate
def edit_entry(request, title):
    if request.method == 'POST':
        # saves the entry over the old md file
        util.save_entry(title, request.POST['content'])
        # redirect to newly saved page
        return HttpResponseRedirect(reverse('entry', args=(title,)))
    else:
        # show the original content
        content = util.get_entry(title)
        form = EntryForm(request.POST or None, original={'content': content})
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content,
            "form": form
        })
