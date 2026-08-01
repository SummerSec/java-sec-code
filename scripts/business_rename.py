#!/usr/bin/env python3
"""
Disguise security-domain names as business-domain names for AI benchmark realism.

Does NOT rename third-party library identifiers (XStream, fastjson, log4j, shiro, XSSF*, QLExpressRunStrategy, etc.).
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Class file renames: relative to src/main/java/org/joychou/
CLASS_RENAMES: list[tuple[str, str]] = [
    ("controller/SSRF.java", "controller/ResourceProxy.java"),
    ("controller/XXE.java", "controller/XmlImport.java"),
    ("controller/SQLI.java", "controller/UserQuery.java"),
    ("controller/Rce.java", "controller/JobRunner.java"),
    ("controller/XSS.java", "controller/ContentView.java"),
    ("controller/SpEL.java", "controller/ExprService.java"),
    ("controller/SSTI.java", "controller/TemplateService.java"),
    ("controller/CommandInject.java", "controller/FileTool.java"),
    ("controller/PathTraversal.java", "controller/AssetStore.java"),
    ("controller/Deserialize.java", "controller/ObjectStore.java"),
    ("controller/Fastjson.java", "controller/JsonApi.java"),
    ("controller/XStreamRce.java", "controller/XmlStreamApi.java"),
    ("controller/CRLFInjection.java", "controller/HeaderWriter.java"),
    ("controller/Cors.java", "controller/CrossDomain.java"),
    ("controller/Jsonp.java", "controller/JsonCallback.java"),
    ("controller/Log4j.java", "controller/AppLogger.java"),
    ("controller/Shiro.java", "controller/SessionAuth.java"),
    ("controller/Jwt.java", "controller/AuthToken.java"),
    ("controller/URLRedirect.java", "controller/NavRedirect.java"),
    ("controller/URLWhiteList.java", "controller/DomainGate.java"),
    ("controller/IPForge.java", "controller/ClientAddress.java"),
    ("controller/CSRF.java", "controller/FormAction.java"),
    ("controller/QLExpress.java", "controller/RuleEngine.java"),
    ("controller/GetRequestURI.java", "controller/PathAccess.java"),
    ("controller/ClassDataLoader.java", "controller/ModuleLoader.java"),
    ("controller/Dotall.java", "controller/PathPatternDemo.java"),
    ("controller/Jdbc.java", "controller/DriverProbe.java"),
    ("controller/Cookies.java", "controller/CookieApi.java"),
    ("controller/FileUpload.java", "controller/UploadApi.java"),
    ("controller/WebSockets.java", "controller/RealtimeChannel.java"),
    ("controller/office/ooxmlXXE.java", "controller/office/OoxmlReader.java"),
    ("controller/office/xlsxStreamerXXE.java", "controller/office/XlsxReader.java"),
    ("security/ssrf/SSRFChecker.java", "security/netguard/UrlGuard.java"),
    ("security/ssrf/SSRFException.java", "security/netguard/UrlGuardException.java"),
    ("security/ssrf/SocketHook.java", "security/netguard/SocketHook.java"),
    ("security/ssrf/SocketHookFactory.java", "security/netguard/SocketHookFactory.java"),
    ("security/ssrf/SocketHookImpl.java", "security/netguard/SocketHookImpl.java"),
    ("security/ssrf/SocketHookUtils.java", "security/netguard/SocketHookUtils.java"),
]

# Identifier renames applied after file moves (order matters for longer-first)
IDENT_REPLACEMENTS: list[tuple[str, str]] = [
    # packages
    ("org.joychou.security.ssrf", "org.joychou.security.netguard"),
    ("package org.joychou.security.ssrf", "package org.joychou.security.netguard"),
    # classes (our own only)
    ("SSRFException", "UrlGuardException"),
    ("SSRFChecker", "UrlGuard"),
    ("class SSRF", "class ResourceProxy"),
    ("class XXE", "class XmlImport"),
    ("class SQLI", "class UserQuery"),
    ("class Rce", "class JobRunner"),
    ("class XSS", "class ContentView"),
    ("class SpEL", "class ExprService"),
    ("class SSTI", "class TemplateService"),
    ("class CommandInject", "class FileTool"),
    ("class PathTraversal", "class AssetStore"),
    ("class Deserialize", "class ObjectStore"),
    ("class Fastjson", "class JsonApi"),
    ("class XStreamRce", "class XmlStreamApi"),
    ("class CRLFInjection", "class HeaderWriter"),
    ("class Cors", "class CrossDomain"),
    ("class Jsonp", "class JsonCallback"),
    ("class Log4j", "class AppLogger"),
    ("class Shiro", "class SessionAuth"),
    ("class Jwt", "class AuthToken"),
    ("class URLRedirect", "class NavRedirect"),
    ("class URLWhiteList", "class DomainGate"),
    ("class IPForge", "class ClientAddress"),
    ("class CSRF", "class FormAction"),
    ("class QLExpress", "class RuleEngine"),
    ("class GetRequestURI", "class PathAccess"),
    ("class ClassDataLoader", "class ModuleLoader"),
    ("class Dotall", "class PathPatternDemo"),
    ("class Jdbc", "class DriverProbe"),
    ("class Cookies", "class CookieApi"),
    ("class FileUpload", "class UploadApi"),
    ("class WebSockets", "class RealtimeChannel"),
    ("class ooxmlXXE", "class OoxmlReader"),
    ("class xlsxStreamerXXE", "class XlsxReader"),
    # LoggerFactory.getLogger(OldClass)
    ("LoggerFactory.getLogger(SSRF.class)", "LoggerFactory.getLogger(ResourceProxy.class)"),
    ("LoggerFactory.getLogger(XXE.class)", "LoggerFactory.getLogger(XmlImport.class)"),
    ("LoggerFactory.getLogger(SQLI.class)", "LoggerFactory.getLogger(UserQuery.class)"),
    ("LoggerFactory.getLogger(this.getClass())", "LoggerFactory.getLogger(this.getClass())"),
    ("LogManager.getLogger(\"Log4j\")", "LogManager.getLogger(\"AppLogger\")"),
    # SecurityUtil methods
    ("checkSSRFByWhitehosts", "checkUrlByWhitehosts"),
    ("checkSSRFWithoutRedirect", "checkUrlWithoutRedirect"),
    ("checkSSRF(", "checkUrl("),
    ("startSSRFHook", "startUrlHook"),
    ("stopSSRFHook", "stopUrlHook"),
    # WebConfig field accessors
    ("getSsrfSafeDomains", "getUrlSafeDomains"),
    ("setSsrfSafeDomains", "setUrlSafeDomains"),
    ("getSsrfBlockDomains", "getUrlBlockDomains"),
    ("setSsrfBlockDomains", "setUrlBlockDomains"),
    ("getSsrfBlockIps", "getUrlBlockIps"),
    ("setSsrfBlockIps", "setUrlBlockIps"),
    ("ssrfSafeDomains", "urlSafeDomains"),
    ("ssrfBlockDomains", "urlBlockDomains"),
    ("ssrfBlockIps", "urlBlockIps"),
    ("ssrfSafeDomain", "urlSafeDomain"),
    ("ssrfBlockDomain", "urlBlockDomain"),
    ("ssrfRootTag", "urlRootTag"),
    ("ssrfFinalTag", "urlFinalTag"),
    ("ssrfIpFinalTag", "urlIpFinalTag"),
    ("ssrfSafeDomainClassPath", "urlSafeDomainClassPath"),
    ("ssrf_safe_domain.xml", "url_safe_domain.xml"),
    ("ssrfsafeconfig", "urlsafeconfig"),
    # method / local renames that leak
    ("jdbc_sqli_case", "jdbc_query_case"),
    ("jdbc_sqli_safe", "jdbc_query_safe"),
    ("jdbc_ps_case", "jdbc_ps_case"),
    ("ooxml_xxe", "readOoxml"),
    ("xllx_streamer_xxe", "readXlsxStream"),
    ("shiro_deserialize", "sessionRestore"),
    ("URLConnectionCase", "urlConnectionCase"),
    ("URLConnectionSec", "urlConnectionSafe"),
    ("httpURLConnectionCase", "httpUrlConnectionCase"),
    # path segments (string literals in annotations / props)
    ('"/ssrf', '"/proxy'),
    ("'/ssrf", "'/proxy"),
    ("/ssrf/", "/proxy/"),
    ("/ssrf\"", "/proxy\""),
    ("/ssrf'", "/proxy'"),
    ('"/xxe', '"/xml'),
    ("'/xxe", "'/xml"),
    ("/xxe/", "/xml/"),
    ("/xxe\"", "/xml\""),
    ("/xxe'", "/xml'"),
    ("/xxe/**", "/xml/**"),
    ('"/sqli', '"/query'),
    ("'/sqli", "'/query"),
    ("/sqli/", "/query/"),
    ("/sqli\"", "/query\""),
    ('"/rce', '"/job'),
    ("'/rce", "'/job"),
    ("/rce/", "/job/"),
    ("/rce\"", "/job\""),
    ("/rce/**", "/job/**"),
    ('"/xss', '"/content'),
    ("'/xss", "'/content"),
    ("/xss/", "/content/"),
    ("/xss\"", "/content\""),
    ('"/spel', '"/expr'),
    ("'/spel", "'/expr"),
    ("spel/", "expr/"),
    ("/spel/", "/expr/"),
    ("/spel/**", "/expr/**"),
    ('"/ssti', '"/tpl'),
    ("'/ssti", "'/tpl"),
    ("/ssti/", "/tpl/"),
    ("/ssti\"", "/tpl\""),
    ('"/path_traversal', '"/assets'),
    ("/path_traversal/", "/assets/"),
    ('"/deserialize', '"/object'),
    ("/deserialize/", "/object/"),
    ("/deserialize/**", "/object/**"),
    ("/deserialize\"", "/object\""),
    ('"/fastjson', '"/jsonapi'),
    ("/fastjson/", "/jsonapi/"),
    ("/fastjson/**", "/jsonapi/**"),
    ('"/xstream', '"/xmlstream'),
    ("/xstream\"", "/xmlstream\""),
    ("/xstream/**", "/xmlstream/**"),
    ('"/codeinject', '"/tools/file'),
    ("/codeinject/", "/tools/file/"),
    ("/codeinject\"", "/tools/file\""),
    ('"/crlf', '"/header'),
    ("/crlf/", "/header/"),
    ("/crlf\"", "/header\""),
    ('"/cors', '"/crossdomain'),
    ("/cors/", "/crossdomain/"),
    ("/cors\"", "/crossdomain\""),
    ('"/jsonp', '"/callback'),
    ("/jsonp/", "/callback/"),
    ("/jsonp/**", "/callback/**"),
    ("/jsonp\"", "/callback\""),
    ('"/log4j', '"/applog'),
    ("/log4j\"", "/applog\""),
    ('"/shiro', '"/session'),
    ("/shiro/", "/session/"),
    ("/shiro/**", "/session/**"),
    ("/shiro\"", "/session\""),
    ('"/jwt', '"/token'),
    ("/jwt/", "/token/"),
    ("/jwt\"", "/token\""),
    ('"/urlRedirect', '"/nav'),
    ("/urlRedirect/", "/nav/"),
    ("/urlRedirect\"", "/nav\""),
    # DomainGate base path /url -> /domain (careful: only controller mapping)
    ('@RequestMapping("/url")', '@RequestMapping("/domain")'),
    ('"/url/case', '"/domain/case'),
    ('"/url/sec', '"/domain/sec'),
    ('@RequestMapping("/ip")', '@RequestMapping("/clientip")'),
    ("/ip/", "/clientip/"),
    ('@RequestMapping("/csrf")', '@RequestMapping("/form")'),
    ("/csrf/", "/form/"),
    ('@RestController(value = "/qlexpress")', '@RestController'),
    ('@RequestMapping("/qlexpress")', '@RequestMapping("/rules")'),
    ("/qlexpress/", "/rules/"),
    ("/qlexpress/**", "/rules/**"),
    ('@RequestMapping("/classloader")', '@RequestMapping("/module")'),
    ('@RequestMapping("uri")', '@RequestMapping("/access")'),
    ('@RequestMapping("ooxml")', '@RequestMapping("/office/ooxml")'),
    ('@RequestMapping("xlsx-streamer")', '@RequestMapping("/office/xlsx")'),
    # messages that leak
    ("[-] SSRF check failed", "[-] url check failed"),
    ("SSRF check failed", "url check failed"),
    ("ImageIO ssrf test", "ImageIO proxy test"),
    ("IOUtils ssrf test", "IOUtils proxy test"),
    ("Shiro deserialize", "session restore"),
    ("return \"xstream\"", 'return "xmlstream"'),
    # variable names that leak in XXE
    ("NodeList xxe =", "NodeList nodes ="),
    ("for (int j = 0; j < xxe.getLength(); j++)", "for (int j = 0; j < nodes.getLength(); j++)"),
    ("Node xxeNode = xxe.item(j)", "Node itemNode = nodes.item(j)"),
    ("xxeNode.getNodeValue()", "itemNode.getNodeValue()"),
    # XSS param name in ContentView
    ("String xss)", "String text)"),
    ("String xss,", "String text,"),
    ("@CookieValue(\"xss\") String xss", '@CookieValue("msg") String text'),
    ("new Cookie(\"xss\", xss)", 'new Cookie("msg", text)'),
    ("encode(xss)", "encode(text)"),
    ("return xss;", "return text;"),
    # JobRunner cmd param (only annotations / method signatures - careful)
    # leave Runtime API alone
    # comments cleanup
    ("// This will cause all XStream versions to be affected.", ""),
    ("// Insecure configuration", ""),
    ("// Fix method: update xstream to 1.4.11", ""),
    ("// 解析SSRF配置", "// parse url allowlist config"),
    ("// 解析SSRF配置", "// parse url allowlist config"),
    ("解析SSRF配置", "parse url allowlist config"),
    ("// 域名支持一级或者多级，如果在白名单。SecurityUtil.checkUrlByWhitehosts()方法的域名配置",
     "// domain allowlist for checkUrlByWhitehosts"),
]

# Path replacements for properties / html that may not have quotes as above
PATH_GLOBAL = [
    ("/ssrf/", "/proxy/"),
    ("/ssrf/**", "/proxy/**"),
    ("/xxe/", "/xml/"),
    ("/xxe/**", "/xml/**"),
    ("/rce/", "/job/"),
    ("/rce/**", "/job/**"),
    ("/sqli/", "/query/"),
    ("/deserialize/", "/object/"),
    ("/deserialize/**", "/object/**"),
    ("/fastjson/", "/jsonapi/"),
    ("/fastjson/**", "/jsonapi/**"),
    ("/xstream/", "/xmlstream/"),
    ("/xstream/**", "/xmlstream/**"),
    ("/spel/", "/expr/"),
    ("/spel/**", "/expr/**"),
    ("/shiro/", "/session/"),
    ("/shiro/**", "/session/**"),
    ("/qlexpress/", "/rules/"),
    ("/qlexpress/**", "/rules/**"),
    ("/jsonp/", "/callback/"),
    ("/jsonp/**", "/callback/**"),
    ("/cors/", "/crossdomain/"),
    ("/path_traversal/", "/assets/"),
    ("/codeinject", "/tools/file"),
    ("/urlRedirect/", "/nav/"),
    ("/log4j", "/applog"),
    ("/jwt/", "/token/"),
]


def move_classes() -> None:
    base = ROOT / "src/main/java/org/joychou"
    for old_rel, new_rel in CLASS_RENAMES:
        src = base / old_rel
        dst = base / new_rel
        if not src.exists():
            if dst.exists():
                print(f"  skip (already moved): {old_rel}")
            else:
                print(f"  missing: {old_rel}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        print(f"  move {old_rel} -> {new_rel}")
    # remove empty ssrf dir
    ssrf = base / "security/ssrf"
    if ssrf.exists() and not any(ssrf.iterdir()):
        ssrf.rmdir()
        print("  removed empty security/ssrf")


def rename_resource_xml() -> None:
    old = ROOT / "src/main/resources/url/ssrf_safe_domain.xml"
    new = ROOT / "src/main/resources/url/url_safe_domain.xml"
    if old.exists():
        text = old.read_text(encoding="utf-8")
        for a, b in IDENT_REPLACEMENTS + PATH_GLOBAL:
            text = text.replace(a, b)
        new.write_text(text, encoding="utf-8")
        old.unlink()
        print("  renamed ssrf_safe_domain.xml -> url_safe_domain.xml")


def apply_text_replacements() -> None:
    exts = {".java", ".xml", ".html", ".properties", ".yml", ".md", ".json"}
    roots = [
        ROOT / "src",
        ROOT / "benchmark",
        ROOT / "pom.xml",
        ROOT / "README.md",
        ROOT / "README_zh.md",
    ]
    files: list[Path] = []
    for r in roots:
        if r.is_file():
            files.append(r)
        elif r.is_dir():
            for p in r.rglob("*"):
                if p.is_file() and p.suffix in exts:
                    files.append(p)

    # also transform scripts references? skip

    changed = 0
    for path in files:
        # skip this script
        if "business_rename" in path.name:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        orig = text
        for a, b in IDENT_REPLACEMENTS:
            text = text.replace(a, b)
        for a, b in PATH_GLOBAL:
            text = text.replace(a, b)

        # Logger class refs after renames
        text = text.replace("LoggerFactory.getLogger(SQLI.class)", "LoggerFactory.getLogger(UserQuery.class)")
        text = text.replace("LoggerFactory.getLogger(SSRF.class)", "LoggerFactory.getLogger(ResourceProxy.class)")
        text = text.replace("LoggerFactory.getLogger(XXE.class)", "LoggerFactory.getLogger(XmlImport.class)")

        # Fastjson controller path already handled; Index app field name ok

        # Fix QLExpress RestController - ensure RequestMapping /rules exists
        if path.name == "RuleEngine.java":
            if '@RequestMapping("/rules")' not in text and "@RestController" in text:
                text = text.replace(
                    "@RestController",
                    '@RestController\n@RequestMapping("/rules")',
                    1,
                )
            # strip leftover teaching comment block about URLClassLoader if still present
            text = re.sub(
                r"/\*\*[\s\S]*?URLClassLoader[\s\S]*?\*/\s*",
                "",
                text,
                count=1,
            )

        # Strip remaining educational comments in XmlStreamApi
        if path.name == "XmlStreamApi.java":
            text = re.sub(r"/\*\*[\s\S]*?\*/\s*", "", text, count=1)

        # ResourceProxy leftover comments with /proxy already ok; strip long teaching javadocs with baidu.com attack samples
        if path.suffix == ".java":
            # remove javadoc that still contains attack-like samples
            def drop_leak_javadoc(m: re.Match) -> str:
                body = m.group(0)
                if re.search(
                    r"localhost:8080|whoami|/etc/passwd|alert\(|Calculator|ldap://|evil\.|bypass|POC|payload",
                    body,
                    re.I,
                ):
                    return ""
                return body

            text = re.sub(r"/\*\*[\s\S]*?\*/", drop_leak_javadoc, text)

        if text != orig:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"  update {path.relative_to(ROOT)}")
    print(f"[ok] text updates: {changed}")


def rewrite_index() -> None:
    (ROOT / "src/main/resources/templates/index.html").write_text(
        """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8" />
    <title>Home</title>
</head>
<body>
<p>Hello <span th:text="${user}"></span>.</p>
<p>Welcome to java-ai-benchmark. <a th:href="@{/appInfo}">Application Information</a></p>
<p>
    <a th:href="@{/swagger-ui.html}">Swagger</a>&nbsp;&nbsp;
    <a th:href="@{/tools/file}">File Tool</a>&nbsp;&nbsp;
    <a th:href="@{/callback/getToken}">Callback</a>&nbsp;&nbsp;
    <a th:href="@{/file/pic}">Picture Upload</a>&nbsp;&nbsp;
    <a th:href="@{/file/any}">File Upload</a>&nbsp;&nbsp;
    <a th:href="@{/crossdomain/sec/originFilter}">Cross Domain</a>&nbsp;&nbsp;
    <a th:href="@{/assets/case}">Assets</a>&nbsp;&nbsp;
    <a th:href="@{/query/mybatis/case01}">Query</a>&nbsp;&nbsp;
    <a th:href="@{/proxy/urlConnection/case}">Proxy</a>&nbsp;&nbsp;
    <a th:href="@{/job/runtime/exec}">Job</a>&nbsp;&nbsp;
    <a th:href="@{/office/ooxml/upload}">OOXML</a>&nbsp;&nbsp;
    <a th:href="@{/office/xlsx/upload}">XLSX</a>&nbsp;&nbsp;
    <a th:href="@{/env}">Actuator</a>
</p>
<p>
    <a th:href="@{/token/createToken}">Create Token</a>
    <a th:href="@{/token/getName}">Parse Token</a>
</p>
<a th:href="@{/logout}">logout</a>
</body>
</html>
""",
        encoding="utf-8",
    )
    print("[ok] index.html")


def rewrite_ground_truth() -> None:
    gt_path = ROOT / "benchmark/ground-truth.json"
    gt = json.loads(gt_path.read_text(encoding="utf-8"))

    file_map = {
        "controller/SSRF.java": "controller/ResourceProxy.java",
        "controller/XXE.java": "controller/XmlImport.java",
        "controller/SQLI.java": "controller/UserQuery.java",
        "controller/Rce.java": "controller/JobRunner.java",
        "controller/XSS.java": "controller/ContentView.java",
        "controller/SpEL.java": "controller/ExprService.java",
        "controller/SSTI.java": "controller/TemplateService.java",
        "controller/CommandInject.java": "controller/FileTool.java",
        "controller/PathTraversal.java": "controller/AssetStore.java",
        "controller/Deserialize.java": "controller/ObjectStore.java",
        "controller/Fastjson.java": "controller/JsonApi.java",
        "controller/XStreamRce.java": "controller/XmlStreamApi.java",
        "controller/CRLFInjection.java": "controller/HeaderWriter.java",
        "controller/Cors.java": "controller/CrossDomain.java",
        "controller/Jsonp.java": "controller/JsonCallback.java",
        "controller/Log4j.java": "controller/AppLogger.java",
        "controller/Shiro.java": "controller/SessionAuth.java",
        "controller/Jwt.java": "controller/AuthToken.java",
        "controller/URLRedirect.java": "controller/NavRedirect.java",
        "controller/URLWhiteList.java": "controller/DomainGate.java",
        "controller/IPForge.java": "controller/ClientAddress.java",
        "controller/GetRequestURI.java": "controller/PathAccess.java",
        "controller/QLExpress.java": "controller/RuleEngine.java",
        "controller/office/ooxmlXXE.java": "controller/office/OoxmlReader.java",
        "controller/office/xlsxStreamerXXE.java": "controller/office/XlsxReader.java",
        "controller/FileUpload.java": "controller/UploadApi.java",
    }

    method_map = {
        "jdbc_sqli_case": "jdbc_query_case",
        "jdbc_sqli_safe": "jdbc_query_safe",
        "URLConnectionCase": "urlConnectionCase",
        "URLConnectionSec": "urlConnectionSafe",
        "httpURLConnectionCase": "httpUrlConnectionCase",
        "ooxml_xxe": "readOoxml",
        "xllx_streamer_xxe": "readXlsxStream",
        "reflect": "reflect",
        "CommandExec": "CommandExec",
        "case1": "case1",
    }

    endpoint_map = [
        ("/ssrf/", "/proxy/"),
        ("/xxe/", "/xml/"),
        ("/sqli/", "/query/"),
        ("/rce/", "/job/"),
        ("/xss/", "/content/"),
        ("/spel/", "/expr/"),
        ("/ssti/", "/tpl/"),
        ("/path_traversal/", "/assets/"),
        ("/deserialize/", "/object/"),
        ("/fastjson/", "/jsonapi/"),
        ("/xstream", "/xmlstream"),
        ("/codeinject", "/tools/file"),
        ("/crlf/", "/header/"),
        ("/cors/", "/crossdomain/"),
        ("/jsonp/", "/callback/"),
        ("/log4j", "/applog"),
        ("/shiro/", "/session/"),
        ("/jwt/", "/token/"),
        ("/urlRedirect/", "/nav/"),
        ("/url/", "/domain/"),
        ("/ip/", "/clientip/"),
        ("/qlexpress/", "/rules/"),
        ("/ooxml/", "/office/ooxml/"),
        ("/xlsx-streamer/", "/office/xlsx/"),
        ("/exclued/", "/access/exclued/"),
    ]

    def map_file(f: str | None) -> str | None:
        if not f:
            return f
        for old, new in file_map.items():
            if f.endswith(old):
                return f[: -len(old)] + new
        return f

    def map_endpoint(e: str | None) -> str | None:
        if not e:
            return e
        for a, b in endpoint_map:
            e = e.replace(a, b)
        return e

    for inst in gt["instances"]:
        inst["file"] = map_file(inst.get("file"))
        if inst.get("method") in method_map:
            inst["method"] = method_map[inst["method"]]
        if inst.get("endpoint"):
            inst["endpoint"] = map_endpoint(inst["endpoint"])
        # method renames already in method_map; also handle null methods

    for hn in gt.get("hard_negatives", []):
        hn["file"] = map_file(hn.get("file"))
        if hn.get("method") in method_map:
            hn["method"] = method_map[hn["method"]]
        # specific hard neg methods
        if hn.get("method") == "jdbc_sqli_safe":
            hn["method"] = "jdbc_query_safe"
        if hn.get("method") == "URLConnectionSec":
            hn["method"] = "urlConnectionSafe"

    # fix hard neg methods explicitly
    for hn in gt.get("hard_negatives", []):
        m = hn.get("method")
        if m == "jdbc_sqli_safe":
            hn["method"] = "jdbc_query_safe"
        if m == "URLConnectionSec":
            hn["method"] = "urlConnectionSafe"

    gt["version"] = "1.1.0"
    gt["notes"] = gt.get("notes", []) + [
        "v1.1.0: business-domain class/path disguise applied."
    ]
    gt_path.write_text(json.dumps(gt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("[ok] ground-truth.json updated")


def rewrite_prompt_example() -> None:
    p = ROOT / "benchmark/prompts/static_audit.md"
    if p.exists():
        t = p.read_text(encoding="utf-8")
        t = t.replace("SQLI.java", "UserQuery.java")
        t = t.replace("jdbc_sqli_case", "jdbc_query_case")
        p.write_text(t, encoding="utf-8")


def post_check() -> None:
    print("\n[check] residual security-domain names in src (sample):")
    patterns = [
        r"\bclass SSRF\b",
        r"\bclass XXE\b",
        r"\bclass SQLI\b",
        r"\bclass Rce\b",
        r"\bclass XSS\b",
        r"@RequestMapping\(\"/ssrf",
        r"@RequestMapping\(\"/xxe",
        r"@RequestMapping\(\"/sqli",
        r"@RequestMapping\(\"/rce",
        r"@RequestMapping\(\"/xss",
        r"security\.ssrf",
        r"othervulns",
        r"/path_traversal",
        r"/codeinject",
        r"checkSSRF",
        r"SSRFChecker",
        r"SSRFException",
    ]
    hits = 0
    for path in (ROOT / "src").rglob("*"):
        if not path.is_file() or path.suffix not in {".java", ".xml", ".html", ".properties"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pat in patterns:
            for m in re.finditer(pat, text):
                line = text[: m.start()].count("\n") + 1
                print(f"  {path.relative_to(ROOT)}:{line}: {text.splitlines()[line-1].strip()[:100]}")
                hits += 1
    print("  clean" if hits == 0 else f"  hits={hits}")


def fix_content_view() -> None:
    """Ensure ContentView params are business-neutral after bulk replace."""
    p = ROOT / "src/main/java/org/joychou/controller/ContentView.java"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    text = text.replace("@RequestMapping(\"/xss\")", "@RequestMapping(\"/content\")")
    text = text.replace("class XSS", "class ContentView")
    # param xss -> text if still present
    text = re.sub(r"\bString xss\b", "String text", text)
    text = text.replace("return xss;", "return text;")
    text = text.replace("encode(xss)", "encode(text)")
    text = text.replace('new Cookie("xss", text)', 'new Cookie("msg", text)')
    text = text.replace('new Cookie("xss", xss)', 'new Cookie("msg", text)')
    text = text.replace('@CookieValue("xss") String text', '@CookieValue("msg") String text')
    text = text.replace('@CookieValue("msg") String xss', '@CookieValue("msg") String text')
    p.write_text(text, encoding="utf-8")
    print("[ok] ContentView.java fixed")


def fix_crossdomain_filters() -> None:
    """Filters still reference /cors/sec paths — PATH_GLOBAL should have fixed; verify key files."""
    for rel in [
        "src/main/java/org/joychou/filter/OriginFilter.java",
        "src/main/java/org/joychou/filter/BaseCorsFilter.java",
        "src/main/java/org/joychou/config/CustomCorsConfig.java",
        "src/main/java/org/joychou/security/WebSecurityConfig.java",
    ]:
        p = ROOT / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        t2 = t.replace("/cors/", "/crossdomain/")
        if t2 != t:
            p.write_text(t2, encoding="utf-8")
            print(f"  cors path fix {rel}")


def fix_upload_paths() -> None:
    # UploadApi may still use /file — that's fine (business). Keep.
    pass


def fix_job_runner_params() -> None:
    p = ROOT / "src/main/java/org/joychou/controller/JobRunner.java"
    if not p.exists():
        return
    t = p.read_text(encoding="utf-8")
    # rename user-facing param cmd -> command in method signatures only
    t = re.sub(r"\bString cmd\b", "String command", t)
    t = t.replace("run.exec(cmd)", "run.exec(command)")
    t = t.replace('{"/bin/sh", "-c", cmd}', '{"/bin/sh", "-c", command}')
    # ProcessBuilder uses arrCmd already
    p.write_text(t, encoding="utf-8")
    print("[ok] JobRunner param rename")


def fix_app_properties() -> None:
    p = ROOT / "src/main/resources/application.properties"
    t = p.read_text(encoding="utf-8")
    for a, b in PATH_GLOBAL + [
        ("/ssrf/**", "/proxy/**"),
        ("/xxe/**", "/xml/**"),
        ("/rce/**", "/job/**"),
        ("/deserialize/**", "/object/**"),
        ("/fastjson/**", "/jsonapi/**"),
        ("/xstream/**", "/xmlstream/**"),
        ("/spel/**", "/expr/**"),
        ("/shiro/**", "/session/**"),
        ("/qlexpress/**", "/rules/**"),
        ("/jsonp/**", "/callback/**"),
    ]:
        t = t.replace(a, b)
    p.write_text(t, encoding="utf-8")
    print("[ok] application.properties")


def main() -> None:
    print("== Business-domain rename ==")
    move_classes()
    rename_resource_xml()
    apply_text_replacements()
    rewrite_index()
    fix_content_view()
    fix_crossdomain_filters()
    fix_job_runner_params()
    fix_app_properties()
    rewrite_ground_truth()
    rewrite_prompt_example()
    post_check()
    print("Done.")


if __name__ == "__main__":
    main()
