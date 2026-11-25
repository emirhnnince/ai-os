#!/bin/bash
# ==============================================================================
# AI-OS Tam İşletim Sistemi ve Bootable ISO Derleme Hattı (Debian Bookworm)
# Bu betik sıfırdan bir Linux Çekirdeği, RootFS, Wayland Kiosk ve
# USB'den doğrudan önyüklenebilen hibrit bir ISO dosyası üretir.
# ==============================================================================

set -e

if [ "$(id -u)" -ne 0 ]; then
    echo "❌ Bu derleme betiği root yetkisi gerektirir: sudo ./build_full_os.sh"
    exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BUILD_DIR="/tmp/aios_os_build"
CHROOT_DIR="$BUILD_DIR/chroot"
ISO_DIR="$BUILD_DIR/iso"
OUTPUT_ISO="$PROJECT_ROOT/aios-live-v0.1-amd64.iso"

echo "=================================================================="
echo "   🚀 AI-OS BOOTABLE LINUX İŞLETİM SİSTEMİ DERLEME BAŞLATILDI    "
echo "=================================================================="

# 1. Gerekli Derleme Araçları
echo "[1/7] Gerekli sistem paketleri kontrol ediliyor..."
apt-get update
apt-get install -y debootstrap squashfs-tools xorriso isolinux syslinux-efi grub-pc-bin grub-efi-amd64-bin mtools dosfstools

# 2. Çalışma Dizinlerini Temizle ve Oluştur
rm -rf "$BUILD_DIR"
mkdir -p "$CHROOT_DIR" "$ISO_DIR/live" "$ISO_DIR/boot/grub" "$ISO_DIR/EFI/BOOT"

# 3. Temel Linux Sistemi Kurulumu (Debootstrap Debian 12)
echo "[2/7] Debian 12 (Bookworm) 64-bit temel dosya sistemi (RootFS) indiriliyor..."
debootstrap --arch=amd64 bookworm "$CHROOT_DIR" http://deb.debian.org/debian/

# 4. Chroot Ortamını Yapılandırma
echo "[3/7] Linux Çekirdeği, Sürücüler, Wayland ve Ağ Servisleri kuruluyor..."

mount --bind /dev "$CHROOT_DIR/dev"
mount --bind /proc "$CHROOT_DIR/proc"
mount --bind /sys "$CHROOT_DIR/sys"

cat << 'CHROOT_EXEC' | chroot "$CHROOT_DIR" /bin/bash
set -e

# Depoları Güncelle
cat <<EOF > /etc/apt/sources.list
deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
EOF

apt-get update
export DEBIAN_FRONTEND=noninteractive

# Donanım, Çekirdek, Wi-Fi Firmware ve Live Boot Paketleri
apt-get install -y --no-install-recommends \
    linux-image-amd64 \
    live-boot \
    live-config \
    firmware-linux-free \
    firmware-misc-nonfree \
    network-manager \
    wireless-tools \
    pipewire \
    pipewire-pulse \
    cage \
    chromium \
    python3 \
    python3-pip \
    python3-venv \
    sudo \
    curl \
    git \
    nano \
    systemd-sysv

# Canlı Kullanıcıyı Oluştur (live / live)
useradd -m -s /bin/bash -G sudo,video,audio live
echo "live:live" | chpasswd
echo "live ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Hostname Tanımla
echo "ai-os" > /etc/hostname

# Ağ Ayarı
systemctl enable NetworkManager

CHROOT_EXEC

# 5. AI-OS Kodlarının Sisteme Gömülmesi
echo "[4/7] AI-OS Ajanik Motoru ve Web Kiosk Arayüzü sisteme yerleştiriliyor..."
mkdir -p "$CHROOT_DIR/opt/ai-os"
cp -r "$PROJECT_ROOT/src" "$CHROOT_DIR/opt/ai-os/"
cp -r "$PROJECT_ROOT/config" "$CHROOT_DIR/opt/ai-os/"
cp "$PROJECT_ROOT/main.py" "$CHROOT_DIR/opt/ai-os/"
cp "$PROJECT_ROOT/requirements.txt" "$CHROOT_DIR/opt/ai-os/"

# Bağımlılıkları chroot içinde kur
chroot "$CHROOT_DIR" /bin/bash -c "pip3 install --no-cache-dir -r /opt/ai-os/requirements.txt --break-system-packages"

# 6. Otomatik Başlatma Servisleri (Kiosk & AI-OS Server)
echo "[5/7] Systemd servisleri (Kiosk ve Canlı Sunucu) konfigüre ediliyor..."

# AI-OS Backend Sunucu Servisi
cat << 'EOF' > "$CHROOT_DIR/etc/systemd/system/aios-server.service"
[Unit]
Description=AI-OS Agentic Backend Server
After=network.target

[Service]
Type=simple
User=live
WorkingDirectory=/opt/ai-os
ExecStart=/usr/bin/python3 -m src.ui.server
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Wayland Cage Kiosk Otomatik Masaüstü Servisi
cat << 'EOF' > "$CHROOT_DIR/etc/systemd/system/aios-kiosk.service"
[Unit]
Description=AI-OS Fullscreen Wayland Kiosk
After=aios-server.service
Wants=aios-server.service

[Service]
Type=simple
User=live
Environment=XDG_RUNTIME_DIR=/run/user/1000
Environment=WAYLAND_DISPLAY=wayland-0
ExecStartPre=/bin/sleep 2
ExecStart=/usr/bin/cage -- /usr/bin/chromium --no-sandbox --kiosk --noerrdialogs --disable-infobars http://localhost:8080
Restart=always

[Install]
WantedBy=graphical.target
EOF

chroot "$CHROOT_DIR" systemctl enable aios-server.service
chroot "$CHROOT_DIR" systemctl enable aios-kiosk.service
chroot "$CHROOT_DIR" systemctl set-default graphical.target

# Kernel ve Initrd dosyalarını ISO klasörüne kopyala
cp "$CHROOT_DIR"/boot/vmlinuz-* "$ISO_DIR/live/vmlinuz"
cp "$CHROOT_DIR"/boot/initrd.img-* "$ISO_DIR/live/initrd.img"

# Chroot bağlantılarını sök (Unmount)
umount "$CHROOT_DIR/sys"
umount "$CHROOT_DIR/proc"
umount "$CHROOT_DIR/dev"

# 7. Sıkıştırılmış Salt-Okunur Dosya Sistemi Üretimi (SquashFS)
echo "[6/7] RootFS SquashFS imajı sıkıştırılıyor (XZ Yüksek Sıkıştırma)..."
mksquashfs "$CHROOT_DIR" "$ISO_DIR/live/filesystem.squashfs" -comp xz -b 1048576 -Xbcj x86

# GRUB ve EFI Önyükleyici Yapılandırmasını Kopyala
cp "$PROJECT_ROOT/iso_root/boot/grub/grub.cfg" "$ISO_DIR/boot/grub/grub.cfg"

# 8. Hibrit Bootable ISO Dosyasını Derle (xorriso)
echo "[7/7] UEFI & Legacy BIOS uyumlu hibrit bootable ISO oluşturuluyor..."
xorriso -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "AIOS_LIVE" \
    -output "$OUTPUT_ISO" \
    -eltorito-boot boot/grub/bios.img \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    --eltorito-catalog boot/grub/boot.cat \
    -eltorito-alt-boot \
    -e EFI/BOOT/BOOTX64.EFI \
    -no-emul-boot \
    -isohybrid-gpt-basdat \
    "$ISO_DIR" 2>/dev/null || {
        # Sadeleştirilmiş xorriso komutu
        xorriso -as mkisofs \
            -r -V "AIOS_LIVE" \
            -J -l -b isolinux/isolinux.bin \
            -c isolinux/boot.cat \
            -no-emul-boot -boot-load-size 4 -boot-info-table \
            -o "$OUTPUT_ISO" "$ISO_DIR"
    }

echo "=================================================================="
echo " 🎉 İŞLEM TAMAMLANDI! Önyüklenebilir İşletim Sistemi İmajı Hazır:"
echo " 📁 $OUTPUT_ISO"
echo "=================================================================="
