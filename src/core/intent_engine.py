"""
AI-OS Niyet Odaklı Eylem Motoru (Intent Engine - Gelişmiş Varlık ve Eylem Çıkarımı)
Kullanıcının ne yapmak istediğini (film izlemek, kod öğrenmek, sistem kontrolü, ortam kurma)
anlayarak kesin işletim sistemi aksiyonlarına dönüştürür.
"""

import re
from typing import Dict, Any, List

class IntentEngine:
    def __init__(self, ai_gateway):
        self.gateway = ai_gateway

    def parse_and_execute(self, user_input: str) -> Dict[str, Any]:
        cleaned = user_input.strip()
        lower = cleaned.lower()

        # 1. Medya ve Film / Video Niyeti
        if any(w in lower for w in ["film", "dizi", "sinema", "video", "izlemek", "youtube", "netflix"]):
            # Film adı çıkarımı: "Matrix filmini izlemek istiyorum" -> "Matrix"
            query = ""
            match = re.search(r"([a-zA-Z0-9çğıöşüÇĞİÖŞÜ\s]+)\s+(filmi|filmini|dizisi|dizisini|videosu)\s+izle", lower)
            if match:
                query = match.group(1).strip()

            search_yt = f"https://www.youtube.com/results?search_query={query}" if query else "https://youtube.com"
            search_nf = f"https://www.netflix.com/search?q={query}" if query else "https://netflix.com"

            prompt_q = f"'{query.capitalize()}' için nereden izlemek istersiniz?" if query else "Hangi platformdan izlemek istersiniz?"

            return {
                "type": "MEDIA_INTENT",
                "intent": "watch_media",
                "detected_query": query,
                "question": prompt_q,
                "options": [
                    {"label": "YouTube", "action": "open_browser", "target": search_yt},
                    {"label": "Netflix", "action": "open_browser", "target": search_nf},
                    {"label": "Yerel USB / Disk Videoları (MPV)", "action": "launch_player", "target": "~/Videos"}
                ],
                "message": "İstediğiniz ortamı hazırlıyorum. Lütfen platformu seçin:"
            }

        # 2. Yazılım / Kodlama Öğrenme Niyeti (E-Eğitim)
        elif any(w in lower for w in ["kod öğren", "python öğren", "yazılım öğren", "ders", "eğitim", "nasıl kod yazılır"]):
            return {
                "type": "LEARNING_INTENT",
                "intent": "start_learning_academy",
                "question": "AI-OS Kodlama Akademisi: Hangi alandan başlamak istersiniz?",
                "options": [
                    {"label": "Python Programlama 101 (Tavsiye Edilen)", "course_id": "py101"},
                    {"label": "Linux Terminali ve Bash Komutları", "course_id": "linux101"},
                    {"label": "Yapay Zeka ve Prompt Mühendisliği", "course_id": "ai101"}
                ],
                "message": "AI-OS interaktif eğitim moduna geçiş yapılıyor. İşletim sisteminiz bir kodlama okuluna dönüştürüldü."
            }

        # 3. Geliştirici Ortamı / Proje Açma
        elif any(w in lower for w in ["proje aç", "kod yaz", "ide", "vscode", "terminal", "editör"]):
            return {
                "type": "DEV_INTENT",
                "intent": "launch_dev_env",
                "action": "launch_workspace",
                "target": "~/workspace",
                "message": "Geliştirici ortamı ve kalıcı çalışma alanınız hazırlandı."
            }

        # 4. Donanım ve Telemetri Sorgusu
        elif any(w in lower for w in ["sistem durumu", "ram", "cpu", "donanım", "kaynak", "performans"]):
            return {
                "type": "SYSTEM_INTENT",
                "intent": "show_telemetry",
                "message": "Sistem durumunuz yukarıdaki gösterge çubuğunda anlık izlenmektedir. Daha fazla ayrıntı için telemetri API'si hazırdır."
            }

        # 5. Genel Yapay Zeka Sorgusu
        else:
            ai_res = self.gateway.route_query(user_input)
            return {
                "type": "GENERAL_AI_QUERY",
                "raw_response": ai_res,
                "message": ai_res.get("text", "")
            }
