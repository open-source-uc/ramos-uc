from django.test import TestCase
from django.urls import reverse
from .models import Course, Section, FullSchedule


class CoursesRoutesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        course1 = Course.objects.create(
            initials="ING1001", name="Practica I", credits=0
        )
        Course.objects.create(initials="BIO141C", name="Biocel", credits=10)
        Course.objects.create(initials="ABC001", name="Genérico 1", credits=10)
        Course.objects.create(initials="ABC002", name="Genérico 2", credits=10)
        Course.objects.create(initials="ABC003", name="Genérico 3", credits=10)
        Course.objects.create(initials="ABC004", name="Genérico 4", credits=10)
        Course.objects.create(initials="ABC005", name="Genérico 5", credits=10)
        Course.objects.create(initials="ABC006", name="Genérico 6", credits=10)
        Course.objects.create(initials="ABC007", name="Genérico 7", credits=80)

        section1 = Section.objects.create(
            course=course1,
            period="2021-1",
            section=1,
            nrc=12345,
            teachers="Profesor Apellido",
            schedule=":",
            format="Online",
            campus="Casa Central",
            is_english=False,
            is_removable=True,
            is_special=False,
            available_quota=10,
            total_quota=20,
        )

        FullSchedule.objects.create(section=section1)

    def test_index_response_succesful(self):
        res = self.client.get(reverse("courses:index"))
        self.assertEqual(res.status_code, 200)

    def test_share_response_succesful(self):
        res = self.client.get(reverse("courses:share"), {"ids": "1,2,3,8,1000000"})
        self.assertEqual(res.status_code, 200)

        res = self.client.get(reverse("courses:share"))
        self.assertEqual(res.status_code, 200)

    def test_planner_response_succesful(self):
        res = self.client.get(reverse("courses:planner"))
        self.assertEqual(res.status_code, 200)

    def test_browse_response_succesful(self):
        res = self.client.get(reverse("courses:browse"))
        self.assertEqual(res.status_code, 200)

        res = self.client.get(
            reverse("courses:browse"),
            {
                "escuela": "Ingeniería",
                "page": 1,
            },
        )
        self.assertEqual(res.status_code, 200)

        res = self.client.get(
            reverse("courses:browse"),
            {
                "escuela": "Ingeniería",
                "page": 1000,  # Out of range page
            },
        )
        self.assertNotEqual(res.status_code, 500)

    def test_search_response_succesful(self):
        res = self.client.get(reverse("courses:search"))
        self.assertEqual(res.status_code, 200)

        res = self.client.get(reverse("courses:search"), {"q": "ing1001"})
        self.assertEqual(res.status_code, 200)

        res = self.client.get(reverse("courses:search"), {"q": "nombre del ramo"})
        self.assertEqual(res.status_code, 200)

    def test_course_response_succesful_with_name_and_initials(self):
        for c in Course.objects.all():
            res = self.client.get(
                reverse("courses:course", kwargs={"initials": c.initials})
            )
            self.assertEqual(res.status_code, 200)
            self.assertContains(res, c.initials)
            self.assertContains(res, c.name)

        res = self.client.get(reverse("courses:course", kwargs={"initials": "NOT000"}))
        self.assertEqual(res.status_code, 404)

    def test_p_search_response_is_json(self):
        res = self.client.get(reverse("courses:p_search"))
        self.assertJSONNotEqual(str(res.content, encoding="utf-8"), {})

    def test_detail_response_is_json(self):
        res = self.client.get(reverse("courses:p_detail", args=[999]))
        self.assertJSONNotEqual(str(res.content, encoding="utf-8"), {})

        res = self.client.get(reverse("courses:p_detail", args=[1]))
        self.assertJSONNotEqual(str(res.content, encoding="utf-8"), {})

    def test_schedule_response_is_json(self):
        res = self.client.get(reverse("courses:p_schedule", args=[999]))
        self.assertJSONNotEqual(str(res.content, encoding="utf-8"), {})

        res = self.client.get(reverse("courses:p_schedule", args=[1]))
        self.assertJSONNotEqual(str(res.content, encoding="utf-8"), {})

    def test_banner_response_is_json(self):
        res = self.client.get(reverse("courses:banner", args=[999]))
        self.assertJSONNotEqual(str(res.content, encoding="utf-8"), {})

        res = self.client.get(reverse("courses:banner", args=[1]))
        self.assertJSONNotEqual(str(res.content, encoding="utf-8"), {})
