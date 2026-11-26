$ErrorActionPreference = 'Stop'
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=AI OS Open Source Project, O=AI OS, C=TR" -CertStoreLocation "Cert:\CurrentUser\My" -HashAlgorithm "SHA256"
$exePath = "C:\Users\incey\.gemini\antigravity\scratch\ai-os\website\downloads\AI-OS-USB-Installer.exe"
try {
    Set-AuthenticodeSignature -FilePath $exePath -Certificate $cert -TimestampServer "http://timestamp.digicert.com"
} catch {
    Set-AuthenticodeSignature -FilePath $exePath -Certificate $cert
}
$sig = Get-AuthenticodeSignature $exePath
Write-Host "SIGNATURE_STATUS:" $sig.Status
Write-Host "SIGNER:" $sig.SignerCertificate.Subject
