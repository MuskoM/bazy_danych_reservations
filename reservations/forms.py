from django import forms
from django.forms import ModelForm
from .models import Student, RezerwacjaSali
import datetime


class NewReservationForm(ModelForm):

    class Meta:
        model = RezerwacjaSali
        fields = ['data_od', 'data_do']


class ChangeStatusForm(ModelForm):
    class Meta:
        model = RezerwacjaSali
        fields = ['status']