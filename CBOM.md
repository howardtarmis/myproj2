# Cryptography Bill of Materials (CBOM)

**Project:** myproj2  
**Format:** CycloneDX 1.6 (machine-readable: CBOM.json)  
**Generated:** 2026-10-04T00:00:00Z  
**Status:** 9 cryptographic asset(s) identified  

---

## Summary

| Category | Count |
|---|---|
| Algorithms | 4 |
| Protocols | 0 |
| Related material (keys, IVs, salts) | 5 |
| Flagged risks | 2 |

---

## Algorithms

| Name | Primitive | Detail | Functions | Found at |
|---|---|---|---|---|
| AES-256-GCM | ae | mode=gcm, params=256 | encrypt, decrypt | `crypto_operations.py:100`, `crypto_operations.py:82` |
| PBKDF2-HMAC-SHA256 | kdf | params=100000-iterations | keyderive | `crypto_operations.py:132` |
| RSA-2048-OAEP-SHA256 | pke | padding=oaep, params=2048 | keygen, encrypt, decrypt | `crypto_operations.py:25`, `crypto_operations.py:43`, `crypto_operations.py:63` |
| SHA-256 | hash | - | digest | `crypto_operations.py:114`, `crypto_operations.py:133`, `crypto_operations.py:44` |

---

## Related Cryptographic Material

| Name | Type | Size | Found at |
|---|---|---|---|
| AES-256 symmetric key | secret-key | 256 bits | `crypto_operations.py:185` |
| AES-GCM IV/nonce | iv | 96 bits | `crypto_operations.py:81` |
| PBKDF2 salt | salt | 128 bits | `crypto_operations.py:130` |
| RSA private key | private-key | 2048 bits | `crypto_operations.py:158`, `crypto_operations.py:25` |
| RSA public key | public-key | 2048 bits | `crypto_operations.py:143` |

---

## Flagged Risks

- **RSA-2048-OAEP-SHA256** — Not quantum-resistant. RSA is broken by Shor's algorithm on a sufficiently large quantum computer; no post-quantum migration path is implemented.
- **PBKDF2-HMAC-SHA256** — Iteration count (100000) is below the OWASP 2023 recommended minimum of 600000 for PBKDF2-HMAC-SHA256. Review before using this path for password storage or key derivation in production.

---

## References

- [CycloneDX CBOM Specification](https://cyclonedx.org/capabilities/cbom/)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
