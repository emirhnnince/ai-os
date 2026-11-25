# Hibrit Yapay Zeka Motoru (AI Orchestrator Specification)

## 1. Çift Çekirdekli (Dual-Brain) Mantığı

AI-OS'in en kritik farkı, internet olsun ya da olmasın **her zaman çalışabilen bir yapay zekaya** sahip olmasıdır.

```
                        +------------------------+
                        |  Kullanıcı Talebi /    |
                        |  Doğal Dil Girdisi     |
                        +------------------------+
                                    |
                                    v
                        +------------------------+
                        | Ağ Bağlantı Kontrolü   |
                        |   (Network Ping/DNS)   |
                        +------------------------+
                               /          \
                     Var /              \ Yok
                        v                  v
        +-----------------------+   +------------------------+
        |   ÇEVRİMİÇİ MOD       |   |    ÇEVRİMDIŞI MOD      |
        | Google Gemini API     |   | Dahili Yerel SLM       |
        | (Öncelikli)           |   | (Qwen2.5-Coder / Gemma)|
        | Alternatif: OpenAI/   |   | llama.cpp Motoru       |
        | Claude / Groq         |   | CPU/RAM Optimize 4-bit |
        +-----------------------+   +------------------------+
                        \                  /
                         v                v
                        +------------------------+
                        | Ortak Cevap & Eylem    |
                        | Formatlayıcı (JSON)    |
                        +------------------------+
```

---

## 2. Çevrimdışı Model (Offline Mini-AI)

- **Motor:** `llama.cpp` veya hafif `ollama-core` (C++ tabanlı, harici GPU gerektirmeyen, salt CPU üzerinde AVX2/NEON ile ultra hızlı çalışan motor).
- **Varsayılan Model:**
  - **Qwen2.5-Coder-1.5B-Instruct-Q4_K_M** (~1.1 GB disk boyutu, ~1.8 GB RAM tüketimi)
  - Veya **Gemma-2-2B-IT-Q4_K_M**
- **Yetenekler:**
  - Linux bash komutları üretme ve açıklama.
  - Temel Python/JavaScript kod yazımı ve hata ayıklama.
  - Çevrimdışı sistem ayarları (Wi-Fi, ses, parlaklık, disk durumu).
  - İnternetsiz çalışma anında kullanıcıya internet ayarını yapması için rehberlik etme.

---

## 3. Çevrimiçi Model & Gemini Önceliği

İnternet bağlantısı sağlandığı anda sistem otomatik olarak bulut zekasına yükseltilir:
- **Birincil Model:** **Google Gemini 2.0 / 1.5 Flash & Pro**
  - Hızlı yanıt süresi (düşük gecikme).
  - Geniş bağlam penceresi (1M+ token ile tüm kod projelerini veya belgeleri okuma imkanı).
  - Çok modlu (Multimodal) yetenek: Ekran görüntüsü alma ve ekrandaki hatayı analiz etme.
- **Esnek Sağlayıcı Desteği:** Kullanıcı dilerse arayüzden tek tıkla OpenAI (GPT-4o), Anthropic (Claude 3.5), Groq (Llama-3.3-70B) veya yerel büyük modelleri seçebilir.

---

## 4. Akıllı İlk Kurulum & API Sihirbazı (Onboarding Wizard)

Sistem ilk kez internete bağlandığında kullanıcıyı zorlamayan, rehber niteliğinde bir arayüz açılır:

1. **Ağ Algılama:** Wi-Fi veya Ethernet bağlantısı kurulduğunda sağ altta bildirim çıkar:  
   *"İnternet bağlantısı tespit edildi. Üstün zeka modunu (Gemini API) aktifleştirmek ister misiniz?"*
2. **Adım Adım API Asistanı:**
   - Kullanıcıya ücretsiz Gemini API anahtarı alabileceği Google AI Studio bağlantısını sunar (dahili mini tarayıcı penceresinde).
   - Kullanıcı API anahtarını yapıştırdığında, asistan bir ping isteği ile anahtarı doğrular.
   - Anahtar, kullanıcının şifreli yerel anahtarlığında (`secret-service` / `libsecret` / AES-256) saklanır.
3. **Profil Özelleştirme:**
   - Kullanıcının rolü seçilir: *(Öğrenci, Junior Yazılımcı, Veri Bilimci, Genel Kullanıcı)*.
   - Bu role göre sistemin başlangıç davranışları optimize edilir.
