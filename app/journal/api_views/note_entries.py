from datetime import date

from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import NoteEntry
from ..serializers import NoteEntrySerializer


class NoteEntryList(APIView):
    """
    List all note entries or create a new note entry
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, slug, date_request=None, format=None):
        """
        List all note entries or filter by date
        """
        return self._handle_note_list_action(request, slug, date_request)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "content": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def post(self, request, slug, date_request, format=None):
        """
        Create a new note entry
        """
        return self._handle_note_list_action(request, slug, date_request)

    def _handle_note_list_action(self, request, slug, date_request):
        """
        Private helper method to handle both GET and POST requests

        Check if request is allowed based on the date and either
        lists all note entries or creates a new note entry
        """
        if request.method == "GET":
            if request.user.slug == slug:
                if date_request is not None:
                    try:
                        requested_date = date.fromisoformat(date_request)
                    except ValueError:
                        return Response(
                            {
                                "error": "Invalid date format. Please user "
                                "YYYY-MM-DD."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    note_entries = NoteEntry.objects.filter(
                        created_on__date=requested_date
                    )
                else:
                    note_entries = NoteEntry.objects.all()

                serializer = NoteEntrySerializer(note_entries, many=True)
                return Response(serializer.data)

        if request.method == "POST":
            if request.user.slug == slug:
                current_date = date.today().strftime("%Y-%m-%d")
                if date_request != current_date:
                    return Response(
                        {
                            "error": "You are not allowed to change notes \
                                    for past or future dates."
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
                serializer = NoteEntrySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED
                    )
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        raise MethodNotAllowed(request.method)


class NoteEntryDetail(APIView):
    """
    Retrieve, update or delete an note entry
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get an note entry object from the database
        or raise a 404 error
        """
        try:
            return NoteEntry.objects.get(pk=pk)
        except NoteEntry.DoesNotExist:
            raise Http404

    def get(self, request, slug, date_request, pk, format=None):
        """
        Retrieve an note entry
        """
        return self._handle_note_detail_action(request, slug, date_request, pk)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "content": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def put(self, request, slug, date_request, pk, format=None):
        """
        Update an note entry
        """
        return self._handle_note_detail_action(request, slug, date_request, pk)

    def delete(self, request, slug, date_request, pk, format=None):
        """
        Delete an note entry
        """
        return self._handle_note_detail_action(request, slug, date_request, pk)

    def _handle_note_detail_action(self, request, slug, date_request, pk):
        """
        Private helper method to handle GET, PUT and DELETE requests

        Check if request is allowed based on date and
        either retrieve, update or delete an note entry
        """
        current_date = date.today().strftime("%Y-%m-%d")
        if date_request != current_date:
            return Response(
                {
                    "error": "You are not allowed to change notes \
                            for past or future dates."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        if request.user.slug == slug:
            if pk is not None:
                try:
                    isinstance(pk, int)
                    note_entry = self.get_object(pk)
                except (ValueError, Http404):
                    if isinstance(pk, str):
                        return Response(
                            {"error": "Invalid note ID"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    return Response(status=status.HTTP_404_NOT_FOUND)

                if request.method == "GET":
                    serializer = NoteEntrySerializer(note_entry)
                    return Response(serializer.data)

                elif request.method == "PUT":
                    serializer = NoteEntrySerializer(
                        note_entry, data=request.data
                    )
                    if serializer.is_valid():
                        serializer.save(user=request.user)
                        return Response(serializer.data)
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

                elif request.method == "DELETE":
                    note_entry.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_403_FORBIDDEN)
