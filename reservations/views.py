from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import RezerwacjaSali,Wydzial
from .forms import UserForm


def index(request):
    return render(request, 'generic_site.html')


def reservations(request):
    # TODO: kalendarz insert
    all_reservations = RezerwacjaSali.objects.all()
    context = {
        "lista_rezerwacji": all_reservations
    }

    return render(request, 'reservations/reservation_list.html', context)


# TODO: Wydziały do wyboru dla niezalogowanych użytkowników
def rooms(request):

    wydzialy = Wydzial.objects.all()
    wydzial_1  = wydzialy[0].id_wydzialu

    context = {
        "wydzialy" : wydzialy
    }

    return render(request, 'reservations/available_classrooms.html',context)


# TODO: POGrupować pomieszczenia i wyświetlać możliwe do wyboru w wybranej strukturze [lista, dropdown etc.]
def plan_wydzialu(request, wydzial_id):

    context = {
        "wydzial": wydzial_id
    }

    return  render(request, 'reservations/sale_wydzialu.html', context)


# TODO: Szczegóły daty rezerwacji danej sali na danym wydziale, wyświetlać już zarezerwowane terminy,
#  wybór daty i godziny rezerwacji
def room_reservations(request, wydzial_id, room_id):
    return render(request, 'generic_site.html')


@login_required
def pending_reservations(request):

    pending = RezerwacjaSali.objects.filter(status="R")

    context = {
        "pending": pending
    }

    return render(request, 'reservations/pending_reservations_list.html', context)


@login_required
def declined_reservations(request):

    context = {

    }

    return render(request, 'reservations/declined_reservations_list.html', context)


@login_required
def accepted_reservations(request):

    context = {

    }

    return render(request, 'reservations/accepted_reservations_list.html', context)


@login_required
def user_pending_reservations(request):

    context = {

    }

    return render(request, 'reservations/user_pending_reservations_list.html', context)


@login_required
def user_declined_reservations(request):

    context = {

    }

    return render(request, 'reservations/user_declined_reservations_list.html', context)


@login_required
def user_accepted_reservations(request):

    context = {

    }

    return render(request, 'reservations/user_accepted_reservations_list.html', context)


@login_required
def detailed_reservation(request,reservation_id):
    selected_reservation = RezerwacjaSali.objects.get(id_rezerwacji_sali=reservation_id);

    context = {
        "reservation": selected_reservation.id_pomieszczenia,
    }

    return render(request, 'reservations/detailed_reservation.html', context)


@login_required
def resign_from_reservation(request,reservation_id):

    selected_reservation = RezerwacjaSali.objects.get(id_rezerwacji_sali= reservation_id);

    context = {
        "reservation": selected_reservation.id_pomieszczenia,
    }

    return render(request, 'reservations/detailed_reservation.html',context)


@login_required
def request_reservation(request,reservation_id):
    return render(request, 'generic_site.html')


@login_required
def detailed_profile(request):

    current_user = request.user

    context = {
        "name": current_user.uzytkownik.imie,
        "surname": current_user.uzytkownik.nazwisko,
        "e_mail": current_user.uzytkownik.e_mail,
        "kierunek": current_user.uzytkownik.student.id_kierunku,
        "wydział": current_user.uzytkownik.id_wydzialu,
        "telefon": current_user.uzytkownik.student.nr_telefonu,
        "nr_indeksu": current_user.uzytkownik.student.nr_indeksu
    }

    return render(request, 'reservations/profile.html', context)


@login_required
def edit_profile(request):
    # TODO: Zrobić formę do edycji profilu
    # profile_form = UserForm(request.POST)
    # if profile_form.is_valid():
    #     new_profile_form = profile_form.save(commit=False)
    #     profile_form.save()
    return render(request, 'reservations/edit_profile.html')