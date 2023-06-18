from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()

admin.site.site_header = "Task Manager App Admin"
admin.site.site_title = "Task Manager App"


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "gender",
                )
            },
        ),
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    list_display = [
        "first_name",
        "last_name",
        "gender",
        "is_active",
    ]
    list_filter = ("gender",)


admin.site.register(User, CustomUserAdmin)
