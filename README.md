# Java AI Benchmark (evaluation branch)

This branch packages **evaluation assets** for AI / SAST code-audit experiments on top of the application sources.

| Branch | Contents |
|---|---|
| [`master`](https://github.com/SummerSec/java-sec-code/tree/master) | Application only — product-facing README, no ground truth |
| **`benchmark` (this branch)** | Application + `benchmark/` labels + helper `scripts/` |

## Recommended workflow

### 1. Blind audit (model context)

Use **master** only. Do not give the model this branch’s `benchmark/` directory.

```bash
git clone https://github.com/SummerSec/java-sec-code.git
cd java-sec-code
git checkout master
# Provide src/ (and optionally pom.xml) to the model
```

### 2. Scoring (evaluator only)

Stay on this branch, or extract labels without checking it out:

```bash
git show benchmark:benchmark/ground-truth.json > ground-truth.json
git show benchmark:benchmark/score.py > score.py
python score.py findings.json
```

Or:

```bash
git checkout benchmark
python benchmark/score.py findings.json
```

## Layout (this branch)

```text
.
├── src/                         # Same application surface as master
├── benchmark/
│   ├── ground-truth.json        # Labeled instances (never show to model)
│   ├── classes.json
│   ├── EVALUATION.md            # Scoring protocol
│   ├── NAME_MAP.md              # Historical → business name map
│   ├── prompts/static_audit.md
│   └── score.py
└── scripts/                     # One-off transform helpers (not runtime)
```

## Metrics

See `benchmark/EVALUATION.md`.

Primary:

```text
class_recall = |classes with ≥1 TP| / |classes|
```

Instance-level precision / recall / F1 via `benchmark/score.py`.

## Notes

- Application controllers use **business-domain** names (`UserQuery`, `/proxy`, …). Evaluator map: `benchmark/NAME_MAP.md`.
- Hardened variants under `/sec` and `/safe` should not be reported as findings (hard negatives).
- Keep `benchmark/` out of training / few-shot context if you claim zero-shot results.

## Product docs

For install, login, modules, and Docker, see the **master** README:

https://github.com/SummerSec/java-sec-code/blob/master/README.md
