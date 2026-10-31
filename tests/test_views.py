import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import TaskType, Position, Task


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position1")

        self.user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=self.position,
        )
        self.client.force_login(self.user)

    def test_create_position(self):
        self.assertEqual(Position.objects.get(id=1).name, "test_position1")

    def test_update_position(self):
        position = Position.objects.create(
            name="test_name1"
        )
        response = self.client.post(
            reverse(
                "manager:position-update", kwargs={"pk": position.id}
            ),
            {"name": "new_test_name1"},
        )
        Position.objects.get(id=position.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Position.objects.get(id=position.id).name, "new_test_name1"
        )

    def test_delete_position(self):
        position = Position.objects.create(
            name="test_name1"
        )
        response = self.client.post(
            reverse("manager:position-delete", kwargs={"pk": position.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Position.objects.filter(id=position.id).exists()
        )

    def test_position_list_paginated_correctly(self):
        for i in range(1, 7):
            Position.objects.create(name=f"test_name{i}")

        response = self.client.get(reverse('manager:position-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 5)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].num_pages, 2)


class PrivateTaskTypeTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position1")

        self.user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=self.position,
        )
        self.client.force_login(self.user)

    def test_create_task_type(self):
        response = self.client.post(
            reverse(
                "manager:task-type-create",
            ),
            {"name": "test_name1"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskType.objects.get(id=1).name, "test_name1")

    def test_update_task_type(self):
        task_type = TaskType.objects.create(
            name="test_name1"
        )
        response = self.client.post(
            reverse(
                "manager:task-type-update", kwargs={"pk": task_type.id}
            ),
            {"name": "new_test_name1"},
        )
        TaskType.objects.get(id=task_type.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            TaskType.objects.get(id=task_type.id).name, "new_test_name1"
        )

    def test_delete_task_type(self):
        task_type = TaskType.objects.create(
            name="test_name1"
        )
        response = self.client.post(
            reverse("manager:task-type-delete", kwargs={"pk": task_type.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            TaskType.objects.filter(id=task_type.id).exists()
        )

    def test_task_type_list_paginated_correctly(self):
        for i in range(1, 7):
            TaskType.objects.create(name=f"test_name{i}")

        response = self.client.get(reverse('manager:task-type-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 5)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].num_pages, 2)


class PrivateWorkerTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position1")

        self.user = get_user_model().objects.create_user(
            username="test_user",
            first_name="test",
            last_name="user",
            password="q1a2z3w4",
            position=self.position,
        )
        self.client.force_login(self.user)

        self.worker = get_user_model().objects.create(
            username="test_worker1",
            first_name="test1",
            last_name="worker1",
            password="q1a2z3w4",
            position=self.position,
        )

    def test_create_worker(self):
        response = self.client.post(
            reverse("manager:worker-create"),
            {
                "username": "test_worker2",
                "first_name": "test2",
                "last_name": "worker2",
                "password1": "q1a2z3w4",
                "password2": "q1a2z3w4",
                "position": self.position.id,
            },
        )
        self.assertEqual(response.status_code, 302)

        worker = get_user_model().objects.get(username="test_worker2")

        self.assertEqual(worker.username, "test_worker2")
        self.assertEqual(worker.first_name, "test2")
        self.assertEqual(worker.last_name, "worker2")
        self.assertTrue((worker.check_password("q1a2z3w4")))
        self.assertEqual(worker.position.name, "test_position1")

    def test_update_worker(self):
        new_position = Position.objects.create(name="test_position2")

        response = self.client.post(
            reverse("manager:worker-update", kwargs={"pk": self.worker.id}),
            {
                "pk": self.worker.id,
                "position": new_position.id,
            },
        )
        get_user_model().objects.get(id=self.worker.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            get_user_model().objects.get(id=self.worker.id).position.name,
            "test_position2"
        )

    def test_update_user(self):
        new_position = Position.objects.create(name="test_position2")

        response = self.client.post(
            reverse("manager:worker-update", kwargs={"pk": self.user.id}),
            {
                "pk": self.user.id,
                "username": "test_user2",
                "first_name": "test2",
                "last_name": "user2",
                "email": "test@test.com",
                "position": new_position.id,
            },
        )

        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "test_user2")
        self.assertEqual(self.user.first_name, "test2")
        self.assertEqual(self.user.last_name, "user2")
        self.assertEqual(self.user.email, "test@test.com")
        self.assertEqual(self.user.position.name, "test_position2")

    def test_delete_task(self):
        response = self.client.post(
            reverse("manager:worker-delete", kwargs={"pk": self.worker.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.worker.id).exists())

    def test_worker_list_paginated_correctly(self):
        for i in range(2, 7):
            get_user_model().objects.create(
                username=f"test_worker{i}",
                first_name=f"test{i}",
                last_name=f"worker{i}",
                password="q1a2z3w4",
                position=self.position,
            )

        response = self.client.get(reverse('manager:worker-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 5)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].num_pages, 2)

    def test_worker_detail_tasks_paginated_correctly(self):
        task_type = TaskType.objects.create(
            name="test_task_name"
        )
        tasks = [
            Task.objects.create(
                name=f"test_task{i}",
                description=f"Task description {i}",
                deadline=datetime.date.today(),
                priority=Task.Priority.LOW,
                task_type=task_type,
            )
            for i in range(1, 6)
        ]

        self.user.tasks.set(tasks)

        url = reverse(
            "manager:worker-detail",
            kwargs={"pk": self.user.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 4)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].num_pages, 2)


class PrivateTaskTest(TestCase):
    def setUp(self) -> None:
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

    def test_create_task(self):
        response = self.client.post(
            reverse("manager:task-create"),
            {
                "name": "test_task2",
                "description": "Task description",
                "deadline": datetime.date.today(),
                "priority": Task.Priority.LOW,
                "task_type": self.task_type.id,
            },
        )
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(name="test_task2")

        self.assertEqual(task.name, "test_task2")
        self.assertEqual(task.description, "Task description")
        self.assertEqual(task.deadline, datetime.date.today())
        self.assertEqual(task.priority, Task.Priority.LOW)
        self.assertEqual(task.task_type, self.task_type)
        self.assertFalse(task.is_completed)
        self.assertEqual(task.assignees.count(), 0)

    def test_update_task_status(self):
        response = self.client.post(
            reverse("manager:task-update", kwargs={"pk": self.task.id}),
            {
                "pk": self.task.id,
                "is_completed": True,
            },
        )
        Task.objects.get(id=self.task.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.get(id=self.task.id).is_completed, True)

    def test_update_task_assignees(self):
        self.task.assignees.add(self.user.id)

        worker1 = get_user_model().objects.create_user(
            username="test_worker1",
            first_name="test1",
            last_name="worker1",
            password="q1a2z3w4",
            position=Position.objects.get(name="test_position1"),
        )
        worker2 = get_user_model().objects.create_user(
            username="test_worker2",
            first_name="test2",
            last_name="worker2",
            password="q1a2z3w4",
            position=Position.objects.get(name="test_position1"),
        )

        response = self.client.post(
            reverse("manager:task-assign", kwargs={"pk": self.task.id}),
            {
                "pk": self.task.id,
                "assignees": [worker1.id, worker2.id],
            },
        )

        Task.objects.get(id=self.task.id).refresh_from_db()
        self.assertEqual(
            response.status_code,
            302
        )
        self.assertEqual(
            Task.objects.get(id=self.task.id).assignees.count(),
            2
        )
        self.assertEqual(
            Task.objects.get(id=self.task.id).assignees.get(
                username="test_worker1"
            ).first_name,
            "test1"
        )
        self.assertEqual(
            Task.objects.get(id=self.task.id).assignees.get(
                username="test_worker1"
            ).last_name,
            "worker1"
        )
        self.assertEqual(
            Task.objects.get(id=self.task.id).assignees.get(
                username="test_worker2"
            ).first_name,
            "test2"
        )
        self.assertEqual(
            Task.objects.get(id=self.task.id).assignees.get(
                username="test_worker2"
            ).last_name,
            "worker2"
        )

    def test_delete_task(self):
        response = self.client.post(
            reverse("manager:task-delete", kwargs={"pk": self.task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_list_paginated_correctly(self):
        for i in range(2, 7):
            Task.objects.create(
                name=f"test_task{i}",
                description=f"Task description {i}",
                deadline=datetime.date.today(),
                priority=Task.Priority.LOW,
                task_type=self.task_type,
            )

        response = self.client.get(reverse('manager:task-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 5)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].num_pages, 2)

    def test_task_detail_tasks_paginated_correctly(self):
        position = Position.objects.create(
            name="test_position"
        )

        assignees = [
            get_user_model().objects.create(
                username=f"test_worker{i}",
                first_name=f"test{i}",
                last_name=f"worker{i}",
                password="q1a2z3w4",
                position=position,
            )
            for i in range(1, 7)
        ]

        self.task.assignees.set(assignees)

        url = reverse(
            "manager:task-detail",
            kwargs={"pk": self.user.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 5)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(response.context["paginator"].num_pages, 2)
