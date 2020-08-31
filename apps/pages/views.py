from django.shortcuts import render
from .models import Page


def pages(request, slug):
    return render(request, 'shop/pages/page.html', {'page' : Page.objects.get(slug=slug)})