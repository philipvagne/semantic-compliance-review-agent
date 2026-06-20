# Architecture

Developer
-> CLI
-> ADK Spike Runner
-> Minimal ADK Agent
-> Custom Tool: `load_sensitive_terms()`
-> Structured Finding JSON

## Phase 0.5 Scope

This document currently reflects the feasibility spike only.

Implemented in Phase 0.5:

- CLI review text input
- one ADK agent
- one custom tool
- one structured finding schema

Not implemented in Phase 0.5:

- file reading
- text extraction
- report generation
- evaluation
- clean copy generation
- repository-wide scanning

# MVP Workflow v1

The MVP processes a single source code file and generates a Markdown audit report.

The workflow is intentionally simple and follows the principle:

> One file in → One report out.

Workflow:

User
↓
CLI
↓
File Reader
↓
Text Extractor
↓
Context Loader
↓
Agent Review
↓
Report Writer
↓
CLI Summary

The first MVP does not include:

* Repository-wide scanning
* Web UI
* Database
* Authentication
* Automatic source modification
* Multi-agent architecture

---

# Component Contracts

## CLI

Input:

* Path to a single source code file
* Optional output directory
* Optional future flags

Output:

* Console summary
* Exit code
* Report location

On Failure:

* Prints clear error message
* Exits with non-zero status

Responsibility:

* Coordinate workflow
* Validate command usage
* Display final results

Does NOT:

* Extract text
* Review content
* Generate findings

---

## File Reader

Input:

* Path to source file

Output:

FileContent

* path
* filename
* extension
* raw_text
* line_count

On Failure:

Raises FileReadError

Examples:

* Missing file
* Permission denied
* Invalid encoding

Responsibility:

* Read source file safely

Does NOT:

* Extract comments
* Call agent
* Generate reports

---

## Text Extractor

Input:

* FileContent

Output:

List[ReviewableText]

Fields:

* id
* source_type
* text
* line_start
* line_end
* language
* surrounding_context

On Failure:

Raises ExtractionError

Returns empty list if no reviewable text exists.

Responsibility:

* Extract comments
* Extract TODO/FIXME notes
* Extract reviewable human-written text

Does NOT:

* Classify findings
* Generate reports

---

## Context Loader

Input:

* sensitive_terms.yaml
* project_context.yaml

Output:

ReviewContext

* sensitive_terms
* project_context
* config_warnings

On Failure:

* Missing config → warn and continue
* Empty sensitive terms → semantic-only mode
* Invalid config → raise ContextLoadError

Responsibility:

* Load project context
* Load organization-defined sensitive terms

Does NOT:

* Classify findings
* Modify configuration

---

## Agent Review

Input:

* ReviewableText
* ReviewContext

Output:

List[Finding]

Fields:

* id
* category
* severity
* confidence
* detection_method
* source_text
* line_start
* line_end
* explanation
* recommendation
* suggested_replacement

On Failure:

Raises AgentReviewError

Responsibility:

* Perform semantic review
* Use project context
* Generate structured findings

Does NOT:

* Read files
* Write reports
* Modify source code

Important Boundary:

agent.review(reviewable_text, context) -> findings

This boundary should remain isolated so ADK can be replaced later if required.

---

## Report Writer

Input:

* FileContent
* Findings
* ReviewContext

Output:

output/<filename>-audit-report.md

On Failure:

Raises ReportWriteError

Responsibility:

* Generate Markdown audit report
* Write report to output directory

Does NOT:

* Modify source files
* Re-run agent review

---

## Clean Copy Writer

Input:

* FileContent
* Findings

Output:

output/<filename>-clean-copy.<ext>

On Failure:

Raises CleanCopyWriteError

Responsibility:

* Generate optional suggested clean copy

Does NOT:

* Overwrite original files
* Modify executable code

---

## Evaluation

Input:

* Evaluation cases
* Expected outputs

Output:

Evaluation metrics

* precision
* recall
* false positives
* false negatives

On Failure:

Raises EvaluationError

Responsibility:

* Evaluate agent quality

Does NOT:

* Modify source files
* Affect normal scans
