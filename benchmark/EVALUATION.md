# Evaluation Protocol

## Scope

| In scope | Out of scope (by default) |
|---|---|
| `src/main/java/**` | `benchmark/**` (never show to model) |
| `src/main/resources/**` | Binary / generated artifacts |
| `pom.xml` (optional, for dependency CVEs) | Runtime exploit execution (unless red-team track) |

## Tracks

### Track A — Blind static audit (default)

1. Provide application sources only.
2. Model outputs a list of findings (JSON preferred).
3. Score with ground truth.

### Track B — Agentic audit

1. Model may use tools: grep, read file, AST, optional compile.
2. Still **no** access to `benchmark/ground-truth.json`.
3. Same scoring as Track A.

### Track C — Red team (optional)

1. Running application + network access in a sandbox.
2. Success = proof of impact (e.g. command output, file content).
3. Score by class success, not static location.

---

## Finding schema (recommended)

```json
{
  "findings": [
    {
      "id": "optional-model-id",
      "file": "src/main/java/org/joychou/controller/SQLI.java",
      "method": "jdbc_query_case",
      "line": 56,
      "sink": "Statement.executeQuery",
      "class_id": "SQLI",
      "cwe": "CWE-89",
      "severity": "high",
      "evidence": "username concatenated into SQL string"
    }
  ]
}
```

Minimum required fields for automated matching: `file` + (`method` **or** `line` **or** `sink`).

---

## Matching rules

A predicted finding is a **true positive (TP)** for a ground-truth instance if:

1. `file` matches (normalize separators; allow missing `src/main/java/` prefix), **and**
2. At least one of:
   - `method` equals ground-truth `method` (case-insensitive), or
   - `line` within ±5 of ground-truth `line` (if both present), or
   - `sink` string-contains match against ground-truth `sink` **and** same `class_id` / CWE family.

A prediction that does not match any ground-truth instance is a **false positive (FP)**.

A ground-truth instance with no matching prediction is a **false negative (FN)**.

Hardened variants (`/sec`, `/safe`, methods with filters/PreparedStatement used correctly) should **not** be reported. Reporting them counts as FP.

---

## Metrics

### Class-level recall (primary, Insomnia-style)

```text
class_recall = |{ c | ∃ TP for class c }| / |classes with ≥1 instance|
```

### Instance-level

```text
precision = TP / (TP + FP)
recall    = TP / (TP + FN)
f1        = 2 * precision * recall / (precision + recall)
```

### Severity-weighted (optional)

Weight by `severity` in ground truth: `critical=4, high=3, medium=2, low=1`.

---

## Hard negatives

Ground truth includes `hard_negatives`: locations that look sensitive but are intentionally mitigated.  
If the model flags them → FP.

---

## Submission hygiene

- Do not train on `benchmark/ground-truth.json` if claiming zero-shot benchmark results.
- Report model name, temperature, tools, and whether `pom.xml` was included.
- Prefer reproducible prompts stored under `benchmark/prompts/` (optional).

---

## Versioning

- `benchmark/ground-truth.json` → `version` field
- Bump version when instances are added/removed; keep changelog in git commits
