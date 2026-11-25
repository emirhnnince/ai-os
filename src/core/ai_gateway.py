"""
AI-OS Hibrit Yapay Zeka Ağ Geçidi (AI Gateway - Gelişmiş Sürüm)
Çevrimdışı iken yerel GGUF SLM modelini (OfflineSLMManager),
Çevrimiçi iken Google Gemini 2.0 / 1.5 Flash veya OpenAI API'lerini yönetir.
Aktif kullanıcı profiline göre API anahtarlarını otomatik çözer.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from .network_detector import NetworkDetector
from .offline_slm import OfflineSLMManager
from .multi_user import MultiUserManager

class AIGateway:
    def __init__(self, user_manager: Optional[MultiUserManager] = None):
        self.network = NetworkDetector()
        self.users = user_manager or MultiUserManager()
        self.offline_slm = OfflineSLMManager()

    def get_api_key(self, provider: str = "gemini") -> str:
        """Kullanıcı profilinden veya çevre değişkenlerinden API anahtarını çeker."""
        prof = self.users.get_current_user_profile()
        if prof and "api_keys" in prof:
            key = prof["api_keys"].get(provider.lower(), "")
            if key:
                return key
        
        # Çevre değişkeni yedeği
        env_map = {
            "gemini": "GEMINI_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY"
        }
        return os.environ.get(env_map.get(provider.lower(), ""), "")

    def route_query(self, prompt: str, system_context: Optional[str] = None) -> Dict[str, Any]:
        """Gelen isteği ağ ve yapılandırma durumuna göre yönlendirir."""
        is_online = self.network.is_connected()
        gemini_key = self.get_api_key("gemini")

        # 1. Öncelik: Çevrimiçi ve Gemini Anahtarı Tanımlı
        if is_online and gemini_key:
            return self._call_gemini(prompt, system_context, gemini_key)
        
        # 2. Durum: Çevrimiçi ama Anahtar Yok -> Kullanıcıya Kurulum Rehberi Sun
        elif is_online and not gemini_key:
            return {
                "mode": "ONLINE_NEEDS_KEY",
                "provider": "Google Gemini (Kurulum Bekliyor)",
                "text": (
                    "İnternet bağlantısı tespit edildi! Üstün zeka moduna geçmek için ücretsiz Gemini API anahtarınızı tanımlayabilirsiniz.\n"
                    "Adım adım rehber için 'kurulum' yazabilir veya ayarlar panelini açabilirsiniz."
                ),
                "trigger_onboarding": True
            }
        
        # 3. Durum: Çevrimdışı Mod (İnternet Yok)
        else:
            return self._call_offline_slm(prompt, system_context)

    def _call_gemini(self, prompt: str, system_context: Optional[str], api_key: str) -> Dict[str, Any]:
        """Google Gemini 2.0 Flash REST API çağrısı."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        contents = []
        if system_context:
            contents.append({"role": "user", "parts": [{"text": f"[System Context]\n{system_context}"}]})
            contents.append({"role": "model", "parts": [{"text": "Anlaşıldı. AI-OS sistem çekirdeği olarak kullanıcının niyetlerini yerine getirmeye hazırım."}]})

        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048
            }
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "mode": "ONLINE_GEMINI",
                    "provider": "Google Gemini 2.0 Flash",
                    "text": text,
                    "success": True
                }
        except urllib.error.HTTPError as http_err:
            # API Anahtarı geçersizliği veya kota aşımında yerel modele dön
            offline_fallback = self._call_offline_slm(prompt, system_context)
            offline_fallback["warning"] = f"Gemini API hatası ({http_err.code}), yerel modele geri düşüldü."
            return offline_fallback
        except Exception as e:
            offline_fallback = self._call_offline_slm(prompt, system_context)
            offline_fallback["warning"] = f"Bağlantı hatası ({str(e)}), yerel model devrede."
            return offline_fallback

    def _call_offline_slm(self, prompt: str, system_context: Optional[str]) -> Dict[str, Any]:
        """Yerel internetsiz yapay zeka sorgulaması."""
        res = self.offline_slm.query_local_model(prompt, system_context)
        return {
            "mode": "OFFLINE_LOCAL",
            "provider": res.get("engine", "Offline SLM"),
            "text": res.get("text", ""),
            "success": True
        }
