from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta


def generate_self_signed_cert(common_name, days_valid=365, key_size=2048):
    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )

    # Build certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=days_valid))
        .sign(key, hashes.SHA256())
    )

    return (
        cert.public_bytes(serialization.Encoding.PEM),
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ),
    )

def save_certificate(cert_pem, key_pem, file_path):
    with open(file_path + "_cert.pem", "wb") as f:
        f.write(cert_pem)

    with open(file_path + "_key.pem", "wb") as f:
        f.write(key_pem)
