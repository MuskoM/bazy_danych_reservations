from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import RezerwacjaSali, Wydzial, Pomieszczenie, Sala, PracowaniaSpecjalistyczna, Laboratorium
from .models import Pokoj, RezerwacjaPokoju, Akademik
from .forms import UserForm, NewReservationForm
from django.views import View
from django.contrib import messages


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

def plan_wydzialu(request, wydzial_id):
    id_wydzialu = wydzial_id
    wydzial = Wydzial.objects.get(id_wydzialu=wydzial_id)
    classrooms = Pomieszczenie.objects.filter(id_wydzialu=wydzial_id)
    labs_list = classrooms.filter(rodzaj_pom="L")
    class_list = classrooms.filter(rodzaj_pom="S")
    workroom_list = classrooms.filter(rodzaj_pom="P")
    lecture_hall_list = classrooms.filter(rodzaj_pom="A")

    context = {
        "id_wydzialu": id_wydzialu,
        "nazwa_wydzialu": wydzial,
        "classrooms_list": classrooms,
        "labs_list": labs_list,
        "class_list": class_list,
        "workroom_list": workroom_list,
        "lecture_hall_list": lecture_hall_list
    }

    return  render(request, 'reservations/sale_wydzialu.html', context)

class Room_reservations(View):
    def get(self, request, wydzial_id, room_id):
        selected_classroom = Pomieszczenie.objects.get(id_wydzialu=wydzial_id, id_pomieszczenia=room_id)
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

        elif type_of_room == "S" or type_of_room == "A":
            selected_classroom = Sala.objects.get(id_wydzialu=wydzial_id, id_pomieszczenia=room_id)
            no_seats = selected_classroom.ilosc_miejsc
            czy_rzutnik = selected_classroom.czy_rzutnik
            aux_descrp = selected_classroom.jaka_tablica

        elif type_of_room == "P":
            selected_classroom = PracowaniaSpecjalistyczna.objects.get(id_wydzialu=wydzial_id, id_pomieszczenia=room_id)
            no_seats = selected_classroom.ilosc_miejsc
            czy_rzutnik = selected_classroom.czy_rzutnik
            aux_descrp = selected_classroom.osprzet

        context = {
            "wydzial_id": wydzial_id,
            "type_of_room": type_of_room,
            "selected_classroom": selected_classroom,
            "nr_pom": nr_pom,
            "no_seats": no_seats,
            "czy_rzutnik": czy_rzutnik,
            "aux_descrp": aux_descrp,
            "lista_rezerwacji": room_reservations_list
        }

        return render(request, 'reservations/selected_classroom.html', context)

    def post(self, request, wydzial_id, room_id):
        new_reservation = NewReservationForm(request.POST)
        #print(request)
        if new_reservation.is_valid():
            new_reservation_form = new_reservation.save(commit=False)
            new_reservation_form.id_pomieszczenia = Pomieszczenie.objects.get(pk=room_id)
            new_reservation_form.id_uzytkownika = request.user.uzytkownik
            new_reservation_form.data_od = new_reservation.cleaned_data['data_od']
            new_reservation_form.data_do = new_reservation.cleaned_data['data_do']
            new_reservation.save()
            messages.success(request, 'Pomyślnie dodkonano rezerwacji!!')

        return redirect('sala', wydzial_id, room_id)


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

    user_id = request.user.uzytkownik
    pending = RezerwacjaSali.objects.filter(id_uzytkownika=user_id, status="R")

    context = {
        "pending_user_reservations": pending,
    }

    return render(request, 'reservations/user_reservations/user_pending_reservations.html', context)


@login_required
def user_declined_reservations(request):
    user_id = request.user.uzytkownik
    declined = RezerwacjaSali.objects.filter(id_uzytkownika=user_id, status="O")

    context = {
        "declined_user_reservations": declined
    }

    return render(request, 'reservations/user_reservations/user_declined_reservations.html', context)


@login_required
def user_accepted_reservations(request):
    user_id = request.user.uzytkownik
    accepted_reservations = RezerwacjaSali.objects.filter(id_uzytkownika=user_id, status="Z")

    context = {
        "accepted_user_reservations": accepted_reservations
    }

    return render(request, 'reservations/user_reservations/user_accepted_reservations.html', context)


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

    if request.user.is_staff:
        return render(request, 'reservations/admin_profile.html',context)
    else:
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