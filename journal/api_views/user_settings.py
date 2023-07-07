from datetime import date

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from ..models import UserSettings
from ..serializers import UserSettingsSerializer


class UserSettingsView(APIView):
    """
    Retrieve, update, delete user settings for a specific user
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, user_id):
        """
        Helper method to get the user settings object
        for the given user ID or raise a 404 error if not found
        """
        try:
            return UserSettings.objects.get(user=user_id)
        except UserSettings.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        """
        Retrieve user settings for specified user
        """
        if request.user.id != user_id:
            return Response(
                {"error": "You are not authorised to access these settings."},
                status=status.HTTP_403_FORBIDDEN
            )

        user_settings = self.get_object(user_id)
        serializer = UserSettingsSerializer(user_settings)
        return Response(serializer.data)

    def post(self, request, user_id, format=None):
        """
        Create user settings for the specified user
        """
        if request.user.id != user_id:
            return Response(
                {"error": "You are not authorised to create these settings."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserSettingsSerializer(data=request.data)

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

    def delete(self, request, user_id, format=None):
        """
        Delete user setting of the specified user
        """
        if request.user.id != user_id:
            return Response(
                {"error": "You are not authorised to delete these settings."},
                status=status.HTTP_403_FORBIDDEN
            )

        user_settings = self.get_object(user_id)
        user_settings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, user_id, format=None):
        """
        Update user settings for the specified user 
        """
        if request.user.id != user_id:
            return Response(
                {"error": "You are not authorised to update these settings."},
                status=status.HTTP_403_FORBIDDEN
            )

        user_settings = get_object_or_404(UserSettings, user=user_id)
        serializer = UserSettingsSerializer(user_settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
