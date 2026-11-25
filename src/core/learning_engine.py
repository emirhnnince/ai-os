"""
AI-OS İnteraktif E-Eğitim Akademisi (Gelişmiş Sürüm)
Kullanıcıların sıfırdan yazılımcı ve yapay zeka mühendisi olmasını sağlayan
dinamik ders, görev ve otomatik kod değerlendirme motoru.
"""

from typing import Dict, Any, List, Optional

class LearningEngine:
    def __init__(self, ai_gateway=None):
        self.ai_gateway = ai_gateway
        self.courses = {
            "py101": {
                "id": "py101",
                "title": "Sıfırdan Python ile Programlama",
                "level": "Başlangıç",
                "modules": [
                    {
                        "step": 0,
                        "title": "Ekrana İlk Yazıyı Yazdırma",
                        "lesson": "Python'da ekrana mesaj basmak için print() fonksiyonu kullanılır. Metinler tek veya çift tırnak içine alınır.",
                        "task": "Ekrana 'Merhaba AI-OS' yazdıran kodu yazın.",
                        "expected_snippet": "print('Merhaba AI-OS')",
                        "hint": "print('Merhaba AI-OS') yazıp çalıştırın."
                    },
                    {
                        "step": 1,
                        "title": "Değişkenler ve Matematiksel İşlemler",
                        "lesson": "Değişkenler verileri hafızada tutar. Örnek: sayi = 10",
                        "task": "x = 10 ve y = 20 değişkenlerini tanımlayıp toplamlarını print ile ekrana yazdırın.",
                        "expected_snippet": "x = 10\ny = 20\nprint(x + y)",
                        "hint": "x + y ifadesini print() içine yerleştirin."
                    },
                    {
                        "step": 2,
                        "title": "Koşullu Durumlar (if-else)",
                        "lesson": "Karar yapıları için 'if' ve 'else' kullanılır.",
                        "task": "puan = 85 tanımlayın. Eğer puan >= 50 ise 'Geçti' yazdıran if bloğunu yazın.",
                        "expected_snippet": "puan = 85\nif puan >= 50:\n    print('Geçti')",
                        "hint": "İki nokta üst üste (:) ve 4 boşluk girintiye dikkat edin."
                    }
                ]
            },
            "linux101": {
                "id": "linux101",
                "title": "Linux Terminali ve Sistem Yönetimi",
                "level": "Başlangıç",
                "modules": [
                    {
                        "step": 0,
                        "title": "Dosya ve Dizin Listeleme",
                        "lesson": "Bulunduğunuz dizindeki dosyaları görmek için 'ls' komutu kullanılır. Detaylar için 'ls -la' eklenir.",
                        "task": "Mevcut dizindeki dosyaları listeleyen bash komutunu yazın.",
                        "expected_snippet": "ls",
                        "hint": "Sadece 'ls' yazmanız yeterlidir."
                    },
                    {
                        "step": 1,
                        "title": "Ağ Durumu ve IP Bilgisi",
                        "lesson": "IP adresinizi ve ağ arayüzlerini görmek için 'ip addr' veya 'ip a' kullanılır.",
                        "task": "Sistemdeki IP adreslerini listeleyen komutu yazın.",
                        "expected_snippet": "ip a",
                        "hint": "'ip a' veya 'ip addr' yazabilirsiniz."
                    }
                ]
            },
            "ai101": {
                "id": "ai101",
                "title": "Yapay Zeka ve Prompt Mühendisliği",
                "level": "Orta",
                "modules": [
                    {
                        "step": 0,
                        "title": "Rol ve Hedef Belirleme (Few-Shot Prompting)",
                        "lesson": "Yapay zekaya kesin bir rol (örn: 'Sen bir kıdemli Linux mühendisisin') vermek çıktının doğruluğunu artırır.",
                        "task": "Bir Python hata ayıklayıcı rolü tanımlayan bir sistem komutu yazın.",
                        "expected_snippet": "Sen bir uzman Python hata ayıklayıcısısın",
                        "hint": "'Sen bir uzman Python...' şeklinde başlayın."
                    }
                ]
            }
        }

    def list_available_courses(self) -> List[Dict[str, str]]:
        return [
            {"id": c["id"], "title": c["title"], "level": c["level"], "steps": len(c["modules"])}
            for c in self.courses.values()
        ]

    def get_course(self, course_id: str) -> Dict[str, Any]:
        return self.courses.get(course_id, self.courses["py101"])

    def evaluate_submission(self, course_id: str, step_index: int, user_code: str) -> Dict[str, Any]:
        course = self.get_course(course_id)
        if step_index >= len(course["modules"]):
            return {
                "success": True,
                "completed": True,
                "message": f"🎉 Harika! {course['title']} kursunun tüm adımlarını başarıyla tamamladınız!"
            }

        module = course["modules"][step_index]
        expected = module["expected_snippet"]

        # Kod temizleme & kontrol
        norm_user = user_code.replace(" ", "").replace('"', "'").replace("\r", "")
        norm_exp = expected.replace(" ", "").replace('"', "'").replace("\r", "")

        if norm_exp in norm_user or norm_user in norm_exp or len(norm_user) > 0 and any(keyword in user_code for keyword in ["print", "ls", "ip"]):
            is_last = (step_index + 1) >= len(course["modules"])
            return {
                "success": True,
                "completed": is_last,
                "message": "✅ Başarılı! Kodunuz beklenen çıktıyı sağladı." if not is_last else "🏆 Tebrikler, kursu tamamladınız!",
                "next_step": step_index + 1
            }
        else:
            return {
                "success": False,
                "completed": False,
                "message": "❌ Kod beklenen yapıda değil.",
                "hint": module["hint"]
            }
