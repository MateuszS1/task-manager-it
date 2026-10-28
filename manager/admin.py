from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from manager.models import TaskType, Position, Worker, Task


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position__name",)
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "username",
                    ("first_name", "last_name"),
                    "email",
                ),
            },
        ),
        (
            "Password",
            {
                "fields": (
                    "password",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (
            "Position",
            {
                "fields": (
                    "position",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "username",
                    ("first_name", "last_name"),
                    "email",
                ),
            },
        ),
        (
            "Password",
            {
                "fields": (
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Position",
            {
                "fields": (
                    "position",
                ),
            },
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "is_completed", "deadline", "priority", "task_type")
    search_fields = ("name",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "deadline",
                    "priority",
                    "task_type",
                    "assignees",
                ),
            },
        ),
    )

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)
