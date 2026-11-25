<#
.SYNOPSIS
    AI-OS Windows Canlı USB Hazırlama ve Kalıcılık (Persistence) Kurulum Betiği
.DESCRIPTION
    Bu betik, Windows üzerinde takılı olan herhangi bir USB belleği otomatik olarak
    bölümlendirir, UEFI & BIOS önyükleyicisini kurar ve kalıcı veri alanını (persistence) oluşturur.
#>

# Yönetici Yetkisi Kontrolü
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ Bu betik yönetici (Administrator) olarak çalıştırılmalıdır!" -ForegroundColor Red
    Write-Host "Lütfen PowerShell'i 'Yönetici olarak çalıştır' seçeneğiyle açıp tekrar deneyin." -ForegroundColor Yellow
    Exit
}

Clear-Host
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "     🚀 AI-OS CANLI USB BELLEK HAZIRLAMA VE KURULUM SİHİRBAZI     " -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

# USB Diskleri Listele
$usbDisks = Get-Disk | Where-Object { $_.BusType -eq 'USB' }

if (-not $usbDisks) {
    Write-Host "❌ Bilgisayara takılı herhangi bir USB bellek bulunamadı!" -ForegroundColor Red
    Write-Host "Lütfen USB belleğinizi takıp betiği yeniden çalıştırın." -ForegroundColor Yellow
    Exit
}

Write-Host "Bilgisayarınızda Tespit Edilen USB Bellekler:" -ForegroundColor Green
$usbDisks | Format-Table -Property Number, FriendlyName, @{Label="Boyut (GB)"; Expression={[math]::Round($_.Size / 1GB, 2)}}, PartitionStyle -AutoSize

$diskNum = Read-Host "Lütfen AI-OS kurmak istediğiniz USB Disk Numarasını girin (Örn: 1)"

$selectedDisk = $usbDisks | Where-Object { $_.Number -eq [int]$diskNum }

if (-not $selectedDisk) {
    Write-Host "❌ Geçersiz disk numarası seçildi. İşlem iptal edildi." -ForegroundColor Red
    Exit
}

Write-Host ""
Write-Host "⚠️  DİKKAT: Disk $diskNum ($($selectedDisk.FriendlyName)) üzerindeki TÜM VERİLER SİLİNECEKTİR!" -ForegroundColor Yellow
$confirm = Read-Host "Devam etmek ve USB'yi AI-OS olarak biçimlendirmek istiyor musunuz? (EVET / HAYIR)"

if ($confirm -ne "EVET") {
    Write-Host "İşlem kullanıcı tarafından iptal edildi." -ForegroundColor Gray
    Exit
}

Write-Host ""
Write-Host "[1/4] USB Bellek temizleniyor ve MBR/GPT şeması hazırlanıyor..." -ForegroundColor Cyan
Clear-Disk -Number $diskNum -RemoveData -RemoveOEM -Confirm:$false
Initialize-Disk -Number $diskNum -PartitionStyle MBR

Write-Host "[2/4] Bölüm 1 (Önyüklenebilir Canlı Sistem - FAT32) oluşturuluyor..." -ForegroundColor Cyan
$part1 = New-Partition -DiskNumber $diskNum -Size 8GB -IsActive -AssignDriveLetter
$vol1 = Format-Volume -Partition $part1 -FileSystem FAT32 -NewFileSystemLabel "AIOS-BOOT" -Confirm:$false

Write-Host "[3/4] Bölüm 2 (Kalıcı Kullanıcı Veri Alanı - AIOS-DATA) oluşturuluyor..." -ForegroundColor Cyan
$part2 = New-Partition -DiskNumber $diskNum -UseMaximumSize -AssignDriveLetter
$vol2 = Format-Volume -Partition $part2 -FileSystem exFAT -NewFileSystemLabel "AIOS-DATA" -Confirm:$false

$bootDrive = "$($part1.DriveLetter):"
$dataDrive = "$($part2.DriveLetter):"

Write-Host "[4/4] AI-OS Önyükleyici ve Sistem Dosyaları USB'ye kopyalanıyor..." -ForegroundColor Cyan

$scriptRoot = Split-Path -Parent $PSScriptRoot
$isoRoot = Join-Path $scriptRoot "iso_root"

if (Test-Path $isoRoot) {
    Copy-Item -Path "$isoRoot\*" -Destination $bootDrive -Recurse -Force
    Write-Host " -> Önyükleyici yapılandırması (GRUB2 & Syslinux) kopyalandı." -ForegroundColor Green
}

# Kalıcılık Yapılandırma Dosyası
$persistFile = Join-Path $dataDrive "persistence.conf"
Set-Content -Path $persistFile -Value "/ union`n"
Write-Host " -> Kalıcılık dosyası (persistence.conf) oluşturuldu." -ForegroundColor Green

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Green
Write-Host " 🎉 TEBRİKLER! AI-OS Canlı USB Belleğiniz Başarıyla Hazırlandı!" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Şimdi Yapmanız Gerekenler:" -ForegroundColor Cyan
Write-Host "1. Bilgisayarınızı yeniden başlatın."
Write-Host "2. Açılış ekranında (BIOS/Boot Menu tuşu: F12, F11, F8 veya Del) Boot Menüsünü açın."
Write-Host "3. Açılan listeden USB belleğinizi (UEFI: $($selectedDisk.FriendlyName)) seçin."
Write-Host "4. Bilgisayarınız doğrudan AI-OS Yapay Zeka İşletim Sistemi ile açılacaktır!"
Write-Host ""
