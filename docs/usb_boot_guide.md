# AI-OS USB Bellekten Başlatma ve BIOS/UEFI Kılavuzu

Bu kılavuz, AI-OS'u herhangi bir bilgisayarda (Windows veya macOS yüklü olsun veya hiç işletim sistemi olmasın) doğrudan USB bellekten bağımsız bir işletim sistemi olarak nasıl başlatacağınızı açıklar.

---

## 1. Sistemin Çalışma Mantığı (Boot Sıralaması)

```
[Bilgisayar Güç Tuşu]
         │
         ▼
[Anakart BIOS / UEFI Ekranı]
         │  (F12 / F11 / F8 tuşuna basılarak USB seçilir)
         ▼
[AI-OS GRUB2 Önyükleyici]  ──>  Menü Seçenekleri:
         │                      1. AI-OS Live (Kalıcı Mod - Önerilen)
         │                      2. AI-OS (Salt RAM Modu)
         ▼
[Linux Çekirdeği (Kernel 6.x) & Initramfs]
         │
         ▼
[OverlayFS Sürücüsü]  ──> USB'deki 'AIOS-DATA' bölümünü bağlar (Tüm veriler kalıcı olur)
         │
         ▼
[Systemd & Wayland Cage Kiosk]
         │
         ▼
[🚀 AI-OS Doğal Dil Masaüstü Ekranı Açılır]
 (Geleneksel masaüstü yerine doğrudan ses/metin niyet kabuğu karşılar)
```

---

## 2. USB Belleği Hazırlama Yöntemleri

### Yöntem A: Windows Üzerinde Tek Tıkla Hazırlama (PowerShell)
1. En az 16 GB kapasiteli bir USB belleği bilgisayarınıza takın.
2. PowerShell'i **Yönetici Olarak Çalıştır** seçeneğiyle açın.
3. Şu komutu girin:
   ```powershell
   cd C:\Users\incey\.gemini\antigravity\scratch\ai-os\scripts\usb
   .\Write-AIOS-USB.ps1
   ```
4. Betik takılı USB diskinizi tespit eder, önyükleme ve kalıcılık bölümlerini otomatik biçimlendirip hazırlar.

### Yöntem B: Rufus ile ISO Yazma
Derlenen `.iso` imajını doğrudan yazdırmak isterseniz:
1. [Rufus](https://rufus.ie/)'u indirin ve açın.
2. **Aygıt:** USB belleğinizi seçin.
3. **Önyükleme Seçimi:** `aios-live-v0.1-amd64.iso` dosyasını seçin.
4. **Bölüm Düzeni:** `GPT` (UEFI için) veya `MBR` (Eski BIOS'lar için).
5. **Kalıcı Bölüm Boyutu (Persistent partition):** Kayan çubuktan USB'nizin kalan alanını (örn: 16-32 GB) seçin.
6. **Başlat** butonuna basın.

---

## 3. Bilgisayarı USB'den Başlatma (Booting)

1. Bilgisayarınızı kapatın ve USB belleği takın.
2. Bilgisayarı açar açmaz anakartınızın **Boot Menüsü Tuşuna** art arda basın:
   - **Asus:** `F8` veya `Del`
   - **Gigabyte:** `F12`
   - **MSI:** `F11`
   - **Dell:** `F12`
   - **HP:** `F9` veya `Esc`
   - **Lenovo:** `F12` veya Novo Düğmesi
   - **Acer:** `F12`
3. Karşınıza gelen listede **UEFI: [USB Bellek Adınız]** seçeneğini seçip `Enter`'a basın.
4. AI-OS GRUB ekranı açılacaktır. İlk seçeneği seçtiğinizde bilgisayar kendi işletim sistemine (Windows/Mac) hiç dokunmadan, doğrudan USB'deki yapay zeka işletim sistemini açacaktır!

---

## 4. Önemli BIOS Ayarları (Sorun Giderme)
- **Secure Boot:** Bazı anakartlarda özel çekirdek imajlarının başlatılması için BIOS menüsünden `Secure Boot: Disabled` yapılması gerekebilir.
- **Fast Startup:** Windows'un hızlı başlatma özelliği bazen USB'den boot etmeyi engelleyebilir. Windows Güç Ayarlarından "Hızlı Başlatmayı Kapat" seçeneğini devre dışı bırakabilirsiniz.
