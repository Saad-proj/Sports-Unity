

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserSignupForm, UniversityRegistrationForm, PlayerRegistrationForm, BookingForm, SponsorForm, LoginForm, Player
from django.utils import timezone
from .models import Event, Team, Stall, StallBooking, Sponsor, Event, Notice, Match, Result, University
from calendar import HTMLCalendar
from django.contrib import messages
import calendar





# def home(request):
#     # Fetch all matches
#     matches = Match.objects.all().order_by('-date')  # Ordered by the most recent match
    
#     # Fetch the latest 3 events
#     latest_events = Event.objects.order_by('-start_time')[:3]
#     sponsors = Sponsor.objects.all()
#     sponsors_card = Sponsor.objects.all()[:4]
#     results = Result.objects.all()
    
#     # Pass both matches and latest events to the template
#     return render(request, 'index.html', {'matches': matches, 'latest_events': latest_events, 'sponsors': sponsors, 'sponsors_card': sponsors_card, 'results': results})


from django.shortcuts import render
from .models import Booking, StallBooking, University

def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('user_login')  # Redirect to login if unauthenticated

    # Fetch user-specific data
    booked_events = Booking.objects.filter(user=request.user).select_related('event')
    stall_bookings = StallBooking.objects.filter(user=request.user).select_related('stall')
    universities = University.objects.all()
    registrations = EventPlayerRegister.objects.filter(email=request.user.email)
    # Calculate counts for event statuses
    total_events = booked_events.count()
    cancelled_events = booked_events.filter(status='Cancelled').count()
    pending_events = booked_events.filter(status='Pending').count()
    confirmed_events = booked_events.filter(status='Confirmed').count()

    context = {
        'username': request.user.username,
        'booked_events': booked_events,
        'stall_bookings': stall_bookings,
        'universities': universities,
        'total_events': total_events,
        'cancelled_events': cancelled_events,
        'pending_events': pending_events,
        'confirmed_events': confirmed_events,
        'registrations': registrations,
    }
    return render(request, 'user_dashboard.html', context)






from datetime import date

from django.utils.timezone import localtime, now




def home(request):
    # Fetch all matches
    matches = Match.objects.all().order_by('-date')
    next_match = Match.objects.filter(date__gte=timezone.now()).order_by('date').first()
     # Get the current month and year
    current_month = now().month
    current_year = now().year

    # Fetch events for the current month
    events = Event.objects.filter(
        start_time__month=current_month,
        start_time__year=current_year
    ).order_by('start_time')

     # Fetch all universities
    universities = University.objects.all()

    # Prepare data for the chart
    university_names = [uni.name for uni in universities]  # Replace 'name' with the actual field for university names
    university_counts = [1 for _ in universities]  # Assuming one instance per university


    # Extract event dates
    events_dates = [event.start_time.strftime('%Y-%m-%d') for event in events]
    # Process the next match display value
    if next_match:
        next_match_display = localtime(next_match.date).strftime('%Y-%m-%d %H:%M:%S')
    else:
        next_match_display = "No upcoming match"

    # Fetch data for graphs
    total_universities = University.objects.count()
    total_players = Player.objects.count()
    total_events = Event.objects.count()
    events_this_month = Event.objects.filter(
        start_time__month=timezone.now().month,
        start_time__year=timezone.now().year
    ).count()
    total_matches = matches.count()

    # Latest events and sponsors
    latest_events = Event.objects.order_by('-start_time')[:3]
    sponsors = Sponsor.objects.all()
    sponsors_card = Sponsor.objects.all()[:4]
    results = Result.objects.all()

    # Pass data to template
    return render(request, 'index.html', {
        'matches': matches,
        'next_match_display': next_match_display,  # Pass formatted display value
        'events_dates': events_dates,  # Pass event dates to the template
        'latest_events': latest_events,
        'sponsors': sponsors,
        'sponsors_card': sponsors_card,
        'results': results,
        'total_universities': total_universities,
        'total_players': total_players,
        'total_events': total_events,
        'events_this_month': events_this_month,
        'total_matches': total_matches,
        'university_names': university_names,  # Pass names to the template
        'university_counts': university_counts,  # Pass counts to the template
    })




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


# def event_list(request):
#     # Ordering events by start_time in descending order (latest event first)
#     year = request.GET.get('year', timezone.now().year)
#     month = request.GET.get('month', timezone.now().month)

#     # Convert to integers
#     year, month = int(year), int(month)

#     # Set up the calendar with events
#     events = Event.objects.all()
#     cal = EventCalendar(events=events).formatmonth(year, month)

#     # Calculate previous and next month
#     prev_month = month - 1 if month > 1 else 12
#     prev_year = year if month > 1 else year - 1
#     next_month = month + 1 if month < 12 else 1
#     next_year = year if month < 12 else year + 1
#     universities = University.objects.all()  # Fetch all universities

#     events = Event.objects.order_by('-start_time')  # Or '-created_at' if sorting by creation date
#     return render(request, 'university/event_list.html', {'events': events ,   'calendar': cal,
#         'month': calendar.month_name[month],
#         'year': year,
#         'prev_month': prev_month,
#         'prev_year': prev_year,
#         'next_month': next_month,
#         'next_year': next_year,
#         'universities': universities,})


from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Event, University
from .forms import EventPlayerRegisterForm
import calendar

def event_list(request):
    # Handling calendar logic
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

    # Fetch universities
    universities = University.objects.all()

    # Handle event registration form submission
    show_modal = False  # Track if the modal should remain open
    if request.method == 'POST':
        form = EventPlayerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect after successful submission
            return redirect('event_list')
        else:
            # Keep modal open on validation errors
            show_modal = True
    else:
        form = EventPlayerRegisterForm()  # Empty form for GET requests

    # Pass all required data to the template
    return render(request, 'university/event_list.html', {
        'events': events.order_by('-start_time'),
        'calendar': cal,
        'month': calendar.month_name[month],
        'year': year,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'universities': universities,
        'form': form,
        'show_modal': show_modal
    })




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





from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import EventPlayerRegister, University, Event

def event_register(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Please log in to register for an event.'}, status=401)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        date_of_birth = request.POST.get('date_of_birth')
        age = request.POST.get('age')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        event_id = request.POST.get('event')
        university_id = request.POST.get('university')
        password = request.POST.get('password')

        event = get_object_or_404(Event, id=event_id)
        university = get_object_or_404(University, id=university_id)

        # Verify university password
        if university.password != password:
            return JsonResponse({'success': False, 'error': 'Incorrect university password.'})

        # Save registration
        EventPlayerRegister.objects.create(
            full_name=full_name,
            date_of_birth=date_of_birth,
            age=age,
            phone_number=phone_number,
            email=email,
            event=event,
            university=university,
            password=password,  # Storing plain password for validation only
            status='Pending'
        )
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)
