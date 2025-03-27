# Generate SSL certificates for development
$domain = "localhost"
$password = "your-password"
$certPath = "..\ssl"

# Create SSL directory if it doesn't exist
New-Item -ItemType Directory -Force -Path $certPath

# Generate self-signed certificate
$cert = New-SelfSignedCertificate `
    -DnsName $domain `
    -CertStoreLocation cert:\LocalMachine\My `
    -NotAfter (Get-Date).AddYears(1) `
    -KeyAlgorithm RSA `
    -KeyLength 2048 `
    -KeyExportPolicy Exportable `
    -KeyUsage DigitalSignature, KeyEncipherment

# Export certificate with private key
$certPassword = ConvertTo-SecureString -String $password -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "$certPath\certificate.pfx" -Password $certPassword

# Export certificate public key
Export-Certificate -Cert $cert -FilePath "$certPath\certificate.crt"
