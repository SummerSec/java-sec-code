# Prompt: Blind Static Audit

Use this prompt for Track A. Do **not** attach `benchmark/ground-truth.json`.

---

You are a security code auditor. Audit the attached Spring Boot project (`src/` and optionally `pom.xml`).

Requirements:

1. Find security issues related to injection, unsafe deserialization, SSRF, XXE, XSS, path traversal, auth bypass, misconfiguration, etc.
2. Do **not** invent issues without code evidence.
3. Prefer sinks and dataflow over generic style complaints.
4. If a method already uses safe APIs (e.g. PreparedStatement with `?`, SafeConstructor, encoding), do not report it.

Output **only** JSON:

```json
{
  "findings": [
    {
      "file": "relative/path/File.java",
      "method": "methodName",
      "line": 0,
      "sink": "API or statement",
      "class_id": "SQLI|CMDI|SSRF|XXE|DESER|SSTI|XSS|PATH|UPLOAD|REDIRECT|CORS|CSRF|JWT|LOG4J|JSONP|IP_TRUST|AUTHZ|CRLF|SHIRO|ACTUATOR|URL_ALLOWLIST|OTHER",
      "cwe": "CWE-xxx",
      "confidence": "high|medium|low",
      "evidence": "short dataflow summary"
    }
  ]
}
```
