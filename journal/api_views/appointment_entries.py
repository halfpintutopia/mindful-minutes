from datetime import date

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from ..models import AppointmentEntry
from ..serializers import AppointmentEntrySerializer


class AppointmentEntryList(APIView):
    """
    List all appointment entries or create a new appointment entry
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, date_request, format=None):
        """
        List all appointment entries or filter by date
        """
        return self._handle_appointment_list_action(request, date_request)

    def post(self, request, date_request, format=None):
        """
        Create a new appointment entry
        """
        return self._handle_appointment_list_action(request, date_request)

    def _handle_appointment_list_action(self, request, date_request):
        """
        Private helper method to handle both GET and POST requests

        Check if request is allowed based on the date and either
        lists all appointment entries or creates a new appointment entry
        """
        if request.method == "GET":
            if date_request is not None:
                try:
                    requested_date = date.fromisoformat(date_request)
                except ValueError:
                    return Response(
                        {
                            "error":
                            "Invalid date format. Please user YYYY-MM-DD."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                appointment_entries = AppointmentEntry.objects.filter(
                    created_on__date=requested_date)
            else:
                appointment_entries = AppointmentEntry.objects.all()

            serializer = AppointmentEntrySerializer(
                appointment_entries, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            current_date = date.today().strftime("%Y-%m-%d")
            if date_request != current_date:
                return Response(
                    {
                        "error":
                        "You are not allowed to change appointments \
                            for past or future dates."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = AppointmentEntrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        raise MethodNotAllowed(request.method)

        # return Response(
        #     {"error":
        #      f"The requested method: {request.method} is not allowed.",
        #      },
        #     status=status.HTTP_405_METHOD_NOT_ALLOWED
        # )


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

    def get(self, request, date_request, pk, format=None):
        """
        Retrieve an appointment entry
        """
        return self._handle_appointment_detail_action(request, date_request, pk)

    def put(self, request, date_request, pk, format=None):
        """
        Update an appointment entry
        """
        return self._handle_appointment_detail_action(request, date_request, pk)

    def delete(self, request, date_request, pk, format=None):
        """
        Delete an appointment entry
        """
        return self._handle_appointment_detail_action(request, date_request, pk)

    def _handle_appointment_detail_action(self, request, date_request, pk):
        """
        Private helper method to handle GET, PUT and DELETE requests

        Check if request is allowed based on date and
        either retrieve, update or delete an appointment entry
        """
        current_date = date.today().strftime("%Y-%m-%d")
        if date_request != current_date:
            return Response(
                {
                    "error":
                    "You are not allowed to change appointments \
                        for past or future dates."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if pk is not None:
            try:
                isinstance(pk, int)
                appointment_entry = self.get_object(pk)
            except (ValueError, Http404):
                if isinstance(pk, str):
                    return Response(
                        {"error": "Invalid appointment ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.method == "GET":
                serializer = AppointmentEntrySerializer(appointment_entry)
                return Response(serializer.data)

            elif request.method == "PUT":
                serializer = AppointmentEntrySerializer(
                    appointment_entry, data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(serializer.data)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            elif request.method == "DELETE":
                appointment_entry.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
