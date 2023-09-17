from django.urls import path
from . import views


urlpatterns = [
    path('room-list/', views.RoomListAPIView.as_view(), name='room_list'),
    path('room-create/', views.RoomCreateAPIView.as_view(), name='room_create'),
    path('reservation-list/', views.ReservationListAPIView.as_view(), name='reservation_list'),
    path(
        'reservation-list/<int:pk>/',
        views.ReservationRetrieveAPIView.as_view(),
        name='reservation_detail'
    ),
    path(
        'reservation-list/<int:pk>/cancel/',
        views.ReservationCancelAPIView.as_view(),
        name='reservation_cancel'
    ),
    path(
        'reservation-create/',
        views.ReservationCreateAPIView.as_view(),
        name='reservation_create'
    ),
]
