# Semantic Compliance Audit Report

|                            |                            |
| -------------------------- | -------------------------- |
| Target File                | `examples/sample_input.py` |
| Generated On               | 2026-06-21 · 12:58 UTC     |
| Backend                    | Gemini                     |
| Model                      | `gemini-2.5-flash`         |
| Configured Sensitive Terms | 3                          |
| Findings Count             | 2                          |
| Audit Status               | **ISSUES FOUND**           |

---

## Scan Statistics

| Metric                         | Value |
| ------------------------------ | ----- |
| Reviewable text items analyzed | 6     |
| Findings generated             | 2     |

---

## Findings

### SEC-001: Security Risk

- Category: Security Risk
- Severity: CRITICAL
- Confidence: HIGH
- Detection Method: HYBRID
- Line Numbers: 3-3

#### Source Text

```text
TODO: remove the temporary admin password before release
```

#### Explanation

The text explicitly mentions a "temporary admin password" that needs to be removed. This indicates a severe security vulnerability if not addressed, as temporary credentials can be inadvertently left in production or exposed through version control.

#### Recommendation

Immediately remove all hard-coded or temporary credentials. Implement secure secrets management practices and ensure no sensitive authentication details are ever committed to source control. Conduct a security audit to confirm no other credentials are exposed.

#### Suggested Replacement

TODO: Implement secure credential management before release

### PRO-001: Professionalism Risk

- Category: Professionalism Risk
- Severity: LOW
- Confidence: HIGH
- Detection Method: SEMANTIC_ANALYSIS
- Line Numbers: 14-14

#### Source Text

```text
FIXME: replace the hard-coded example value later
```

#### Explanation

The text indicates a hard-coded example value is used, which is generally considered a poor practice. Hard-coding values can lead to inflexibility, difficulty in testing, and potential security risks if sensitive data is accidentally hard-coded in the future.

#### Recommendation

Avoid hard-coding values. Use configurable options (e.g., environment variables, configuration files, constants) for values that may change or need to be different in various environments.

#### Suggested Replacement

FIXME: use a configurable value here

---

## Audit Summary Matrix

| Reference | Category             | Severity | Confidence |
| --------- | -------------------- | -------- | ---------- |
| SEC-001   | Security Risk        | CRITICAL | HIGH       |
| PRO-001   | Professionalism Risk | LOW      | HIGH       |

---

## Finding Reference Guide

| Prefix | Description                |
| ------ | -------------------------- |
| CDX    | Internal Codename Exposure |
| SEC    | Security Risk              |
| PRO    | Professionalism Risk       |
| CMP    | Compliance Risk            |
| IPR    | Intellectual Property Risk |
| REP    | Reputation Risk            |

---

## Review Philosophy

- AI-assisted review
- Human review required
- No automatic source modification
- Developer remains responsible
