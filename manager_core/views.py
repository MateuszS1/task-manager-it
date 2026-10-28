from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from manager_core.models import TaskType, Position, Worker, Task


# Create your views here.

class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "manager/task_type_list_view.html"
    context_object_name = "task_type_list"

class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    template_name = "manager/position_list_view.html"
    context_object_name = "position_list"

class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    paginate_by = 5

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 5
