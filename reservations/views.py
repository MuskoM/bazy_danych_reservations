from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import RezerwacjaSali, Wydzial, Pomieszczenie, Sala, PracowaniaSpecjalistyczna, Laboratorium
from .models import Pokoj, RezerwacjaPokoju, Akademik
from .forms import NewReservationForm, ChangeStatusForm, NewRoomReservationForm, ChangeRoomStatusForm
from django.views import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta


def index(request):
    return render(request, 'reservations/index.html')


def reservations(request):
    # TODO: kalendarz insert

    accepted_reservations = RezerwacjaSali.objects.filter(status="Z")

    next_week_reservations = accepted_reservations.filter(data_od__gt=timezone.now() + timedelta(days=7),
                                                          data_od__lte=timezone.now() + timedelta(days=14)).order_by(
        "data_od")
    tomorrow_reservations = accepted_reservations.filter(data_od__gt=timezone.now(),
                                                         data_od__lte=timezone.now() + timedelta(days=1)).order_by(
        "data_od")

    context = {
        "lista_rezerwacji": accepted_reservations,
        "next_week_reservations": next_week_reservations,
        "tomorrow_reservations": tomorrow_reservations
    }

    return render(request, 'reservations/reservation_list.html', context)


# TODO: Wydziały do wyboru dla niezalogowanych użytkowników
def rooms(request):
    wydzialy = Wydzial.objects.all()

    context = {
        "wydzialy": wydzialy
    }

    return render(request, 'reservations/available_classrooms.html', context)


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

    return render(request, 'reservations/sale_wydzialu.html', context)


class Room_reservations(View):
    def get(self, request, wydzial_id, room_id):
        selected_classroom = Pomieszczenie.objects.get(id_wydzialu=wydzial_id, id_pomieszczenia=room_id)
        type_of_room = selected_classroom.rodzaj_pom
        no_seats = 0
        nr_pom = selected_classroom.id_pomieszczenia
        czy_rzutnik = False

        room_reservations_list = RezerwacjaSali.objects.filter(id_pomieszczenia=room_id, status="Z")
        room_reservations_list = room_reservations_list.order_by("data_od")

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
        print(new_reservation)
        if new_reservation.is_valid():
            new_reservation_form = new_reservation.save(commit=False)
            new_reservation_form.id_pomieszczenia = Pomieszczenie.objects.get(pk=room_id)
            new_reservation_form.id_uzytkownika = request.user.uzytkownik
            new_reservation_form.data_od = new_reservation.cleaned_data['data_od']
            new_reservation_form.data_do = new_reservation.cleaned_data['data_do']
            new_reservation.save()
            messages.success(request, 'Pomyślnie dokonano rezerwacji!!')

        return redirect('sala', wydzial_id, room_id)


class Dormitory_Room_reservations(View):
    def get(self, request, id_akademika, id_pokoju):
        selected_room = Pokoj.objects.get(id_akademika=id_akademika, id_pokoju=id_pokoju)
        nr_pom = selected_room.id_pokoju

        room_reservations_list = RezerwacjaPokoju.objects.filter(id_pokoju=id_pokoju, status='Z')
        room_reservations_list = room_reservations_list.order_by("data_od")

        context = {
            "akademik_id": id_akademika,
            "selected_room": selected_room,
            "nr_pom": nr_pom,
            "lista_rezerwacji": room_reservations_list
        }

        return render(request, 'reservations/akademiki/pokoj.html', context)

    def post(self, request, id_akademika, id_pokoju):
        new_reservation = NewRoomReservationForm(request.POST)
        print(new_reservation)
        if new_reservation.is_valid():
            new_reservation_form = new_reservation.save(commit=False)
            new_reservation_form.id_pomieszczenia = Pomieszczenie.objects.get(pk=id_pokoju)
            new_reservation_form.id_uzytkownika = request.user.uzytkownik
            new_reservation_form.data_od = new_reservation.cleaned_data['data_od']
            new_reservation_form.data_do = new_reservation.cleaned_data['data_do']
            new_reservation.save()
            messages.success(request, 'Pomyślnie dokonano rezerwacji!!')

        return redirect('sala', id_akademika, id_pokoju)


class Pending_reservations(View):
    def get(self, request):
        pending = RezerwacjaSali.objects.filter(status="R")
        pending = pending.order_by("data_od")
        context = {
            "reservations_list": pending
        }

        return render(request, 'reservations/admin_reservations/pending_reservations_list.html', context)

    def post(self, request, reservation_id):
        new_status = ChangeStatusForm(request.POST)
        reservation = RezerwacjaSali.objects.get(pk=reservation_id)
        if new_status.is_valid():
            reservation.status = new_status.cleaned_data['status']
            reservation.save()

        return redirect(request.META.get('HTTP_REFERER'))


class Pending_room_reservations(View):
    def get(self, request):
        pending = RezerwacjaPokoju.objects.filter(status="R")
        pending = pending.order_by("data_od")
        context = {
            "reservations_list": pending
        }

        return render(request, 'reservations/admin_reservations/pending_room_reservations_list.html', context)

    def post(self, request, reservation_id):
        new_status = ChangeStatusForm(request.POST)
        reservation = RezerwacjaPokoju.objects.get(pk=reservation_id)
        if new_status.is_valid():
            reservation.status = new_status.cleaned_data['status']
            reservation.save()

        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def declined_reservations(request):
    declined = RezerwacjaSali.objects.filter(status="O")
    context = {
        "reservations_list": declined,
    }

    return render(request, 'reservations/admin_reservations/declined_reservations_list.html', context)


@login_required
def accepted_reservations(request):
    accepted = RezerwacjaSali.objects.filter(status="Z")

    context = {
        "reservations_list": accepted,
    }

    return render(request, 'reservations/admin_reservations/accepted_reservations_list.html', context)


@login_required
def declined_room_reservations(request):
    declined = RezerwacjaPokoju.objects.filter(status="O")
    context = {
        "reservations_list": declined,
    }

    return render(request, 'reservations/admin_reservations/declined_reservations_list.html', context)


@login_required
def accepted_room_reservations(request):
    accepted = RezerwacjaPokoju.objects.filter(status="Z")

    context = {
        "reservations_list": accepted,
    }

    return render(request, 'reservations/admin_reservations/accepted_reservations_list.html', context)


@login_required
def user_pending_reservations(request):
    user_id = request.user.uzytkownik
    pending = RezerwacjaSali.objects.filter(id_uzytkownika=user_id, status="R")

    context = {
        "reservations_list": pending,
    }

    return render(request, 'reservations/user_reservations/user_pending_reservations.html', context)


@login_required
def user_declined_reservations(request):
    user_id = request.user.uzytkownik
    declined = RezerwacjaSali.objects.filter(id_uzytkownika=user_id, status="O")

    context = {
        "reservations_list": declined
    }

    return render(request, 'reservations/user_reservations/user_declined_reservations.html', context)


@login_required
def user_accepted_reservations(request):
    user_id = request.user.uzytkownik
    accepted_reservations = RezerwacjaSali.objects.filter(id_uzytkownika=user_id, status="Z")

    context = {
        "reservations_list": accepted_reservations
    }

    return render(request, 'reservations/user_reservations/user_accepted_reservations.html', context)


@login_required
def user_pending_room_reservations(request):
    user_id = request.user.uzytkownik
    pending = RezerwacjaPokoju.objects.filter(id_uzytkownika=user_id, status="R")

    context = {
        "reservations_list": pending,
    }

    return render(request, 'reservations/user_reservations/user_pending_room_reservations_list.html', context)


@login_required
def user_declined_room_reservations(request):
    user_id = request.user.uzytkownik
    declined = RezerwacjaPokoju.objects.filter(id_uzytkownika=user_id, status="O")

    context = {
        "reservations_list": declined
    }

    return render(request, 'reservations/user_reservations/user_declined_room_reservations_list.html', context)


@login_required
def user_accepted_room_reservations(request):
    user_id = request.user.uzytkownik
    accepted_reservations = RezerwacjaPokoju.objects.filter(id_uzytkownika=user_id, status="Z")

    context = {
        "reservations_list": accepted_reservations
    }

    return render(request, 'reservations/user_reservations/user_accepted_room_reservations_list.html', context)


@login_required
def detailed_reservation(request, reservation_id):
    selected_reservation = RezerwacjaSali.objects.get(id_rezerwacji_sali=reservation_id);
    type_of_room = selected_reservation.id_pomieszczenia.rodzaj_pom
    wydzial_id = selected_reservation.id_pomieszczenia.id_wydzialu
    print(type_of_room)
    czy_rzutnik = False
    no_seats = 0
    aux_descrp = ""
    rodzaj_pomieszczenia = ""
    room_id = selected_reservation.id_pomieszczenia.id_pomieszczenia

    if type_of_room == "L":
        selected_classroom = Laboratorium.objects.get(id_wydzialu=wydzial_id, id_pomieszczenia=room_id)
        no_seats = selected_classroom.ilosc_miejsc
        rodzaj_pomieszczenia = "Laboratorium"
        czy_rzutnik = selected_classroom.czy_rzutnik
        aux_descrp = selected_classroom.osprzet

    elif type_of_room == "S" or type_of_room == "A":
        selected_classroom = Sala.objects.get(id_wydzialu=wydzial_id, id_pomieszczenia=room_id)
        no_seats = selected_classroom.ilosc_miejsc
        rodzaj_pomieszczenia = "Sala"
        czy_rzutnik = selected_classroom.czy_rzutnik
        aux_descrp = selected_classroom.jaka_tablica

    elif type_of_room == "P":
        selected_classroom = PracowaniaSpecjalistyczna.objects.get(id_wydzialu=wydzial_id, id_pomieszczenia=room_id)
        no_seats = selected_classroom.ilosc_miejsc
        rodzaj_pomieszczenia = "Pracownia"
        czy_rzutnik = selected_classroom.czy_rzutnik
        aux_descrp = selected_classroom.osprzet

    context = {
        "reservation": selected_reservation,
        "no_seats": no_seats,
        "isProjector": czy_rzutnik,
        "aux_descr": aux_descrp,
        "rodzaj_pomieszczenia": rodzaj_pomieszczenia
    }

    return render(request, 'reservations/detailed_reservation.html', context)


@login_required
def resign_from_reservation(request, reservation_id):
    user_reservations = RezerwacjaSali.objects.filter(id_uzytkownika=request.user.uzytkownik)
    selected_reservation = user_reservations.get(id_rezerwacji_sali=reservation_id)

    selected_reservation.delete()

    return redirect('profil')


@login_required
def detailed_profile(request):
    current_user = request.user
    try:
        rezerwacja_akademik = RezerwacjaPokoju.objects.get(id_uzytkownika=current_user.uzytkownik)
    except ObjectDoesNotExist:
        rezerwacja_akademik = "Nie mieszka w akademiku"

    context = {
        "name": current_user.uzytkownik.imie,
        "surname": current_user.uzytkownik.nazwisko,
        "e_mail": current_user.uzytkownik.e_mail,
        "kierunek": current_user.uzytkownik.student.id_kierunku,
        "wydział": current_user.uzytkownik.id_wydzialu,
        "telefon": current_user.uzytkownik.student.nr_telefonu,
        "nr_indeksu": current_user.uzytkownik.student.nr_indeksu,
        "pokoj_w_akademiku": rezerwacja_akademik
    }

    if request.user.is_staff:
        return render(request, 'reservations/admin_profile.html', context)
    else:
        return render(request, 'reservations/profile.html', context)


def akademiki(request):
    lista_akademikow = Akademik.objects.all()

    context = {
        "lista_akademikow": lista_akademikow
    }

    return render(request, 'reservations/akademiki/akademiki.html', context)


def akademik(request, id_akademika):
    nazwa_akademika = Akademik.objects.get(id_akademika=id_akademika)
    lista_pokoi = Pokoj.objects.filter(id_akademika=id_akademika)

    context = {
        "nazwa_akademika": nazwa_akademika,
        "lista_pokoi": lista_pokoi
    }

    return render(request, 'reservations/akademiki/akademik.html', context)


def pokoj(request, id_akademika, id_pokoju):
    selected_room = Pokoj.objects.get(id_akademika=id_akademika, id_pokoju=id_pokoju)
    nazwa_pokoju = selected_room.opis

    context = {
        "nazwa_pokoju": nazwa_pokoju
    }

    return render(request, 'reservations/selected_room.html', context)
