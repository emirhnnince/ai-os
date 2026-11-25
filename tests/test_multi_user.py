import unittest
import shutil
import os
from src.core.multi_user import MultiUserManager

class TestMultiUserManager(unittest.TestCase):
    def setUp(self):
        self.test_root = "data/test_users"
        self.manager = MultiUserManager(data_root=self.test_root)

    def tearDown(self):
        if os.path.exists(self.test_root):
            shutil.rmtree(self.test_root)

    def test_create_and_auth_user(self):
        res = self.manager.create_user("ahmet", "parola123", display_name="Ahmet")
        self.assertTrue(res["success"])

        auth_res = self.manager.authenticate("ahmet", "parola123")
        self.assertTrue(auth_res["success"])
        self.assertEqual(auth_res["session"]["username"], "ahmet")

    def test_invalid_password(self):
        self.manager.create_user("mehmet", "dogru123")
        auth_res = self.manager.authenticate("mehmet", "yanlis123")
        self.assertFalse(auth_res["success"])

    def test_api_key_update(self):
        self.manager.create_user("testuser", "pass")
        self.manager.authenticate("testuser", "pass")
        self.manager.update_user_api_key("gemini", "AIzaSyTestKey123")
        prof = self.manager.get_current_user_profile()
        self.assertEqual(prof["api_keys"]["gemini"], "AIzaSyTestKey123")
