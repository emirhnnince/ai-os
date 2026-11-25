# AI-OS Sistem Mimarisi (Architecture Specification)

## 1. Genel Bakış

AI-OS, geleneksel monolitik işletim sistemlerinin aksine üç temel prensip üzerine kuruludur:
1. **Değişmez (Immutable) Çekirdek:** Sistemin işletim sistemi bileşenleri bozulmaya karşı salt okunur (read-only) `squashfs` formatında paketlenir.
2. **Kalıcı (Persistent) Veri Katmanı:** Kullanıcı profilleri, kişisel dosyalar, oturumlar ve modeller ayrılmış şifrelenebilir bir disk bölümünde tutulur.
3. **Ajan Tabanlı Kabuk (Agentic Shell Layer):** Kullanıcı etkileşiminin ana katmanı klasik masaüstü yöneticisi (GNOME/KDE) değil; hafif bir Wayland kompozitörü (örneğin Sway/Hyprland temelli) üzerinde koşan `AI-Shell` arayüzüdür.

```
+--------------------------------------------------------------------+
|                       KULLANICI ARAYÜZÜ                            |
|    AI-First Agentic Shell / Niyet Odaklı Komut & Ses & Web Paneli  |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
|                      AI ENGINE ORCHESTRATOR                        |
|   +--------------------------+    +----------------------------+   |
|   | OFFLINE SLM (Yerel Model)|    | CLOUD AI GATEWAY           |   |
|   | Qwen2.5-Coder / Gemma 2B |    | Google Gemini 1.5/2.0 API  |   |
|   | (llama.cpp / Ollama)     |    | (OpenAI / Claude / Groq)   |   |
|   +--------------------------+    +----------------------------+   |
|                  ^                               ^                 |
|                  +---------------+---------------+                 |
|                                  | (Bağlantı Denetimi & Router)    |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
|                    EYLEM & SİSTEM DAĞITICI (DISPATCHER)            |
|       Paket Yönetimi | Servisler | Ağ | Docker/Sandbox | Medya    |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
|                LINUX TEMEL SİSTEMİ (Debian Live Base)              |
|        Linux Kernel 6.x | Wayland | OverlayFS | Systemd            |
+--------------------------------------------------------------------+
                                  |
                                  v
+--------------------------------------------------------------------+
|                       DEPOLAMA KATMANI (USB)                       |
|   [Partition 1: EFI] [Partition 2: System.squashfs] [Part 3: Data] |
+--------------------------------------------------------------------+
```

---

## 2. Disk ve Bölüntüleme Şeması (Storage Layout)

Hedef USB bellek (minimum 16GB, önerilen 32GB-64GB 3.0+):

| Bölüm No | Dosya Sistemi | Etiket | Boyut | Açıklama |
|---|---|---|---|---|
| **Bölüm 1** | FAT32 | `EFI-BOOT` | ~512 MB | GRUB2 / Systemd-boot, UEFI & BIOS ikili önyükleyici |
| **Bölüm 2** | SquashFS / ext4 | `AIOS-SYS` | ~6-8 GB | Salt-okunur ana sistem imajı (A/B güncelleme için slotlu) |
| **Bölüm 3** | ext4 / LUKS | `AIOS-DATA` | Kalan Alan | Kalıcı kullanıcı verileri (`/home`, Docker alanları, yerel modeller) |

### Kalıcılık (Persistence) Nasıl Çalışır?
Linux çekirdeği boot parametresi olarak `persistence persistence-label=AIOS-DATA` alır.  
`overlayfs` mekanizması ile `AIOS-SYS` (salt-okunur alt katman) ile `AIOS-DATA` (okunur/yazılır üst katman) birleştirilir. Sistem dosyalarına yapılan değişiklikler doğrudan veri bölümüne kaydedilir, ana sistem asla çökmez veya bozulmaz.

---

## 3. Çok Kullanıcılı Mimari (Multi-User Isolation)

AI-OS, ortak bir USB bellekten birden fazla kullanıcının izole bir şekilde yararlanmasına olanak tanır:
- **Kullanıcı Profilleri:** Her kullanıcı için ayrı `/home/<user>` dizini.
- **İsteğe Bağlı Şifreleme:** Her profil kullanıcının belirlediği parola ile LUKS / fscrypt ile şifrelenebilir.
- **Bireysel AI Hafızası & Ayarları:** Her kullanıcının kendi API anahtarları, kendi e-eğitim ilerleme seviyesi ve favori yerel komutları saklanır.

---

## 4. Niyet Çözümleme (Intent-to-Execution Pipeline)

Kullanıcı bir istekte bulunduğunda (`"Python ile web kazıma öğrenmek istiyorum"` veya `"İnternetten bir film aç"`):

1. **Giriş:** Ses veya metin girişi AI Shell'e iletilir.
2. **Niyet Sınıflandırma (Intent Classification):**
   - Sistem Komutu (Ses açma, parlaklık, Wi-Fi bağlama)
   - Uygulama Başlatma / Yapılandırma (Browser, Media Player, IDE)
   - Öğrenme / Eğitim (Öğretici arayüzü başlatma)
   - Genel Soru-Cevap & Kod Üretimi
3. **Güvenlik & Yetkilendirme Kontrolü:**
   - Tehlikeli sistem komutları (`rm -rf`, disk biçimlendirme vb.) önce kullanıcı onayına sunulur.
4. **Yürütme:**
   - Linux D-Bus, systemd veya subprocess üzerinden ilgili araç çalıştırılır.
