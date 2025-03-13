"""
URL configuration for saadfyp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
from saadfyp import views
from univeristy import views as university_views
from univeristy import views as uni_views


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", views.home, name='home'),
    path('about/', views.about, name='about'), 
    # path('players/', views.players, name='players'), 
    path('contact/', views.contact, name='contact'), 
    path('uni/', views.uni, name='uni'), 
    # path('schedule/', views.schedule, name='schedule'), 
    path('uni/', views.uni, name='uni'), 
    path('', include('univeristy.urls')),
    path('schedule/', university_views.event_calendar, name='event_calendar'), 
    path('players/', uni_views.player_list, name='player_list'),
    path('notices/', uni_views.notice_list, name='notice_list'),
    path('notices/<int:notice_id>/', uni_views.notice_detail, name='notice_detail'),
    path('tournament-standings/', uni_views.tournament_standings, name='tournament_standings'),
    path('stalls/', uni_views.stall_list, name='stall_list'),
    path('stalls/book/<int:stall_id>/', uni_views.book_stall, name='book_stall'),
    path('results/', uni_views.results_view, name='results'),
]
