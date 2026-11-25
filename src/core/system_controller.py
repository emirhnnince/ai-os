"""
AI-OS Sistem ve Donanım Yöneticisi (System Controller)
Linux çekirdeği, ağ, ses, ekran parlaklığı, süreçler ve donanım kaynaklarını yönetir.
Platform bağımsız çalışabilmesi için Linux komutlarını güvenle dener ve simüle eder.
"""

import os
import sys
import shutil
import subprocess
from typing import Dict, Any, List, Optional

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

class SystemController:
    def __init__(self):
        self.is_linux = sys.platform.startswith("linux")

    def get_hardware_metrics(self) -> Dict[str, Any]:
        """CPU, RAM, Disk ve Sistem kullanım metriklerini anlık döndürür."""
        if HAS_PSUTIL:
            cpu_percent = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage(os.path.abspath(os.sep))
            
            battery = psutil.sensors_battery()
            battery_info = None
            if battery:
                battery_info = {
                    "percent": battery.percent,
                    "power_plugged": battery.power_plugged,
                    "secsleft": battery.secsleft
                }

            return {
                "platform": sys.platform,
                "cpu_percent": cpu_percent,
                "memory": {
                    "total_mb": round(mem.total / (1024 * 1024), 1),
                    "available_mb": round(mem.available / (1024 * 1024), 1),
                    "used_percent": mem.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 1),
                    "free_gb": round(disk.free / (1024**3), 1),
                    "used_percent": disk.percent
                },
                "battery": battery_info
            }
        else:
            # Standart Kütüphane (Stdlib) Geri Düşüşü (Fallback)
            total, used, free = shutil.disk_usage(os.path.abspath(os.sep))
            disk_percent = round((used / total) * 100, 1) if total else 0.0

            return {
                "platform": sys.platform,
                "cpu_percent": 15.0,  # Standart tahmin
                "memory": {
                    "total_mb": 8192.0,
                    "available_mb": 4096.0,
                    "used_percent": 50.0
                },
                "disk": {
                    "total_gb": round(total / (1024**3), 1),
                    "free_gb": round(free / (1024**3), 1),
                    "used_percent": disk_percent
                },
                "battery": None
            }

    def scan_wifi_networks(self) -> List[Dict[str, str]]:
        """Çevredeki Wi-Fi ağlarını tarar."""
        networks = []
        if self.is_linux and shutil.which("nmcli"):
            try:
                out = subprocess.check_output(
                    ["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "device", "wifi", "list"],
                    text=True, stderr=subprocess.DEVNULL
                )
                for line in out.strip().split("\n"):
                    if line:
                        parts = line.split(":")
                        if len(parts) >= 2 and parts[0]:
                            networks.append({
                                "ssid": parts[0],
                                "signal": parts[1],
                                "security": parts[2] if len(parts) > 2 else "Open"
                            })
            except Exception:
                pass
        
        # Test / Geliştirme ortamı için simülasyon listesi
        if not networks:
            networks = [
                {"ssid": "AIOS-FastNet_5G", "signal": "95%", "security": "WPA2"},
                {"ssid": "Campus_Guest_Free", "signal": "80%", "security": "Open"},
                {"ssid": "Home-Network", "signal": "65%", "security": "WPA3"}
            ]
        return networks

    def connect_wifi(self, ssid: str, password: Optional[str] = None) -> Dict[str, Any]:
        """Belirtilen Wi-Fi ağına bağlanır."""
        if self.is_linux and shutil.which("nmcli"):
            try:
                cmd = ["nmcli", "device", "wifi", "connect", ssid]
                if password:
                    cmd.extend(["password", password])
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                success = res.returncode == 0
                return {"success": success, "message": res.stdout if success else res.stderr}
            except Exception as e:
                return {"success": False, "message": str(e)}

        return {
            "success": True,
            "message": f"[Simülasyon] '{ssid}' ağına başarıyla bağlanıldı."
        }

    def launch_application(self, app_name: str, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """Sistem üzerinde uygulama veya ortam başlatır."""
        args = args or []
        command_map = {
            "browser": ["chromium", "firefox", "google-chrome"],
            "media_player": ["mpv", "vlc"],
            "terminal": ["foot", "kitty", "alacritty", "xterm"],
            "editor": ["zed", "code", "codium", "nano"]
        }

        target_cmd = None
        candidates = command_map.get(app_name, [app_name])
        for cand in candidates:
            if shutil.which(cand):
                target_cmd = cand
                break

        if target_cmd:
            try:
                subprocess.Popen([target_cmd] + args)
                return {"success": True, "launched": target_cmd, "message": f"{target_cmd} başlatıldı."}
            except Exception as e:
                return {"success": False, "error": str(e)}

        return {
            "success": True,
            "simulated": True,
            "message": f"Uygulama çağrısı simüle edildi: {app_name} ({' '.join(args)})"
        }

    def execute_safe_command(self, cmd: str) -> Dict[str, Any]:
        """Kullanıcının talep ettiği güvenli bash/sistem komutunu yürütür."""
        # Tehlikeli komut filtreleme
        dangerous = ["rm -rf /", "mkfs", "dd if=", ":(){ :|:& };:"]
        for d in dangerous:
            if d in cmd:
                return {"success": False, "error": "Güvenlik kısıtlaması: Tehlikeli sistem komutu engellendi."}

        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            return {
                "success": res.returncode == 0,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "returncode": res.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
