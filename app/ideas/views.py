from datetime import date

from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import IdeasEntry
from .serializers import IdeasEntrySerializer


class IdeasEntryList(APIView):
    """
    List all ideas entries or create a new ideas entry
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        """
        List all ideas entries
        """
        if request.method == "GET":
            if request.user.slug == slug:
                ideas_entries = IdeasEntry.objects.all()

                serializer = IdeasEntrySerializer(ideas_entries, many=True)
                return Response(serializer.data)

            raise MethodNotAllowed(request.method)


class IdeasEntryListCreate(APIView):
    """
    List or create ideas entries for a specific date
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, slug, date_request=None):
        """
        List all ideas entries or filter by date
        """
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
                ideas_entries = IdeasEntry.objects.filter(
                    created_on__date=requested_date
                )

                serializer = IdeasEntrySerializer(ideas_entries, many=True)
                return Response(serializer.data)

        raise MethodNotAllowed(request.method)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "date": openapi.Schema(type=openapi.TYPE_STRING),
                "time_from": openapi.Schema(type=openapi.TYPE_STRING),
                "time_until": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def post(self, request, slug, date_request=None):
        """
        Create a new ideas entry
        """
        if request.method == "POST":
            if request.user.slug == slug:
                current_date = date.today().strftime("%Y-%m-%d")
                if date_request != current_date:
                    return Response(
                        {
                            "error": "You are not allowed to change "
                            "ideass \
                                             for past or future dates."
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
                serializer = IdeasEntrySerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED
                    )
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        raise MethodNotAllowed(request.method)


class IdeasEntryDetail(APIView):
    """
    Retrieve, update or delete an ideas entry
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get an ideas entry object from the database
        or raise a 404 error
        """
        try:
            return IdeasEntry.objects.get(pk=pk)
        except IdeasEntry.DoesNotExist:
            raise Http404

    def get(self, request, slug, date_request, pk):
        """
        Retrieve an ideas entry
        """
        return self._handle_ideas_detail_action(request, slug, date_request, pk)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "date": openapi.Schema(type=openapi.TYPE_STRING),
                "time_from": openapi.Schema(type=openapi.TYPE_STRING),
                "time_until": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def put(self, request, slug, date_request, pk):
        """
        Update an ideas entry
        """
        return self._handle_ideas_detail_action(request, slug, date_request, pk)

    def delete(self, request, slug, date_request, pk):
        """
        Delete an ideas entry
        """
        return self._handle_ideas_detail_action(request, slug, date_request, pk)

    def _handle_ideas_detail_action(self, request, slug, date_request, pk):
        """
        Private helper method to handle GET, PUT and DELETE requests

        Check if request is allowed based on date and
        either retrieve, update or delete an ideas entry
        """
        current_date = date.today().strftime("%Y-%m-%d")
        if date_request != current_date:
            return Response(
                {
                    "error": "You are not allowed to change ideass \
                            for past or future dates."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if request.user.slug == slug:
            if pk is not None:
                try:
                    isinstance(pk, int)
                    ideas_entry = self.get_object(pk)
                except (ValueError, Http404):
                    if isinstance(pk, str):
                        return Response(
                            {"error": "Invalid ideas ID"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    return Response(status=status.HTTP_404_NOT_FOUND)

                if request.method == "GET":
                    serializer = IdeasEntrySerializer(ideas_entry)
                    return Response(serializer.data)

                elif request.method == "PUT":
                    serializer = IdeasEntrySerializer(
                        ideas_entry, data=request.data
                    )
                    if serializer.is_valid():
                        serializer.save(user=request.user)
                        return Response(serializer.data)
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

                elif request.method == "DELETE":
                    ideas_entry.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_403_FORBIDDEN)
