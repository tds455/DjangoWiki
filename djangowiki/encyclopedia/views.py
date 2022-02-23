from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import markdown2
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Display the requested page
# ref: https://docs.djangoproject.com/en/4.0/intro/tutorial03/
def display(request, title):
    # Check if page exists / validate input
    if not util.get_entry(title):
        # Placeholder return value.  
        return render(request, 'encyclopedia/error.html', {"title": title})
    #Return page
    else:
        markdownpage = util.get_entry(title)
        # Convert content from markdown to html
        # Code taken from / based on https://github.com/trentm/python-markdown2
        markdowner = Markdown()
        htmlpage = markdowner.convert(markdownpage)

        # Pass html into render function.
        return render(request, 'encyclopedia/page.html', {"title": title, "pagebody": htmlpage})

def search(query):

    # Take search input and either return page, or possibly related results based on substring.
    if request.method == POST:
        # Create a form instance and pass data into it
        # Based on https://docs.djangoproject.com/en/4.0/topics/forms/
        form = searchform(request.post)
        
        # Check for a direct match for search value
        if util.get_entry(form):
            # If found, return relevant page
            markdownpage = util.get_entry(query)
            markdowner = Markdown()
            htmlpage = markdowner.convert(markdownpage)   
            # Pass html into render function.        
            return render(request, 'encyclopedia/page.html', {"title": title, "pagebody": htmlpage})
        else:
            # Placeholder render return
            return render(request, 'encyclopedia/error.html', {"title": title})
            # Return search page with any partial substring matches



# Following classes based on https://docs.djangoproject.com/en/4.0/topics/forms/
class searchform(forms.Form):
    query = forms.CharField(label='Search', max_length=100)