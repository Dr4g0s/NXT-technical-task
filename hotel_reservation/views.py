from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from datetime import datetime
import logging

from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer


logger = logging.getLogger(__name__)


class RoomListAPIView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        # Get the date parameter from the request URL
        date_param = self.request.query_params.get('date')

        # Query rooms that are not reserved for the specified date
        if date_param:
            try:
                date_param = datetime.fromisoformat(date_param).date()
                if date_param < datetime.today().date():
                    raise serializers.ValidationError({
                        'date': 'Invalid date range'
                    })
            except:
                raise serializers.ValidationError({
                    'date': 'Invalid date'
                })
            
            reserved_room_ids = Reservation.objects.filter(
                check_in_date__lte=date_param,
                check_out_date__gte=date_param
            ).values_list('room_id', flat=True)

            return Room.objects.exclude(id__in=reserved_room_ids)
        else:
            # If no date is specified, return empty list
            return []


class RoomCreateAPIView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        # log action
        logger.info(f"Added room {instance.room_number} of type {instance.room_type}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservationListAPIView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user
        )


class ReservationCreateAPIView(generics.CreateAPIView):
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.validated_data.get('room')
        check_in_date = serializer.validated_data.get('check_in_date')
        check_out_date = serializer.validated_data.get('check_out_date')

        # validate dates
        if check_in_date > check_out_date or check_in_date < datetime.today().date():
            raise serializers.ValidationError({
                'check_in_date': 'Invalid date range'
            })

        # Check if the room is available for the specified date range
        reservations = Reservation.objects.filter(
            room=room,
            check_out_date__gte=check_in_date,
            check_in_date__lte=check_out_date
        )

        if reservations.exists():
            raise serializers.ValidationError({
                'room_number': 'Room is already reserved for this date range'
            })

        # If the room is available, create the reservation
        instance = serializer.save()
        # log action
        logger.info(f"Made a reservation for room {instance.room.room_number} by user {instance.user.username}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservationRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationCancelAPIView(generics.DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer



