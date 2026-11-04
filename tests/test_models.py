import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.models import TaskType, Position, Task


class TaskTypeModelTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(
            name="test_type1",
        )

    def test_task_type_max_length(self):
        name_max_length = self.task_type._meta.get_field(
            "name"
        ).max_length

        self.assertEqual(255, name_max_length)

    def test_task_type_str(self):
        self.assertEqual(
            self.task_type.name,
            str(self.task_type)
        )

    def test_task_type_ordering(self):
        TaskType.objects.create(name="test_type3")
        TaskType.objects.create(name="test_type2")

        task_type = TaskType.objects.all()

        self.assertEqual(
            ["test_type1", "test_type2", "test_type3"],
            list(task_type.values_list("name", flat=True))
        )


class PositionModelTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="test_position1",
        )

    def test_position_max_length(self):
        name_max_length = self.position._meta.get_field(
            "name"
        ).max_length

        self.assertEqual(255, name_max_length)

    def test_position_str(self):
        self.assertEqual(
            self.position.name,
            str(self.position)
        )

    def test_position_ordering(self):
        Position.objects.create(name="test_position3")
        Position.objects.create(name="test_position2")

        position = Position.objects.all()

        self.assertEqual(
            ["test_position1", "test_position2", "test_position3"],
            list(position.values_list("name", flat=True))
        )


class WorkerModelTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="test_position"
        )
        self.worker = get_user_model().objects.create_user(
            username="test_user1",
            first_name="test1",
            last_name="user1",
            password="q1a2z3w4",
            position=self.position,
        )

    def test_verbose_name(self):
        self.assertEqual("worker", self.worker._meta.verbose_name)
        self.assertEqual("workers", self.worker._meta.verbose_name_plural)

    def test_worker_str(self):
        self.assertEqual(
            f"{self.worker.first_name} {self.worker.last_name}",
            str(self.worker)
        )

    def test_get_absolute_url(self):
        self.assertEqual("/workers/1/", self.worker.get_absolute_url())

    def test_worker_ordering(self):
        get_user_model().objects.create_user(
            username="test_user3",
            first_name="test3",
            last_name="user3",
            password="q1a2z3w4",
            position=self.position,
        )
        get_user_model().objects.create_user(
            username="test_user2",
            first_name="test2",
            last_name="user2",
            password="q1a2z3w4",
            position=self.position,
        )

        workers = get_user_model().objects.all()

        self.assertEqual(
            ["test_user1", "test_user2", "test_user3"],
            list(workers.values_list("username", flat=True))
        )


class TaskModelTests(TestCase):
    def setUp(self):
        position = Position.objects.create(
            name="test_position"
        )
        self.worker = get_user_model().objects.create_user(
            username="test_user1",
            first_name="test1",
            last_name="user1",
            password="q1a2z3w4",
            position=position,
        )

        self.task_type = TaskType.objects.create(
            name="test_type1",
        )

        self.task = Task.objects.create(
            name="test_task1",
            description="Task description 1",
            deadline=datetime.date.today(),
            priority=Task.Priority.LOW,
            task_type=self.task_type,
        )

    def test_task_str(self):
        self.assertEqual(
            self.task.name,
            str(self.task)
        )

    def test_task_ordering(self):
        Task.objects.create(
            name="test_task3",
            description="Task description 3",
            deadline=datetime.date.today(),
            priority=Task.Priority.LOW,
            task_type=self.task_type,
        )
        Task.objects.create(
            name="test_task2",
            description="Task description 2",
            deadline=datetime.date.today(),
            priority=Task.Priority.LOW,
            task_type=self.task_type,
        )

        task = Task.objects.all()

        self.assertEqual(
            ["test_task1", "test_task2", "test_task3"],
            list(task.values_list("name", flat=True))
        )

    def test_get_absolute_url(self):
        self.assertEqual("/tasks/1/", self.task.get_absolute_url())

    def test_priority_color(self):
        expected_colors = {
            Task.Priority.URGENT: "danger",
            Task.Priority.HIGH: "warning",
            Task.Priority.MEDIUM: "info",
            Task.Priority.LOW: "success",
        }

        for priority, color in expected_colors.items():
            self.task.priority = priority
            self.assertEqual(self.task.priority_color, color)

    def test_priority_color_fallback(self):
        self.task.priority = "UNKNOWN"
        self.assertEqual(self.task.priority_color, "secondary")

    def test_task_type_relationship(self):
        self.assertEqual(self.task.task_type, self.task_type)

    def test_worker_relationship(self):
        self.task.assignees.add(self.worker)
        self.assertIn(self.worker, self.task.assignees.all())
        self.assertIn(self.task, self.worker.tasks.all())
