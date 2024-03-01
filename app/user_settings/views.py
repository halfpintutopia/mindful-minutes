from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserSettings
from .serializers import UserSettingsSerializer


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
    
    def get(self, request, slug, format=None):
        """
        Retrieve user settings for specified user
        """
        if request.user.slug != slug:
            return Response(
                {"error": "You are not authorised to access these settings."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        user_settings = self.get_object(request.user.id)
        serializer = UserSettingsSerializer(user_settings)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "start_week_day": openapi.Schema(type=openapi.TYPE_INTEGER),
                "morning_check_in": openapi.Schema(type=openapi.TYPE_STRING),
                "evening_check_in": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def post(self, request, slug, format=None):
        """
        Create user settings for the specified user
        """
        if request.user.slug != slug:
            return Response(
                {"error": "You are not authorised to create these settings."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        serializer = UserSettingsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug, format=None):
        """
        Delete user setting of the specified user
        """
        if request.user.slug != slug:
            return Response(
                {"error": "You are not authorised to delete these settings."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        user_settings = self.get_object(request.user.id)
        user_settings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "start_week_day": openapi.Schema(type=openapi.TYPE_INTEGER),
                "morning_check_in": openapi.Schema(type=openapi.TYPE_STRING),
                "evening_check_in": openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def put(self, request, slug, format=None):
        """
        Update user settings for the specified user
        """
        if request.user.slug != slug:
            return Response(
                {"error": "You are not authorised to update these settings."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        user_settings = get_object_or_404(UserSettings, user=request.user.id)
        serializer = UserSettingsSerializer(user_settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
