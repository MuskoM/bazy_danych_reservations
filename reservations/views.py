from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import RezerwacjaSali, Wydzial, Pomieszczenie, Sala, PracowaniaSpecjalistyczna, Laboratorium
from .models import Pokoj, RezerwacjaPokoju, Akademik
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

    context = {
        "wydzialy" : wydzialy
    }

    return render(request, 'reservations/available_classrooms.html',context)


# TODO: POGrupować pomieszczenia i wyświetlać możliwe do wyboru w wybranej strukturze [lista, dropdown etc.]
def plan_wydzialu(request, wydzial_id):

    wydzial = Wydzial.objects.get(id_wydzialu=wydzial_id)
    classrooms = Pomieszczenie.objects.filter(id_wydzialu=wydzial_id)
    labs_list = classrooms.filter(rodzaj_pom="L")
    class_list = classrooms.filter(rodzaj_pom="S")
    workroom_list = classrooms.filter(rodzaj_pom="P")

    context = {
        "nazwa_wydzialu": wydzial,
        "classrooms_list": classrooms,
        "labs_list": labs_list,
        "class_list": class_list,
        "workroom_list": workroom_list
    }

    return  render(request, 'reservations/sale_wydzialu.html', context)


# TODO: Szczegóły daty rezerwacji danej sali na danym wydziale, wyświetlać już zarezerwowane terminy,
#  wybór daty i godziny rezerwacji
# TODO: przerobić na Klasę i dać opcję POST

def room_reservations(request, wydzial_id, room_id):

    selected_classroom = Pomieszczenie.objects.get(id_wydzialu=wydzial_id,id_pomieszczenia=room_id)
    type_of_room = selected_classroom.rodzaj_pom
    no_seats = 0
    nr_pom = selected_classroom.id_pomieszczenia
    czy_rzutnik = False

    room_reservations_list = RezerwacjaSali.objects.filter(id_pomieszczenia=room_id)

    aux_descrp = ""

    if type_of_room == "L":
        selected_classroom = Laboratorium.objects.get(id_wydzialu=wydzial_id, id_pomieszczenia=room_id)
        no_seats = selected_classroom.ilosc_miejsc
        czy_rzutnik = selected_classroom.czy_rzutnik
        aux_descrp = selected_classroom.osprzet

    elif type_of_room == "S":
        selected_classroom = Sala.objects.get(id_wydzialu=wydzial_id, id_pomieszczenia=room_id)
        no_seats = selected_classroom.ilosc_miejsc
        czy_rzutnik = selected_classroom.czy_rzutnik
        aux_descrp = selected_classroom.jaka_tablica

    elif type_of_room == "P":
        selected_classroom = PracowaniaSpecjalistyczna.objects.get(id_wydzialu=wydzial_id, id_pomieszczenia=room_id)
        no_seats = selected_classroom.ilosc_miejsc
        czy_rzutnik = selected_classroom.czy_rzutnik
        aux_descrp = selected_classroom.osprzet

    context ={
        "selected_classroom": selected_classroom,
        "nr_pom": nr_pom,
        "no_seats": no_seats,
        "czy_rzutnik": czy_rzutnik,
        "aux_descrp": aux_descrp,
        "lista_rezerwacji": room_reservations_list
    }

    return render(request, 'reservations/selected_classroom.html', context)


@login_required
def pending_reservations(request):

    pending = RezerwacjaSali.objects.filter(status="R")

    context = {
        "pending_reservations": pending
    }

    return render(request, 'reservations/admin_reservations/pending_reservations_list.html', context)


@login_required
def declined_reservations(request):

    declined = RezerwacjaSali.objects.filter(status="O")

    context = {
        "declined_reservations": declined,
    }

    return render(request, 'reservations/admin_reservations/declined_reservations_list.html', context)


@login_required
def accepted_reservations(request):
    accepted = RezerwacjaSali.objects.filter(status="Z")

    context = {
        "accepted_reservations": accepted,
    }

    return render(request, 'reservations/admin_reservations/accepted_reservations_list.html', context)


@login_required
def user_pending_reservations(request):

    user_id = request.user.uzytkownik.id
    pending = RezerwacjaSali.objects.filter(id_uzytkownika=user_id, status="R")

    context = {
        "pending_user_reservations": pending,
    }

    return render(request, 'reservations/user_pending_reservations_list.html', context)


@login_required
def user_declined_reservations(request):
    user_id = request.user.uzytkownik.id
    declined = RezerwacjaSali.objects.filter(id_uzytkownika=user_id, status="O")

    context = {
        "declined_user_reservations": declined
    }

    return render(request, 'reservations/user_declined_reservations_list.html', context)


@login_required
def user_accepted_reservations(request):
    user_id = request.user.uzytkownik.id
    accepted_reservations = RezerwacjaSali.objects.filter(id_uzytkownika=user_id, status="Z")

    context = {
        "accepted_user_reservations": accepted_reservations
    }

    return render(request, 'reservations/user_accepted_reservations_list.html', context)


@login_required
def detailed_reservation(request,reservation_id):
    selected_reservation = RezerwacjaSali.objects.get(id_rezerwacji_sali=reservation_id);

    context = {
        "reservation": selected_reservation.id_pomieszczenia,
    }

    return render(request, 'reservations/detailed_reservation.html', context)

# TODO: Zrobić POST request do usunięcia rezerwacji D z CRUD
@login_required
def resign_from_reservation(request,reservation_id):

    selected_reservation = RezerwacjaSali.objects.get(id_rezerwacji_sali= reservation_id)


    context = {
        "reservation": selected_reservation.id_pomieszczenia,
    }

    return render(request, 'reservations/detailed_reservation.html',context)

# NIE POTRZEBNE, ZOSTAWIC NARAZIE
@login_required
def request_reservation(request,reservation_id):
    return render(request, 'generic_site.html')


# TODO: dodać informację o dacie wyrejestrowania z akademika oraz nr pokoju i nazwę akademika
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


def akademiki(request):

    lista_akademikow = Akademik.objects.all()

    context = {
        "lista_akademikow": lista_akademikow
    }

    return render(request,'reservations/akademiki/akademiki.html',context)


def akademik(request,id_akademika):

    nazwa_akademika = Akademik.objects.get(id_akademika=id_akademika)
    lista_pokoi = Pokoj.objects.filter(id_akademika=id_akademika)

    context = {
        "nazwa_akademika":nazwa_akademika,
        "lista_pokoi": lista_pokoi
    }

    return render(request, 'reservations/akademiki/akademik.html',context)


def pokoj(request,id_akademika,id_pokoju):

    selected_room = Pokoj.objects.get(id_akademika=id_akademika,id_pokoju=id_pokoju)
    nazwa_pokoju = selected_room.opis

    context = {
        "nazwa_pokoju": selected_room
    }

    return render(request, 'reservations/akademiki/pokoj.html',context)