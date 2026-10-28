from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from manager_core.forms import WorkerCreationForm, TaskCreationForm
from manager_core.models import TaskType, Position, Worker, Task


def index(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "manager/index.html",
    )

#   List Views
class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    context_object_name = "task_type_list"


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    context_object_name = "position_list"


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    paginate_by = 5


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 5

#   Detail Views
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    queryset = Task.objects.all().prefetch_related("task_type__name")


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("position__name")

#   Create Views
class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("manager:task-type-list")


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:worker-list")


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("manager:task-list")

#   Update Views
class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("manager:task-type-list")


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:worker-list")


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("manager:task-list")

#   Delete Views
class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    success_url = reverse_lazy("manager:task-type-list")


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy("manager:position-list")


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:worker-list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    success_url = reverse_lazy("manager:task-list")
