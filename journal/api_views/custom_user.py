from datetime import date

from django.http import Http404
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from ..serializers import CustomUserSerializer

User = get_user_model()


class CustomUserList(APIView):
    """
    List all users or create a new user
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        List all users or filter by date
        """
        return self._handle_user_list_action(request)

    def post(self, request, format=None):
        """
        Create a new user
        """
        return self._handle_user_list_action(request)

    def _handle_user_list_action(self, request):
        """
        Private helper method to handle both GET and POST requests

        Check if request is allowed based on the date and either
        lists all users or creates a new user
        """
        if request.method == "GET":
            user_entries = User.objects.all()

            serializer = CustomUserSerializer(
                user_entries, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            serializer = CustomUserSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        raise MethodNotAllowed(request.method)


class CustomUserDetail(APIView):
    """
    Retrieve, update or delete an user
    """
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get an user object from the database
        or raise a 404 error
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Retrieve an user
        """
        return self._handle_user_detail_action(request, pk)

    def put(self, request, pk, format=None):
        """
        Update an user
        """
        return self._handle_user_detail_action(request, pk)

    def delete(self, request, pk, format=None):
        """
        Delete an user
        """
        return self._handle_user_detail_action(request, pk)

    def _handle_user_detail_action(self, request, pk):
        """
        Private helper method to handle GET, PUT and DELETE requests

        Check if request is allowed based on date and
        either retrieve, update or delete an user
        """
        if pk is not None:
            try:
                user_id = isinstance(pk, int)
                user = self.get_object(pk)
            except (ValueError, Http404):
                if isinstance(pk, str):
                    return Response(
                        {"error": "Invalid user ID"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.method == "GET":
                serializer = CustomUserSerializer(user)
                return Response(serializer.data)

            elif request.method == "PUT":
                serializer = CustomUserSerializer(
                    user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            elif request.method == "DELETE":
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
