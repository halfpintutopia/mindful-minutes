from django.shortcuts import render


def index(request):
	"""
	Render the index page
	"""
	title = "Home"
	context = {"title": title}
	return render(request, 'index.html', context)
