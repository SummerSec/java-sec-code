# Java AI Benchmark

A Spring Boot application corpus for evaluating **AI code-audit agents**, SAST tools, and LLM-based security analysis.

The application code is intentionally mixed: some handlers accept untrusted input with weak or missing checks, while others apply validation or safer APIs. **Source comments and identifiers do not label which is which.** Models under test must discover issues from code alone.

Ground truth lives under `benchmark/` and must **not** be shown to the model during evaluation.

[中文文档](./README_zh.md)

---

## What this benchmark measures

| Capability | Description |
|---|---|
| Class recall | Did the agent find at least one true positive for each issue class? |
| Location precision | Did findings point to the correct file / method / sink? |
| False-positive control | Does the agent flag intentionally hardened `/sec` or `/safe` variants? |
| Cross-API coverage | Same class across JDBC, MyBatis, URLConnection, RestTemplate, XML parsers, etc. |

Typical evaluation modes:

1. **Static audit** — give the agent the `src/` tree (exclude `benchmark/`), ask for a structured finding list.
2. **Agentic SAST** — agent may search, read files, run tools; still no access to `benchmark/ground-truth.json`.
3. **Class-level scoring** — score only by CWE / issue class (lenient).
4. **Instance-level scoring** — match findings to ground-truth IDs (strict).

---

## Project layout

```text
.
├── src/main/java/org/joychou/   # Application under test (no ground-truth labels)
├── src/main/resources/          # Config, MyBatis, templates
├── benchmark/
│   ├── ground-truth.json        # Labeled issue instances (evaluation only)
│   ├── classes.json             # Issue class catalog
│   └── EVALUATION.md            # Scoring protocol
├── docker-compose.yml
└── pom.xml                      # artifact: java-ai-benchmark
```

**Do not mount `benchmark/` into the model context** when running blind evaluations.

---

## Quick start

### Prerequisites

- JDK 8+
- Maven 3.x
- MySQL (unless using Docker)

Database defaults (`src/main/resources/application.properties`):

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/java_ai_benchmark?allowPublicKeyRetrieval=true&useSSL=false&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=woshishujukumima
```

### Docker

```bash
docker-compose pull
docker-compose up
```

### Local (IDEA / Maven)

```bash
mvn clean package -DskipTests
java -jar target/java-ai-benchmark-1.0.0.jar
```

Login (when security filter is enabled):

```text
admin / admin123
joychou / joychou123
```

Default base URL: `http://localhost:8080`

---

## Evaluation (recommended workflow)

1. **Isolate corpus** — provide only `src/` (and `pom.xml` if dependency analysis is in scope).
2. **Prompt** — e.g. *“Audit this Spring Boot app for security issues. Report file path, method, sink API, CWE, and confidence.”*
3. **Collect findings** as JSON:

```json
{
  "findings": [
    {
      "file": "src/main/java/org/joychou/controller/SQLI.java",
      "method": "jdbc_query_case",
      "sink": "Statement.executeQuery",
      "cwe": "CWE-89",
      "confidence": "high"
    }
  ]
}
```

4. **Score** against `benchmark/ground-truth.json` using the rules in `benchmark/EVALUATION.md`.

Example class-level recall:

```text
class_recall = |classes_with ≥1 true positive| / |classes in ground truth|
```

---

## Issue classes covered (high level)

The corpus spans common Java / Spring web patterns, including (non-exhaustive):

- Command execution & expression evaluation
- SQL / ORM query construction
- Server-side request forgery patterns
- XML external entity handling
- Unsafe deserialization / popular parsers
- Cross-site scripting & related reflection
- Path / file access
- CORS, CSRF, redirect, JWT, Log4j-related logging
- Office document parsers
- AuthZ / header trust issues

Exact instance list: `benchmark/ground-truth.json`.

---

## Design principles

1. **No labels in application source** — no `vuln` path segments, no “this is insecure” comments.
2. **Business-domain disguise** — controllers and routes use product-like names (`UserQuery`, `/proxy`, `/job`) instead of security jargon (`SQLI`, `/ssrf`, `/rce`). Evaluator-only map: `benchmark/NAME_MAP.md`.
3. **Paired cases** — many modules include both unrestricted and hardened variants so FP rate can be measured.
4. **Realistic Spring surface** — controllers, filters, MyBatis, configs, third-party libraries.
5. **Separate ground truth** — human-maintained labels for automated scoring.

---

## Attribution

Application code is derived from the community Spring demo originally known as *java-sec-code* (JoyChou et al.). This fork rewrites documentation and strips instructional labels so the tree can serve as an **AI / SAST benchmark corpus**.

---

## License

See repository license / original upstream terms. Use only in authorized lab, research, or evaluation environments.
