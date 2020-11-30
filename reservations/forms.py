from django import forms
from django.forms import ModelForm
from .models import Student, RezerwacjaSali
import datetime

class UserForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['nr_indeksu','id_uzytkowanika','id_kierunku']
        widgets = {
            "nr_telefonu": forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Numer telefonu",
                    'aria-label': 'nr_telefonu',
                }
            )
        }


class NewReservationForm(ModelForm):

    class Meta:
        model = RezerwacjaSali
        fields = ['data_od', 'data_do']
