"""
AI-OS Bağlam Yöneticisi (Context Manager)
Yapay zekanın sistem durumunu (donanım, açık uygulamalar, kullanıcı kimliği)
anlık olarak bilmesini sağlayan dinamik bağlam üretici.
"""

from typing import Dict, Any
from .system_controller import SystemController
from .multi_user import MultiUserManager

class ContextManager:
    def __init__(self, system_controller: SystemController, user_manager: MultiUserManager):
        self.sys = system_controller
        self.users = user_manager

    def build_system_context(self) -> str:
        """Yapay zeka için anlık işletim sistemi durum bağlamı üretir."""
        metrics = self.sys.get_hardware_metrics()
        user_prof = self.users.get_current_user_profile() or {}
        username = user_prof.get("username", "live")
        role = user_prof.get("role", "developer")

        mem = metrics["memory"]
        disk = metrics["disk"]

        context = f"""Sen AI-OS (Yapay Zeka Destekli Taşınabilir İşletim Sistemi) Çekirdek Asistanısın.
Kullanıcı seninle geleneksel menüler yerine doğrudan konuşarak işletim sistemini yönetir.

SİSTEM VE ORTAM BİLGİLERİ:
- Aktif Kullanıcı: {username} (Rol: {role})
- RAM Durumu: %{mem['used_percent']} kullanılıyor ({mem['available_mb']} MB boş)
- CPU Yükü: %{metrics['cpu_percent']}
- Disk Alanı: %{disk['used_percent']} dolu ({disk['free_gb']} GB boş)
- Platform: {metrics['platform']} Live USB Server

GÖREVLERİN:
1. Kullanıcı film veya müzik istediğinde hangi platformu/aracı istediğini anla veya uygun oynatıcıyı aç.
2. Yazılım öğrenmek istediğinde onu interaktif ders ve görev moduna geçir.
3. Kod yazmak istediğinde çalışma alanını ve geliştirme araçlarını başlat.
4. Sistem ayarları (Wi-Fi, ses, parlaklık) istendiğinde komutları ve adımları net bir şekilde organize et.
5. Her zaman yardımcı, nazik, net ve doğrudan çözüme odaklı ol.
"""
        return context
