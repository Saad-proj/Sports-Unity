# # university/urls.py
# from django.urls import path
# from .views import register, login_view, dashboard

# urlpatterns = [
#     path('register/', register, name='register'),
#     path('login/', login_view, name='login'),
#     path('dashboard/', dashboard, name='dashboard'),
# ]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='home'),
     path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_signup, name='user_signup'),
    path('logout/', views.logout_view, name='logout'),
    path('players/', views.player_list, name='player_list'),
     path('events/register/', views.event_register, name='event_register'), 
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('register/', views.university_registration, name='university_registration'),
    path('player/register/', views.player_registration, name='player_registration'),
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('calendar/', views.event_calendar, name='event_calendar'),
    path('tournament-standings/', views.tournament_standings, name='tournament_standings'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),  
    # path('events/<int:event_id>/like/', views.like_event, name='like_event'),
    # path('events/<int:event_id>/comment/', views.add_comment, name='add_comment'),
    # path('events/book/<int:event_id>/', views.book_event, name='book_event'),
    path('book-event/<int:event_id>/', views.book_event, name='book_event'),
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('stalls/', views.stall_list, name='stall_list'),
    path('stalls/book/<int:stall_id>/', views.book_stall, name='book_stall'),
    path('sponsors/', views.sponsor_list, name='sponsor_list'),
    path('sponsors/add/', views.sponsor_add, name='sponsor_add'),
    path('sponsors/edit/<int:sponsor_id>/', views.sponsor_edit, name='sponsor_edit'),
    path('sponsors/delete/<int:sponsor_id>/', views.sponsor_delete, name='sponsor_delete'),
    path('results/', views.results_view, name='results'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += [
#     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
# ]