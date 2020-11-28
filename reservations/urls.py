from . import views
from django.urls import path,include


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
    path('plan/', views.rooms),
    path('plan/wydzial=<int:wydzial_id>/', views.plan_wydzialu),
    path('plan/wydzial=<int:wydzial_id>/room=<int:room_id>/', views.room_reservations),

    # login required and admin sites
    path('admin/pending_reservations/',views.pending_reservations),
    path('admin/declined_reservations/',views.declined_reservations),
    path('admin/accepted_reservations/',views.accepted_reservations),

    # user sitee
    path('user/pending_reservations/', views.user_pending_reservations),
    path('user/declined_reservations/', views.user_declined_reservations),
    path('user/accepted_reservations/', views.user_accepted_reservations),

    # Szczegóły już zarezerwowanych sal
    path('user/all_reservations/res=<int:reservation_id>/detail', views.detailed_reservation),

    # Zrezygnowanie bądź przełożenie rezerwacji
    path('user/all_reservations/res=<int:reservation_id>/resign', views.resign_from_reservation),

    # path('user/all_reservations/res=<int:reservation_id>/request', views.request_reservation),

    path('user/', views.detailed_profile),
    path('user/edit/', views.edit_profile),

]