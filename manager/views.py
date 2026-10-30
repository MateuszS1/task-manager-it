from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from manager.forms import WorkerCreationForm, TaskCreationForm, WorkerSearchForm, TaskSearchForm, PositionSearchForm, \
    TaskTypeSearchForm, TaskStatusUpdateForm, TaskAssigneeUpdateForm, WorkerUpdateForm, UserUpdateForm
from manager.models import TaskType, Position, Worker, Task


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_workers": Worker.objects.count(),
        "num_completed_tasks": Task.objects.filter(is_completed=False).count(),
    }
    return render(
        request,
        "manager/index.html",
        context=context
    )

#   List Views
class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "manager/task_type_list.html"
    context_object_name = "task_type_list"
    queryset = TaskType.objects.annotate(task_count=Count("tasks"))
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name}
        )

        paginator = context["page_obj"].paginator

        start = max(context["page_obj"].number - 2, 1)
        end = min(start + 4, paginator.num_pages)
        start = max(end - 4, 1)

        context["page_range"] = range(start, end + 1)

        context["breadcrumbs"] = [
            {
                "title": "Task Types",
                "active": True,
            },
        ]

        return context

    def get_queryset(self):
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    queryset = Position.objects.annotate(worker_count=Count("workers"))
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )

        paginator = context["page_obj"].paginator

        start = max(context["page_obj"].number - 2, 1)
        end = min(start + 4, paginator.num_pages)
        start = max(end - 4, 1)

        context["page_range"] = range(start, end + 1)

        context["breadcrumbs"] = [
            {
                "title": "Positions",
                "active": True,
            },
        ]

        return context

    def get_queryset(self):
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )

        paginator = context["page_obj"].paginator

        start = max(context["page_obj"].number - 2, 1)
        end = min(start + 4, paginator.num_pages)
        start = max(end - 4, 1)

        context["page_range"] = range(start, end + 1)

        context["breadcrumbs"] = [
            {
                "title": "Workers",
                "active": True,
            },
        ]

        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )

        paginator = context["page_obj"].paginator

        start = max(context["page_obj"].number - 2, 1)
        end = min(start + 4, paginator.num_pages)
        start = max(end - 4, 1)

        context["page_range"] = range(start, end + 1)

        context["breadcrumbs"] = [
            {
                "title": "Tasks",
                "active": True,
            },
        ]

        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

#   Detail Views
class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object.tasks.all(), self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["paginator"] = paginator
        context["is_paginated"] = page_obj.has_other_pages()

        start = max(context["page_obj"].number - 2, 1)
        end = min(start + 4, paginator.num_pages)
        start = max(end - 4, 1)

        context["page_range"] = range(start, end + 1)

        context["breadcrumbs"] = [
            {
                "title": "Workers",
                "url": reverse("manager:worker-list"),
            },
            {
                "title": "Details",
                "active": True,
            },
        ]

        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object.assignees.all(), self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["paginator"] = paginator
        context["is_paginated"] = page_obj.has_other_pages()

        start = max(context["page_obj"].number - 2, 1)
        end = min(start + 4, paginator.num_pages)
        start = max(end - 4, 1)

        context["page_range"] = range(start, end + 1)

        context["breadcrumbs"] = [
            {
                "title": "Tasks",
                "url": reverse("manager:task-list"),
            },
            {
                "title": "Details",
                "active": True,
            },
        ]

        return context

#   Create Views
class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "manager/task_type_form.html"
    context_object_name = "task_type_create"
    success_url = reverse_lazy("manager:task-type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {
                "title": "Task Types",
                "url": reverse("manager:task-type-list"),
            },
            {
                "title": "Create",
                "active": True,
            },
        ]

        return context


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {
                "title": "Positions",
                "url": reverse("manager:position-list"),
            },
            {
                "title": "Create",
                "active": True,
            },
        ]

        return context


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:worker-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {
                "title": "Worker",
                "url": reverse("manager:worker-list"),
            },
            {
                "title": "Create",
                "active": True,
            },
        ]

        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {
                "title": "Tasks",
                "url": reverse("manager:task-list"),
            },
            {
                "title": "Create",
                "active": True,
            },
        ]

        return context

#   Update Views
class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "manager/task_type_form.html"
    context_object_name = "task_type_update"
    success_url = reverse_lazy("manager:task-type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {
                "title": "Task Types",
                "url": reverse("manager:task-type-list"),
            },
            {
                "title": "Create",
                "active": True,
            },
        ]

        return context

class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {
                "title": "Positions",
                "url": reverse("manager:position-list"),
            },
            {
                "title": "Create",
                "active": True,
            },
        ]

        return context


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("manager:worker-list")

    def get_form_class(self):
        if self.object == self.request.user:
            return UserUpdateForm

        return WorkerUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {
                "title": "Workers",
                "url": reverse("manager:worker-list"),
            },
            {
                "title": "Details",
                "url": reverse("manager:worker-detail", kwargs={"pk": self.kwargs.get("pk")}),
            },
            {
                "title": "Update",
                "active": True,
            },
        ]

        return context


class TaskStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskStatusUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {
                "title": "Tasks",
                "url": reverse("manager:task-list"),
            },
            {
                "title": "Details",
                "url": reverse("manager:task-detail", kwargs={"pk": self.kwargs.get("pk")}),
            },
            {
                "title": "Update",
                "active": True,
            },
        ]

        return context

class TaskAssigneeUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskAssigneeUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {
                "title": "Tasks",
                "url": reverse("manager:task-list"),
            },
            {
                "title": "Details",
                "url": reverse("manager:task-detail", kwargs={"pk": self.kwargs.get("pk")}),
            },
            {
                "title": "Update",
                "active": True,
            },
        ]

        return context

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
    model = Task
    success_url = reverse_lazy("manager:task-list")
