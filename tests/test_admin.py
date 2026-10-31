from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Position


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
