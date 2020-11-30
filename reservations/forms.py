from django import forms
from django.forms import ModelForm
from .models import Student, RezerwacjaSali


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

    id_pomieszczenia = forms.IntegerField()


    class Meta:
        model = RezerwacjaSali
        fields = '__all__'
        exclude = ['id_rezerwacji', 'id_pomieszczenia', 'status', 'id_uzytkownika', 'data_wykonania_rezerwacji']
        widgets = {
          "data_od": forms.NumberInput(
              attrs={
                  'class': 'form-control form-control-sm',
                  'area-label': 'start_date,',
                  'aria-describedby': 'add-btn',
              }
          ),
            "data_do": forms.NumberInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'area-label': 'end_date',
                    'aria-describedby': 'add-btn',
                }
            )
        }
