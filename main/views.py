from django.shortcuts import render
from django.http import HttpResponse

from services.models import Categories, Masters, Products

# Create your views here.
def index(request):

    categories = Categories.objects.all()
    procedures = Products.objects.filter(show_on_homepage=True)

    context = {
        'title': 'Koloristika - Главная страница',
        'categories': categories,
        'procedures': procedures,
    }

    return render(request, 'main/index.html', context)

def about(request):

    masters = Masters.objects.all()

    context = {
        'title': 'Koloristika - О нас',
        'masters': masters,
    }

    return render(request, 'main/about.html', context)