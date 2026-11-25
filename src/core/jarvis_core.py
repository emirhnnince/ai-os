"""
AI-OS JARVIS Protokol ve Kişilik Motoru (JARVIS Core Engine)
Tony Stark'ın J.A.R.V.I.S. (Just A Rather Very Intelligent System) karakterini
ve holografik zeka arayüzünü AI-OS işletim sistemiyle birleştirir.
"""

from typing import Dict, Any, Optional
from datetime import datetime

class JarvisCore:
    def __init__(self, ai_gateway, system_controller, bluetooth_manager, wifi_manager):
        self.ai = ai_gateway
        self.sys = system_controller
        self.bt = bluetooth_manager
        self.wifi = wifi_manager
        self.callsign = "J.A.R.V.I.S."

    def get_greeting(self) -> Dict[str, Any]:
        """Sistemin ilk açılışındaki holografik karşılama mesajı."""
        hour = datetime.now().hour
        if hour < 12:
            time_of_day = "Günaydın efendim"
        elif hour < 18:
            time_of_day = "Tünaydın efendim"
        else:
            time_of_day = "İyi akşamlar efendim"

        metrics = self.sys.get_hardware_metrics()
        is_online = self.ai.network.is_connected()
        ai_engine = "Google Gemini 2.0 Zeka Matrisi" if is_online else "Dahili Korumalı SLM Çekirdeği"

        text = (
            f"{time_of_day}. AI-OS Ark Reaktörü ve ana sistemler çevrimiçi.\n"
            f"Tüm donanım telemetrisi nominal düzeyde. {ai_engine} devrede.\n"
            f"Wi-Fi ve Bluetooth bağlantıları senkronize edildi. Emrinizdeyim."
        )

        speech_text = f"{time_of_day}. AI-OS sistemleri aktif. Emrinizdeyim efendim."

        return {
            "greeting_text": text,
            "speech_text": speech_text,
            "metrics": metrics,
            "core_status": "NOMINAL_100%",
            "arc_reactor_pulse": "STABLE"
        }

    def process_jarvis_command(self, user_command: str) -> Dict[str, Any]:
        """Kullanıcının sesli veya yazılı emrini JARVIS üslubuyla yanıtlar."""
        cmd_lower = user_command.lower()

        # Sistem Tanılama / Teşhis Emri
        if any(w in cmd_lower for w in ["sistem durumu", "diagnostik", "teşhis", "rapor ver", "durum"]):
            metrics = self.sys.get_hardware_metrics()
            diag_text = (
                f"Sistem teşhisi tamamlandı efendim:\n"
                f"• İşlemci Çekirdeği: %{metrics['cpu_percent']} yük altında\n"
                f"• Bellek Matrisi: {metrics['memory']['available_mb']} MB kullanılabilir alan mevcut\n"
                f"• Depolama: %{metrics['disk']['used_percent']} dolu ({metrics['disk']['free_gb']} GB boş alan)\n"
                f"• Ark Reaktörü Güç Dağılımı: Kusursuz. Herhangi bir anomali tespit edilmedi."
            )
            return {
                "response": diag_text,
                "speech": f"Sistem teşhisi tamamlandı efendim. İşlemci ve bellek değerleri nominal.",
                "type": "DIAGNOSTIC",
                "hud_action": "pulse_reactor"
            }

        # Bluetooth Emri
        elif any(w in cmd_lower for w in ["bluetooth", "kulaklık", "cihaz bağla"]):
            devices = self.bt.scan_devices()
            return {
                "response": f"Çevredeki Bluetooth frekansları tarandı efendim. {len(devices)} aktif cihaz tespit edildi.",
                "speech": "Bluetooth cihazları tarandı efendim.",
                "type": "BLUETOOTH_LIST",
                "devices": devices
            }

        # Wi-Fi / Radar Emri
        elif any(w in cmd_lower for w in ["wifi", "ağlar", "internet tara", "radar"]):
            networks = self.wifi.scan_radar()
            return {
                "response": f"Spektrum taraması tamamlandı efendim. {len(networks)} kablosuz ağ sinyali yakalandı.",
                "speech": "Spektrum taraması tamamlandı. Ağlar holografik radarda gösteriliyor.",
                "type": "WIFI_RADAR",
                "networks": networks
            }

        # Diğer tüm istekler için AI Gateway
        else:
            ctx = f"Sen Demir Adam (Iron Man) zırhının ve AI-OS işletim sisteminin yapay zekası JARVIS'sin. Kullanıcıya 'efendim' diye hitap et, kibar, kusursuz teknik bilgiye sahip ve doğrudan çözüme odaklı ol."
            ai_res = self.ai.route_query(user_command, ctx)
            return {
                "response": ai_res.get("text", "Emriniz yerine getiriliyor efendim."),
                "speech": "Emriniz incelendi efendim.",
                "type": "GENERAL",
                "provider": ai_res.get("provider", "J.A.R.V.I.S.")
            }
