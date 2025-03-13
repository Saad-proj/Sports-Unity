# # university/views.py
# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import AuthenticationForm
# from .forms import UniversityRegistrationForm
# from .models import University

# def register(request):
#     if request.method == 'POST':
#         form = UniversityRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = UniversityRegistrationForm()
#     return render(request, 'university/register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'university/login.html', {'form': form})

# def dashboard(request):
#     if request.user.is_authenticated:
#         university = University.objects.get(user=request.user)
#         return render(request, 'university/dashboard.html', {'university': university})
#     else:
#         return redirect('login')


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserSignupForm, UniversityRegistrationForm, PlayerRegistrationForm, BookingForm, SponsorForm, LoginForm, Player
from django.utils import timezone
from .models import Event, Team, Stall, StallBooking, Sponsor, Event, Notice, Match, Result
from calendar import HTMLCalendar
from django.contrib import messages
import calendar




# def home(request):
#     return render(request, 'index.html')

def home(request):
    # Fetch all matches
    matches = Match.objects.all().order_by('-date')  # Ordered by the most recent match
    
    # Fetch the latest 3 events
    latest_events = Event.objects.order_by('-start_time')[:3]
    sponsors = Sponsor.objects.all()
    sponsors_card = Sponsor.objects.all()[:4]
    results = Result.objects.all()
    
    # Pass both matches and latest events to the template
    return render(request, 'index.html', {'matches': matches, 'latest_events': latest_events, 'sponsors': sponsors, 'sponsors_card': sponsors_card, 'results': results})




# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
                
#                 # Redirect to the 'next' parameter if it exists, otherwise go to 'home'
#                 next_url = request.GET.get('next', 'home')
#                 return redirect(next_url)
#     else:
#         form = UserLoginForm()

#     return render(request, 'university/login.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)
                
                # If "Remember Me" is checked, extend session expiry
                if not remember_me:
                    request.session.set_expiry(0)  # Browser closes = logout
                else:
                    request.session.set_expiry(1209600)  # 2 weeks

                messages.success(request, 'You have successfully logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = LoginForm()

    return render(request, 'university/login.html', {'form': form})

# def user_signup(request):
#     if request.method == 'POST':
#         form = UserSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  
#             return redirect('home')
#     else:
#         form = UserSignupForm()
    
#     return render(request, 'university/signup.html', {'form': form})

# def user_signup(request):
#     if request.method == 'POST':
#         form = UserSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, 'You have registered successfully! Now you can login.')
#             return redirect('user_login')  # Redirect to the login page
#         else:
#             print(form.errors)  # For debugging, print form errors to console
#     else:
#         form = UserSignupForm()

#     return render(request, 'university/signup.html', {'form': form})


def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'You have registered successfully! Now you can log in.')
            return redirect('user_login')
        else:
            # Add error messages for invalid form inputs
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, error)
    else:
        form = UserSignupForm()

    return render(request, 'university/signup.html', {'form': form})




# def user_signup(request):
#     if request.method == 'POST':
#         form = UserSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#         else:
#             print(form.errors)  # For debugging, print form errors to console
#     else:
#         form = UserSignupForm()

#     return render(request, 'university/signup.html', {'form': form})



# User = get_user_model()

# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return render(request, 'university/account_activation_complete.html')
#     else:
#         return render(request, 'university/account_activation_invalid.html')
    
def university_registration(request):
    if request.method == 'POST':
        form = UniversityRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'university/registration_success.html')
    else:
        form = UniversityRegistrationForm()
    
    return render(request, 'university/university_registration.html', {'form': form})

@login_required
def player_registration(request):
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user  # Associate the player with the logged-in user
            player.save()
            return render(request, 'university/player_registration_success.html')
    else:
        form = PlayerRegistrationForm()
    
    return render(request, 'university/player_registration.html', {'form': form})




def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})



def logout_view(request):
    logout(request)
    return redirect('home')

def notice_list(request):
  
    notices = Notice.objects.all().order_by('-posted_at')
    return render(request, 'university/notice_list.html', {'notices': notices})

def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    return render(request, 'university/notice_detail.html', {'notice': notice})

class EventCalendar(HTMLCalendar):
    def __init__(self, events):
        super().__init__()
        self.events = events

    def formatday(self, day, weekday):
        events_from_day = self.events.filter(start_time__day=day)
        day_html = f'<span class="day">{day}</span>'
        
        if events_from_day:
            event_html = '<ul>'
            for event in events_from_day:
                event_html += f'<li>{event.title}</li>'
            event_html += '</ul>'
            return f'<td class="event-day">{day_html} {event_html}</td>'
        return f'<td>{day_html}</td>'

    def formatmonth(self, year, month):
        events = Event.objects.filter(start_time__year=year, start_time__month=month)
        self.events = events
        return super().formatmonth(year, month)

# def event_calendar(request):
#     year = timezone.now().year
#     month = timezone.now().month
#     cal = EventCalendar(events=Event.objects.all()).formatmonth(year, month)
#     return render(request, 'university/calendar.html', {'calendar': cal})


def event_calendar(request):
    # Get current year and month, or use provided values
    year = request.GET.get('year', timezone.now().year)
    month = request.GET.get('month', timezone.now().month)

    # Convert to integers
    year, month = int(year), int(month)

    # Set up the calendar with events
    events = Event.objects.all()
    cal = EventCalendar(events=events).formatmonth(year, month)

    # Calculate previous and next month
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render(request, 'university/calendar.html', {
        'calendar': cal,
        'month': calendar.month_name[month],
        'year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    })


def event_list(request):
    # Ordering events by start_time in descending order (latest event first)


    events = Event.objects.order_by('-start_time')  # Or '-created_at' if sorting by creation date
    return render(request, 'university/event_list.html', {'events': events})






@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            booking.save()
            messages.success(request, "You have successfully booked the event!")
            # No redirect; just re-render the same page to show the message
    else:
        form = BookingForm(initial={'event': event})
    
    return render(request, 'university/book_event.html', {'form': form, 'event': event})



@login_required
def booking_confirmation(request):
    return render(request, 'university/booking_confirmation.html')

def tournament_standings(request):
    teams = Team.objects.all().order_by('-points', '-wins', 'losses')
    return render(request, 'university/tournament_standings.html', {'teams': teams})

def stall_list(request):
    stalls = Stall.objects.filter(availability=True)
    return render(request, 'university/stall_list.html', {'stalls': stalls})

def book_stall(request, stall_id):
    stall = get_object_or_404(Stall, id=stall_id)

    if request.method == 'POST':
        StallBooking.objects.create(user=request.user, stall=stall)
        stall.availability = False
        stall.save()
        return redirect('stall_list')  # Redirect to the stall list or another page after booking

    return render(request, 'university/book_stall.html', {'stall': stall})

def sponsor_list(request):
    sponsors = Sponsor.objects.all()
    return render(request, 'university/sponsor_list.html', {'sponsors': sponsors})

def sponsor_marque(request):
    sponsors = Sponsor.objects.all()
    return render(request, 'university/index.html', {'sponsors': sponsors})


def sponsor_add(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sponsor_list')
    else:
        form = SponsorForm()
    return render(request, 'university/sponsor_form.html', {'form': form})

def sponsor_edit(request, sponsor_id):
    sponsor = Sponsor.objects.get(id=sponsor_id)
    if request.method == 'POST':
        form = SponsorForm(request.POST, request.FILES, instance=sponsor)
        if form.is_valid():
            form.save()
            return redirect('sponsor_list')
    else:
        form = SponsorForm(instance=sponsor)
    return render(request, 'university/sponsor_form.html', {'form': form})

def sponsor_delete(request, sponsor_id):
    sponsor = Sponsor.objects.get(id=sponsor_id)
    sponsor.delete()
    return redirect('sponsor_list')




def results_view(request):
    results = Result.objects.all()
    return render(request, 'university/results.html', {'results': results})







from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def event_list2(request):
    # Get unread notifications
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    notification_count = unread_notifications.count()

    return render(request, 'university/index.html', {
        'notification_count': notification_count,
        'unread_notifications': unread_notifications,
    })




@login_required
def notifications(request):
    # Fetch only unread notifications
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications.html', {'notifications': unread_notifications})




@login_required
def event_detail(request, event_id):
    # Get the event
    event = get_object_or_404(Event, id=event_id)

    # Mark the associated notification as read
    Notification.objects.filter(user=request.user, event=event, is_read=False).update(is_read=True)

    return render(request, 'university/event_detail.html', {'event': event})


@login_required
def mark_as_read(request, notification_id):
    # Get the notification object
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)

    # Mark the notification as read
    notification.is_read = True
    notification.save()

    # Get updated unread notification count
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    notification_count = unread_notifications.count()

    # Redirect to the appropriate page (result, event, etc.)
    if notification.result:
        return redirect('results')
    elif notification.event:
        return redirect('event_detail', event_id=notification.event.id)
    elif notification.match:
        return redirect('tournament_standings')
    elif notification.notice:
        return redirect('notice_list')

    # Fallback if no recognized notification type
    return redirect('notifications')








import plotly.express as px
import plotly.graph_objs as go
from django.http import JsonResponse
from django.shortcuts import render
from .models import Event, Player, University, Match

from django.db import models  # Import this


import plotly.express as px
from django.db.models import Count
from django.db import models
from .models import Event, Match, Player, University

from django.http import HttpResponse
import plotly.express as px
from django.db.models import Count
from .models import Event, Match, Player, University

from django.shortcuts import render
from django.http import HttpResponse
import plotly.express as px
from django.db.models import Count
from .models import Event, Match, Player, University

# Graph generating functions
def events_graph_data(request):
    total_events = Event.objects.count()
    fig = px.pie(
        names=["Total Events"],
        values=[total_events],
        title="Total Events Distribution",
        hole=0.5,
        color_discrete_sequence=["#EF553B"]
    )
    return HttpResponse(fig.to_html(full_html=False))

def matches_graph_data(request):
    total_matches = Match.objects.count()
    fig = px.bar(
        x=["Total Matches"],
        y=[total_matches],
        title="Total Matches",
        orientation="h",
        labels={"x": "Matches", "y": "Count"},
        color_discrete_sequence=["#636EFA"]
    )
    return HttpResponse(fig.to_html(full_html=False))

def players_graph_data(request):
    players = Player.objects.values('university__name').annotate(count=Count('id'))
    universities = [player['university__name'] for player in players]
    counts = [player['count'] for player in players]
    fig = px.bar(x=universities, y=counts, title="Players per University", labels={'x': "University", 'y': "Players"})
    return HttpResponse(fig.to_html(full_html=False))

def universities_graph_data(request):
    universities = University.objects.annotate(player_count=Count('player')).values('name', 'player_count')
    names = [university['name'] for university in universities]
    player_counts = [university['player_count'] for university in universities]
    fig = px.bar(x=names, y=player_counts, title="Players per University", labels={'x': "University", 'y': "Players"})
    return HttpResponse(fig.to_html(full_html=False))

# View to render graphs
def grph(request):
    context = {
        'event_graph': events_graph_data(request),
        'matches_graph': matches_graph_data(request),
        'players_graph': players_graph_data(request),
        'universities_graph': universities_graph_data(request),
    }
    return render(request, 'graph.html', context)





# def grph(request):
    
#     context = {
#         'event_graph': events_graph_data(),
#         'player_graph': players_graph_data(),
#         'university_graph': universities_graph_data(),
#         'match_graph': matches_graph_data(),
#     }
#     return render(request, 'graph.html', context)



# index page to show the graph 

#  <div class="dashboard">
#         <h1>Dashboard</h1>
#         <div class="graphs-grid">
#             <div class="graph-card">
#                 <h3>Total Matches</h3>
#                 {{ matches_graph|safe }}
#             </div>
#             <div class="graph-card">
#                 <h3>Total Events</h3>
#                 {{ events_graph|safe }}
#             </div>
#             <div class="graph-card">
#                 <h3>Event Categories</h3>
#                 {{ event_categories_graph|safe }}
#             </div>
#             <div class="graph-card">
#                 <h3>Players per University</h3>
#                 {{ players_graph|safe }}
#             </div>
#             <div class="graph-card">
#                 <h3>Players per University</h3>
#                 {{ universities_graph|safe }}
#             </div>
#         </div>
#     </div>


# urls for route 

#   path('grph/', views.grph, name='grph'),
    
#     path('matches-graph/', views.matches_graph_data, name='matches_graph'),
#     path('players-graph/', views.players_graph_data, name='players_graph'),
#     path('universities-graph/', views.universities_graph_data, name='universities_graph'),
#     # path('players-graph/', views.players_graph, name='players_graph'),
#     # path('universities-graph/', views.universities_graph, name='universities_graph'),
#     # path('matches-graph/', views.matches_graph, name='matches_graph'),