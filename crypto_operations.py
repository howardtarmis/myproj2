"""Cryptographic operations demonstration for CBOM analysis.

This module showcases various cryptographic algorithms and implementations
that can be scanned for cryptographic bill of materials (CBOM) reporting.
"""

import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_rsa_keypair(key_size: int = 2048) -> tuple:
    """Generate RSA public/private key pair.

    Args:
        key_size: RSA key size in bits (default 2048)

    Returns:
        Tuple of (private_key, public_key)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=key_size, backend=default_backend()
    )
    return private_key, private_key.public_key()


def encrypt_with_rsa(public_key, plaintext: bytes) -> bytes:
    """Encrypt data using RSA-OAEP with SHA-256.

    Args:
        public_key: RSA public key
        plaintext: Data to encrypt

    Returns:
        Encrypted ciphertext
    """
    return public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_with_rsa(private_key, ciphertext: bytes) -> bytes:
    """Decrypt data using RSA-OAEP with SHA-256.

    Args:
        private_key: RSA private key
        ciphertext: Encrypted data

    Returns:
        Decrypted plaintext
    """
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def encrypt_with_aes_gcm(key: bytes, plaintext: bytes) -> tuple:
    """Encrypt data using AES-256-GCM.

    Args:
        key: 32-byte AES-256 key
        plaintext: Data to encrypt

    Returns:
        Tuple of (ciphertext, iv, tag)
    """
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext, iv, encryptor.tag


def decrypt_with_aes_gcm(key: bytes, ciphertext: bytes, iv: bytes, tag: bytes) -> bytes:
    """Decrypt data using AES-256-GCM.

    Args:
        key: 32-byte AES-256 key
        ciphertext: Encrypted data
        iv: Initialization vector
        tag: Authentication tag

    Returns:
        Decrypted plaintext
    """
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def hash_data(data: bytes) -> bytes:
    """Hash data using SHA-256.

    Args:
        data: Data to hash

    Returns:
        SHA-256 hash digest
    """
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(data)
    return digest.finalize()


def derive_key_from_password(password: str, salt: bytes = None) -> tuple:
    """Derive encryption key from password using PBKDF2-SHA256.

    Args:
        password: User password
        salt: Optional salt (16 bytes). If None, generates random salt.

    Returns:
        Tuple of (derived_key, salt)
    """
    if salt is None:
        salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    derived_key = kdf.derive(password.encode())
    return derived_key, salt


def serialize_public_key(public_key) -> bytes:
    """Serialize public key to PEM format.

    Args:
        public_key: RSA public key

    Returns:
        PEM-encoded public key
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def serialize_private_key(private_key, password: str = None) -> bytes:
    """Serialize private key to PEM format.

    Args:
        private_key: RSA private key
        password: Optional password for key encryption

    Returns:
        PEM-encoded private key
    """
    encryption_algorithm = serialization.NoEncryption()
    if password:
        encryption_algorithm = serialization.BestAvailableEncryption(password.encode())

    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm,
    )


if __name__ == "__main__":
    # Example usage
    print("Generating RSA keypair...")
    private_key, public_key = generate_rsa_keypair()

    print("Testing AES-256-GCM encryption...")
    key = os.urandom(32)
    plaintext = b"Sensitive data requiring confidentiality"
    ciphertext, iv, tag = encrypt_with_aes_gcm(key, plaintext)
    decrypted = decrypt_with_aes_gcm(key, ciphertext, iv, tag)
    assert decrypted == plaintext, "AES decryption mismatch"

    print("Testing SHA-256 hashing...")
    data_hash = hash_data(plaintext)
    print(f"Hash: {data_hash.hex()}")

    print("Testing PBKDF2 key derivation...")
    derived_key, salt = derive_key_from_password("secure_password")
    print(f"Derived key length: {len(derived_key)} bytes")

    print("All cryptographic operations completed successfully!")
