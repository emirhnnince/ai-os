#!/usr/bin/env python3
"""
AI-OS USB Hazırlama ve Kalıcılık (Persistence) Kurulum Aracı
Herhangi bir USB belleği seçilen boyutta bölüntüler:
1. EFI Boot (FAT32)
2. Sistem İmajı (SquashFS)
3. Kalıcı Veri (ext4 / LUKS Persistence - persistence.conf)
"""

import os
import sys
import subprocess
import shutil

def run_cmd(cmd):
    print(f"[*] Çalıştırılıyor: {' '.join(cmd)}")
    subprocess.check_call(cmd)

def setup_usb(target_device: str, iso_path: str):
    if os.geteuid() != 0:
        print("❌ Bu işlem yönetici (root/sudo) yetkisi gerektirir.")
        sys.exit(1)

    if not os.path.exists(target_device):
        print(f"❌ Hedef aygıt bulunamadı: {target_device}")
        sys.exit(1)

    print("=============================================================")
    print(f"  DİKKAT: {target_device} üzerindeki TÜM VERİLER SİLİNECEKTİR! ")
    print("=============================================================")
    confirm = input("Devam etmek istiyor musunuz? (evet/hayir): ").strip().lower()
    if confirm != "evet":
        print("İptal edildi.")
        sys.exit(0)

    # 1. ISO İmajını USB'ye yaz
    print(f"[1/3] ISO İmajı yazılıyor: {iso_path} -> {target_device}")
    run_cmd(["dd", f"if={iso_path}", f"of={target_device}", "bs=4M", "status=progress", "conv=fsync"])

    # 2. Kalıcılık Bölümü Oluştur (Partition 3)
    part_target = f"{target_device}3"
    print(f"[2/3] Kalıcılık bölümü oluşturuluyor: {part_target}")
    run_cmd(["parted", target_device, "--script", "mkpart", "primary", "ext4", "8GB", "100%"])
    run_cmd(["mkfs.ext4", "-F", "-L", "AIOS-DATA", part_target])

    # 3. Persistence.conf Yapılandırması
    print("[3/3] Kalıcılık dosyası (persistence.conf) yazılıyor...")
    mount_dir = "/tmp/aios_persist_mount"
    os.makedirs(mount_dir, exist_ok=True)
    run_cmd(["mount", part_target, mount_dir])
    
    with open(os.path.join(mount_dir, "persistence.conf"), "w") as f:
        f.write("/ union\n")
    
    run_cmd(["umount", mount_dir])
    print("\n🎉 TEBRİKLER! AI-OS Canlı USB Belleğiniz Hazır.")
    print("Artık herhangi bir bilgisayarı bu USB'den başlatabilirsiniz.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: sudo python3 create_live_usb.py /dev/sdX /yol/aios.iso")
    else:
        setup_usb(sys.argv[1], sys.argv[2])
