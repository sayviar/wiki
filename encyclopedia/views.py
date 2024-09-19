from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

class newEntryForm(forms.Form):
    title = forms.CharField(label="",widget = forms.TextInput(attrs={
        "placeholder": "Page Title"
    }))
    text = forms.CharField(label = "",widget = forms.Textarea(attrs={
        "placeholder": "Page Content in Markdown Format"
    }))
class editForm(forms.Form):
    text = forms.CharField(label = "",widget = forms.Textarea(attrs={
        "placeholder": "Page Content in Markdown Format"
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def title(request, title):
    content = util.get_entry(title)
    if content:
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": content
        })
    else: 
        return render(request, "encyclopedia/error.html",{
            "title": title,
            "error": "Error: Page not found"
        })

def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        content = util.get_entry(title)
        if content: 
            content = markdown2.markdown(content)
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "content": content
            })
        else:
            list = util.list_entries()
            similar = []
            for entry in list:
                if title.lower() in entry.lower():
                    similar.append(entry)
            return render(request, "encyclopedia/searchresult.html", {
                "titles": similar
            })

def createEntry(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["text"]
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "title": title,
                "error": "Error: Page already exists"
            })
        util.save_entry(title, content)
        content = util.get_entry(title)
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": content
        })
    return render(request, "encyclopedia/create.html", {
        "createForm" : newEntryForm()
    })

def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": editForm(initial={"text": content})  
        })
    if request.method == "POST":
        form = editForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["text"] 
            content = content.replace('\r', '')
            util.save_entry(title, content) 
            return HttpResponseRedirect(reverse("title", args=[title]))  
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })
def randomPage(request):
    list = util.list_entries()
    title = random.choice(list)
    content = util.get_entry(title)
    content = markdown2.markdown(content)
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "content": content
    })