from django.http import HttpResponseForbidden
from django.shortcuts import render


def index(request):
    """
    Render the index page
    """
    if request.user.is_authenticated:
        title = "Home"
        context = {"title": title}
        return render(request, "morning_page.html", context)
    else:
        title = "Home"
        context = {"title": title}
        return render(request, "index.html", context)


def search(request):
    """
    Render the search page
    """
    title = "Search"
    context = {"title": title, "search": "active"}
    return render(request, "search.html", context)


def account_page(request):
    """
    Render the user's account page
    """
    title = "Search"
    context = {"title": title, "account_page": "active"}
    return render(request, "account.html", context)


def morning_page(request):
    """
    Render the user's morning page
    """
    title = "Morning"
    context = {"title": title, "morning_page": "active"}
    return render(request, "morning_page.html", context)


def evening_page(request):
    """
    Render the user's evening page
    """
    title = "Evening"
    context = {"title": title, "evening_page": "active"}
    return render(request, "evening_page.html", context)


def design_system(request):
    """
    Render design system page
    Only visible for superusers
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    title = "Design System"
    context = {"title": title}
    return render(request, "design_system.html", context)
