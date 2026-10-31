import datetime

from django.test import TestCase
from django.urls import reverse

from manager.models import TaskType, Position, Worker, Task


class PublicHomePageTests(TestCase):
    def test_home_page_login_not_required(self):
        res = self.client.get(reverse('manager:index'))
        self.assertEqual(res.status_code, 200)


class PublicTaskTypeTests(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="test_type1")

    def test_task_type_list_login_required(self):
        response = self.client.get(reverse('manager:task-type-list'))
        self.assertNotEqual(response.status_code, 200)

    def test_task_type_create_login_required(self):
        response = self.client.get(reverse('manager:task-type-create'))
        self.assertNotEqual(response.status_code, 200)

    def test_task_type_update_required(self):
        url = reverse(
            "manager:task-type-update",
            kwargs={"pk": self.task_type.id},
        )
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PublicPositionAccessTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_type1")

    def test_position_list_login_required(self):
        response = self.client.get(reverse('manager:position-list'))
        self.assertNotEqual(response.status_code, 200)

    def test_task_type_create_login_required(self):
        response = self.client.get(reverse('manager:position-create'))
        self.assertNotEqual(response.status_code, 200)

    def test_task_type_update_required(self):
        url = reverse(
            "manager:position-update",
            kwargs={"pk": self.position.id},
        )
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PublicWorkerAccessTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position1")

        self.worker = Worker.objects.create(
            username="test_worker1",
            first_name="test1",
            last_name="worker1",
            password="q1a2z3w4",
            position=self.position,
        )

    def test_worker_list_login_required(self):
        response = self.client.get(reverse('manager:worker-list'))
        self.assertNotEqual(response.status_code, 200)

    def test_worker_create_login_required(self):
        response = self.client.get(reverse('manager:worker-create'))
        self.assertNotEqual(response.status_code, 200)

    def test_worker_update_required(self):
        url = reverse(
            "manager:worker-update",
            kwargs={"pk": self.worker.id},
        )
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_worker_detail_required(self):
        url = reverse(
            "manager:worker-detail",
            kwargs={"pk": self.worker.id},
        )
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_worker_delete_required(self):
        url = reverse(
            "manager:worker-delete",
            kwargs={"pk": self.worker.id},
        )
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PublicTaskAccessTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(
            name="test_task_name"
        )
        self.task = Task.objects.create(
            name="test_task1",
            description="Task description 1",
            deadline=datetime.date.today(),
            priority=Task.Priority.LOW,
            task_type=self.task_type,
        )

    def test_task_list_login_required(self):
        response = self.client.get(reverse('manager:task-list'))
        self.assertNotEqual(response.status_code, 200)

    def test_task_create_login_required(self):
        response = self.client.get(reverse('manager:task-create'))
        self.assertNotEqual(response.status_code, 200)

    def test_task_update_required(self):
        url = reverse(
            "manager:task-update",
            kwargs={"pk": self.task.id},
        )
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_task_detail_required(self):
        url = reverse(
            "manager:task-detail",
            kwargs={"pk": self.task.id},
        )
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)

    def test_task_delete_required(self):
        url = reverse(
            "manager:task-delete",
            kwargs={"pk": self.task.id},
        )
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
