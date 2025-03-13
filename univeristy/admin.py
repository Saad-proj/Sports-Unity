from django.contrib import admin
from .models import University, Notice, Event, Team, Match, Booking, Stall, StallBooking, Sponsor, EventSponsor, Player, Result, EventPlayerRegister

# from .models import University, Event, Player, Notice, Schedule

from django.utils.html import format_html
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .models import Event

admin.site.register(University)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Booking)
admin.site.register(Stall)
admin.site.register(StallBooking)
admin.site.register(Sponsor)
admin.site.register(EventSponsor)
admin.site.register(Player)




@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_at', 'expiration_date')
    search_fields = ('title', 'content')
    list_filter = ('posted_at', 'expiration_date')




@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('university', 'match', 'team', 'result_date')
    list_filter = ('university', 'match', 'team')
    search_fields = ('university__name', 'match__team1__name', 'match__team2__name', 'team__name')





class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'start_time': forms.SplitDateTimeWidget(date_attrs={
                'type': 'date',
                'min': now().date()
            }, time_attrs={
                'type': 'time',
            }),
            'end_time': forms.SplitDateTimeWidget(date_attrs={
                'type': 'date',
                'min': now().date()
            }, time_attrs={
                'type': 'time',
            }),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time and start_time < now():
            raise ValidationError('Start time cannot be in the past.')
        return start_time

    def clean_end_time(self):
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        if end_time and end_time < now():
            raise ValidationError('End time cannot be in the past.')
        if start_time and end_time and end_time < start_time:
            raise ValidationError('End time cannot be before the start time.')
        return end_time

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm
    list_display = ('title', 'start_time', 'end_time', 'venue', 'image')
    search_fields = ('title', 'description', 'venue')
    list_filter = ('start_time', 'end_time', 'venue')




@admin.register(EventPlayerRegister)
class EventPlayerRegisterAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'event', 'university', 'status', 'request_date')
    list_filter = ('status',)
    search_fields = ('full_name', 'event__title', 'university__name')
    actions = ['confirm_registration', 'cancel_registration']

    def confirm_registration(self, request, queryset):
        queryset.update(status='Confirmed')
        self.message_user(request, "Selected registrations have been confirmed.")

    def cancel_registration(self, request, queryset):
        queryset.update(status='Cancelled')
        self.message_user(request, "Selected registrations have been cancelled.")

    confirm_registration.short_description = "Confirm selected registrations"
    cancel_registration.short_description = "Cancel selected registrations"
