import unittest
import os
from src.updater.ota_manager import OTAManager

class TestOTAManager(unittest.TestCase):
    def setUp(self):
        self.slot_file = "data/test_current_slot"
        self.manager = OTAManager(slot_file=self.slot_file)

    def tearDown(self):
        if os.path.exists(self.slot_file):
            os.remove(self.slot_file)

    def test_slot_switching(self):
        # Varsayılan A olmalı
        self.assertEqual(self.manager.get_active_slot(), "A")
        self.assertEqual(self.manager.get_inactive_slot(), "B")

        # B'ye geçir
        self.manager.apply_update_slot("B")
        self.assertEqual(self.manager.get_active_slot(), "B")
        self.assertEqual(self.manager.get_inactive_slot(), "A")
