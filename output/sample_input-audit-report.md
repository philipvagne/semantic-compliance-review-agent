# Semantic Compliance Audit Report

|                                |                              |
| ------------------------------ | ---------------------------- |
| **Target File**                | `examples/sample_input.html` |
| **Generated On**               | 2026-06-22 · 06:49 UTC       |
| **Backend**                    | Gemini                       |
| **Model**                      | `gemini-2.5-flash`           |
| **Configured Sensitive Terms** | 3                            |
| **Findings Count**             | 2                            |
| **Audit Status**               | **ISSUES FOUND**             |

---

## Executive Summary

This audit completed with status **ISSUES FOUND**.

- Reviewable text items analyzed: 4
- Findings generated: 2
- Highest severity found: 🟢 Low
- Categories detected: Professionalism Risk

---

## Audit Summary Matrix

| Reference | Category             | Severity | Confidence |
| --------- | -------------------- | -------- | ---------- |
| PRO-001   | Professionalism Risk | 🟢 Low    | ● High     |
| PRO-002   | Professionalism Risk | 🟢 Low    | ● High     |

---

## Detailed Findings

### PRO-001: Professionalism Risk

**Severity:** 🟢 Low | **Confidence:** ● High

**Detection Method:** Semantic Analysis

`examples/sample_input.html` — line 12

#### Source Text

```text
TODO: replace the placeholder support text before release.
```

#### Why This Was Flagged

- The TODO indicates unfinished work to replace placeholder text before release, which can lead to unprofessional or incomplete content being publicly visible.

#### Recommended Action

Replace placeholder text with final content or a more neutral, descriptive placeholder that doesn't imply incompleteness before release.

#### Suggested Replacement

```diff
- TODO: replace the placeholder support text before release.
+ TODO: finalize the support text before release.
```

### PRO-002: Professionalism Risk

**Severity:** 🟢 Low | **Confidence:** ● High

**Detection Method:** Semantic Analysis

`examples/sample_input.html` — line 25

#### Source Text

```text
FIXME: swap the demo footer label later.
```

#### Why This Was Flagged

- The FIXME indicates unfinished work to replace a 'demo' label, which can lead to unprofessional or temporary content being publicly visible.

#### Recommended Action

Replace the 'demo' label with the final label or a more neutral temporary label.

#### Suggested Replacement

```diff
- FIXME: swap the demo footer label later.
+ FIXME: finalize the footer label.
```

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

The Semantic Compliance Review Agent provides AI-assisted semantic review to help identify potentially risky human-written text.

Human review is required before any action is taken.

No source code was modified during this audit.

No changes should be applied automatically without developer review.

The developer remains responsible for final decisions.
