#!/usr/bin/env python3
"""
Transform java-sec-code into an AI code-audit benchmark corpus.

- Neutralize vuln/漏洞 labels in paths, methods, comments, and return strings
- Rename package othervulns -> office
- Strip educational security comments that leak ground truth
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Keywords that mark a comment as ground-truth leakage (case-insensitive)
LEAK_PATTERNS = [
    r"\bvuln\b",
    r"\bvulnerable\b",
    r"\bvulnerability\b",
    r"\bvulnerabilities\b",
    r"漏洞",
    r"\bpoc\b",
    r"\bpayload\b",
    r"\bexploit\b",
    r"\binjection\b",
    r"security code",
    r"vuln code",
    r"safe code",
    r"fix code",
    r"修复",
    r"不安全",
    r"存在漏洞",
    r"CVE-\d",
    r"bypass",
    r"evil\.",
    r"/etc/passwd",
    r"whoami",
    r"alert\s*\(",
    r"Calculator",
    r"trigger vulnerability",
    r"xxe vuln",
    r"sql injection",
    r"spel injection",
    r"host injection",
    r"crlf",
    r"yaml-payload",
    r"artsploit",
    r"ldap://",
    r"commons-collections gadget",
    r"deserialize rce",
    r"反射",
    r"跨域漏洞",
    r"ssrf漏洞",
    r"path traversal vulns",
    r"must be vulnerable",
    r"vul code",
    r"vuln:",
    r"no crlf vulns",
]

LEAK_RE = re.compile("|".join(f"(?:{p})" for p in LEAK_PATTERNS), re.IGNORECASE)

# Line-level comment markers to blank when they leak
INLINE_LEAK_RE = re.compile(
    r"//.*(?:vuln|漏洞|POC|payload|exploit|security code|fix code|trigger vulnerability|"
    r"CVE-|xxe vuln|sqli vuln|不安全|修复该漏洞|认定为不安全|防止重复注入)",
    re.IGNORECASE,
)


def rename_othervulns_package() -> None:
    src = ROOT / "src/main/java/org/joychou/controller/othervulns"
    dst = ROOT / "src/main/java/org/joychou/controller/office"
    if src.exists():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.move(str(src), str(dst))
        print(f"[ok] moved package othervulns -> office")
    for path in dst.glob("*.java") if dst.exists() else []:
        text = path.read_text(encoding="utf-8")
        text = text.replace("org.joychou.controller.othervulns", "org.joychou.controller.office")
        path.write_text(text, encoding="utf-8")


def neutralize_identifiers(text: str) -> str:
    """Rename vuln-style identifiers without touching unrelated English words carefully."""
    # Order matters: longer / more specific first
    replacements = [
        ("othervulns", "office"),
        ("findByUserNameVuln", "findByUserNameCase"),
        ("mybatisVuln", "mybatisCase"),
        ("URLConnectionVuln", "URLConnectionCase"),
        ("httpURLConnectionVuln", "httpURLConnectionCase"),
        ("xmlReaderVuln", "xmlReaderCase"),
        ("SAXBuilderVuln", "SAXBuilderCase"),
        ("SAXReaderVuln", "SAXReaderCase"),
        ("SAXParserVuln", "SAXParserCase"),
        ("DigesterVuln", "DigesterCase"),
        ("DocumentBuilderVuln", "DocumentBuilderCase"),
        ("DocumentBuilderXincludeVuln", "DocumentBuilderXincludeCase"),
        ("XMLReaderVuln", "XMLReaderCase"),
        ("jdbc_ps_vuln", "jdbc_ps_case"),
        ("jdbc_sqli_vul", "jdbc_sqli_case"),
        ("jdbc_sqli_sec", "jdbc_sqli_safe"),
        ("spel_vuln", "spel_case"),
        ("spel_sec", "spel_safe"),
        ("secYarm", "safeYarm"),
        # path / mapping tokens
        ('"/vuln/', '"/case/'),
        ("'/vuln/", "'/case/"),
        ('"/vuln"', '"/case"'),
        ("'/vuln'", "'/case'"),
        ('"/vuln1"', '"/case1"'),
        ("'/vuln1'", "'/case1'"),
        ('"/vuln2"', '"/case2"'),
        ("value = \"/vuln", 'value = "/case'),
        ('"/rememberMe/vuln"', '"/rememberMe/case"'),
        ('"/exclued/vuln"', '"/exclued/case"'),
        ('"/path_traversal/vul"', '"/path_traversal/case"'),
        ('"/jdbc/vuln"', '"/jdbc/case"'),
        ('"/jdbc/ps/vuln"', '"/jdbc/ps/case"'),
        ('"/mybatis/vuln', '"/mybatis/case'),
        ('"/urlConnection/vuln"', '"/urlConnection/case"'),
        ('"/HttpURLConnection/vuln"', '"/HttpURLConnection/case"'),
        ('"/HttpSyncClients/vuln"', '"/HttpSyncClients/case"'),
        ('"/restTemplate/vuln', '"/restTemplate/case'),
        ('"/hutool/vuln"', '"/hutool/case"'),
        ('"/dnsrebind/vuln"', '"/dnsrebind/case"'),
        ('"/xmlReader/vuln"', '"/xmlReader/case"'),
        ('"/SAXBuilder/vuln"', '"/SAXBuilder/case"'),
        ('"/SAXReader/vuln"', '"/SAXReader/case"'),
        ('"/SAXParser/vuln"', '"/SAXParser/case"'),
        ('"/Digester/vuln"', '"/Digester/case"'),
        ('"/DocumentBuilder/vuln"', '"/DocumentBuilder/case"'),
        ('"/DocumentBuilder/xinclude/vuln"', '"/DocumentBuilder/xinclude/case"'),
        ('"/XMLReader/vuln"', '"/XMLReader/case"'),
        ('"/DocumentHelper/vuln"', '"/DocumentHelper/case"'),
        ('"/xmlbeam/vuln"', '"/xmlbeam/case"'),
        ('"/vuln/yarm"', '"/case/yarm"'),
        ('"/spel/vuln1"', '"/spel/case1"'),
        ('"spel/vuln2"', '"spel/case2"'),
        ('"/vuln01"', '"/case01"'),
        ('"/vuln02"', '"/case02"'),
        ('"/vuln03"', '"/case03"'),
        ('"/vuln04"', '"/case04"'),
        ('"/vuln05"', '"/case05"'),
        ('"/vuln06"', '"/case06"'),
        # method names remaining
        ("public void vuln01", "public void case01"),
        ("public void vuln1", "public void case1"),
        ("public String vuln01", "public String case01"),
        ("public String vuln02", "public String case02"),
        ("public String vuln03", "public String case03"),
        ("public String vuln04", "public String case04"),
        ("public String vuln05", "public String case05"),
        ("public String vuln06", "public String case06"),
        ("public String vuln1", "public String case1"),
        # return / log strings
        (" xxe vuln code", " processed"),
        (" xxe security code", " processed"),
        ("vuln code", "implementation"),
        ("security code", "implementation"),
        # variable names
        ("vuln_pattern", "path_pattern"),
        # generic path fragments still containing vuln
        ("/vuln/", "/case/"),
        ("/vuln1", "/case1"),
        ("/vuln2", "/case2"),
        ("/vuln?", "/case?"),
        ("/vuln ", "/case "),
        ("/vuln\"", "/case\""),
        ("/vuln'", "/case'"),
        ("/vul?", "/case?"),
        ("/vul\"", "/case\""),
        ("/vul'", "/case'"),
        ("/vul ", "/case "),
        # remaining Vuln/vuln identifiers (word-ish)
        ("Vuln", "Case"),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    # Remaining lowercase vuln as identifier fragment: vuln01, vuln, etc.
    text = re.sub(r"\bvuln(\d*)\b", r"case\1", text)
    text = re.sub(r"\bvulnerable\b", "unrestricted", text)
    text = re.sub(r"\bvulnerability\b", "issue", text)
    text = re.sub(r"\bvulnerabilities\b", "issues", text)

    # Chinese 漏洞
    text = text.replace("漏洞", "")
    return text


def strip_javadoc_blocks(text: str) -> str:
    """Remove javadoc / block comments that leak ground truth."""

    def repl_block(m: re.Match) -> str:
        body = m.group(0)
        if LEAK_RE.search(body):
            return ""
        return body

    # /** ... */ and /* ... */
    text = re.sub(r"/\*\*.*?\*/", repl_block, text, flags=re.DOTALL)
    text = re.sub(r"/\*[^*].*?\*/", repl_block, text, flags=re.DOTALL)
    return text


def strip_inline_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        # full-line // comment that leaks
        stripped = line.lstrip()
        if stripped.startswith("//") and LEAK_RE.search(stripped):
            continue
        # trailing // comment that leaks — drop the comment tail
        if "//" in line and LEAK_RE.search(line[line.find("//") :]):
            code = line[: line.find("//")].rstrip()
            if code:
                lines.append(code)
            continue
        lines.append(line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def clean_return_messages(text: str) -> str:
    # Neutralize leftover teaching return strings
    text = re.sub(
        r'return\s+"([^"]*(?:vuln|security code|xxe|POC)[^"]*)"',
        lambda m: 'return "ok"',
        text,
        flags=re.IGNORECASE,
    )
    return text


def process_text_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    text = original

    if path.suffix == ".java":
        text = strip_javadoc_blocks(text)
        text = strip_inline_comments(text)
        text = clean_return_messages(text)

    text = neutralize_identifiers(text)

    # pom.xml specific
    if path.name == "pom.xml":
        text = re.sub(
            r"<!--\s*For testing, you can use the vulnerable version[^>]*-->",
            "",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(
            r"<!--\s*use latest version to exploit vuln[^>]*-->",
            "",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(
            r"<!--\s*vuln maven jar[^>]*-->",
            "<!-- office document support -->",
            text,
            flags=re.IGNORECASE,
        )
        text = text.replace(
            '<!-- use latest version to exploit vuln by using xstream.addPermission-->',
            "",
        )
        text = re.sub(r"\bvulnerable\b", "previous", text, flags=re.IGNORECASE)
        text = re.sub(r"\bvuln\b", "case", text, flags=re.IGNORECASE)

    # html: neutralize demo links
    if path.suffix == ".html":
        text = text.replace("java-sec-code", "java-ai-benchmark")
        text = text.replace("java security code", "Java AI Benchmark")
        # remove attack-like query examples from links
        text = re.sub(
            r'(th:href="@\{[^}]*?)(\?[^}"]*)"',
            r'\1"',
            text,
        )
        # neutralize labels
        for old, new in [
            ("CmdInject", "Cmd"),
            ("SqlInject", "Query"),
            ("PathTraversal", "File"),
            ("ooxml XXE", "OOXML"),
            ("xlsx-streamer XXE", "XLSX"),
        ]:
            text = text.replace(old, new)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def walk_and_process() -> None:
    targets = []
    for pattern in [
        "src/**/*.java",
        "src/**/*.xml",
        "src/**/*.html",
        "src/**/*.properties",
        "src/**/*.yml",
        "pom.xml",
    ]:
        targets.extend(ROOT.glob(pattern))

    changed = 0
    for path in sorted(set(targets)):
        if path.is_file() and process_text_file(path):
            changed += 1
            print(f"  updated: {path.relative_to(ROOT)}")
    print(f"[ok] updated {changed} files")


def post_check() -> None:
    print("\n[check] remaining leak keywords in src:")
    patterns = [
        r"\bvuln\b",
        r"\bvulnerable\b",
        r"\bvulnerability\b",
        r"漏洞",
        r"othervulns",
        r"Vuln Code",
        r"vuln code",
    ]
    hits = 0
    for path in ROOT.glob("src/**/*"):
        if not path.is_file():
            continue
        if path.suffix not in {".java", ".xml", ".html", ".properties", ".yml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for pat in patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                # show line
                line_no = text[: m.start()].count("\n") + 1
                line = text.splitlines()[line_no - 1].strip()[:120]
                print(f"  {path.relative_to(ROOT)}:{line_no}: {line}")
                hits += 1
    if hits == 0:
        print("  clean")
    else:
        print(f"  total hits: {hits}")


def main() -> None:
    print("== Transform to AI Benchmark ==")
    rename_othervulns_package()
    walk_and_process()
    post_check()
    print("Done.")


if __name__ == "__main__":
    main()
