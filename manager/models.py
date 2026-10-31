from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="workers"
    )

    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"
        ordering = ["username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("manager:worker-detail", args=[str(self.id)])


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "URGENT", "Urgent"
        HIGH = "HIGH", "High"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"

    PRIORITY_COLORS = {
        Priority.URGENT: "danger",
        Priority.HIGH: "warning",
        Priority.MEDIUM: "info",
        Priority.LOW: "success",
    }

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.LOW,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.PROTECT,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        Worker,
        blank=True,
        related_name="tasks",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("manager:task-detail", args=[str(self.id)])

    @property
    def priority_color(self):
        return self.PRIORITY_COLORS.get(self.priority, "secondary")
