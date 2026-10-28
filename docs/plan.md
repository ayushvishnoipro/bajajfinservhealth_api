# BFHL API – Requirement-Driven Implementation Plan

_Repository: `ayushvishnoipro/bajajfinservhealth_api`_
JT_Target file: `docs/plan.md`
_Last updated: 2026-10-28_

> This plan is generated from the latest Requirement Assistant JSON output. It preserves finding, story, and task IDs as traceability artifacts. No new IDs are invented.

---

## 1) Project summary and scope

The project delivers a FastAPI implementation of the “BFHL” spec: accept an input array via `POST /bfhl` and return classifications (alphabets, odd/even numbers, special characters), a sum of numeric, and a derived alternating-caps reverse-concat string.

This plan focuses on add2+6ingaplog: contract consistency (docs/tests/implementation) for error handling, CORS hardening, config/test isolation, and usability/observability enhancements.

---

## 2) Input source and validation

Source: latest Requirement Assistant JSON output (as provided in the chat) containing:

- Finding IDs: `BFHL`-FIND-001` … `BFHL`-FIND-007`
- Epics: `EPIC-001`…`EPIC-004`
- Stories: `STORY-001`…`STORY-007`
- Tasks: `TASK-001` … `TASK-012`

Validation notes:
- The JSON signals a primary blocker on STORY-001/STORY-002/STORY-003 and parts of STORY-004/006/007 due to contract ambiguity (e.g. “always 200” vs 422).

---

## 3) Findings and derived requirements

### POKPD findings

- **BFHL-FIND-001 - Spec mismatch: “always returns HTTP 200” vs validation 422**
  - Docs/code/tests contradict each other; spec decision required.

- **BFHL-FIND-002 - Overly broad exception handling masks error types **
  - Current code catches all exceptions and responds with 200, impacting monitoring and client handling.

- **BFHL`-FIND-003 - CORS allows all origins with credentials **
  - Security/browser-compatibility issue; need env-driven config.

- **BFHL`-FIND-004 - Import-time config locking can harm test isolation **
  - Config read at module import time makes multi-config testing harder.

### POP3 enhancements

- **BFHL-FIND-005 - OpenAPI clarity and stricter typing **
- **BFHL`-FIND-006 - Logging lacks request correlation/context **

- **BFHL-FIND-007 - Contract ambiguity requires human decision **impacts BFHL-FIND-001/002.

---

## 4) Implementation phases and tasks

The plan is grouped by the epics specified in the Requirement Assistant JSON. Tasks in each phase use the original task IDs (`TASK-012` etc.) for traceability.

### Phase 0 – Decisions (Blocker resolution)

Focus: unblock P0 stories requiring hand-reected contract selection.

- **STORY-001 (EPIC-001) - Decide and document HTTP status-code contract** [BFHL`-FIND-001, BFHL-FIND-002, BFHL-FIND-007]
  - `TASK-001`: Resolve contract decision and update docs/testing plan.
  - Decision outcomes to choose between:
    1) **Contract A**: Always HTTP 200, return `BFHLResponse` for all errors (toggle `_is_success`/`error`).
    2) **Contract B**: Standard HTTP semantics (validation 422, server errors 5xx), success 200.

**Acceptance criteria (phase 0)**

- README/endpoint docs and tests do not contradict each other on status codes.
- Open questions are either answered or explicitly documented as deferred with owners.

### Phase 1 – Contract alignment for validation errors

- **STORY-002 (EPIC-001) - Implement chosen validation error behavior for `POST /bfhl`** [BFHL-FIND-001, BFHL-FIND-007]
  - `TASK-002: Implement validation error response handling aligned to contract.
  - `TASK-003: Update/expand automated tests for invalid request structures.

Design notes (implementation options, non-code-action guidance):

- If **Contract A** (always 200) is selected:
  - Add a FastAPI exception handler for `RequestValidationError` that returns a `BFHLResponse` payload with `is_success=false`, optional `error`_code`, and a clear `error` message.
  - Adjust tests to assert HTTP 200 for missing `data` and malformed bodies, and verify response shape.
  - Update README error examples to match (remove or configure away from FstAPP 422 detail shape).
- If **Contract B** (standard status codes) is selected:
  - Remove/mellow the “always 200” claim in docs/pcomments. Ensure README explicitly states 422 for schema/validation errors.
  - Keep test expectations for 422, but ensure error examples match FastAPI's actual error format (or a documented custom error handler that returns 422 with a stable body).

** Acceptance criteria (phase 1)**

- The behavior on missing `data` and wrong types matches the decided contract.
- `tests/test_bfhl.py` has passing assertions for invalid requests that do not contradict README.

---

## Phase 2 – Runtime error handling and observability

- **STORY-003 (EPIC-001) - Make runtime error handling predictable and observable** [BFHL`-FIND-002, BFHL-FIND-007]
  - `TASK-004`: Refine runtime exception handling and logging strategy.
  - `TASK-005`: Add a test scenario to validate runtime error responses (controlled error trigger mechanism).

**Acceptance criteria (phase 2)**

- Given a runtime failure, the API responds with the decided status code and stable error payload shape.
- Logs include actionable diagnostics info (type, message, stack trace or equivalent).
- Client-facing error messages don't leak unsanitized stack traces or sensitive inputs.