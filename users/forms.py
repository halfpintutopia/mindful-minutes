from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Form to create the custom user model to add new users
    """
    class Meta:
        """
        Meta options for the CustomUser model
        """
        model = CustomUser
        fields = ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    """
    Form to change the custom user model
    """
    class Meta:
        """
        Meta options for the CustomUser model
        """
        model = CustomUser
        fields = ("email", "first_name", "last_name")
