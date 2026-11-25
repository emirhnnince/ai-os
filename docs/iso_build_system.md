# ISO Derleme & USB Kurulum Sistemi (Build & Deployment)

## 1. Temel Linux Dağıtımı Seçimi

AI-OS, hafifliği, kaya gibi sağlam kararlılığı ve geniş paket ekosistemi nedeniyle **Debian 12 (Bookworm) Live** altyapısını veya **Arch Linux (Archiso)** tabanını kullanır.
İlk kararlı referans sürüm için **Debian Live-Build (`live-build`)** tercih edilmiştir:
- Yüksek donanım uyumluluğu (Intel/AMD, eski/yeni anakartlar).
- Düşük kaynak tüketimi (boşta 300-500 MB RAM).
- Kolay özelleştirilebilir ISO yapılandırması.

---

## 2. Derleme Ön Koşulları

ISO derleme süreci bir Linux ortamında (Ubuntu, Debian veya WSL2) gerçekleştirilir:

```bash
sudo apt-get update
sudo apt-get install -y live-build debootstrap squashfs-tools xorriso isolinux
```

---

## 3. USB Bölüntüleme ve Hazırlama (USB Persistence Kurulumu)

Kullanıcının USB belleğine yazması için iki yöntem sunulur:
1. **Hazır İmaj Yazıcı (BalenaEtcher / Rufus / dd):** İndirilen hibrit ISO doğrudan belleğe yazdırılır.
2. **Kalıcılık Bölümü Oluşturma Betiği (`setup_usb.sh`):**

```bash
# USB disk örneğin /dev/sdb olsun:
# 1. ISO'yu USB'ye yaz
sudo dd if=aios-v1.0-amd64.iso of=/dev/sdb bs=4M status=progress conv=fsync

# 2. Geriye kalan boş alanda kalıcılık bölümü oluştur
sudo parted /dev/sdb --script mkpart primary ext4 8GB 100%
sudo e2label /dev/sdb3 persistence
sudo mkfs.ext4 -L persistence /dev/sdb3

# 3. Persistence ayar dosyasını ekle
sudo mount /dev/sdb3 /mnt
echo "/ union" | sudo tee /mnt/persistence.conf
sudo umount /mnt
```

---

## 4. Güvenli Atomik Güncelleme Sistemi (Atomic OTA Update)

Geleneksel `apt-get upgrade` işlemleri elektrik kesintisinde veya USB çekildiğinde sistemi bozabilir.
AI-OS bunun yerine **İki Yuvalı (A/B) SquashFS İmaj Değiştirme** mimarisi kullanır:

```
USB Bellek (Bölüm 2):
├── /live/
│   ├── system-A.squashfs   (Şu an çalışan v1.0 imajı)
│   ├── system-B.squashfs   (Arka planda indirilen yeni v1.1 imajı)
│   └── current_slot        (İşaretçi: "A" veya "B")
```

1. Yeni bir sürüm çıktığında sistem arka planda `system-B.squashfs` dosyasını indirir ve SHA256 imzasını doğrular.
2. `current_slot` dosyasını `B` olarak günceller.
3. Kullanıcı sistemi yeniden başlattığında yeni sürüm açılır.
4. Herhangi bir boot sorunu yaşanırsa, GRUB menüsünden tek tuşla önceki sürüme (A slotuna) geri dönülebilir.
5. Kullanıcı verileri (Bölüm 3'teki `persistence`) bağımsız olduğu için güncellemelerden asla etkilenmez.
