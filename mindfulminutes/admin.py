from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import CustomUser

class CustomUserAdminForm(forms.ModelForm):
    """
    A custom form for the CustomUserAdmin to manage CustomUser model

    The form includes the necessary fields and customisation for the admin interface
    """
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    reset_password = forms.BooleanField(required=False, initial=False)

    class Meta:
        """
        Metadata options for the CustomUserAdminForm.
        Defines the model (CustomUser) associated with this form and the fields (__all__) to be included
        """
        model = CustomUser
        fields = '__all__'


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin configuration for User model

    The class defines the display and behaviour of the User model
    """
    list_display = ('email', 'first_name', 'last_name',
                    'display_password', 'is_active', 'is_staff', 'is_superuser')

    form = CustomUserAdminForm
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'reset_password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Tracking', {'fields': ('last_login', 'created_at')}),
    )

    def display_password(self, obj):
        """ Retrieve the hashed password and return it in a non-editable format """
        hashed_password = obj.password
        return mark_safe(f'<span title="{hashed_password}">********</span>')

    display_password.short_description = 'Password'
    display_password.admin_order_field = 'password'
    display_password.empty_value_display = 'N/A'

    def save_model(self, request, obj, form, change):
        """ Check if the password field was reset """
        if form.cleaned_data['reset_password']:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
