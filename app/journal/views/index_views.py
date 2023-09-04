from django.shortcuts import render


def index(request):
    """
    Render the index page
    """
    title = "Home"
    context = {"title": title}
    return render(request, "index.html", context)


def design_system(request):
    """
    Render design system page
    """
    title = "Design System"
    context = {"title": title}
    return render(request, "design_system.html", context)
