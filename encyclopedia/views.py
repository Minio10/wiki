from django.shortcuts import render,redirect
from django import forms
from markdown2 import markdown

from . import util
import random

class NewEntryForm(forms.Form):

    title = forms.CharField(label = "Title")
    info = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write the Content using Markdown Format'}),label ="Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pageInfo(request,title):

    entry = util.get_entry(title.strip())
    if(entry is not None):
        entry = markdown(entry)
        return render (request, "encyclopedia/pageInfo.html",{
            "title":title,"info":entry
        })
    return render(request,"encyclopedia/error.html",{
        "title":title
    })

def searchRes(request):
    if request.method == "GET":
        title = request.GET['entry']
        entry = util.get_entry(title)
        possible_entries = searchSub(title)
        if(entry is not None):
            return render (request, "encyclopedia/pageInfo.html",{
                "title":title,"info":entry
            })
        elif possible_entries:
            return render (request, "encyclopedia/searchResults.html",{
                "entries":possible_entries
            })

        return render(request,"encyclopedia/error.html",{
            "title":title
        })


def searchSub(title):

     entries = util.list_entries()
     new_entries = []
     for elem in entries:
         if (title in elem):
             new_entries.append(elem)
     return new_entries

def newEntry(request):
    return render(request,"encyclopedia/newEntry.html",{
        "form":NewEntryForm()
    })

def verifyEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            info = form.cleaned_data["info"]
            if(util.get_entry(title) is not None):
                return render(request,"encyclopedia/newEntry.html",{
                    "error":"Title already exists !","form":NewEntryForm()
                })
            util.save_entry(title,info)
            return redirect("pageInfo", title=title)

    return render(request,"encyclopedia/index.html")

def editPage(request,title):
    content = util.get_entry(title)
    form = NewEntryForm({'title': title, 'info': content})
    return render(request,"encyclopedia/editEntry.html",{
        "form":form
    })

def editEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            info = form.cleaned_data["info"]
            util.save_entry(title,info)
            return redirect("pageInfo", title=title)

def randomPage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect("pageInfo", title=title)
