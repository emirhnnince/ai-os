$ErrorActionPreference = 'Stop'
Write-Host "Creating Trusted Code Signing Authority..."

# Create Root CA
$rootCert = New-SelfSignedCertificate -Type Custom -Subject "CN=AI OS Root Authority, O=AI OS Open Source Project, C=TR" `
    -KeyUsage CertSign, CRLSign, DigitalSignature `
    -KeyExportPolicy Exportable -KeyLength 2048 `
    -HashAlgorithm SHA256 -CertStoreLocation "Cert:\CurrentUser\My" `
    -NotAfter (Get-Date).AddYears(10)

# Export and import to Root store
$certPath = "$PSScriptRoot\AI_OS_Root.cer"
Export-Certificate -Cert $rootCert -FilePath $certPath -Force | Out-Null
Import-Certificate -FilePath $certPath -CertStoreLocation "Cert:\CurrentUser\Root" | Out-Null

# Create Code Signing Certificate issued by Root CA
$codeCert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=AI OS Open Source Project, O=AI OS, C=TR" `
    -Signer $rootCert `
    -KeyExportPolicy Exportable -KeyLength 2048 `
    -HashAlgorithm SHA256 -CertStoreLocation "Cert:\CurrentUser\My" `
    -NotAfter (Get-Date).AddYears(5)

Import-Certificate -FilePath $certPath -CertStoreLocation "Cert:\CurrentUser\TrustedPublisher" | Out-Null

$exePath = "C:\Users\incey\.gemini\antigravity\scratch\ai-os\website\downloads\AI-OS-USB-Installer.exe"
if (Test-Path $exePath) {
    Set-AuthenticodeSignature -FilePath $exePath -Certificate $codeCert -HashAlgorithm SHA256
    $sig = Get-AuthenticodeSignature $exePath
    Write-Host "SIGNATURE STATUS: " $sig.Status
    Write-Host "PUBLISHER NAME: " $sig.SignerCertificate.Subject
}
