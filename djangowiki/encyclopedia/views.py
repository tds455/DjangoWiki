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

        # Return error page and reset form
        form = searchform()
        return render(request, 'encyclopedia/error.html', {"title": title, 'form': form})

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
            # Validate input and strip relevant data.  Convert to lowercase to allow for matching substrings to titles.
            form = form.cleaned_data["search"].lower()

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
                # Get list of all entries
                entries = util.list_entries()

                # Check to see if query is present as a substring and return as a list.  Convert results to lowercase to allow matching substrings to titles.

                # sample code from util.py
                # for filename in filenames if filename.endswith(".md")))
                query = []
                for filename in entries:
                    if form in filename.lower():
                        query.append(filename)

                # Debugging value
                print(query)

                # Return list of search results.  Reset form.
                form = searchform()

                # If results found, return list of results
                if len(query) > 0:
                    return render(request, 'encyclopedia/search.html', {"entries": query, 'form': form})
                
                if len(query) is 0:
                    query = "No results found"
                    return render(request, 'encyclopedia/search.html', {"feedback": query, 'form': form}) 

        else:
            # If form input cannot be validated, return to index page
            form = searchform()
            return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), 'form': form})
            
    else: 
        # If someone attempts to navigate to /search directly, display the index page instead.
        form = searchform()
        return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), 'form': form})

def create(request):
    if request.method == "POST":
        # If method is POST, process input.
        form = createform(request.POST)
        if form.is_valid():

            # Validate input and strip relevant data.
            title = form.cleaned_data["title"]
            body = form.cleaned_data["create"]
            # If page already exists, return error.
            if util.get_entry(title):
                form = searchform()
                error = "Page already exists!"
                return render(request, 'encyclopedia/error.html', {'form': form, 'error': error})
            else:
                # Otherwise, create new page
                util.save_entry(title,body)
                
                # Display new page
                # Convert content from markdown to html
                # Code taken from / based on https://github.com/trentm/python-markdown2
                markdownpage = util.get_entry(title)
                markdowner = Markdown()
                htmlpage = markdowner.convert(markdownpage)
                form = searchform()

                # Pass html into render function.
                return render(request, 'encyclopedia/page.html', {"title": title, "pagebody": htmlpage, 'form': form})
            
    else:
        # If method is GET, return form.
        newform = createform()
        form = searchform()
        return render(request, "encyclopedia/create.html", {'form': form, 'createform': newform})

def edit(request):
    return None






# Following classes based on https://docs.djangoproject.com/en/4.0/topics/forms/
class searchform(forms.Form):
    search = forms.CharField(label='search', max_length=100)

class createform(forms.Form):
    title = forms.CharField(label='title', max_length=50, widget = forms.TextInput(attrs={'class':'col-sm-12'}))
    # Based on http://www.learningaboutelectronics.com/Articles/How-to-create-a-text-area-in-a-Django-form.php
    create = forms.CharField(label='body', widget=forms.Textarea(attrs={'class':'col-sm-12'}))


    