from allauth.account.forms import SignupForm
from django import forms
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


class EmailInputWithPlaceholder(forms.EmailInput):
    def __init__(self, placeholder="", attrs=None):
        if placeholder:
            attrs = attrs or {}
            attrs["placeholder"] = placeholder

        super(EmailInputWithPlaceholder, self).__init__(attrs=attrs)


class CustomSignupForm(SignupForm):
    """
    Form to sign up new users
    """

    first_name = forms.CharField(
        max_length=35,
        label="What is your first name?",
        required=True,
        help_text="We'll address you by this",
        widget=forms.TextInput(attrs={"placeholder": "Arthur"}),
    )
    last_name = forms.CharField(
        max_length=35,
        label="What is your last name?",
        required=True,
        help_text="To ensure your journal entries are for your eyes only!",
        widget=forms.TextInput(attrs={"placeholder": "Dent"}),
    )
    email = forms.EmailField(
        label="What is your email address?",
        required=True,
        help_text="You'll need this to log in",
        widget=EmailInputWithPlaceholder(
            attrs={"placeholder": "arthur.dent@hitchhikersguide.com"}
        ),
    )
    password1 = forms.CharField(
        label="Provide a secure password.",
        help_text="The password should be at least 16 characters, "
        "and contain both lowercase and uppercase plus special "
        "characters",
        widget=forms.PasswordInput(
            attrs={
                "label": "Provide a secure password.",
                "placeholder": "s3cureP@ssw0rd!1234",
            }
        ),
    )
    password2 = forms.CharField(
        label="Repeat the password.",
        help_text="Just to make sure you are awake",
        widget=forms.PasswordInput(
            attrs={"placeholder": "s3cureP@ssw0rd!1234"}
        ),
    )

    # https://stackoverflow.com/a/63625914/8614652
    field_order = [
        "first_name",
        "last_name",
        "email",
        "password1",
        "password2",
    ]

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user
