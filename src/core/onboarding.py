"""
AI-OS İlk Kurulum ve API Yardımcısı (Onboarding Wizard)
Kullanıcıya adım adım internet tespiti, yapay zeka seçimi ve API alma rehberliği sunar.
"""

class OnboardingWizard:
    def __init__(self, ai_gateway):
        self.gateway = ai_gateway

    def start_cli_wizard(self):
        print("\n" + "="*65)
        print("  🌟 HOŞ GELDİNİZ! AI-OS Akıllı Kurulum & Yapay Zeka Asistanı 🌟")
        print("="*65)
        print("AI-OS, bilgisayarınızı yapay zeka ile yönetmenizi sağlayan canlı sistemdir.\n")

        is_connected, status_msg = self.gateway.network.check_status()
        print(f"📡 Ağ Durumu: {status_msg}")

        if not is_connected:
            print("\n⚠️ Şu anda internet bağlantısı bulunamadı.")
            print("Sistem 'Çevrimdışı Yerel Yapay Zeka (Qwen2.5/Gemma)' ile tam fonksiyonel çalışmaya devam ediyor.")
            print("İnternete bağlandığınızda bu sihirbaz otomatik olarak Gemini API entegrasyonu için açılacaktır.\n")
            return

        print("\n✅ İnternet bağlantısı tespit edildi!")
        print("Hangi yapay zekayı birincil motor olarak kullanmak istersiniz?\n")
        print("  [1] Google Gemini 2.0 / 1.5 Flash (ÖNERİLEN - Hızlı, Çok Modlu, Ücretsiz)")
        print("  [2] OpenAI GPT-4o / Mini")
        print("  [3] Anthropic Claude 3.5")
        print("  [4] Çevrimdışı Yerel Modeli Kullanmaya Devam Et (İnternetsiz/Gizli)")

        choice = input("\nSeçiminiz (Varsayılan 1): ").strip() or "1"

        if choice == "1":
            self._setup_gemini()
        elif choice == "2":
            self._setup_openai()
        else:
            print("Yerel model modu korundu.")

    def _setup_gemini(self):
        print("\n--- 🔷 Google Gemini Kurulumu ---")
        print("Gemini API anahtarınız var mı?")
        print("Eğer yoksa, tarayıcınızda ücretsiz anahtar oluşturma sayfasını açabiliriz.")
        print("🔗 https://aistudio.google.com/app/apikey\n")

        key = input("Lütfen Gemini API Anahtarınızı girin (Boş bırakırsanız yerel model çalışır): ").strip()
        if key:
            self.gateway.config["active_provider"] = "gemini"
            self.gateway.config["gemini_api_key"] = key
            self.gateway.save_config()
            print("✅ Gemini API anahtarınız güvenli yerel anahtarlığa kaydedildi!")
            print("🚀 Sistem artık üstün zeka moduyla çalışıyor.")
        else:
            print("Anahtar girilmedi. Yerel model aktif.")

    def _setup_openai(self):
        key = input("Lütfen OpenAI API Anahtarınızı girin: ").strip()
        if key:
            self.gateway.config["active_provider"] = "openai"
            self.gateway.config["openai_api_key"] = key
            self.gateway.save_config()
            print("✅ OpenAI API anahtarınız kaydedildi!")
