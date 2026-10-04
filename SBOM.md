# Software Bill of Materials (SBOM)

**Project:** myproj2  
**Format:** CycloneDX 1.4 (machine-readable: SBOM.json)  
**Generated:** 2026-09-29 (refreshed 2026-10-04, v2)  
**Status:** Complete inventory with vulnerability details  

---

## 📊 Summary

| Category | Count |
|----------|-------|
| **Total Components** | 14 |
| **Direct Dependencies** | 6 |
| **Vulnerabilities Found** | 4 |
| **Critical** | 0 |
| **High** | 2 |
| **Medium** | 2 |
| **Low** | 0 |

**Since v1 (2026-09-29):** added `cryptography@50.0.1` (resolved the prior HIGH CVE-2026-26007 cluster), the `semgrep` CI tool, and three SHA-pinned GitHub Actions used by the new `sbom-cbom.yml` workflow. The four vulnerable fixtures and the three tag-referenced Actions below are unchanged.

---

## 🛠️ Node.js Dependencies

### express@4.21.2
- **Type:** Web Framework
- **License:** MIT
- **Source:** npm (https://www.npmjs.com/package/express)
- **Status:** ⚠️ VULNERABLE (6 vulnerabilities)
- **CVE:** CVE-2026-4867
- **Severity:** HIGH (CVSS 8.5)
- **Issue:** Body-parser vulnerability
- **Action:** Upgrade to express >= 4.22.0
- **Note:** Intentional fixture for testing

### lodash@4.17.21
- **Type:** Utility Library
- **License:** MIT
- **Source:** npm (https://www.npmjs.com/package/lodash)
- **Status:** ⚠️ VULNERABLE (3 vulnerabilities)
- **CVE:** CVE-2025-13465
- **Severity:** HIGH (CVSS 7.8)
- **Issue:** Prototype pollution vulnerability
- **Action:** Upgrade to lodash >= 4.17.22
- **Note:** Intentional fixture for testing

---

## 🐍 Python Dependencies

### jinja2@3.1.4
- **Type:** Template Engine
- **License:** BSD-3-Clause
- **Source:** PyPI (https://pypi.org/project/jinja2/)
- **Status:** ⚠️ VULNERABLE (1 vulnerability)
- **CVE:** CVE-2024-56201
- **Severity:** MEDIUM (CVSS 6.5)
- **Issue:** Template injection vulnerability
- **Action:** Upgrade to jinja2 >= 3.1.5
- **Note:** Intentional fixture for testing

### requests@2.32.3
- **Type:** HTTP Library
- **License:** Apache-2.0
- **Source:** PyPI (https://pypi.org/project/requests/)
- **Status:** ⚠️ VULNERABLE (1 vulnerability)
- **CVE:** CVE-2024-47081
- **Severity:** MEDIUM (CVSS 5.3)
- **Issue:** Improper file handling vulnerability
- **Action:** Upgrade to requests >= 2.32.4
- **Note:** Intentional fixture for testing

---

## 🐍 Python Dependencies (continued)

### cryptography@50.0.1
- **Type:** Cryptography Library
- **License:** Apache-2.0 / BSD-3-Clause (dual-licensed)
- **Source:** PyPI (https://pypi.org/project/cryptography/)
- **Status:** ✅ SECURE
- **Note:** Upgraded from 43.0.0, which carried a HIGH finding (CVE-2026-26007 and 5 related CVEs/GHSAs). 50.0.1 is the first vulnerability-free version per the Armis scan.

---

## ⚙️ CI/CD Actions

### actions/checkout@v4
- **Type:** GitHub Action
- **License:** MIT
- **Status:** ⚠️ SECURITY RISK
- **Issue:** Uses tag reference (@v4) instead of commit SHA
- **CWE:** CWE-1357 (Reliance on Insufficiently Trustworthy Component)
- **Risk:** Tag can be reassigned by attacker
- **Action:** Use commit SHA instead
- **Recommended:** `actions/checkout@a12a3943b4dde5fcd4e8c689dfe5a1aa8e8b2fca`

### actions/setup-python@v5
- **Type:** GitHub Action
- **License:** MIT
- **Status:** ⚠️ SECURITY RISK
- **Issue:** Uses tag reference (@v5) instead of commit SHA
- **CWE:** CWE-1357
- **Risk:** Supply chain attack via tag reassignment
- **Action:** Use commit SHA instead
- **Recommended:** `actions/setup-python@0b93645e9fea7318ecaed2b359558ac514576753`

### github/codeql-action/upload-sarif@v3
- **Type:** GitHub Action
- **License:** MIT
- **Status:** ⚠️ SECURITY RISK + DEPRECATED
- **Issue:** Uses tag reference (@v3) instead of commit SHA
- **CWE:** CWE-1357
- **Deprecation:** Will be deprecated in December 2026
- **Action:** Use v4 with commit SHA
- **Recommended:** `github/codeql-action/upload-sarif@012739e5a7ed1eb25ba086e4c0db777d8eb8f312` (v4)

### actions/checkout@11d5960a3... (pinned, v4)
- **Type:** GitHub Action
- **License:** MIT
- **Status:** ✅ SECURE
- **Usage:** sbom-cbom.yml, pinned to commit SHA

### actions/setup-python@a26af69be... (pinned, v5)
- **Type:** GitHub Action
- **License:** MIT
- **Status:** ✅ SECURE
- **Usage:** sbom-cbom.yml, pinned to commit SHA

### actions/upload-artifact@ea165f8d6... (pinned, v4)
- **Type:** GitHub Action
- **License:** MIT
- **Status:** ✅ SECURE
- **Usage:** Publishes the `boms` artifact from sbom-cbom.yml, pinned to commit SHA

---

## 🔧 Development Tools

### semgrep@1.136.0
- **Type:** Static Analysis Tool
- **License:** LGPL-2.1
- **Source:** PyPI (https://pypi.org/project/semgrep/)
- **Status:** ⚠️ VERSION NOT PINNED IN CI
- **Purpose:** Static detection of cryptographic API usage for CBOM generation
- **Risk:** Installed via `pip install semgrep` with no version pin in sbom-cbom.yml; the version running in CI floats to whatever is latest on each run.
- **Usage:** CI/CD workflow (sbom-cbom.yml)

### ruff@0.6.9
- **Type:** Python Linter
- **License:** MIT
- **Status:** ✅ SECURE
- **Purpose:** Code quality analysis and formatting
- **Usage:** CI/CD workflows

### armis-cli@1.22.0
- **Type:** Security Scanner
- **License:** Proprietary (Armis Security)
- **Status:** ✅ SECURE
- **Purpose:** Application security scanning
- **Usage:** Local development + CI/CD
- **Update Available:** v1.24.0

---

## 📋 License Compliance

| License | Count | Status |
|---------|-------|--------|
| MIT | 9 | ✅ Approved |
| BSD-3-Clause | 2 | ✅ Approved |
| Apache-2.0 | 2 | ✅ Approved |
| Proprietary | 1 | ⚠️ Commercial |
| LGPL-2.1 | 1 | ⚠️ Needs review |

**Compliance:** ✅ All direct-dependency licenses are permissive and approved for use. ⚠️ `semgrep` (LGPL-2.1, a weak-copyleft license) is used only as a build-time CI tool, not linked into or distributed with the application — but per the copyleft-approval rule it should get an explicit sign-off rather than being waved through.

---

## 🚨 Vulnerability Details

### HIGH Severity Vulnerabilities

#### 1. CVE-2026-4867 (express@4.21.2)
- **CVSS Score:** 8.5
- **Component:** Body-parser (transitive dependency)
- **Impact:** Request parsing bypass
- **Remediation:** Upgrade express to 4.22.0 or later

#### 2. CVE-2025-13465 (lodash@4.17.21)
- **CVSS Score:** 7.8
- **Component:** Lodash utility library
- **Impact:** Prototype pollution attack
- **Remediation:** Upgrade lodash to 4.17.22 or later

### MEDIUM Severity Vulnerabilities

#### 3. CVE-2024-56201 (jinja2@3.1.4)
- **CVSS Score:** 6.5
- **Component:** Jinja2 template engine
- **Impact:** Template injection vulnerability
- **Remediation:** Upgrade jinja2 to 3.1.5 or later

#### 4. CVE-2024-47081 (requests@2.32.3)
- **CVSS Score:** 5.3
- **Component:** Requests HTTP library
- **Impact:** Improper file handling
- **Remediation:** Upgrade requests to 2.32.4 or later

---

## ⚠️ Important Notes

### Intentional Vulnerable Fixtures
This repository **intentionally includes vulnerable code** for security testing and demonstration:
- `sqli_xss_vulnerable.py` — SQL injection & XSS examples
- `redos_vulnerable.py` — Regular expression DoS
- `exposed_secrets.py` — Hardcoded credentials
- `compliance_violations.tf` — IaC misconfigurations
- `requirements-vulnerable.txt` — Known vulnerable packages
- `package.json` — Known vulnerable Node modules

**These must NOT be deployed to production.**

### GitHub Actions Security Risk
All GitHub Actions use tag references (@v3, @v4, @v5) instead of commit SHAs. This is a **supply chain risk** because tags can be reassigned.

**Recommendation:** Pin all actions to specific commit SHAs:
```yaml
# ❌ RISKY
uses: actions/checkout@v4

# ✅ SAFE
uses: actions/checkout@a12a3943b4dde5fcd4e8c689dfe5a1aa8e8b2fca
```

---

## 📈 Remediation Roadmap

| Priority | Component | Action | Timeline |
|----------|-----------|--------|----------|
| 🔴 HIGH | express | Upgrade to 4.22.0 | Immediate |
| 🔴 HIGH | lodash | Upgrade to 4.17.22 | Immediate |
| 🟠 MEDIUM | jinja2 | Upgrade to 3.1.5 | Next sprint |
| 🟠 MEDIUM | requests | Upgrade to 2.32.4 | Next sprint |
| 🟡 LOW | GitHub Actions (security-gate-*.yml) | Use commit SHAs | Backlog |
| 🟡 LOW | semgrep | Pin version in sbom-cbom.yml | Backlog |
| 🟡 LOW | semgrep license | Get LGPL-2.1 copyleft sign-off | Backlog |

---

## 🔍 Verification

**SBOM Format:** CycloneDX 1.4 (industry standard)  
**Machine-Readable:** SBOM.json  
**Last Updated:** 2026-10-04  
**Next Review:** 2026-10-06 (weekly)  

**Verification Command:**
```bash
armis-cli scan repo . --fail-on HIGH,CRITICAL
```

---

## 📚 References

- [CycloneDX Specification](https://cyclonedx.org/spec/v1.4/)
- [NTIA Minimum Elements](https://www.ntia.gov/files/ntia/publications/sbom_minimum_elements_report.pdf)
- [CVE Details](https://www.cvedetails.com/)
- [Armis Security](https://www.armis.com/)
