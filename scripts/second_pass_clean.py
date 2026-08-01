#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

# --- index.html ---
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
    <a th:href="@{/codeinject}">Cmd</a>&nbsp;&nbsp;
    <a th:href="@{/jsonp/getToken}">JSONP</a>&nbsp;&nbsp;
    <a th:href="@{/file/pic}">Picture Upload</a>&nbsp;&nbsp;
    <a th:href="@{/file/any}">File Upload</a>&nbsp;&nbsp;
    <a th:href="@{/cors/sec/originFilter}">Cors</a>&nbsp;&nbsp;
    <a th:href="@{/path_traversal/case}">File Read</a>&nbsp;&nbsp;
    <a th:href="@{/sqli/mybatis/case01}">Query</a>&nbsp;&nbsp;
    <a th:href="@{/ssrf/urlConnection/case}">URL Fetch</a>&nbsp;&nbsp;
    <a th:href="@{/rce/runtime/exec}">Exec</a>&nbsp;&nbsp;
    <a th:href="@{/ooxml/upload}">OOXML</a>&nbsp;&nbsp;
    <a th:href="@{/xlsx-streamer/upload}">XLSX</a>&nbsp;&nbsp;
    <a th:href="@{/env}">Actuator</a>
</p>
<p>
    <a th:href="@{/jwt/createToken}">JWT Create</a>
    <a th:href="@{/jwt/getName}">JWT Parse</a>
</p>
<a th:href="@{/logout}">logout</a>
</body>
</html>
""",
    encoding="utf-8",
)
print("index.html rewritten")

# --- pom ---
pom = ROOT / "pom.xml"
t = pom.read_text(encoding="utf-8")
t = t.replace("<!-- For testing, you can use the unrestricted version of 1.4.10. -->", "")
t = t.replace(" <!-- use latest version to exploit case by using xstream.addPermission-->", "")
t = t.replace("<!-- case maven jar. Solve xlsx.-->", "<!-- xlsx support -->")
t = t.replace("<groupId>sec</groupId>", "<groupId>org.benchmark</groupId>")
t = t.replace("<artifactId>java-sec-code</artifactId>", "<artifactId>java-ai-benchmark</artifactId>")
pom.write_text(t, encoding="utf-8")
print("pom.xml cleaned")

replacements = {
    "src/main/java/org/joychou/controller/XXE.java": [
        ("// parse xml", ""),
        ("// cause xxe", ""),
        ('private static final String EXCEPT = "xxe except";', 'private static final String EXCEPT = "xml error";'),
        ("// 测试不能blind xxe，所以强行加了一个回显", ""),
        ('logger.info("xxeNode: "', 'logger.info("node: "'),
    ],
    "src/main/java/org/joychou/controller/GetRequestURI.java": [
        ('return "You have bypassed the login page.";', 'return "ok";'),
    ],
    "src/main/java/org/joychou/controller/Dotall.java": [
        ("String poc =", "String sample ="),
        ('"Poc: " + poc', '"sample: " + sample'),
        ("path_pattern.matcher(poc)", "path_pattern.matcher(sample)"),
        ("sec_pattern.matcher(poc)", "sec_pattern.matcher(sample)"),
    ],
    "src/main/java/org/joychou/controller/Log4j.java": [
        ("String poc =", "String message ="),
        ("logger.error(poc);", "logger.error(message);"),
    ],
    "src/main/java/org/joychou/controller/Deserialize.java": [
        ("public void Jackson(String payload)", "public void Jackson(String content)"),
        ("mapper.readValue(payload, Object.class)", "mapper.readValue(content, Object.class)"),
    ],
    "src/main/java/org/joychou/controller/Fastjson.java": [
        ("String payload =", "String content ="),
        ("JSON.parseObject(payload,", "JSON.parseObject(content,"),
    ],
    "src/main/java/org/joychou/controller/URLWhiteList.java": [
        ('@GetMapping("/case/url_bypass")', '@GetMapping("/case/url_parse")'),
        ("public void url_bypass(", "public void url_parse("),
    ],
    "src/main/java/org/joychou/controller/office/ooxmlXXE.java": [
        ('return "ok"; // return xxe_upload.html page', 'return "ok";'),
    ],
    "src/main/java/org/joychou/controller/office/xlsxStreamerXXE.java": [
        ('return "ok"; // return xxe_upload.html page', 'return "ok";'),
        (
            'StreamingReader.builder().open((new FileInputStream("poc.xlsx")));',
            'StreamingReader.builder().open((new FileInputStream("sample.xlsx")));',
        ),
    ],
    "src/main/resources/templates/xxe_upload.html": [
        ("xlsx xxe test page", "xlsx upload page"),
    ],
    "src/main/java/org/joychou/security/AntObjectInputStream.java": [
        ("只允许反序列化SerialObject class", "Only allow SerialObject class"),
        (
            "在应用上使用黑白名单校验方案比较局限，因为只有使用自己定义的AntObjectInputStream类，进行反序列化才能进行校验。",
            "Whitelist checks only apply when this ObjectInputStream subclass is used.",
        ),
        ("类似fastjson通用类的反序列化就不能校验。", ""),
        ("// 创建一个包含对象进行反序列化信息的/tmp/object数据文件", "// write object to /tmp/object"),
        ("// 从文件中反序列化obj对象", "// read object from file"),
        ("//恢复对象即反序列化", "// restore object"),
    ],
    "src/main/java/org/joychou/config/TomcatFilterMemShell.java": [
        ("// 判断下防止重复注入", "// skip if already present"),
    ],
    "src/main/java/org/joychou/controller/Index.java": [
        ('"java security code"', '"java-ai-benchmark"'),
        ('"Java AI Benchmark"', '"java-ai-benchmark"'),
        ('"java-ai-benchmark"', '"java-ai-benchmark"'),
    ],
    "src/main/test/org/test/XStreamTest.java": [
        ("poc_xml", "sample_xml"),
        ("public void case01", "public void case01"),
    ],
    "src/main/test/org/test/QLExpressTest.java": [
        ("private static final String poc =", "private static final String sample ="),
        ("System.out.println(poc);", "System.out.println(sample);"),
        ("runner.execute(poc,", "runner.execute(sample,"),
        ("load evil class", "load remote class"),
    ],
}

for rel, pairs in replacements.items():
    p = ROOT / rel
    if not p.exists():
        print("missing", rel)
        continue
    text = p.read_text(encoding="utf-8")
    orig = text
    for a, b in pairs:
        text = text.replace(a, b)
    if text != orig:
        p.write_text(text, encoding="utf-8")
        print("updated", rel)
    else:
        print("no change", rel)

# strip leftover leak comments
leak_re = re.compile(
    r"(cause xxe|xxe vuln|POC|payload|exploit|漏洞|\bvuln\b|bypass the|gadget|evil class)",
    re.I,
)
for p in (ROOT / "src").rglob("*.java"):
    text = p.read_text(encoding="utf-8")
    lines = []
    changed = False
    for line in text.splitlines():
        if "//" in line and leak_re.search(line[line.find("//") :]):
            if line.strip().startswith("//"):
                changed = True
                continue
            code = line[: line.find("//")].rstrip()
            lines.append(code)
            changed = True
            continue
        lines.append(line)
    if changed:
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("comment-clean", p.relative_to(ROOT))

# application.properties db name cosmetic
props = ROOT / "src/main/resources/application.properties"
pt = props.read_text(encoding="utf-8")
pt2 = pt.replace("java_sec_code", "java_ai_benchmark")
if pt2 != pt:
    props.write_text(pt2, encoding="utf-8")
    print("application.properties db name updated")

print("second pass done")
