import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Position, TaskType, Task


class TaskTypeAdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        position = Position.objects.create(
            name="test_position"
        )
        self.user = get_user_model().objects.create_superuser(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=position,
        )
        self.client.force_login(self.user)

        self.task_type = TaskType.objects.create(
            name="test_name1"
        )

    def test_task_type_name_listed(self):
        url = reverse("admin:manager_tasktype_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.task_type.name)

    def test_task_type_detail_name_listed(self):
        url = reverse(
            "admin:manager_tasktype_change",
            args=[self.task_type.id]
        )
        res = self.client.get(url)

        self.assertContains(res, self.task_type.name)


class PositionAdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.position = Position.objects.create(
            name="test_position"
        )
        self.user = get_user_model().objects.create_superuser(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=self.position,
        )
        self.client.force_login(self.user)

    def test_position_name_listed(self):
        url = reverse("admin:manager_position_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.position.name)

    def test_position_detail_name_listed(self):
        url = reverse("admin:manager_position_change", args=[self.position.id])
        res = self.client.get(url)

        self.assertContains(res, self.position.name)


class WorkerAdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        position = Position.objects.create(
            name="test_position"
        )
        self.user = get_user_model().objects.create_superuser(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=position,
        )
        self.client.force_login(self.user)

        self.worker = get_user_model().objects.create_user(
            username="test_worker1",
            first_name="test1",
            last_name="worker1",
            password="q1a2z3w4",
            position=position,
        )

    def test_worker_position_listed(self):
        url = reverse("admin:manager_worker_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.worker.position)

    def test_worker_detail_position_listed(self):
        url = reverse("admin:manager_worker_change", args=[self.worker.id])
        res = self.client.get(url)

        self.assertContains(res, self.worker.position)


class TaskAdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        position = Position.objects.create(
            name="test_position"
        )
        self.user = get_user_model().objects.create_superuser(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=position,
        )
        self.client.force_login(self.user)

        self.task_type = TaskType.objects.create(
            name="test_task"
        )
        self.task = Task.objects.create(
            name="test_task",
            description="Task description",
            deadline=datetime.date.today(),
            priority=Task.Priority.LOW,
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user.id)

    def test_task_data_listed(self):
        url = reverse("admin:manager_task_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.task.name)
        self.assertContains(res, self.task.is_completed)
        self.assertContains(res, self.task.deadline.strftime("%b. %d, %Y"))
        self.assertContains(res, "Low")
        self.assertContains(res, self.task_type.name)

    def test_task_detail_data_listed(self):
        url = reverse("admin:manager_task_change", args=[self.task.id])
        res = self.client.get(url)

        self.assertContains(res, self.task.name)
        self.assertContains(res, self.task.description)
        self.assertContains(res, self.task.deadline)
        self.assertContains(res, "Low")
        self.assertContains(res, self.task_type.name)
