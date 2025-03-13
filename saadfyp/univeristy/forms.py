# # university/forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import University

# class UniversityRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     name = forms.CharField(max_length=200)
#     description = forms.CharField(widget=forms.Textarea)
#     location = forms.CharField(max_length=200)
#     established_year = forms.IntegerField()
#     image_url = forms.URLField(required=False)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#             university = University(
#                 user=user,
#                 name=self.cleaned_data['name'],
#                 description=self.cleaned_data['description'],
#                 location=self.cleaned_data['location'],
#                 established_year=self.cleaned_data['established_year'],
#                 image_url=self.cleaned_data['image_url']
#             )
#             university.save()
#         return user


from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import University, Player, Booking, Sponsor
import re
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'id': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'id': 'password'
    }))

# class UserSignupForm(UserCreationForm):
#     email = forms.EmailField(required=True) 

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
#         }



class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # Ensure the password has both letters and numbers
        if not re.search(r'^(?=.*[A-Za-z])(?=.*\d)', password):
            raise forms.ValidationError('Password must contain both letters and numbers.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Check if both passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        

# class UserSignupForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")
        
# class UniversityRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = University
#         fields = ['name', 'location', 'contact_email', 'contact_phone', 'description']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'location': forms.TextInput(attrs={'class': 'form-control'}),
#             'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control'}),
#         }



class UniversityRegistrationForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'location', 'contact_email', 'contact_phone', 'description', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    



class PlayerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['university', 'event', 'player_class', 'contact_phone', 'age']
        widgets = {
            'university': forms.Select(attrs={'class': 'form-control'}),
            'event': forms.TextInput(attrs={'class': 'form-control'}),
            'player_class': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event']

        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
        }

class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ['name', 'logo', 'contact_info', 'sponsorship_amount', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
            'sponsorship_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }




class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())





from django import forms
from .models import EventPlayerRegister


class EventPlayerRegisterForm(forms.ModelForm):
    class Meta:
        model = EventPlayerRegister
        fields = ['full_name', 'date_of_birth', 'age', 'phone_number', 'email', 'event', 'university', 'password']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
            'university': forms.Select(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
