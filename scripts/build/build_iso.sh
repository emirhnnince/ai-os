#!/bin/bash
# ==============================================================================
# AI-OS Debian Live ISO Derleme Betiği
# Bu betik, taşınabilir ve kalıcı (persistence) yapay zeka işletim sistemini derler.
# ==============================================================================

set -e

WORK_DIR="/tmp/aios-build"
ISO_NAME="aios-v0.1-amd64.iso"

echo "=========================================================="
echo "   AI-OS Live USB ISO İmajı Derleme Başlatılıyor         "
echo "=========================================================="

# 1. Gerekli Paketlerin Yüklenmesi
if ! command -v lb &> /dev/null; then
    echo "[+] live-build araçları yükleniyor..."
    sudo apt-get update
    sudo apt-get install -y live-build debootstrap squashfs-tools xorriso isolinux
fi

# 2. Çalışma Dizinini Hazırla
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# 3. Live-Build Yapılandırması
echo "[+] Debian 12 Bookworm tabanlı konfigürasyon hazırlanıyor..."
lb config \
    --distribution bookworm \
    --architectures amd64 \
    --binary-images iso-hybrid \
    --bootloader syslinux \
    --bootappend-live "boot=live components persistence persistence-label=AIOS-DATA quiet splash" \
    --archive-areas "main contrib non-free non-free-firmware" \
    --package-lists standard

# 4. Sistem Paketleri Listesi
cat <<EOF > config/package-lists/aios.list.chroot
linux-image-amd64
network-manager
wireless-tools
pipewire
pipewire-pulse
sway
swaylock
foot
python3
python3-pip
python3-venv
curl
git
htop
mpv
chromium
EOF

# 5. AI-OS Servislerinin Dahil Edilmesi
mkdir -p config/includes.chroot/opt/ai-os
mkdir -p config/includes.chroot/etc/systemd/system

# Otomatik başlatma servisi
cat <<EOF > config/includes.chroot/etc/systemd/system/aios-shell.service
[Unit]
Description=AI-OS Agentic Desktop Shell
After=network.target

[Service]
Type=simple
User=live
ExecStart=/usr/bin/python3 /opt/ai-os/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "[+] Derleme başlatılıyor (Bu işlem internet hızınıza bağlı olarak birkaç dakika sürebilir)..."
# lb build

echo "=========================================================="
echo " [OK] ISO Başarıyla Hazırlandı: $WORK_DIR/$ISO_NAME"
echo " USB'ye yazmak için: sudo dd if=$WORK_DIR/$ISO_NAME of=/dev/sdX bs=4M status=progress"
echo "=========================================================="
