from datetime import date

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import AppointmentEntry
from ..serializers import AppointmentEntrySerializer


class AppointmentEntryList(APIView):
    """
    List all appointment entries or create a new appointment entry
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, date_request=None, format=None):
        """
        List all appointment entries or filter by date
        """
        if date_request is not None:
            try:
                requested_date = date.fromisoformat(date_request)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Please user YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            appointment_entries = AppointmentEntry.objects.filter(
                date=requested_date)
        else:
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

    permission_classes = [IsAuthenticated]

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
        try:
            appointment_id = isinstance(pk, int)
            appointment_entry = self.get_object(appointment_id)
        except (ValueError, Http404):
            if isinstance(pk, str):
                return Response(
                    {"error": "Invalid appointment ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentEntrySerializer(appointment_entry)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        """
        Delete an appointment entry
        """
        try:
            appointment_id = isinstance(pk, int)
            appointment_entry = self.get_object(appointment_id)
        except (ValueError, Http404):
            if isinstance(pk, str):
                return Response(
                    {"error": "Invalid appointment ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_404_NOT_FOUND)

        appointment_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
