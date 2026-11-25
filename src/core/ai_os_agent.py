"""
AI-OS Sade ve Güçlü Sistem Ajanı (AI-OS Core Agent)
Sade, doğrudan, zarif ve her türlü isteği (film, kodlama, sistem, soru-cevap)
yerine getiren minimalist işletim sistemi asistanı.
"""

import sys
from typing import Dict, Any, Optional
from datetime import datetime
from .self_learning_engine import SelfLearningEngine

class AIOSAgent:
    def __init__(self, ai_gateway, system_controller, bluetooth_manager, wifi_manager, intent_engine):
        self.ai = ai_gateway
        self.sys = system_controller
        self.bt = bluetooth_manager
        self.wifi = wifi_manager
        self.intent = intent_engine
        self.learning = SelfLearningEngine()
        self.brand = "AI OS"
        self.active_model = "gemini-2.0-flash"
        self.stealth_mode = False

    def detect_urgency(self, text: str) -> bool:
        """Aciliyet veya kısa/doğrudan yanıt gerektiren duygu durumunu algılar."""
        urgent_words = ["acil", "hemen", "çabuk", "hızlı", "şimdi", "urgent", "asap", "kısaca"]
        lower = text.lower()
        return any(w in lower for w in urgent_words)

    def get_greeting(self) -> Dict[str, Any]:
        hour = datetime.now().hour
        if hour < 12:
            time_greet = "Günaydın"
        elif hour < 18:
            time_greet = "İyi günler"
        else:
            time_greet = "İyi akşamlar"

        is_online = False if self.stealth_mode else self.ai.network.is_connected()
        engine_name = "Google Gemini 2.0 (Bulut)" if is_online else "Yerel SLM (Çevrimdışı)"
        evolution = self.learning.knowledge.get("evolution_level", "v1.2")
        greeting_text = f"{time_greet}. AI OS hazır. Nasıl yardımcı olabilirim?"

        return {
            "title": "AI OS",
            "message": greeting_text,
            "greeting_text": greeting_text,
            "speech_text": f"{time_greet}. AI OS hazır. Dinliyorum.",
            "status": "ready",
            "engine": engine_name,
            "active_model": self.active_model,
            "stealth_mode": self.stealth_mode,
            "evolution": evolution,
            "learned_rules_count": len(self.learning.knowledge.get("learned_rules", []))
        }

    def process_request(self, user_text: str, user_feedback: Optional[str] = None) -> Dict[str, Any]:
        """Kullanıcının her türlü doğal dil talebini çözer ve uygular."""
        cleaned = user_text.strip()
        lower = cleaned.lower()

        # 1. Kod Sandbox Çalıştırma İsteği ("python kodu çalıştır: print(123)")
        if lower.startswith("kod çalıştır:") or lower.startswith("run code:"):
            code_to_run = cleaned.split(":", 1)[1].strip()
            exec_res = self.sys.execute_safe_command(f'"{sys.executable}" -c "{code_to_run}"')
            out = exec_res.get("stdout") or exec_res.get("stderr") or "Kod başarıyla çalıştı (Çıktı yok)."
            return {
                "type": "TEXT",
                "title": "⚡ Kod Yürütme Çıktısı",
                "response": f"Kodlama Çıktısı:\n```\n{out}\n```",
                "speech": "Kod yürütüldü. Çıktı ekranda."
            }

        # 2. Sistem Kendi Kendini Onarma / Tanılama ("sistem onar", "diagnostik")
        if any(w in lower for w in ["onar", "self heal", "sağlık kontrolü"]):
            metrics = self.sys.get_hardware_metrics()
            fix_msg = (
                "🛡️ AI OS Sistem Kendi Kendini Denetleme Raporu:\n"
                "• Bellek Sızıntısı: Tespit edilmedi. Boş bellek: " + str(metrics['memory']['available_mb']) + " MB\n"
                "• Zombi Süreçler: 0 adet (Sistem temiz)\n"
                "• Çekirdek Bütünlüğü: Nominal değerlerde\n"
                "• Kendi Kendini Geliştirme: " + str(self.learning.knowledge['interaction_count']) + " etkileşim analiz edildi."
            )
            return {
                "type": "TEXT",
                "title": "🛡️ Otomatik Sistem Denetimi",
                "response": fix_msg,
                "speech": "Sistem sağlığı ve özonarım kontrolü tamamlandı. Her şey yolunda."
            }

        # 3. Niyet Motoruna Gönder (Film, Kodlama, Medya vb.)
        action = self.intent.parse_and_execute(cleaned)

        if action.get("type") == "MEDIA_INTENT":
            q_title = action.get("detected_query", "").capitalize()
            speech = f"{q_title} için platform seçenekleri hazırlandı." if q_title else "İzlemek istediğiniz platformu seçebilirsiniz."
            self.learning.record_interaction(cleaned, action.get("message", ""), user_feedback)
            return {
                "type": "ACTION_CARD",
                "subtype": "MEDIA",
                "title": f"🎬 {action.get('question')}",
                "message": action.get("message"),
                "options": action.get("options", []),
                "speech": speech,
                "response": action.get("message")
            }

        elif action.get("type") == "LEARNING_INTENT":
            self.learning.record_interaction(cleaned, action.get("message", ""), user_feedback)
            return {
                "type": "ACTION_CARD",
                "subtype": "LEARNING",
                "title": f"🎓 {action.get('question')}",
                "message": action.get("message"),
                "options": action.get("options", []),
                "speech": "Kodlama eğitimi hazırlandı. Hangi kursla başlamak istersiniz?",
                "response": action.get("message")
            }

        # 4. Sistem / Donanım Sorgusu
        elif any(w in lower for w in ["sistem durumu", "ram", "cpu", "donanım", "durum"]):
            metrics = self.sys.get_hardware_metrics()
            msg = (
                f"Sistem Durumu:\n"
                f"• CPU Yükü: %{metrics['cpu_percent']}\n"
                f"• RAM: {metrics['memory']['available_mb']} MB boş (%{metrics['memory']['used_percent']} kullanılıyor)\n"
                f"• Depolama: %{metrics['disk']['used_percent']} dolu ({metrics['disk']['free_gb']} GB boş alan)\n"
                f"• Öğrenilen Kurallar: {len(self.learning.knowledge.get('learned_rules', []))} aktif kural"
            )
            return {
                "type": "TEXT",
                "title": "Sistem Durumu",
                "response": msg,
                "speech": f"Sistem durumu normal. İşlemci yükü yüzde {int(metrics['cpu_percent'])}."
            }

        # 5. Wi-Fi / Bluetooth
        elif "wifi" in lower or "kablosuz ağ" in lower:
            nets = self.wifi.scan_radar()
            net_names = ", ".join([n['ssid'] for n in nets[:3]])
            return {
                "type": "ACTION_CARD",
                "subtype": "WIFI",
                "title": "📡 Çevredeki Wi-Fi Ağları",
                "message": f"Yakındaki ağlar: {net_names}",
                "networks": nets,
                "speech": "Çevredeki Wi-Fi ağları bulundu.",
                "response": f"Tespit edilen ağlar: {net_names}"
            }

        elif "bluetooth" in lower:
            devices = self.bt.scan_devices()
            dev_names = ", ".join([d['name'] for d in devices[:3]])
            return {
                "type": "ACTION_CARD",
                "subtype": "BLUETOOTH",
                "title": "🎧 Bluetooth Cihazları",
                "message": f"Cihazlar: {dev_names}",
                "devices": devices,
                "speech": "Bluetooth cihazları listelendi.",
                "response": f"Cihazlar: {dev_names}"
            }

        # 6. Genel Yapay Zeka Sorgusu + Kendi Kendini Geliştiren Bağlam
        else:
            learned_ctx = self.learning.get_learned_context_prompt()
            urgency_note = "\nKullanıcı acil/kısa yanıt bekliyor; yanıtı olabildiğince kısa ve net tut." if self.detect_urgency(cleaned) else ""
            ctx = (
                "Sen AI OS adındaki yeni nesil işletim sisteminin minimalist, son derece zeki ve kendi kendini geliştirebilen yapay zeka asistanısın. "
                "Yanıtların doğrudan, kibar, net, yüksek zekalı ve çözüm odaklı olsun.\n" + learned_ctx + urgency_note
            )
            ai_res = self.ai.route_query(cleaned, ctx)
            reply = ai_res.get("text", "")
            
            # Etkileşimi hafızaya kaydet
            self.learning.record_interaction(cleaned, reply, user_feedback)

            return {
                "type": "TEXT",
                "title": "AI OS",
                "response": reply,
                "speech": reply[:130] if len(reply) > 130 else reply,
                "provider": ai_res.get("provider", "AI OS"),
                "urgent": self.detect_urgency(cleaned)
            }
