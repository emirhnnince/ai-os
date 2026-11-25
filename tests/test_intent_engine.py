import unittest
from src.core.intent_engine import IntentEngine
from src.core.ai_gateway import AIGateway

class TestIntentEngine(unittest.TestCase):
    def setUp(self):
        self.gateway = AIGateway()
        self.engine = IntentEngine(self.gateway)

    def test_media_intent_detection(self):
        res = self.engine.parse_and_execute("Bir film izlemek istiyorum")
        self.assertEqual(res["type"], "MEDIA_INTENT")
        self.assertIn("YouTube", [opt["label"] for opt in res["options"]])

    def test_media_entity_extraction(self):
        res = self.engine.parse_and_execute("Inception filmini izlemek istiyorum")
        self.assertEqual(res["type"], "MEDIA_INTENT")
        self.assertEqual(res["detected_query"], "inception")

    def test_learning_intent_detection(self):
        res = self.engine.parse_and_execute("Python öğrenmek istiyorum")
        self.assertEqual(res["type"], "LEARNING_INTENT")
        self.assertIn("py101", [opt["course_id"] for opt in res["options"]])

    def test_dev_intent_detection(self):
        res = self.engine.parse_and_execute("Bana kod yazmak için ide aç")
        self.assertEqual(res["type"], "DEV_INTENT")
