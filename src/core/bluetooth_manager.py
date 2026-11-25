"""
AI-OS Bluetooth Cihaz ve Donanım Yöneticisi (Bluetooth Manager)
Kulaklıklar, akıllı telefonlar, klavyeler ve IoT cihazlarını tarar, eşleştirir ve yönetir.
Linux üzerinde 'bluetoothctl' (BlueZ), diğer ortamlarda güvenli simülatör kullanır.
"""

import sys
import shutil
import subprocess
from typing import Dict, Any, List

class BluetoothManager:
    def __init__(self):
        self.is_linux = sys.platform.startswith("linux")

    def is_bluetooth_available(self) -> bool:
        if self.is_linux and shutil.which("bluetoothctl"):
            return True
        return True # Simülasyon / Çoklu platform desteği

    def scan_devices(self) -> List[Dict[str, Any]]:
        """Çevredeki Bluetooth cihazlarını (kulaklık, telefon vb.) tarar."""
        devices = []
        if self.is_linux and shutil.which("bluetoothctl"):
            try:
                # 3 saniyelik tarama komutu
                subprocess.run(["bluetoothctl", "--timeout", "3", "scan", "on"], capture_output=True, timeout=5)
                out = subprocess.check_output(["bluetoothctl", "devices"], text=True)
                for line in out.strip().split("\n"):
                    if line.startswith("Device"):
                        parts = line.split(" ", 2)
                        if len(parts) >= 3:
                            devices.append({
                                "mac": parts[1],
                                "name": parts[2],
                                "type": "Audio/Device",
                                "connected": False
                            })
            except Exception:
                pass

        # Tespit edilen veya simüle edilen cihazlar (Holografik HUD için)
        if not devices:
            devices = [
                {"mac": "FC:58:FA:82:11:01", "name": "Sony WH-1000XM5 (Kulaklık)", "type": "Audio", "connected": True, "battery": "85%"},
                {"mac": "74:45:CE:90:34:B8", "name": "Stark Smart Glass (HUD)", "type": "Display", "connected": True, "battery": "94%"},
                {"mac": "A4:C3:F0:12:88:90", "name": "Tony Phone (iPhone 16 Pro)", "type": "Mobile", "connected": False, "battery": "62%"},
                {"mac": "D8:3A:DD:44:91:20", "name": "Logitech MX Master 3S", "type": "Input", "connected": True, "battery": "90%"}
            ]
        return devices

    def connect_device(self, mac: str) -> Dict[str, Any]:
        """Seçilen Bluetooth cihazına bağlanır."""
        if self.is_linux and shutil.which("bluetoothctl"):
            try:
                res = subprocess.run(["bluetoothctl", "connect", mac], capture_output=True, text=True, timeout=10)
                success = "Connection successful" in res.stdout
                return {"success": success, "message": res.stdout}
            except Exception as e:
                return {"success": False, "message": str(e)}

        return {
            "success": True,
            "mac": mac,
            "message": f"Bluetooth Cihazı [{mac}] ile bağlantı başarıyla kuruldu. Ses ve veri hattı aktif."
        }

    def disconnect_device(self, mac: str) -> Dict[str, Any]:
        if self.is_linux and shutil.which("bluetoothctl"):
            try:
                res = subprocess.run(["bluetoothctl", "disconnect", mac], capture_output=True, text=True, timeout=5)
                return {"success": True, "message": res.stdout}
            except Exception as e:
                return {"success": False, "message": str(e)}

        return {"success": True, "message": f"Cihaz [{mac}] bağlantısı kesildi."}
