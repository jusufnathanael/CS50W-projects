from django.shortcuts import get_object_or_404, render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db import models
from markdown2 import Markdown
from . import util
import re
import random


def check_if_exists(value):
    for entry in util.list_entries():
        if value.lower() == entry.lower():
            message = "An encyclopedia entry with the provided title already exists!"
            raise forms.ValidationError(message)

class Wiki(models.Model):
    title = models.CharField(max_length=100, validators=[check_if_exists])
    content = models.TextField()
    
    def __str__(self):
        return self.title
    
class NewWikiForm(forms.ModelForm):
    class Meta:
        model = Wiki
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "content": forms.Textarea(attrs={'class': 'form-control'})
        }

class EditWikiForm(forms.ModelForm):
    class Meta:
        model = Wiki
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={'class': 'form-control'})
        }


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, name):
    for entry in util.list_entries():
        if name.lower() == entry.lower():
            return render(request, f"entries/html/{entry}.html", {
                "name": entry
            })
    else:
        return render(request, "encyclopedia/error.html")

def rand(request):
    name = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("page", args=(name,)))

def search(request):
    name = request.GET["q"]
    # if the query matches
    for entry in util.list_entries():
        if (name.lower() == entry.lower()):
            return redirect(f"/wiki/{entry}")
    # if the query doesn't match
    result = []
    for entry in util.list_entries():
        if re.search(name.lower(), entry.lower()):
            result.append(entry)
    return render(request, "encyclopedia/results.html", {
        "entries": result
    })

def begin():
    begin = "{% extends \"encyclopedia/entries_layout.html\" %}\n\n"
    begin += "{% block body %}\n\n"
    return begin

def end():
    return "\n{% endblock %}"

def add(request):
    if request.method == "POST":
        form = NewWikiForm(request.POST)
        if form.is_valid():
            # get the title and content
            title = request.POST['title']
            content = request.POST['content']
            # add a new markdown file
            with open(f"entries/{title}.md", "w", newline='') as f:
                f.write(content)
            # convert to a new html file
            with open(f"entries/html/{title}.html", "w", newline='') as f:
                markdowner = Markdown()
                f.write(begin() + markdowner.convert(content) + end())
            # show the new file
            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            # stay in the form page
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    # render an empty form
    return render(request, "encyclopedia/add.html", {
        "form": NewWikiForm()
    })


def edit(request, name):
    # open the markdown file
    with open(f"entries/{name}.md", "r+", newline='') as f:
        inside = f.read()
        wiki = Wiki(title=name, content=inside)
        # if method == POST
        if request.method == "POST":
            form = EditWikiForm(request.POST)
            if form.is_valid():
                # get the new content
                content = request.POST['content']
                # update the markdown file
                f.seek(0)
                f.truncate()
                f.write(content)
                print(content)
                # update the html file
                with open(f"entries/html/{name}.html", "w", newline='') as f:
                    markdowner = Markdown()
                    f.write(begin() + markdowner.convert(content) + end())
                # show the new file
                return HttpResponseRedirect(f"/wiki/{name}")
            else:
                return render(request, f"/wiki/{name}/edit", {
                    "form": form,
                    "title": name
                })
        # render a new edit page
        return render(request, f"encyclopedia/edit.html", {
            "form": EditWikiForm(instance=wiki),
            "title": name
        })
