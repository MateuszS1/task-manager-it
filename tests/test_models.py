from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.models import TaskType, Position


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
            username="test_user",
            first_name="test",
            last_name="user",
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
