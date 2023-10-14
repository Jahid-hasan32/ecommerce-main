from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreation_form

class UserAdmin(BaseUserAdmin):
    add_form = UserCreation_form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'mobile','password1', 'password2'),
        }),
    )
    
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email', 'mobile', 'password1', 'password2', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'is_active'),
    #     }),
    # )
    
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "mobile")}),
        ("Permissions", {"fields": ("is_active", "is_superuser","is_staff", "groups", "user_permissions")}),
    )
    
    ordering = ('username',)
    
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'groups')
    list_display = ["email", "username", "is_superuser", "is_staff"]

    def get_user_permissions(self, obj):
        return ', '.join([str(perm) for perm in obj.user_permissions.all()])
    get_user_permissions.short_description = 'User Permissions'

admin.site.register(User, UserAdmin)
