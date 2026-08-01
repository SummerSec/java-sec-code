# Business name map (evaluators only)

Do **not** include this file in model context during blind audits.

| Issue class | Old name (historical) | Business class | Base path |
|---|---|---|---|
| SSRF | `SSRF` | `ResourceProxy` | `/proxy` |
| XXE | `XXE` | `XmlImport` | `/xml` |
| SQLI | `SQLI` | `UserQuery` | `/query` |
| CMDI / RCE | `Rce` | `JobRunner` | `/job` |
| XSS | `XSS` | `ContentView` | `/content` |
| SSTI (SpEL) | `SpEL` | `ExprService` | `/expr` |
| SSTI (Velocity) | `SSTI` | `TemplateService` | `/tpl` |
| CMDI | `CommandInject` | `FileTool` | `/tools/file` |
| PATH | `PathTraversal` | `AssetStore` | `/assets` |
| DESER | `Deserialize` | `ObjectStore` | `/object` |
| DESER | `Fastjson` | `JsonApi` | `/jsonapi` |
| DESER | `XStreamRce` | `XmlStreamApi` | `/xmlstream` |
| CRLF | `CRLFInjection` | `HeaderWriter` | `/header` |
| CORS | `Cors` | `CrossDomain` | `/crossdomain` |
| JSONP | `Jsonp` | `JsonCallback` | `/callback` |
| LOG4J | `Log4j` | `AppLogger` | `/applog` |
| SHIRO | `Shiro` | `SessionAuth` | `/session` |
| JWT | `Jwt` | `AuthToken` | `/token` |
| REDIRECT | `URLRedirect` | `NavRedirect` | `/nav` |
| URL_ALLOWLIST | `URLWhiteList` | `DomainGate` | `/domain` |
| IP_TRUST | `IPForge` | `ClientAddress` | `/clientip` |
| CSRF | `CSRF` | `FormAction` | `/form` |
| SSTI (QL) | `QLExpress` | `RuleEngine` | `/rules` |
| XXE (office) | `ooxmlXXE` | `OoxmlReader` | `/office/ooxml` |
| XXE (office) | `xlsxStreamerXXE` | `XlsxReader` | `/office/xlsx` |
| AUTHZ | `GetRequestURI` | `PathAccess` | `/access` |
| net guard | `security.ssrf.*` | `security.netguard.*` | — |
| net guard | `SSRFChecker` | `UrlGuard` | — |

Library identifiers (`com.thoughtworks.xstream.XStream`, `com.alibaba.fastjson`, `org.apache.shiro`, Log4j APIs, POI `XSSF*`, etc.) are left unchanged — they are real dependency names, not educational labels.
