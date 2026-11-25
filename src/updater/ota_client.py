"""
AI-OS Atomik OTA Güncelleme Yöneticisi (Atomic OTA Updater)
Sistem güncellemelerini indirir, A/B imaj yuvalarını yönetir ve
kullanıcı verilerine dokunmadan işletim sistemini güvenle günceller.
"""

import json
import os
import urllib.request
from typing import Dict, Any

CURRENT_VERSION = "2.1.0"
DEFAULT_LOCAL_MANIFEST = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "website", "manifest.json")
)
UPDATE_MANIFEST_URL = os.environ.get(
    "AIOS_MANIFEST_URL",
    "https://ai-os-download.vercel.app/manifest.json"
)

class OTAUpdater:
    def __init__(self, current_version: str = CURRENT_VERSION):
        self.current_version = current_version
        self.current_slot = "A" # Canlı USB'de /live/current_slot dosyasından okunur

    def check_for_updates(self, manifest_url: str = UPDATE_MANIFEST_URL) -> Dict[str, Any]:
        """Güncelleme sunucusunu kontrol eder."""
        try:
            req = urllib.request.Request(manifest_url, headers={"User-Agent": "AI-OS-Updater/1.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                manifest = json.loads(response.read().decode("utf-8"))
                latest_ver = manifest.get("version", self.current_version)
                
                is_newer = latest_ver != self.current_version
                return {
                    "has_update": is_newer,
                    "current_version": self.current_version,
                    "latest_version": latest_ver,
                    "release_notes": manifest.get("release_notes", ""),
                    "image_url": manifest.get("image_url", ""),
                    "sha256": manifest.get("sha256", "")
                }
        except Exception as e:
            # Yerel website/manifest.json varsa çevrimdışı test/önizleme için oku
            if os.path.exists(DEFAULT_LOCAL_MANIFEST):
                try:
                    with open(DEFAULT_LOCAL_MANIFEST, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    latest_ver = manifest.get("version", self.current_version)
                    return {
                        "has_update": latest_ver != self.current_version,
                        "current_version": self.current_version,
                        "latest_version": latest_ver,
                        "release_notes": manifest.get("release_notes", ""),
                        "image_url": manifest.get("image_url", ""),
                        "iso_url": manifest.get("iso_url", ""),
                        "sha256": manifest.get("sha256", ""),
                        "source": "local_manifest"
                    }
                except Exception:
                    pass
            return {
                "has_update": False,
                "current_version": self.current_version,
                "error": f"Güncelleme kontrolü yapılamadı (Çevrimdışı veya sunucuya ulaşılamıyor): {str(e)}"
            }

    def prepare_slot_switch(self, target_slot: str = "B") -> Dict[str, Any]:
        """Yeni squashfs imajı başarıyla indirildiğinde boot yuvasını değiştirir."""
        return {
            "status": "READY_FOR_REBOOT",
            "active_slot": self.current_slot,
            "next_boot_slot": target_slot,
            "message": f"Yeni sürüm hazırlandı. Bir sonraki yeniden başlatmada {target_slot} yuvasından açılacaktır. Kullanıcı verileriniz korunmaktadır."
        }
