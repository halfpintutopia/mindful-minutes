from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import AppointmentEntry
from .serializers import AppointmentEntrySerializer


class AppointmentEntryList(APIView):
    """
    List all appointment entries or create a new appointment entry
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        List all appointment entries
        """
        appointment_entries = AppointmentEntry.objects.all()
        serializer = AppointmentEntrySerializer(appointment_entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new appointment entry
        """
        serializer = AppointmentEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentEntryDetail(APIView):
    """
    Retrieve, update or delete an appointment entry
    """

    def get_object(self, pk):
        """
        Helper method to get an appointment entry object from the database
        or raise a 404 error
        """
        try:
            return AppointmentEntry.objects.get(pk=pk)
        except AppointmentEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Retrieve an appointment entry
        """
        appointment = self.get_object(pk)
        serializer = AppointmentEntrySerializer(appointment)
        return Response(serializer.data)
