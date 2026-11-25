"""
AI-OS Kapsamlı Sistem ve Çekirdek Bileşenleri Canlı Doğrulama ve Çalıştırma Scripti
Bu script sistemin tüm parçalarını uçtan uca çalıştırır ve sonuçları raporlar.
"""

import sys
import os

# Kök dizini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.network_detector import NetworkDetector
from src.core.system_controller import SystemController
from src.core.multi_user import MultiUserManager
from src.core.offline_slm import OfflineSLMManager
from src.core.ai_gateway import AIGateway
from src.core.intent_engine import IntentEngine
from src.core.learning_engine import LearningEngine
from src.updater.ota_manager import OTAManager

def run_all():
    print("=" * 70)
    print("      🚀 AI-OS CANLI SİSTEM TESTİ VE BİLEŞENLERİN ÇALIŞTIRILMASI 🚀")
    print("=" * 70)

    # 1. AĞ DENETİMİ
    print("\n[1/6] 📡 AĞ VE İNTERNET DURUMU KONTROLÜ")
    net = NetworkDetector()
    is_online, msg = net.check_status()
    print(f" -> Bağlantı Durumu: {msg}")

    # 2. SİSTEM & DONANIM METRİKLERİ
    print("\n[2/6] ⚙️ SİSTEM VE DONANIM YÖNETİCİSİ (SystemController)")
    sys_ctrl = SystemController()
    metrics = sys_ctrl.get_hardware_metrics()
    print(f" -> Platform: {metrics['platform']}")
    print(f" -> Disk Durumu: Toplam {metrics['disk']['total_gb']} GB, Boş {metrics['disk']['free_gb']} GB (%{metrics['disk']['used_percent']} dolu)")
    print(f" -> Bellek (RAM): Toplam {metrics['memory']['total_mb']} MB (%{metrics['memory']['used_percent']} kullanılıyor)")
    safe_cmd_res = sys_ctrl.execute_safe_command("rm -rf /")
    print(f" -> Güvenlik Koruması Testi (rm -rf /): {safe_cmd_res['error']}")

    # 3. ÇOK KULLANICILI YÖNETİM
    print("\n[3/6] 👥 ÇOK KULLANICILI SİSTEM VE OTURUM (MultiUserManager)")
    users = MultiUserManager(data_root="data/demo_users")
    user_res = users.create_user("ogrenci", "gizli123", display_name="Ali Öğrenci")
    print(f" -> Kullanıcı Oluşturma: {user_res['message']}")
    auth_res = users.authenticate("ogrenci", "gizli123")
    print(f" -> Giriş Doğrulama (Auth): Başarılı={auth_res['success']}, Oturum={auth_res.get('session', {}).get('username')}")
    users.update_user_api_key("gemini", "DEMO_GEMINI_KEY_ABC123")
    prof = users.get_current_user_profile()
    print(f" -> API Anahtarı Kaydı: {prof['api_keys']['gemini'][:12]}... (Güvenli Yerel Depoda)")

    # 4. NİYET MOTORU (INTENT ENGINE)
    print("\n[4/6] 🎯 NİYET ÇÖZÜMLEME (IntentEngine)")
    gateway = AIGateway(users)
    intent = IntentEngine(gateway)
    
    # Test 1: Film İzleme
    film_query = "Yıldızlararası filmini izlemek istiyorum"
    res_film = intent.parse_and_execute(film_query)
    print(f" -> Kullanıcı Girdisi: '{film_query}'")
    print(f"    Tespit Edilen Tür: {res_film['type']} (Varlık: '{res_film.get('detected_query')}')")
    print(f"    Sistemin Sorusu: {res_film['question']}")
    for opt in res_film['options']:
        print(f"      • {opt['label']} -> {opt.get('target')}")

    # Test 2: Kodlama Eğitimi
    edu_query = "Sıfırdan python öğrenmek istiyorum"
    res_edu = intent.parse_and_execute(edu_query)
    print(f"\n -> Kullanıcı Girdisi: '{edu_query}'")
    print(f"    Tespit Edilen Tür: {res_edu['type']}")
    print(f"    Sistemin Yanıtı: {res_edu['message']}")

    # 5. E-EĞİTİM AKADEMİSİ
    print("\n[5/6] 🎓 E-EĞİTİM VE KOD DEĞERLENDİRME MOTORU (LearningEngine)")
    learning = LearningEngine()
    course = learning.get_course("py101")
    mod0 = course["modules"][0]
    print(f" -> Aktif Kurs: {course['title']} ({course['level']})")
    print(f"    Ders Konusu: {mod0['title']}")
    print(f"    Görev: {mod0['task']}")
    
    # Doğru kod testi
    eval_good = learning.evaluate_submission("py101", 0, "print('Merhaba AI-OS')")
    print(f"    Öğrenci Kodu (Doğru): \"print('Merhaba AI-OS')\" -> {eval_good['message']}")
    
    # Hatalı kod testi
    eval_bad = learning.evaluate_submission("py101", 0, "selam ver")
    print(f"    Öğrenci Kodu (Hatalı): \"selam ver\" -> {eval_bad['message']} (İpucu: {eval_bad['hint']})")

    # 6. ATOMİK OTA GÜNCELLEME SİSTEMİ
    print("\n[6/6] 🔄 ATOMİK OTA GÜNCELLEME VE SQUASHFS A/B YÖNETİCİSİ (OTAManager)")
    ota = OTAManager(slot_file="data/demo_slot")
    print(f" -> Mevcut Aktif Yuva: [{ota.get_active_slot()}]")
    print(f" -> Hedef Güncelleme Yuvası: [{ota.get_inactive_slot()}]")
    ota.apply_update_slot("B")
    print(f" -> Yeni Sürüm Kurulduktan Sonraki Yuva: [{ota.get_active_slot()}]")
    ota.apply_update_slot("A") # Geri al

    print("\n" + "=" * 70)
    print("  ✅ TÜM BİLEŞENLER VE MODÜLLER BAŞARIYLA ÇALIŞTIRILDI!")
    print("=" * 70)

if __name__ == "__main__":
    run_all()
