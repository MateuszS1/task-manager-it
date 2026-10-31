import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Position, Task, TaskType


class PrivateTaskTypeTemplateTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_position1")

        self.user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=self.position,
        )
        self.client.force_login(self.user)

        self.task_type = TaskType.objects.create(name="test_type1")

    def test_task_type_list_response(self):
        response = self.client.get(reverse('manager:task-type-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_type_list.html")

    def test_task_type_create_response(self):
        response = self.client.get(reverse('manager:task-type-create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_type_form.html")

    def test_task_type_update_response(self):
        url = reverse(
            "manager:task-type-update",
            kwargs={"pk": self.task_type.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_type_form.html")


class PrivatePositionTemplateTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_position1")

        self.user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=self.position,
        )
        self.client.force_login(self.user)

    def test_position_list_response(self):
        response = self.client.get(reverse('manager:position-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/position_list.html")

    def test_position_create_response(self):
        response = self.client.get(reverse('manager:position-create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/position_form.html")

    def test_position_update_response(self):
        url = reverse(
            "manager:position-update",
            kwargs={"pk": self.position.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/position_form.html")


class PrivateWorkerTemplateTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_position1")

        self.user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=self.position,
        )
        self.client.force_login(self.user)

    def test_worker_list_response(self):
        response = self.client.get(reverse('manager:worker-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/worker_list.html")

    def test_worker_detail_response(self):
        url = reverse(
            "manager:worker-detail",
            kwargs={"pk": self.user.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/worker_detail.html")

    def test_worker_create_response(self):
        response = self.client.get(reverse('manager:worker-create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/worker_form.html")

    def test_worker_update_response(self):
        url = reverse(
            "manager:worker-update",
            kwargs={"pk": self.user.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/worker_form.html")


class PrivateTaskTemplateTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="test_position1")

        self.user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=self.position,
        )
        self.client.force_login(self.user)

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

    def test_task_list_response(self):
        response = self.client.get(reverse('manager:task-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_list.html")

    def test_task_detail_response(self):
        url = reverse(
            "manager:task-detail",
            kwargs={"pk": self.task.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_detail.html")

    def test_task_create_response(self):
        response = self.client.get(reverse('manager:task-create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_form.html")

    def test_task_update_data_response(self):
        url = reverse(
            "manager:task-update",
            kwargs={"pk": self.task.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_form.html")

    def test_task_update_assignees_response(self):
        url = reverse(
            "manager:task-assign",
            kwargs={"pk": self.task.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/task_form.html")
