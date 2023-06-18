from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

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
    list_filter = ("gender", "is_active")
    actions = ["activate", "deactivate"]

    @admin.action(description="Deactivate selected users")
    def deactivate(self, request: WSGIRequest, queryset: models.QuerySet):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            ngettext_lazy(
                "%d user was successfully deactivated.",
                "%d users were successfully deactivated.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description="Activate selected users")
    def activate(self, request: WSGIRequest, queryset: models.QuerySet):
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            ngettext_lazy(
                "%d user was successfully activated.",
                "%d users were successfully activated.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(User, CustomUserAdmin)
