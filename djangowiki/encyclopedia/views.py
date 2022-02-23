from django.shortcuts import render
from django.http import HttpResponse

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
        return HttpResponse("This is a placeholder error")
    #Return page
    else:
        page = util.get_entry(title)
        # provide context

        #Convert content from markdown to html

        #Pass html into render function.
        return render(request, 'encyclopedia/page.html', {"title": title, "pagebody": page})