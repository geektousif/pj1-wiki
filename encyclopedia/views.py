from django.shortcuts import render, redirect
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django import forms
from django.views.generic.edit import UpdateView
import random

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
        if searches.lower() in entry.lower():
            search_result.append(entry)
        else:
            pass


    return render(request, "encyclopedia/search.html", {"search_result" : search_result})

class AddForm(forms.Form):
    title = forms.CharField(max_length=20)
    content = forms.CharField(widget=forms.Textarea)

def add_view(request):
    entries = util.list_entries()
    entries = [entry.lower() for entry in entries]
    errors = []
    if request.method == 'POST':
        form = AddForm(request.POST)
        title = form['title'].value()

        if title.lower() in entries:
            error = "Already Available Data"
            errors.append(error)

        else:
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                util.save_entry(title, content)
            else:
                form = AddForm()

            return HttpResponseRedirect('/')
    else:
        form = AddForm()

    return render(request, "encyclopedia/add_new.html", {"form" : form, "errors": errors})

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def edit_entry(request, title):
    entry = util.get_entry(title)
    if request.method == 'GET':
        form = EditForm(initial={'content' : entry})

    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
        return HttpResponseRedirect('/')

    return render(request, "encyclopedia/edit.html", {"form":form, "title":title})

def random_wiki(request):
    entries = util.list_entries()
    number = len(entries) - 1
    rand_entry_index = random.randint(0, number)
    random_entry = entries[rand_entry_index]
    random_content = util.get_entry(random_entry)
    markdowner = Markdown()
    md_entry = markdowner.convert(random_content)

    return render(request, "encyclopedia/wikipage.html", {
        "content": md_entry,
        "wikientry": random_entry
        })
