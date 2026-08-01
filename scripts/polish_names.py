#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def patch(rel: str, pairs: list[tuple[str, str]]) -> None:
    p = ROOT / rel
    if not p.exists():
        print("missing", rel)
        return
    t = p.read_text(encoding="utf-8")
    orig = t
    for a, b in pairs:
        t = t.replace(a, b)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        print("updated", rel)
    else:
        print("no change", rel)


def main() -> None:
    patch(
        "src/main/java/org/joychou/security/netguard/UrlGuard.java",
        [("checkURLFckSSRF", "checkUrlAllowlist")],
    )
    patch(
        "src/main/java/org/joychou/security/SecurityUtil.java",
        [("checkURLFckSSRF", "checkUrlAllowlist")],
    )
    patch(
        "src/main/java/org/joychou/controller/FileTool.java",
        [
            ("codeInjectHost", "listByHost"),
            ("codeInjectSec", "listSafe"),
            ("codeInject", "listFiles"),
            ('return "Bad boy. I got u.";', 'return "invalid path";'),
        ],
    )
    patch(
        "src/main/java/org/joychou/controller/JobRunner.java",
        [
            ("CommandExec", "runCommand"),
            ('@GetMapping("/jscmd")', '@GetMapping("/script")'),
            ("jsEngine", "runScript"),
        ],
    )
    patch(
        "src/main/java/org/joychou/controller/Index.java",
        [("fastjson_version", "json_lib_version")],
    )
    patch(
        "src/main/java/org/joychou/controller/JsonCallback.java",
        [
            ("fastjsonpCallback", "apiCallback"),
            ("/fastjsonp/", "/jsonpstyle/"),
        ],
    )

    gt_path = ROOT / "benchmark/ground-truth.json"
    gt = json.loads(gt_path.read_text(encoding="utf-8"))
    for inst in gt["instances"]:
        if inst.get("method") == "CommandExec":
            inst["method"] = "runCommand"
        if inst.get("method") == "jsEngine":
            inst["method"] = "runScript"
        if inst.get("endpoint") == "GET /job/jscmd":
            inst["endpoint"] = "GET /job/script"
    gt_path.write_text(json.dumps(gt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("ground-truth polished")


if __name__ == "__main__":
    main()
