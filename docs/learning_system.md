# E-Eğitim ve Dinamik Ortam Dönüştürücü (Learning Engine)

## 1. Konsept: "Dönüşebilen İşletim Sistemi"

Klasik işletim sistemlerinde kullanıcı kod yazmak istediğinde editör arar, derleyici indirir, path ayarları yapar ve kütüphaneleri manuel kurar. Bu süreç yeni başlayanları yıldırır.

**AI-OS'te sistem kullanıcıya uyum sağlar:**
Kullanıcı: *"Sıfırdan Python öğrenmek istiyorum"* dediğinde, AI-OS kendini bir **İnteraktif Kodlama Akademisine** dönüştürür.

---

## 2. Eğitim Modunun İşleyişi

```
+-----------------------------------------------------------+
|              KULLANICI: "Python öğrenmek istiyorum"       |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
|               AI ÖĞRETMEN (TUTOR AGENT)                   |
| 1. Seviye tespiti yapar ("Daha önce kod yazdınız mı?")    |
| 2. Gerekli araçları arka planda hazırlar:                 |
|    - Python 3.12, IPython, VSCode-OSS / Zed / Neovim      |
| 3. Eğitim dizini oluşturur: ~/workspace/python_egitimi    |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
|                  İNTERAKTİF ÇALIŞMA ALANI                 |
| Sol Panel: Yapay Zeka Eğitmeni (Görevler ve Anlatımlar)   |
| Orta Panel: Kod Editörü & REPL                            |
| Sağ Panel: Gerçek Zamanlı Çıktı & Hata Açıklayıcı         |
+-----------------------------------------------------------+
```

---

## 3. Aşamalı Eğitim Müfredatları (Mevcut Şablonlar)

1. **Python Temelleri (Başlangıç Seviyesi):**
   - Değişkenler, döngüler, fonksiyonlar.
   - Her konu sonunda AI anında küçük bir bulmaca/görev üretir (Örn: *"Kullanıcıdan yaşını alıp ehliyet alıp alamayacağını söyleyen programı yaz"*).
   - Kullanıcı hata yaptığında AI hatayı doğrudan çözmek yerine ipucu verir ve neden kaynaklandığını öğretir.

2. **Web Geliştirme (HTML/CSS/JS & FastAPI):**
   - Basit bir web sitesi hazırlama, tarayıcıda anında canlı önizleme.
   - AI arka planda anında yerel bir test sunucusu (`localhost:8000`) ayağa kaldırır.

3. **Yapay Zeka & Veri Analizi:**
   - Pandas, NumPy, veri görselleştirme.
   - Dahili JupyterLab ortamı anında otomatik konfigüre edilir.

---

## 4. Kullanıcı Deneyimi & Gamification (Oyunlaştırma)

- **Başarım Rozetleri (Badges):** İlk fonksiyonunu yazdı, 10 hatayı çözdü, ilk web sitesini yayına aldı.
- **Portfolyo Oluşturucu:** Kullanıcının yazdığı kodlar USB belleğindeki kalıcı Git reposunda (`~/workspace/portfolio`) saklanır; böylece kullanıcı USB'yi nereye götürürse götürsün projeleri yanındadır.
