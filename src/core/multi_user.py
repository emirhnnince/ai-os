"""
AI-OS Çok Kullanıcılı Profil ve Oturum Yöneticisi (Multi-User Manager)
USB bellekte her kullanıcı için bağımsız şifrelenmiş profiller,
bireysel API anahtarları, kişiselleştirilmiş AI hafızası ve oturumları yönetir.
"""

import os
import json
import hashlib
import uuid
from typing import Dict, Any, Optional, List

class MultiUserManager:
    def __init__(self, data_root: str = "data/users"):
        self.data_root = data_root
        os.makedirs(self.data_root, exist_ok=True)
        self.active_session: Optional[Dict[str, Any]] = None
        self._ensure_default_user()

    def _hash_password(self, password: str, salt: Optional[str] = None) -> (str, str):
        if not salt:
            salt = uuid.uuid4().hex
        hashed = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
        return hashed, salt

    def _user_dir(self, username: str) -> str:
        return os.path.join(self.data_root, username)

    def _profile_path(self, username: str) -> str:
        return os.path.join(self._user_dir(username), "profile.json")

    def _ensure_default_user(self):
        """İlk açılışta varsayılan demo/live kullanıcısını tanımlar."""
        users = self.list_users()
        if not users:
            self.create_user("live", "live", display_name="AI-OS Misafir / Demo")

    def create_user(self, username: str, password: str, display_name: str = "") -> Dict[str, Any]:
        """Yeni bir izole kullanıcı profili oluşturur."""
        username = username.strip().lower()
        udir = self._user_dir(username)
        if os.path.exists(udir):
            return {"success": False, "message": "Bu kullanıcı adı zaten mevcut."}

        os.makedirs(udir, exist_ok=True)
        os.makedirs(os.path.join(udir, "workspace"), exist_ok=True)
        os.makedirs(os.path.join(udir, "history"), exist_ok=True)

        hashed, salt = self._hash_password(password)
        profile = {
            "username": username,
            "display_name": display_name or username.capitalize(),
            "password_hash": hashed,
            "salt": salt,
            "role": "developer",
            "api_keys": {
                "gemini": "",
                "openai": "",
                "anthropic": ""
            },
            "preferences": {
                "theme": "dark_modern",
                "default_ai": "gemini",
                "learning_level": "beginner"
            },
            "learning_progress": {
                "active_course": "py101",
                "completed_steps": 0,
                "badges": []
            }
        }

        with open(self._profile_path(username), "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=4, ensure_ascii=False)

        return {"success": True, "username": username, "message": "Kullanıcı profili oluşturuldu."}

    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """Kullanıcı girişi yapar ve oturum başlatır."""
        username = username.strip().lower()
        ppath = self._profile_path(username)
        if not os.path.exists(ppath):
            return {"success": False, "message": "Kullanıcı bulunamadı."}

        with open(ppath, "r", encoding="utf-8") as f:
            profile = json.load(f)

        hashed, _ = self._hash_password(password, profile["salt"])
        if hashed == profile["password_hash"]:
            token = uuid.uuid4().hex
            self.active_session = {
                "token": token,
                "username": username,
                "display_name": profile["display_name"],
                "role": profile["role"],
                "workspace_path": os.path.join(self._user_dir(username), "workspace")
            }
            return {"success": True, "session": self.active_session}
        else:
            return {"success": False, "message": "Geçersiz parola."}

    def list_users(self) -> List[Dict[str, str]]:
        """Kayıtlı kullanıcı profillerini listeler."""
        users = []
        if os.path.exists(self.data_root):
            for entry in os.listdir(self.data_root):
                ppath = os.path.join(self.data_root, entry, "profile.json")
                if os.path.isfile(ppath):
                    try:
                        with open(ppath, "r", encoding="utf-8") as f:
                            p = json.load(f)
                            users.append({
                                "username": p["username"],
                                "display_name": p.get("display_name", p["username"])
                            })
                    except Exception:
                        pass
        return users

    def get_current_user_profile(self) -> Optional[Dict[str, Any]]:
        if not self.active_session:
            # Oturum açılmamışsa varsayılan olarak 'live' profilini yükle
            self.authenticate("live", "live")
        
        if self.active_session:
            ppath = self._profile_path(self.active_session["username"])
            if os.path.exists(ppath):
                with open(ppath, "r", encoding="utf-8") as f:
                    return json.load(f)
        return None

    def update_user_api_key(self, provider: str, key: str) -> bool:
        """Aktif kullanıcının API anahtarını güvenle günceller."""
        prof = self.get_current_user_profile()
        if not prof:
            return False
        prof["api_keys"][provider.lower()] = key
        ppath = self._profile_path(prof["username"])
        with open(ppath, "w", encoding="utf-8") as f:
            json.dump(prof, f, indent=4, ensure_ascii=False)
        return True
