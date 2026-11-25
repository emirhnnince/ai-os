"""
AI-OS İlk Kurulum ve Çok Kullanıcılı Hesap Yöneticisi (OOBE & Identity Manager)
Canlı USB ilk boot edildiğinde veya yeni profil eklenirken çalışır:
- Misafir Girişi (Sıfır iz bırakan hızlı başlangıç)
- AI-OS Yerel Şifreli Hesap (Kalıcı alan, PIN, çalışma alanı)
- Google Hesabı ile Giriş (Google AI Studio Gemini API entegrasyonu)
"""

import os
import json
from typing import Dict, Any, Optional

class OnboardingManager:
    def __init__(self, user_manager, config_path: str = "config/setup_state.json"):
        self.user_manager = user_manager
        self.config_path = config_path
        self.setup_state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "is_setup_completed": False,
            "active_mode": "guest", # guest, local, google
            "user_role": "developer", # developer, student, creator, general
            "selected_ai_engine": "gemini",
            "pin_enabled": False
        }

    def save_state(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.setup_state, f, indent=4, ensure_ascii=False)

    def complete_onboarding(self, setup_data: Dict[str, Any]) -> Dict[str, Any]:
        """Kullanıcının kurulum adımlarını tamamlayıp sistem profilini üretir."""
        mode = setup_data.get("mode", "guest")
        username = setup_data.get("username", "live")
        role = setup_data.get("role", "developer")
        ai_engine = setup_data.get("ai_engine", "gemini")
        api_key = setup_data.get("api_key", "")
        pin = setup_data.get("pin", "")

        # 1. Mod Yönetimi
        if mode == "guest":
            self.setup_state["active_mode"] = "guest"
            display_name = "Misafir Kullanıcı (İz Bırakmaz)"
        elif mode == "google":
            self.setup_state["active_mode"] = "google"
            display_name = setup_data.get("google_name", "Google Kullanıcısı")
            username = "google_user"
            self.user_manager.create_user(username, "google_oauth_pass", display_name=display_name)
        else: # local
            self.setup_state["active_mode"] = "local"
            display_name = setup_data.get("display_name", username.capitalize())
            password = setup_data.get("password", pin or "aios123")
            self.user_manager.create_user(username, password, display_name=display_name)

        # 2. API Anahtarını Kaydet
        if api_key:
            self.user_manager.update_user_api_key(ai_engine, api_key)

        self.setup_state["is_setup_completed"] = True
        self.setup_state["user_role"] = role
        self.setup_state["selected_ai_engine"] = ai_engine
        self.setup_state["pin_enabled"] = bool(pin)
        self.save_state()

        return {
            "success": True,
            "message": f"AI-OS kurulumu başarıyla tamamlandı. Oturum açıldı: {display_name}",
            "mode": mode,
            "username": username,
            "display_name": display_name
        }

    def get_setup_status(self) -> Dict[str, Any]:
        return self.setup_state
