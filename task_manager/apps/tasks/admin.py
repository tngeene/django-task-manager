from django.contrib import admin

from task_manager.apps.tasks import models

# Register your models here.


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title",)
    readonly_fields = ("created_at", "reporter")


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    readonly_fields = (
        "created_at",
        "created_by",
    )


@admin.register(models.TaskComment)
class TaskCommentorAdmin(admin.ModelAdmin):
    readonly_fields = ("commentor",)
