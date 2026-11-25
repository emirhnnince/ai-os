"""
AI-OS Ağ ve İnternet Durumu Algılayıcı
Sistemin çevrimdışı (offline) mı yoksa çevrimiçi (online) mı olduğunu milisaniyeler içinde kontrol eder.
"""

import socket
import urllib.request
from typing import Tuple

class NetworkDetector:
    def __init__(self, check_hosts=None, timeout=2.0):
        self.check_hosts = check_hosts or [
            ("8.8.8.8", 53),        # Google DNS
            ("1.1.1.1", 53),        # Cloudflare DNS
        ]
        self.timeout = timeout

    def is_connected(self) -> bool:
        """Soket seviyesinde en hızlı internet denetimini gerçekleştirir."""
        for host, port in self.check_hosts:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self.timeout)
                s.connect((host, port))
                s.close()
                return True
            except (socket.timeout, socket.error):
                continue
        return False

    def check_status(self) -> Tuple[bool, str]:
        if self.is_connected():
            return True, "ONLINE - İnternet bağlantısı aktif (Bulut Yapay Zeka Hazır)"
        else:
            return False, "OFFLINE - İnternet yok (Dahili Yerel Yapay Zeka Aktif)"
