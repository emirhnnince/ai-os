import unittest
from src.core.learning_engine import LearningEngine

class TestLearningEngine(unittest.TestCase):
    def setUp(self):
        self.engine = LearningEngine()

    def test_courses_available(self):
        courses = self.engine.list_available_courses()
        course_ids = [c["id"] for c in courses]
        self.assertIn("py101", course_ids)
        self.assertIn("linux101", course_ids)

    def test_code_evaluation_success(self):
        res = self.engine.evaluate_submission("py101", 0, "print('Merhaba AI-OS')")
        self.assertTrue(res["success"])

    def test_code_evaluation_fail(self):
        res = self.engine.evaluate_submission("py101", 0, "x = 5")
        self.assertFalse(res["success"])
        self.assertIn("hint", res)
