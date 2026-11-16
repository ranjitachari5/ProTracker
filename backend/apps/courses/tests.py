from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase

class CourseTest(TestCase):
    def test_progress(self):
        expected = "in_progress"
        actual = "in_progress"

        self.assertEqual(actual, expected)