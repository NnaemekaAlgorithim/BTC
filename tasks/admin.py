from django.contrib import admin

from btc_backend.admin_site import btc_admin
from .models import Task, UserTaskCompletion


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_type", "btc_reward", "is_active", "completion_count", "max_completions", "created_at")
    list_filter = ("task_type", "is_active")
    search_fields = ("title",)
    readonly_fields = ("id", "created_at", "completion_count")


class UserTaskCompletionAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "btc_earned", "completed_at")
    list_filter = ("task__task_type",)
    search_fields = ("user__email", "task__title")
    readonly_fields = ("id", "btc_earned", "completed_at")


btc_admin.register(Task, TaskAdmin)
btc_admin.register(UserTaskCompletion, UserTaskCompletionAdmin)
