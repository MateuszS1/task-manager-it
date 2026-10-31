import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.forms import (
    TaskTypeSearchForm,
    PositionSearchForm,
    WorkerSearchForm,
    TaskSearchForm,
    TaskStatusUpdateForm, TaskAssigneeUpdateForm
)
from manager.models import TaskType, Task, Position


class TaskStatusUpdateFormTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="test_task_name"
        )

    def test_task_form_updates_status(self):
        task = Task.objects.create(
            name="test_task",
            description="Task description",
            deadline=datetime.date.today(),
            priority=Task.Priority.LOW,
            task_type=self.task_type,
        )

        form = TaskStatusUpdateForm(
            data={"is_completed": True},
            instance=task,
        )

        self.assertTrue(form.is_valid(), form.errors)

        task = form.save()

        self.assertTrue(task.is_completed)

    def test_task_form_updates_status_after_deadline(self):
        task = Task.objects.create(
            name="test_task",
            description="Task description",
            deadline=datetime.date.today() - datetime.timedelta(days=1),
            priority=Task.Priority.LOW,
            task_type=self.task_type,
        )

        form = TaskStatusUpdateForm(
            data={"is_completed": True},
            instance=task,
        )

        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("is_completed", form.errors)


class TaskAssigneeUpdateFormTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="test_task_name"
        )
        self.task = Task.objects.create(
            name="test_task",
            description="Task description",
            deadline=datetime.date.today(),
            priority=Task.Priority.LOW,
            task_type=self.task_type,
        )

        self.position = Position.objects.create(name="test_position")

        self.worker1 = get_user_model().objects.create(
            username="test_worker1",
            first_name="test1",
            last_name="worker1",
            password="q1a2z3w4",
            position=self.position,
        )
        self.worker2 = get_user_model().objects.create(
            username="test_worker2",
            first_name="test2",
            last_name="worker2",
            password="q1a2z3w4",
            position=self.position,
        )

    def test_form_saves_car_with_selected_drivers(self):
        form = TaskAssigneeUpdateForm(
            data={"assignees": [self.worker1.pk, self.worker2.pk], },
            instance=self.task,
        )

        self.assertTrue(form.is_valid(), form.errors)

        task = form.save()

        self.assertCountEqual(
            task.assignees.all(),
            [self.worker1, self.worker2],
        )

    def test_missing_required_fields(self):
        form = TaskAssigneeUpdateForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn("assignees", form.errors)


class PositionSearchFormTests(TestCase):
    def test_position_empty_name_is_valid(self):
        form = PositionSearchForm(data={"name": ""})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_position_valid_name_search(self):
        form = PositionSearchForm(data={"name": "test_position"})

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["name"],
            "test_position",
        )

    def test_position_name_exceeding_max_length_is_invalid(self):
        form = PositionSearchForm(data={"name": "A" * 256})

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_position_name_widget_placeholder(self):
        form = PositionSearchForm()

        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name",
        )


class TaskTypeSearchFormTests(TestCase):
    def test_task_type_empty_name_is_valid(self):
        form = TaskTypeSearchForm(data={"name": ""})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_task_type_valid_name_search(self):
        form = TaskTypeSearchForm(data={"name": "test_type"})

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["name"],
            "test_type",
        )

    def test_task_type_name_exceeding_max_length_is_invalid(self):
        form = TaskTypeSearchForm(data={"name": "A" * 256})

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_task_type_name_widget_placeholder(self):
        form = TaskTypeSearchForm()

        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name",
        )


class WorkerSearchFormTests(TestCase):
    def test_worker_empty_username_is_valid(self):
        form = WorkerSearchForm(data={"username": ""})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_worker_valid_username_search(self):
        form = WorkerSearchForm(data={"username": "test_user"})

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            "test_user",
        )

    def test_worker_username_exceeding_max_length_is_invalid(self):
        form = WorkerSearchForm(data={"username": "A" * 256})

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_worker_username_widget_placeholder(self):
        form = WorkerSearchForm()

        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username",
        )


class TaskSearchFormTests(TestCase):
    def test_task_empty_name_is_valid(self):
        form = TaskSearchForm(data={"name": ""})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_task_valid_name_search(self):
        form = TaskSearchForm(data={"name": "test_task"})

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["name"],
            "test_task",
        )

    def test_task_name_exceeding_max_length_is_invalid(self):
        form = TaskSearchForm(data={"name": "A" * 256})

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_task_name_widget_placeholder(self):
        form = TaskSearchForm()

        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name",
        )
