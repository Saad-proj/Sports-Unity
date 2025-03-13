
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def players(request):
    return render(request, 'players.html')

def contact(request):
    return render(request, 'contact.html')

def schedule(request):
    return render(request, 'schedule.html')


def uni(request):
    return render(request, 'uni.html')





