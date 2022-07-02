from fileinput import filename
from genericpath import exists
from multiprocessing import context
import random
from django.views.generic.base import TemplateView
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

import markdown2


from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def link_page(request, title):
    return render(request, "encyclopedia/info_page.html", {
        "title" : title,
        "content": markdown2.markdown(util.get_entry(title))
    })


class SearchForm(forms.Form):
    query = forms.CharField(label='New Search', max_length=50)

def search(request):
    # populate the form
    form = SearchForm()
    # prepare for substring search with empty list for possible matches
    matches = []
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
                    return HttpResponseRedirect(reverse("encyclopedia:entries",
                    kwargs={"title": entry}))
                # shows list of possible matches
                elif substring_match:
                    matches.append(entry)
                    print(entry)
    context = {
        "form": SearchForm(),
        "substring_match": matches
    }
    response = render(request, "encyclopedia/search_page.html", context)
    return response


# setup for editing entries with textarea
class EntryForm(forms.Form):
    content = forms.CharField(required = True, widget = forms.Textarea, label = "Edit Page Text")
# calling the request for HttpResponse and title to activate

def edit_entry(request, title):
    if request.method == 'POST':
        # saves the entry over the old md file, also paying attention to utf8 decode
        util.save_entry(title, bytes(request.POST['content'], 'utf8'))
        # redirect to newly saved page
        return link_page(request, title)
    else:
        # show the original content, get since there is nothing being written to db
        title = title
        content = util.get_entry(title)
        form = EntryForm(request.GET or None, initial={'content': content})
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content,
            "form": form
        })
        

# setup for new page creation
class New_Page(forms.Form):
    title = forms.CharField(required = True, widget=forms.TextInput, label = "New Title")
    content = forms.CharField(required = True, widget = forms.Textarea, label = "New Entry Text")
# function to start a new page with save_entry util

def new_entry(request):
    # request method should be post as this will add data
    if request.method == 'POST':
        form = New_Page(request.POST)
        # check if required entered data is valid
        if form.is_valid():
            # strips down title to compare against existing titles
            title = form.cleaned_data["title"].strip()
            content = form.cleaned_data["content"]
            # opens empty page to await new entry
            if util.get_entry(title):
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "exists": True,
                    "title": title
                })
            else:
                form = form.cleaned_data["title"]
                util.save_entry(title, content)
                return link_page(request, title)
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form,
                "exists": False
            })
    return render(request, "encyclopedia/new_page.html", {
        "form": New_Page(),
        "exists": False
    })


def random_entry(request):
    select_entry = util.list_entries()
    random_page = random.choice(select_entry)
    return redirect('encyclopedia:entries', title=random_page)

