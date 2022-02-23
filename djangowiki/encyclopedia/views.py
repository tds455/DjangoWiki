from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import markdown2
from markdown2 import Markdown

from . import util


def index(request):
    form = searchform()
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), 'form': form})

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
        form = searchform()
        # Pass html into render function.
        return render(request, 'encyclopedia/page.html', {"title": title, "pagebody": htmlpage, 'form': form})

def search(request):
    # Take search input and either return page, or possibly related results based on substring.
    if request.method == "POST":
        # Create a form instance and pass data into it
        # Based on https://docs.djangoproject.com/en/4.0/topics/forms/
        form = searchform(request.POST)
        if form.is_valid():
            # Validate input and strip relevant data
            form = form.cleaned_data["search"]

            if not form.isalpha():
                form = searchform()
                return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), 'form': form})

            # Check for a direct match for search value
            if util.get_entry(form):
                # If found, return relevant page, converting markdown to html
                markdownpage = util.get_entry(form)
                markdowner = Markdown()
                htmlpage = markdowner.convert(markdownpage)   
                
                # Pass html into render function.        
                return render(request, 'encyclopedia/page.html', {"title": form, "pagebody": htmlpage})

            else:
                # Check to see if query is present as a substring 
                 return render(request, 'encyclopedia/error.html', {"title": form})

        else:
            # If form input cannot be validated, return to index page
            form = searchform()
            return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), 'form': form})
            
    else: 
        # If someone attempts to navigate to /search directly, display the index page instead.
        form = searchform()
        return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), 'form': form})



# Following classes based on https://docs.djangoproject.com/en/4.0/topics/forms/
class searchform(forms.Form):
    search = forms.CharField(label='search', max_length=100)
    