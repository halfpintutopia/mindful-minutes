from datetime import date

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..models import WinEntry
from ..serializers import WinEntrySerializer


class WinEntryList(APIView):
    """
    List all win entries or create a new win entry
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, slug, date_request=None, format=None):
        """
        List all win entries or filter by date
        """
        return self._handle_win_list_action(request, slug, date_request)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def post(self, request, slug, date_request, format=None):
        """
        Create a new win entry
        """
        return self._handle_win_list_action(request, slug, date_request)

    def _handle_win_list_action(self, request, slug, date_request):
        """
        Private helper method to handle both GET and POST requests

        Check if request is allowed based on the date and either
        lists all win entries or creates a new win entry
        """
        if request.method == "GET":
            if request.user.slug == slug:
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
                    win_entries = WinEntry.objects.filter(
                        created_on__date=requested_date)
                else:
                    win_entries = WinEntry.objects.all()

                serializer = WinEntrySerializer(
                    win_entries, many=True)
                return Response(serializer.data)

        if request.method == "POST":
            if request.user.slug == slug:
                current_date = date.today().strftime("%Y-%m-%d")
                if date_request != current_date:
                    return Response(
                        {
                            "error":
                            "You are not allowed to change wins \
                                for past or future dates."
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
                serializer = WinEntrySerializer(data=request.data)
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


class WinEntryDetail(APIView):
    """
    Retrieve, update or delete an win entry
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get an win entry object from the database
        or raise a 404 error
        """
        try:
            return WinEntry.objects.get(pk=pk)
        except WinEntry.DoesNotExist:
            raise Http404

    def get(self, request, slug, date_request, pk, format=None):
        """
        Retrieve an win entry
        """
        return self._handle_win_detail_action(request, slug, date_request, pk)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def put(self, request, slug, date_request, pk, format=None):
        """
        Update an win entry
        """
        return self._handle_win_detail_action(request, slug, date_request, pk)

    def delete(self, request, slug, date_request, pk, format=None):
        """
        Delete an win entry
        """
        return self._handle_win_detail_action(request, slug, date_request, pk)

    def _handle_win_detail_action(self, request, slug, date_request, pk):
        """
        Private helper method to handle GET, PUT and DELETE requests

        Check if request is allowed based on date and
        either retrieve, update or delete an win entry
        """
        current_date = date.today().strftime("%Y-%m-%d")
        if date_request != current_date:
            return Response(
                {
                    "error":
                    "You are not allowed to change wins \
                        for past or future dates."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        if request.user.slug == slug:
            if pk is not None:
                try:
                    win_id = isinstance(pk, int)
                    win_entry = self.get_object(pk)
                except (ValueError, Http404):
                    if isinstance(pk, str):
                        return Response(
                            {"error": "Invalid win ID"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    return Response(status=status.HTTP_404_NOT_FOUND)

                if request.method == "GET":
                    serializer = WinEntrySerializer(win_entry)
                    return Response(serializer.data)

                elif request.method == "PUT":
                    serializer = WinEntrySerializer(
                        win_entry, data=request.data)
                    if serializer.is_valid():
                        serializer.save(user=request.user)
                        return Response(serializer.data)
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )

                elif request.method == "DELETE":
                    win_entry.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_403_FORBIDDEN)
