$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert | Select-Object -First 1
if (-not $cert) {
    $cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=AI OS Open Source Project, O=AI OS, C=TR" -CertStoreLocation "Cert:\CurrentUser\My"
}
$exe = "C:\Users\incey\.gemini\antigravity\scratch\ai-os\website\downloads\AI-OS-USB-Installer.exe"
Set-AuthenticodeSignature -FilePath $exe -Certificate $cert -HashAlgorithm SHA256
$sig = Get-AuthenticodeSignature $exe
Write-Host "SIGNATURE_STATUS: " $sig.Status
Write-Host "SIGNER: " $sig.SignerCertificate.Subject
