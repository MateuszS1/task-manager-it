from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from manager.forms import WorkerCreationForm, TaskCreationForm, WorkerSearchForm, TaskSearchForm, PositionSearchForm, \
    TaskTypeSearchForm, TaskStatusUpdateForm, TaskAssigneeUpdateForm
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name}
        )

        paginator = context["page_obj"].paginator

        start = max(context["page_obj"].number - 2, 1)
        end = min(start + 4, paginator.num_pages)
        start = max(end - 4, 1)

        context["page_range"] = range(start, end + 1)

        return context


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    template_name = "manager/position_list.html"
    context_object_name = "position_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )

        paginator = context["page_obj"].paginator

        start = max(context["page_obj"].number - 2, 1)
        end = min(start + 4, paginator.num_pages)
        start = max(end - 4, 1)

        context["page_range"] = range(start, end + 1)

        return context

class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = WorkerSearchForm(
            initial={"name": name}
        )

        paginator = context["page_obj"].paginator

        start = max(context["page_obj"].number - 2, 1)
        end = min(start + 4, paginator.num_pages)
        start = max(end - 4, 1)

        context["page_range"] = range(start, end + 1)

        return context

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )

        paginator = context["page_obj"].paginator

        start = max(context["page_obj"].number - 2, 1)
        end = min(start + 4, paginator.num_pages)
        start = max(end - 4, 1)

        context["page_range"] = range(start, end + 1)

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


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task

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


class TaskStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskStatusUpdateForm

class TaskAssigneeUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskAssigneeUpdateForm

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
