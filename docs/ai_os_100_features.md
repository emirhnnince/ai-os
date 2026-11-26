# AI OS — 100+ Kapsamlı Özellik ve Sistem Mimarisi Şartnamesi (v2.1.0)

AI OS, USB bellek üzerinden çalışan, çift beyinli (Google Gemini 2.0 + Akıllı Çevrimdışı SLM), fotogerçekçi WebGL plazma arayüzlü ve otonom kendi kendini geliştiren yeni nesil bir işletim sistemidir.

---

## 🌟 Kategori 1: Yapay Zeka & Çift Çekirdek (Özellik 1 - 20)
1. **Çift Beyin Ağ Yönlendiricisi (Dual-Brain Gateway):** Ağ bağlantısını milisaniye seviyesinde dinler; internet varsa bulut Gemini'ye, yoksa yerel SLM'e kayıpsız yönlendirir.
2. **Akıllı Çevrimdışı SLM (Smart Offline SLM):** İnternetsiz ortamda matematik hesaplama, Python kod şablonları, dosya yönetimi ve Linux sistem komutlarını çözer.
3. **Otonom Öz-Gelişim (Self-Learning Memory):** Her kullanıcı etkileşimini analiz eder, başarılı yanıt kuralları türetir ve hafızasını kalıcı günceller.
4. **Aciliyet & Duygu Algılama (Sentiment Adaptor):** "Acil", "hızlı", "hemen" gibi kelimeleri tespit ederek yanıtları doğrudan ve kısa tutar.
5. **Dinamik Model Değiştirici:** Gemini 2.0 Flash, Gemini 1.5 Pro ve Yerel SLM arasında tek tıkla geçiş sağlar (`/api/settings/model`).
6. **Air-Gap Gizlilik & Stealth Modu:** Tek bir komutla ağ kartlarını sanal olarak izole eder, sıfır log hava boşluklu moda geçer.
7. **Yerel Hibrit RAG:** `docs/` ve öğrenilmiş kurallar üzerinde alt-milisaniye anahtar kelime araması yapar (`/api/rag/search`).
8. **Doğal Dil Niyet Ayrıştırıcı (Intent Engine):** Medya izleme, kod yazma, öğrenme ve sistem işlemlerini doğal dilden çıkarır.
9. **Kendi Kendini Onaran Sistem Ajanı (Self-Healing Agent):** Zombi süreçleri, bellek sızıntılarını ve çöken modülleri otomatik algılayıp yeniden başlatır.
10. **Bağlam Bellek Yönetimi (Context Window Manager):** Kullanıcının geçmiş sohbetlerini özetleyerek bağlama otomatik enjekte eder.
11. **Gelişmiş Formant Ses Sentezi:** Web Audio API formant filtre zinciriyle insan ses tonuna yakın Türkçe ses üretimi.
12. **300 Hz Göğüs Rezonansı (Chest Resonance Filter):** Biquad Low-Shelf filtresi ile sese dolgunluk ve sıcaklık katar.
13. **8 kHz Hava Varlığı (Presence Boost):** Konuşma anlaşılırlığını artıran yüksek frekans tepe filtresi.
14. **7 kHz De-Esser:** 'S', 'Ş', 'Ç' gibi sert patlamalı harfleri yumuşatan dinamik filtre.
15. **Dinamik Ses Kompresörü:** Ses seviyelerini insan konuşma dinamiğine eşitleyen Web Audio kompresörü.
16. **Nefes Simülasyonu:** Cümle başlangıçlarında 40ms'lik doğal duraklama ekler.
17. **İki Yönlü Kesintisiz Konuşma (Duplex Mode):** AI konuştuktan sonra mikrofonu otomatik açık tutarak akıcı diyalog sağlar.
18. **Gürültü Bastırmalı Ses Tanıma:** Web Speech API üzerinde arka plan seslerini filtreleyen gürültü eşiği.
19. **Çoklu Dil Ses Seçici:** Türkçe (Tolga/Emel), İngilizce ve sistemde kurulu en kaliteli nöral sesi otomatik seçer.
20. **Canlı Ses Dalga Spektrumu:** Konuşulan sesin frekansını gerçek zamanlı analiz edip küreye aktarır.

---

## 🫧 Kategori 2: WebGL Plazma Küre & Grafik Arayüz (Özellik 21 - 40)
21. **3D Simplex Gürültü Plazma Küresi:** WebGL GLSL fragment shader ile organik sıvı yüzey dalgalanması.
22. **Sub-Surface Scattering (Kenar Parıltısı):** Işığın küre yüzeyi altından geçip kenarlarda parlamasını sağlayan rim lighting.
23. **Fareye Duyarlı Speküler Yansıma:** Fare hareket ettikçe ışık kaynağının pozisyonunu dinamik güncelleyen Phong aydınlatma.
24. **Kromatik Renk Sapması (Prismatic Aberration):** Küre çeperlerinde kırmızı ve mavi ışığın kırılarak ayrılması.
25. **Durum Bazlı Renk Paletleri:** Hazır (Camgöbeği), Dinliyor (Zümrüt Yeşil), Düşünüyor (Mor), Konuşuyor (Altın Sarısı).
26. **Konuşma Sıvı Dalgalanması:** AI konuştuğunda orb yüzeyinde ses şiddetine göre radyal dalgalar oluşur.
27. **Düşünce Girdabı (Vortex Mode):** Sorgu işlenirken orb merkezinde dönen girdap animasyonu.
28. **Minimalist Zen Modu:** Tüm menüleri gizleyip yalnızca konuşan plazma küreyi bırakan odaklanma modu.
29. **Daktilo (Typewriter) Efekti:** Yapay zeka yanıtlarını harf harf akıcı şekilde ekrana basar.
30. **Cam Efektli (Glassmorphism) Baloncuk:** Arka planı 16px bulanıklaştıran yarı saydam mesaj kutusu.
31. **Yüksek Çözünürlüklü Uygulama İkonu:** 256x256 çok katmanlı, Windows görev çubuğunda ve masaüstünde net görünen ikon.
32. **HUD Telemetri Göstergesi:** CPU, bellek ve disk doluluk oranlarını canlı gösteren minimalist istatistik çubuğu.
33. **Hızlı Eylem Hapları (Quick Actions):** Tek tıkla sık sorulan soruları gönderen hap butonlar.
34. **Responsive Tasarım:** Kiosk ekranından mobil ve tablete kadar otomatik ölçeklenen CSS Grid ve Flex yapısı.
35. **Animasyonlu Yanıp Sönen Durum Işığı:** Sistemin hazır olduğunu gösteren nabız efektli LED gösterge.
36. **Toast Bildirim Yığını:** Sağ üst köşeden kayarak gelen şık bildirim kartları.
37. **Dahili Modal Pencere Motoru:** Sayfayı yenilemeden açılan ayarlar, kod, ağ ve eğitim pencereleri.
38. **Özelleştirilebilir Konuşma Hızı Slider'ı:** Kullanıcının ses hızını 0.6x ile 1.4x arasında ayarlamasını sağlar.
39. **Karanlık Mod Varsayılanı:** Gözü yormayan derin uzay mavisi (#030611) arayüz paleti.
40. **Düzgün Kaydırma ve İnce Scrollbar:** Arayüzün estetiğini bozmayan modern şeffaf kaydırma çubukları.

---

## 💾 Kategori 3: Taşınabilir USB, ISO & Donanım Yönetimi (Özellik 41 - 60)
41. **Debian Live-Build Altyapısı:** SquashFS ile sıkıştırılmış, 500 MB RAM'de bile çalışan ultra hafif Linux çekirdeği.
42. **Kalıcılık (Persistence) Desteği:** USB belleğe yazılan her dosya, AI hafızası ve kullanıcı profili kalıcı olarak saklanır.
43. **Toram (RAM'den Çalışma) Modu:** USB çıkarılsa bile sistemi tamamen RAM'e yükleyerek ultra yüksek hızda çalışma seçeneği.
44. **UEFI & Legacy BIOS Hibrit Boot:** Hem en yeni UEFI anakartlarda hem de eski BIOS bilgisayarlarda sorunsuz önyükleme.
45. **Windows Kurulum Sihirbazı (`AI-OS-USB-Installer.exe`):** ISO'yu otomatik indiren, USB'yi listeleyen yerel Windows uygulaması.
46. **Linux USB Yazıcı (`create_live_usb.py`):** Linux terminalinde tek komutla USB oluşturan Python betiği.
47. **PowerShell Otomatik Hazırlayıcı (`Write-AIOS-USB.ps1`):** PowerShell üzerinden GPT/EFI bölümlendirmesi yapan otomasyon.
48. **Otomatik A/B Yuvalı OTA Güncelleyici:** Sistem çalışırken arka planda yeni SquashFS imajını indirip sonraki açılışta yuva değiştirir.
49. **Wi-Fi Spektrum Radarı:** Çevredeki kablosuz ağları tarayıp sinyal gücüne göre sıralar.
50. **Wi-Fi QR Kod Üretici:** Bağlı olunan Wi-Fi ağını telefonla anında paylaşmak için standart QR metni üretir (`/api/wifi/qr`).
51. **Bluetooth Aygıt Tarayıcı ve Bağlantı:** Kulaklık, hoparlör ve klavyeleri otomatik tarayıp eşleştiren servis.
52. **Pil Sağlığı ve Güç Telemetrisi:** Kalan şarj yüzdesi, priz durumu ve pil ömrünü izleyen API (`/api/system/battery`).
53. **Zararlı Komut Filtresi (Safe Execution):** `rm -rf /`, `format` gibi yıkıcı komutları engelleyen güvenlik kalkanı.
54. **Donanım Metrikleri API'si:** İşlemci yükü, bellek kullanımı ve boş disk alanını JSON olarak dönen `/api/telemetry`.
55. **İzole Kod Sandbox'ı (Python/JS):** Tarayıcı veya sunucu üzerinden güvenli kod çalıştırma ortamı (`/api/sandbox/run`).
56. **Çoklu Kullanıcı (Guest, Local, Google):** İster misafir, ister şifreli yerel kullanıcı, ister Google hesabıyla oturum açma.
57. **SHA-256 Şifreli Kullanıcı Profilleri:** Yerel hesap şifrelerini tuzlanmış (salted) SHA-256 ile saklama.
58. **API Anahtarı Kasası:** Kullanıcının kendi Google Gemini API anahtarını güvenle saklayan şifreli profil alanı.
59. **İlk Kurulum Sihirbazı (OOBE):** İlk açılışta dil, bölge ve klavye düzenini seçtiren interaktif kurulum.
60. **Otomatik Kiosk Modu:** Canlı USB açıldığında masaüstünü tam ekran Wayland/Chromium kiosk olarak başlatma servisi.

---

## 🎓 Kategori 4: E-Öğrenme, Geliştirici Araçları & Database (Özellik 61 - 80)
61. **Merkezi SQLite Veritabanı (`ai_os_core.db`):** Kullanıcı, hafıza, telemetri ve ayarları tek bir hafif veritabanında toplar.
62. **Python 101 Kursu:** Değişkenler, döngüler, fonksiyonlar ve nesne yönelimli programlama interaktif eğitimi.
63. **Linux 101 Kursu:** Terminal komutları, dosya izinleri ve süreç yönetimi rehberi.
64. **AI 101 Kursu:** Makine öğrenmesi temelleri, prompt mühendisliği ve dil modellerinin çalışma prensipleri.
65. **Web 101 Kursu:** HTML5, CSS3, modern JavaScript ve API entegrasyonu eğitimi.
66. **Otomatik Kod Değerlendirme (Auto-Grader):** Öğrencinin yazdığı kodu sandbox'ta çalıştırıp doğru/yanlış testi yapan `/api/learning/evaluate`.
67. **Dahili JavaScript Çalıştırıcı:** Tarayıcı tarafında `eval` korumalı hızlı JS algoritma test alanı.
68. **Sanal Test Ortamı (QEMU / VirtualBox Sandbox):** Bilgisayarı kapatmadan ISO'yu sanal makinede test etme kılavuzu (`/api/virtual-sandbox/specs`).
69. **Medya Niyeti Ayrıştırıcı (Film/Müzik):** "Film izlemek istiyorum" dendiğinde platform seçenekleri (Netflix, YouTube, Yerel Oynatıcı) sunan akıllı kart.
70. **Çoklu Dil Desteği (i18n):** Türkçe, İngilizce ve Almanca çeviri dosyaları (`data/i18n/translations.json`).
71. **Otomatik Dil Algılama:** Kullanıcının tarayıcı veya sistem diline göre arayüzü otomatik yerelleştirme.
72. **Geri Bildirimle Öğrenme (Human-in-the-Loop):** Kullanıcının yanıtı beğenip beğenmediğini analiz eden `/api/self-learning/feedback`.
73. **GitHub Release Entegrasyonu:** En son derlenen ISO dosyalarını doğrudan GitHub sürümlerine aktarma altyapısı.
74. **Vercel İndirme ve Güncelleme Portalı:** Sistemin web sitesini ve OTA manifest dosyasını sunan küresel CDN.
75. **CORS Destekli Güncelleme Manifesti:** Tarayıcıların ve işletim sisteminin `manifest.json` dosyasına her yerden erişebilmesi.
76. **Otomatik SHA-256 Sağlama Doğrulaması:** İndirilen ISO veya SquashFS dosyasının bozulmadığını kontrol eden hash mekanizması.
77. **Sistem Günlüğü (Event Logger):** Önemli donanım ve oturum olaylarını SQLite'a zaman damgalı kaydeden yapı.
78. **WebSocket Çift Yönlü İletişim Hattı:** `/ws/chat` üzerinden gecikmesiz ses ve metin veri akışı.
79. **Hafif Bellek Tüketimi:** Başlangıçta 250 MB'tan az RAM tüketen optimize edilmiş FastAPI backend'i.
80. **Arka Plan Görev Yöneticisi:** Uzun süren indirme ve disk yazma işlemlerini arayüzü dondurmadan yürüten asenkron yapı.

---

## 🚀 Kategori 5: Genişletilmiş Özellikler & Ekosistem (Özellik 81 - 100+)
81. **Sanal Asistan Kısayol Tuşları:** `Ctrl+Space` veya `Super+A` ile her yerden yapay zekayı öne çağırma.
82. **Dahili Sembolik Matematik Çözücü:** Basit cebir ve aritmetik işlemlerini internet olmadan anında çözme.
83. **Akıllı Dosya Arama:** USB içindeki proje ve dökümanları doğal dil sorgusuyla bulma.
84. **Otomatik Yedekleme Servisi:** Kalıcılık alanını tek tıkla sıkıştırıp `.tar.gz` olarak dışa aktarma.
85. **Sıcaklık ve Termal Koruma İzleyicisi:** İşlemci aşırı ısındığında yapay zekanın kullanıcıyı uyarması.
86. **Hızlı Model Sıcaklığı Ayarı (Temperature Control):** Yaratıcı yanıtlar veya kesin kodlama yanıtları için ayar.
87. **Özel Sistem İstemleri (Custom System Prompts):** Kullanıcının AI karakterini özelleştirebilmesi.
88. **İnteraktif Web Sitesi Video Simülatörleri:** Web sitesinde adım adım kurulum adımlarını canlandıran interaktif player'lar.
89. **YouTube / Video Rehber Entegrasyonu:** Kurulum videolarının web sitesinde gömülü gösterilmesi.
90. **Doğrudan İndirme MIME Türü:** Tarayıcının dosyayı kod olarak açmasını engelleyen `application/octet-stream` başlığı.
91. **Çoklu Disk Biçimlendirme Koruması:** Sistem diskini yanlışlıkla silmeyi engelleyen USB tip doğrulama filtresi.
92. **GPT / MBR Dinamik Bölümlendirici:** UEFI için FAT32 önyükleme ve kalıcılık için EXT4 bölümünü ayıran yapı.
93. **Görsel Kurulum İlerleme Çubuğu:** EXE sihirbazında dosya kopyalama durumunu gösteren pürüzsüz ProgressBar.
94. **Windows SmartScreen Uyumlu Dijital İmza:** Authenticode tabanlı yayıncı tanımlama sertifikası.
95. **Sanal Kiosk Başlangıç Ekranı:** Açılışta doğrudan canlı plazma küreyi açan karşılama sayfası.
96. **Hata Yakalayıcı ve Kurtarma Modu (Failsafe Boot):** Sistem bozulursa güvenli modda açılan kurtarma çekirdeği.
97. **Sıfır Kurulum Gereksinimi:** Bilgisayarın sabit diskine hiçbir şey yazmadan doğrudan USB'den çalışma.
98. **GitHub Actions Otomatik CI/CD:** Her kod güncellemesinde sıfırdan Debian ISO imajını derleyen bulut hattı.
99. **Evrensel Donanım Sürücüleri (Universal Drivers):** En yaygın Wi-Fi ve Bluetooth yongalarını içeren Linux firmware paketi.
100. **Açık Kaynak ve Modüler Mimari:** İsteyen herkesin yeni eklenti ve dil modelleri ekleyebileceği temiz Python/JS kod tabanı.
