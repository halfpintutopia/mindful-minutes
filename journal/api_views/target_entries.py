from datetime import date

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import TargetEntry
from ..serializers import TargetEntrySerializer


class TargetEntryList(APIView):
    """
    List all target entries or create a new target entry
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, date_request=None, format=None):
        """
        List all target entries or filter by date
        """
        if date_request is not None:
            try:
                requested_date = date.fromisoformat(date_request)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Please use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # double underscore used to perform field lookups and filters
            # on related fields
            # https://docs.djangoproject.com/en/3.2/topics/db/queries/#field-lookups
            target_entries = TargetEntry.objects.filter(
                created_on__date=requested_date)
        else:
            target_entries = TargetEntry.objects.all()

        serializer = TargetEntrySerializer(target_entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new appointment entry
        """
        serializer = TargetEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TargetEntryDetail(APIView):
    """
    Retrieve, update or delete an target entry
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get an target entry object from the database
        or raise a 404 error
        """
        try:
            return TargetEntry.objects.get(pk=pk)
        except TargetEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Retrieve an target entry
        """
        try:
            target_entry_id = isinstance(pk, int)
            target_entry = self.get_object(target_entry_id)
        except (ValueError, Http404):
            if isinstance(pk, str):
                return Response(
                    {"error": "Invalid appointment ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TargetEntrySerializer(target_entry)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Update an target entry
        """
        try:
            target_entry_id = isinstance(pk, int)
            target_entry = self.get_object(target_entry_id)
        except (ValueError, Http404):
            if isinstance(pk, str):
                return Response(
                    {"error": "Invalid appointment ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TargetEntrySerializer(
            target_entry, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Delete an appointment entry
        """
        try:
            target_entry_id = isinstance(pk, int)
            target_entry = self.get_object(target_entry_id)
        except (ValueError, Http404):
            if isinstance(pk, str):
                return Response(
                    {"error": "Invalid appointment ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_404_NOT_FOUND)

        target_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
