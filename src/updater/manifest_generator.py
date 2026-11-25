"""
AI-OS Sürüm ve Güncelleme Manifest Üreticisi (Release Manifest Builder)
Geliştiricinin yeni bir AI-OS sürümü çıkardığında SHA-256'ları hesaplayıp
kullanıcıların OTA ile alabileceği manifest.json dosyasını üretmesini sağlar.
"""

import os
import sys
import json
import hashlib

def calculate_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def create_release_manifest(
    version: str,
    squashfs_path: str,
    release_notes: str,
    output_path: str = os.path.join("website", "manifest.json"),
    cdn_url: str = "",
    iso_path: str = "",
    iso_url: str = ""
):
    sha = calculate_sha256(squashfs_path) if os.path.exists(squashfs_path) else "pending-ci-build"
    iso_sha = calculate_sha256(iso_path) if iso_path and os.path.exists(iso_path) else "pending-ci-build"
    file_size = os.path.getsize(squashfs_path) if os.path.exists(squashfs_path) else 0
    iso_size = os.path.getsize(iso_path) if iso_path and os.path.exists(iso_path) else 0

    manifest = {
        "version": version,
        "codename": "Plasma Core",
        "release_date": "2026-11-25",
        "release_notes": release_notes,
        "squashfs_size_bytes": file_size,
        "sha256": sha,
        "iso_size_bytes": iso_size,
        "iso_sha256": iso_sha,
        "image_url": cdn_url or f"https://github.com/emirhnnince/ai-os/releases/download/v{version}/filesystem.squashfs",
        "iso_url": iso_url or f"https://github.com/emirhnnince/ai-os/releases/download/v{version}/ai-os-v2.1.0-amd64.iso".replace("2.1.0", version),
        "minimum_compatible_version": "0.1.0"
    }

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)

    print(f"✅ Sürüm manifesti başarıyla oluşturuldu: {output_path}")
    print(f"   Sürüm: {version}")
    print(f"   SHA-256: {sha}")

if __name__ == "__main__":
    create_release_manifest(
        version="2.1.0",
        squashfs_path="nonexistent.squashfs",
        release_notes="WebGL Fotogerçekçi Plazma Küre, Formant Ses Motoru, Kendi Kendini Geliştiren Hafıza ve Çoklu Kullanıcı Kurulum Sihirbazı."
    )
