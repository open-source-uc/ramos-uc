from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from .tasks import collect_task, update_task, delete_task, banner_task
from background_task.models import Task
from .apps import BCScraperConfig
from apps.users.models import User


class ScraperTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser("admin", "admin@test.com", "admin")
        User.objects.create_user(
            "staff", email="staff@test.com", password="staff", is_staff=True
        )
        User.objects.create_user("normal", email="normal@test.com", password="normal")

    def test_management_commands(self):
        # python manage.py scrape <action> <period> [--banner str] [--initials str]
        # Just check that commands dont fail.
        call_command("scrape", ["collect", "2000-1"])
        call_command("scrape", ["update", "2000-1"])
        call_command("scrape", ["delete", "2000-1"])
        call_command("scrape", ["banner", "2000-1", "--banner", "1-5"])
        call_command("scrape", ["search", "2021-1", "--initials", "ing10"])

    def test_direct_task_scheduling(self):
        # Scheduling the task should create a corresponding Task model.
        app_name = BCScraperConfig.name
        task_name_fmt = f"{app_name}.tasks." + "{}"

        collect_task("2000-1", schedule=300)  # run task in 300 seconds
        self.assertTrue(
            Task.objects.get(task_name=task_name_fmt.format("collect_task"))
        )

        update_task("2000-1", schedule=300)
        self.assertTrue(Task.objects.get(task_name=task_name_fmt.format("update_task")))

        delete_task("2000-1", schedule=300)
        self.assertTrue(Task.objects.get(task_name=task_name_fmt.format("delete_task")))

        banner_task("2000-1", schedule=300)
        self.assertTrue(Task.objects.get(task_name=task_name_fmt.format("banner_task")))

    def test_only_staff_schedule_view(self):
        # Users without staff privileges should receive redirection or forbidden
        res = self.client.get(reverse("scraper:schedule"))
        self.assertIn(res.status_code, [302, 403])

        self.client.login(username="normal", password="normal")
        res = self.client.get(reverse("scraper:schedule"))
        self.assertIn(res.status_code, [302, 403])
        self.client.logout()

        # Staff users should receive succesful
        self.client.login(username="admin", password="admin")
        res = self.client.get(reverse("scraper:schedule"))
        self.assertEqual(res.status_code, 200)
        self.client.logout()

        self.client.login(username="staff", password="staff")
        res = self.client.get(reverse("scraper:schedule"))
        self.assertEqual(res.status_code, 200)
        self.client.logout()

    def test_schedule_view_creates_task(self):
        # POST to schedule view should create a corresponding Task
        app_name = BCScraperConfig.name
        task_name_fmt = f"{app_name}.tasks." + "{}"
        self.client.login(username="staff", password="staff")

        res = self.client.post(
            reverse("scraper:schedule"),
            {
                "action": "collect",
                "period": "2000-1",
                "time": "2000-01-31T12:00",
            },
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            Task.objects.get(task_name=task_name_fmt.format("collect_task"))
        )

        res = self.client.post(
            reverse("scraper:schedule"),
            {
                "action": "update",
                "period": "2000-1",
                "time": "2000-01-31T12:00",
            },
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Task.objects.get(task_name=task_name_fmt.format("update_task")))

        res = self.client.post(
            reverse("scraper:schedule"),
            {
                "action": "delete",
                "period": "2000-1",
                "time": "2000-01-31T12:00",
            },
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Task.objects.get(task_name=task_name_fmt.format("delete_task")))

        res = self.client.post(
            reverse("scraper:schedule"),
            {
                "action": "banner",
                "period": "2000-1",
                "banner": "1-5",
                "time": "2000-01-31T12:00",
            },
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Task.objects.get(task_name=task_name_fmt.format("banner_task")))

        self.client.logout()
