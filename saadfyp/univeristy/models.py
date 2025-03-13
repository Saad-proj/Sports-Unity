from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError



# class University(models.Model):
#     name = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     registration_date = models.DateTimeField(auto_now_add=True)
#     contact_email = models.EmailField()
#     contact_phone = models.CharField(max_length=15)
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name
    

from django.db import models

class University(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128, default="default_password")  # Default value


    def __str__(self):
        return self.name




class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey('University', on_delete=models.CASCADE)
    event = models.CharField(max_length=255)
    player_class = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    age = models.IntegerField()
    registration_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='player_images/', blank=True, null=True)  # New image field

    def clean(self):
        if self.age < 18 or self.age > 35:
            raise ValidationError({'age': 'Age must be between 18 and 35.'})

    def __str__(self):
        return f"{self.user.username} - {self.event}"
    




from django.utils.timezone import now


class EventPlayerRegister(models.Model):
    FULL_NAME_MAX_LENGTH = 255
    PHONE_MAX_LENGTH = 15

    full_name = models.CharField(max_length=FULL_NAME_MAX_LENGTH)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=PHONE_MAX_LENGTH)
    email = models.EmailField()
    event = models.ForeignKey('Event', on_delete=models.CASCADE)  # Related to your Event model
    university = models.ForeignKey('University', on_delete=models.CASCADE)  # Related to University model
    password = models.CharField(max_length=128)  # For validation against University password
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )
    request_date = models.DateTimeField(auto_now_add=True)

    # def clean(self):
    #     # Auto-calculate age based on date_of_birth
    #     today = now().date()
    #     calculated_age = today.year - self.date_of_birth.year - (
    #         (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
    #     )
    #     if calculated_age != self.age:
    #         raise ValidationError({'age': 'Age does not match with the date of birth.'})

    def __str__(self):
        return f"{self.full_name} - {self.event.title} - {self.university.name}"








class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def __str__(self):
        return self.title



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Match(models.Model):
    team1 = models.ForeignKey(Team, related_name='team1_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_matches', on_delete=models.CASCADE)
    team1_score = models.PositiveIntegerField()
    team2_score = models.PositiveIntegerField()
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Update team standings based on match result
        if self.team1_score > self.team2_score:
            self.team1.wins += 1
            self.team2.losses += 1
            self.team1.points += 3
        elif self.team1_score < self.team2_score:
            self.team2.wins += 1
            self.team1.losses += 1
            self.team2.points += 3
        else:
            self.team1.draws += 1
            self.team2.draws += 1
            self.team1.points += 1
            self.team2.points += 1

        self.team1.save()
        self.team2.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} on {self.date}"
    
class Stall(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title

class StallBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stall = models.ForeignKey(Stall, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.stall.title}"
    
class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsors/logos/')
    contact_info = models.CharField(max_length=255)
    sponsorship_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class EventSponsor(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    sponsorship_type = models.CharField(max_length=100)  # e.g., Gold, Silver, Bronze
    sponsored_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.sponsor.name} - {self.event.title}"
    




class Result(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    result_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)  # Optional field for result details

    def __str__(self):
        return f"Result of {self.match} for {self.university.name} ({self.team.name})"
    







class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, null=True, blank=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        if self.event:
            return f"Notification for {self.user.username} - Event: {self.event.title}"
        elif self.match:
            return f"Notification for {self.user.username} - Match: {self.match}"
        elif self.notice:
            return f"Notification for {self.user.username} - Notice: {self.notice.title}"
        elif self.result:
            return f"Notification for {self.user.username} - Result: {self.result}"
        return f"Notification for {self.user.username}"



# Event Signal (Already Exists)
@receiver(post_save, sender=Event)
def create_event_notifications(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(is_superuser=False)  # Exclude superusers
        for user in users:
            Notification.objects.create(user=user, event=instance)

@receiver(post_save, sender=Match)
def create_match_notifications(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(is_superuser=False)
        for user in users:
            Notification.objects.create(user=user, match=instance)

@receiver(post_save, sender=Notice)
def create_notice_notifications(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(is_superuser=False)
        for user in users:
            Notification.objects.create(user=user, notice=instance)

@receiver(post_save, sender=Result)
def create_result_notifications(sender, instance, created, **kwargs):
    if created:
        users = User.objects.filter(is_superuser=False)
        for user in users:
            Notification.objects.create(user=user, result=instance)





@receiver(post_save, sender=Event)
def send_event_notification(sender, instance, created, **kwargs):
    if created:  # Check if a new event was created
        subject = f"New Event: {instance.title}"
        message = f"""
Hello,

A new event has been added:
Title: {instance.title}
Description: {instance.description}
Start Time: {instance.start_time}
End Time: {instance.end_time}
Venue: {instance.venue}

Don't miss it!

Best Regards,
Saad and Members
"""
        # Fetch all user email addresses
        recipient_list = User.objects.values_list('email', flat=True)
        # Send the email
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
