# AI-OS (Artificial Intelligence Operating System)

> **"Bilgisayarınızı değil, niyetinizi yönetin."**  
> Herhangi bir bilgisayarda doğrudan USB'den çalışan, çok kullanıcılı, çevrimdışı ve çevrimiçi hibrit yapay zeka çekirdeğine sahip yeni nesil işletim sistemi.

---

## 🌟 Proje Özeti ve Vizyon

**AI-OS**, geleneksel masaüstü paradigmasını (simgeler, pencereler, karmaşık menüler) terk eden; kullanıcı niyetini (*intent-driven*) merkeze alan **Linux tabanlı bir Live USB İşletim Sistemidir**. 

Cebinizdeki tek bir USB bellek ile dünyanın herhangi bir yerindeki herhangi bir x86_64 bilgisayarı (kendi verileriniz, oturumunuz ve özelleştirilmiş AI asistanınızla) anında kişisel yapay zeka istasyonunuza dönüştürür.

### 🎯 Temel Hedef Kitle
1. **Yazılımcılar ve Mühendisler:** Anında hazır izole geliştirme ortamları, AI kodlama asistanı, yerel terminal otomasyonu.
2. **Yazılım Öğrenmek İsteyenler (E-Eğitim):** Sistemin kendisi dinamik bir akademiye dönüşür. Sıfırdan kodlama öğrenmek isteyen bir kullanıcı için yapay zeka sistemi kişiselleştirilmiş bir eğitim ortamına dönüştürür.
3. **Yapay Zeka Meraklıları & Gezginler:** İnternet olsun veya olmasın cebinde çalışan bir yapay zeka işletim sistemi taşımak isteyenler.

---

## 🚀 Öne Çıkan Ana Özellikler

### 1. 🔌 Tak-Çalıştır Taşınabilir Canlı Sunucu (USB Live with Persistence)
- **Donanım Bağımsızlığı:** UEFI ve Legacy BIOS destekli tüm 64-bit bilgisayarlarda doğrudan USB'den boot eder.
- **Kalıcı Depolama (Persistence & OverlayFS):** Yaptığınız değişiklikler, indirdiğiniz modeller ve yazdığınız kodlar USB belleğinizde güvenle saklanır.
- **Çok Kullanıcılı Destek:** Tek bir USB bellek üzerinde şifreli, izole birden fazla kullanıcı profili.

### 2. 🧠 Hibrit Çift Çekirdekli Yapay Zeka (Dual-Brain Architecture)
- **Çevrimdışı (Offline Mini-AI):** İnternet bağlantısı olmadığında sistem içerisindeki hafifletilmiş yerel model (TinyLlama / Qwen2.5-Coder 1.5B / Phi-3 Mini) devreye girer. Temel komutlar, dosya arama, temel kod üretimi ve sistem yönetimi internetsiz çalışır.
- **Çevrimiçi (Cloud AI - Gemini Öncelikli):** İnternet algılandığı an kullanıcıyı karşılayan kurulum sihirbazı ile Google Gemini API (1.5/2.0 Flash/Pro), OpenAI, Anthropic veya özel API bağlantısı kurulur.
- **API Asistanı:** Kullanıcının API anahtarını adım adım almasını sağlayan rehber arayüz.

### 3. 💬 Niyet Odaklı Kabuk (Intent-Driven Agentic Desktop)
- Klasik menüler yerine niyet yönlendirmesi.
  - *Örnek:* *"Film izlemek istiyorum"* dediğinizde sistem: *"Hangi tür veya hangi platformdan (Netflix, YouTube, Yerel disk, Stremio) izlemek istersiniz?"* diyerek ortamı hazırlar.
  - *Örnek:* *"Python ile görüntü işleme çalışmak istiyorum"* dediğinizde sistem OpenCV, JupyterLab ve gerekli sanal ortamları tek komutla kurup önünüze getirir.

### 4. 🔄 Güvenli Atomik Güncelleme (Atomic OTA Build & Update)
- Salt-okunur (read-only) SquashFS çekirdek sistemi ve OverlayFS veri katmanı sayesinde işletim sistemi güncellendiğinde kullanıcı verileri asla silinmez.
- Yeni sürümler yayınlandığında sistem tek tıkla arka planda yeni sistem imajını indirir ve bir sonraki yeniden başlatmada (A/B Boot mekanizması) güvenle yeni sürüme geçer.

### 5. 🌍 Küresel Dağıtım & Gelir Modeli
- **Aşama 1 (Şu an):** %100 Açık Kaynak / Ücretsiz Topluluk Sürümü, ISO derleme betikleri ve demo sürümler.
- **Aşama 2:** Gelişmiş Bulut Eşitleme, Tak-Çalıştır Hazır Yüksek Hızlı NVMe/USB Donanımları satışı, Özel Kurumsal İmajlar ve Gelişmiş E-Eğitim Sertifikasyon Modülü.

---

## 📂 Proje Dizin Yapısı

```
ai-os/
├── docs/                      # Mimari, API, Derleme ve Yol Haritası Dokümanları
│   ├── architecture.md        # Detaylı Linux ve Katman Mimarisi
│   ├── ai_orchestrator.md     # Hibrit Yapay Zeka Motoru ve API Entegrasyonu
│   ├── learning_system.md     # E-Eğitim ve Dinamik Ortam Dönüştürücü
│   ├── iso_build_system.md    # Debian/Arch Live ISO Derleme Rehberi
│   └── roadmap_and_monetization.md # Sürüm ve Gelir Modeli
├── src/                       # Kaynak Kodlar
│   ├── core/                  # Çekirdek Agentik Motor ve Sistem Yöneticisi
│   │   ├── intent_engine.py   # Niyet Çözümleyici ve Eylem Dağıtıcı
│   │   ├── ai_gateway.py      # Offline SLM & Cloud API Yönlendirici
│   │   └── onboarding.py      # İlk Kurulum ve API Anahtar Sihirbazı
│   ├── ui/                    # Arayüz Bileşenleri (Wayland Shell / TUI / Kiosk)
│   └── updater/               # Atomik OTA Güncelleyici (A/B SquashFS)
├── scripts/
│   └── build/                 # Canlı ISO İmajı Oluşturma Betikleri
│       └── build_iso.sh
├── config/                    # Sistem ve Yapay Zeka Varsayılan Ayarları
└── README.md
```

---

## 🛠️ Hızlı Başlangıç & Gereksinimler

Proje geliştirme dokümanlarını incelemek ve ilk simülasyonları çalıştırmak için `docs/` dizinindeki teknik şartnameleri inceleyebilirsiniz.
