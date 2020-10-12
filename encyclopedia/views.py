from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponse
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wikipage(request,title):
    entry = util.get_entry(title)
    markdowner = Markdown()
    md_entry = markdowner.convert(entry)

    return render(request, "encyclopedia/wikipage.html", {
        "content": md_entry,
        "wikientry": title
        })

def new_search(request):
    searches = request.POST.get('q')
    entries = util.list_entries()
    search_result = []


    for entry in entries:
        if entry.lower() == searches.lower():
            search_result.append(searches)
        else:
            return HttpResponse("No Matches")

    return render(request, "encyclopedia/search.html", {"search_result" : search_result})