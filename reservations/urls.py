from . import views
from django.urls import path, include
from .views import Room_reservations, Pending_reservations, Dormitory_Room_reservations, Pending_room_reservations
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path('', views.index, name='index_reservations'),

]

urlpatterns += [

    path('accounts/', include('django.contrib.auth.urls')),

    # Strona główna oraz zarazerwowane już sale
    # TODO: na zasadzie degra zajętość sal
    path('', views.index, name="reservations_index"),
    path('reservations/', views.reservations, name="current_reservations"),

    # Możliwe sale do wyboru
    path('plan/', views.rooms, name="plan"),
    path('plan/wydzial=<int:wydzial_id>/', views.plan_wydzialu, name="wydzial"),
    path('plan/wydzial=<int:wydzial_id>/room=<int:room_id>/', Room_reservations.as_view(), name="sala"),

    # DONE////
    # login required and admin sites
    # TODO: rozminic usprawnienia, zeby tylko admin mial dostep do tych stron
    path('admin/pending_reservations/', login_required(Pending_reservations.as_view()), name="pending_reservations"),
    path('admin/pending_reservations/reservation=<int:reservation_id>/', login_required(Pending_reservations.as_view()),
         name="reservation_temp"),
    path('admin/declined_reservations/', views.declined_reservations, name="declined_reservations"),
    path('admin/accepted_reservations/', views.accepted_reservations, name="accepted_reservations"),

    path('admin/pending_room_reservations/', login_required(Pending_room_reservations.as_view()), name="pending_room_reservations"),
    path('admin/pending_room_reservations/reservation=<int:reservation_id>/', login_required(Pending_room_reservations.as_view()),
         name="temp_reservation_room"),

    path('admin/declined_room_reservations/', views.declined_room_reservations, name="declined_room_reservations"),
    path('admin/accepted_room_reservations/', views.accepted_room_reservations, name="accepted_room_reservations"),
    # user sitee
    path('user/pending_reservations/', views.user_pending_reservations, name="user_pending_reservations"),
    path('user/declined_reservations/', views.user_declined_reservations, name="user_declined_reservations"),
    path('user/accepted_reservations/', views.user_accepted_reservations, name="user_accepted_reservations"),

    path('user/pending_room_reservations/', views.user_pending_room_reservations,
         name="user_pending_room_reservations"),
    path('user/declined_room_reservations/', views.user_declined_room_reservations,
         name="user_declined_room_reservations"),
    path('user/accepted_room_reservations/', views.user_accepted_room_reservations,
         name="user_accepted_room_reservations"),

    # Szczegóły już zarezerwowanych sal
    path('user/all_reservations/res=<int:reservation_id>/detail', views.detailed_reservation,
         name="reservation_details"),
    # Zrezygnowanie bądź przełożenie rezerwacji
    path('user/all_reservations/res=<int:reservation_id>/resign', views.resign_from_reservation,
         name="resign_from_reservation"),

    # ////DONE
    # path('user/all_reservations/res=<int:reservation_id>/request', views.request_reservation),

    path('user/', views.detailed_profile, name='profil'),

    path('akademiki/', views.akademiki, name="akademiki"),
    path('akademiki/akademik=<int:id_akademika>', views.akademik, name="akademik"),
    path('akademiki/akademik=<int:id_akademika>/pokoj=<int:id_pokoju>', Dormitory_Room_reservations.as_view(),
         name="pokoj"),

]
