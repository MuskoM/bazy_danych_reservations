from django import forms
from django.forms import ModelForm
from .models import Student, RezerwacjaSali, RezerwacjaPokoju
import datetime


class NewReservationForm(ModelForm):
    class Meta:
        model = RezerwacjaSali
        fields = ['data_od', 'data_do']


class ChangeStatusForm(ModelForm):
    class Meta:
        model = RezerwacjaSali
        fields = ['status']


class NewRoomReservationForm(ModelForm):
    class Meta:
        model = RezerwacjaPokoju
        fields = ['data_od', 'data_do']


class ChangeRoomStatusForm(ModelForm):
    class Meta:
        model = RezerwacjaPokoju
        fields = ['status']
