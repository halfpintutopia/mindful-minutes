from datetime import date

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from ..models import GratitudeEntry
from ..serializers import GratitudeEntrySerializer


class GratitudeEntryList(APIView):
    """
    List all gratitude entries or create a new gratitude entry
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, slug, date_request=None, format=None):
        """
        List all gratitude entries or filter by date
        """
        return self._handle_gratitude_list_action(request, slug, date_request)

    def post(self, request, slug, date_request, format=None):
        """
        Create a new gratitude entry
        """
        return self._handle_gratitude_list_action(request, slug, date_request)

    def _handle_gratitude_list_action(self, request, slug, date_request):
        """
        Private helper method to handle both GET and POST requests

        Check if request is allowed based on the date and either
        lists all gratitude entries or creates a new gratitude entry
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
                    gratitude_entries = GratitudeEntry.objects.filter(
                        created_on__date=requested_date)
                else:
                    gratitude_entries = GratitudeEntry.objects.all()

                serializer = GratitudeEntrySerializer(
                    gratitude_entries, many=True)
                return Response(serializer.data)

        if request.method == "POST":
            if request.user.slug == slug:
                current_date = date.today().strftime("%Y-%m-%d")
                if date_request != current_date:
                    return Response(
                        {
                            "error":
                            "You are not allowed to change gratitudes \
                                for past or future dates."
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
                serializer = GratitudeEntrySerializer(data=request.data)
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


class GratitudeEntryDetail(APIView):
    """
    Retrieve, update or delete an gratitude entry
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get an gratitude entry object from the database
        or raise a 404 error
        """
        try:
            return GratitudeEntry.objects.get(pk=pk)
        except GratitudeEntry.DoesNotExist:
            raise Http404

    def get(self, request, slug, date_request, pk, format=None):
        """
        Retrieve an gratitude entry
        """
        return self._handle_gratitude_detail_action(request, slug, date_request, pk)

    def put(self, request, slug, date_request, pk, format=None):
        """
        Update an gratitude entry
        """
        return self._handle_gratitude_detail_action(request, slug, date_request, pk)

    def delete(self, request, slug, date_request, pk, format=None):
        """
        Delete an gratitude entry
        """
        return self._handle_gratitude_detail_action(request, slug, date_request, pk)

    def _handle_gratitude_detail_action(self, request, slug, date_request, pk):
        """
        Private helper method to handle GET, PUT and DELETE requests

        Check if request is allowed based on date and
        either retrieve, update or delete an gratitude entry
        """
        current_date = date.today().strftime("%Y-%m-%d")
        if date_request != current_date:
            return Response(
                {
                    "error":
                    "You are not allowed to change gratitudes \
                        for past or future dates."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        if request.user.slug == slug:
            if pk is not None:
                try:
                    gratitude_id = isinstance(pk, int)
                    gratitude_entry = self.get_object(pk)
                except (ValueError, Http404):
                    if isinstance(pk, str):
                        return Response(
                            {"error": "Invalid gratitude ID"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    return Response(status=status.HTTP_404_NOT_FOUND)

                if request.method == "GET":
                    serializer = GratitudeEntrySerializer(gratitude_entry)
                    return Response(serializer.data)

                elif request.method == "PUT":
                    serializer = GratitudeEntrySerializer(
                        gratitude_entry, data=request.data)
                    if serializer.is_valid():
                        serializer.save(user=request.user)
                        return Response(serializer.data)
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )

                elif request.method == "DELETE":
                    gratitude_entry.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_403_FORBIDDEN)
