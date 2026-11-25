import unittest
from src.core.system_controller import SystemController

class TestSystemController(unittest.TestCase):
    def setUp(self):
        self.ctrl = SystemController()

    def test_get_metrics(self):
        metrics = self.ctrl.get_hardware_metrics()
        self.assertIn("cpu_percent", metrics)
        self.assertIn("memory", metrics)
        self.assertIn("disk", metrics)
        self.assertGreater(metrics["memory"]["total_mb"], 0)

    def test_safe_command_blocking(self):
        res = self.ctrl.execute_safe_command("rm -rf /")
        self.assertFalse(res["success"])
        self.assertIn("Güvenlik kısıtlaması", res["error"])
