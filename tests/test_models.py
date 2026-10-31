from django.test import TestCase

from manager.models import TaskType, Position


class TaskTypeModelTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(
            name="test_type1",
        )

    def test_manufacturer_max_length(self):
        name_max_length = self.task_type._meta.get_field(
            "name"
        ).max_length

        self.assertEqual(255, name_max_length)

    def test_manufacturer_str(self):
        self.assertEqual(
            self.task_type.name,
            str(self.task_type)
        )

    def test_manufacturer_ordering(self):
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

    def test_manufacturer_max_length(self):
        name_max_length = self.position._meta.get_field(
            "name"
        ).max_length

        self.assertEqual(255, name_max_length)

    def test_manufacturer_str(self):
        self.assertEqual(
            self.position.name,
            str(self.position)
        )

    def test_manufacturer_ordering(self):
        Position.objects.create(name="test_position3")
        Position.objects.create(name="test_position2")

        position = Position.objects.all()

        self.assertEqual(
            ["test_position1", "test_position2", "test_position3"],
            list(position.values_list("name", flat=True))
        )
