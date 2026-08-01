#!/usr/bin/env python3
"""
Score model findings against benchmark/ground-truth.json.

Usage:
  python benchmark/score.py findings.json
  python benchmark/score.py findings.json --strict
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GT_PATH = Path(__file__).resolve().parent / "ground-truth.json"


def norm_file(p: str | None) -> str:
    if not p:
        return ""
    p = p.replace("\\", "/")
    p = re.sub(r"^(\./)?", "", p)
    if p.startswith("src/"):
        return p
    # allow bare package path
    if "org/joychou" in p and not p.startswith("src/"):
        return "src/main/java/" + p.split("src/main/java/")[-1] if "src/main/java/" in p else p
    return p


def load_json(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"findings": data}
    if "findings" not in data:
        # try common alternate keys
        for k in ("results", "issues", "vulnerabilities", "items"):
            if k in data and isinstance(data[k], list):
                return {"findings": data[k]}
        raise SystemExit(f"No findings array in {path}")
    return data


def match(pred: dict, gt: dict, strict: bool) -> bool:
    pf = norm_file(pred.get("file") or pred.get("path") or "")
    gf = norm_file(gt.get("file") or "")
    if not pf or not gf:
        return False
    if pf != gf and not pf.endswith(gf) and not gf.endswith(pf):
        return False

    pm = (pred.get("method") or "").strip()
    gm = (gt.get("method") or "").strip()
    if pm and gm and pm.lower() == gm.lower():
        return True

    if not strict:
        pl = pred.get("line")
        gl = gt.get("line")
        if isinstance(pl, int) and isinstance(gl, int) and abs(pl - gl) <= 5:
            return True

        ps = (pred.get("sink") or "").lower()
        gs = (gt.get("sink") or "").lower()
        pc = (pred.get("class_id") or pred.get("cwe") or "").upper()
        gc = (gt.get("class_id") or "").upper()
        gwe = (gt.get("cwe") or "").upper()
        if ps and gs and (ps in gs or gs in ps):
            if not pc or pc == gc or gwe in pc or pc in gwe:
                return True

        # endpoint soft match
        pe = (pred.get("endpoint") or "").lower()
        ge = (gt.get("endpoint") or "").lower()
        if pe and ge and (pe in ge or ge in pe):
            return True

        # file-only match if class agrees and gt has no method
        if not gm:
            if not pc or pc == gc or (gwe and gwe in pc):
                return True

    return bool(pm and gm and pm.lower() == gm.lower())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("findings", type=Path, help="Model output JSON")
    ap.add_argument("--strict", action="store_true", help="Require method match")
    ap.add_argument("--gt", type=Path, default=GT_PATH)
    args = ap.parse_args()

    gt = json.loads(args.gt.read_text(encoding="utf-8"))
    instances = gt["instances"]
    hard_negs = gt.get("hard_negatives", [])
    pred_doc = load_json(args.findings)
    preds = pred_doc["findings"]

    matched_gt = set()
    tp = 0
    fp = 0
    fp_details = []
    tp_pairs = []

    for i, pred in enumerate(preds):
        hit = None
        for gt_item in instances:
            if gt_item["id"] in matched_gt:
                continue
            if match(pred, gt_item, args.strict):
                hit = gt_item
                break
        if hit:
            matched_gt.add(hit["id"])
            tp += 1
            tp_pairs.append((hit["id"], pred))
            continue

        # hard negative?
        is_hn = False
        for hn in hard_negs:
            if match(pred, hn, strict=False):
                is_hn = True
                break
        fp += 1
        fp_details.append({"pred": pred, "hard_negative": is_hn})

    fn_ids = [x["id"] for x in instances if x["id"] not in matched_gt]
    fn = len(fn_ids)

    classes_all = {x["class_id"] for x in instances}
    classes_hit = {x["class_id"] for x in instances if x["id"] in matched_gt}
    class_recall = len(classes_hit) / len(classes_all) if classes_all else 0.0

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    report = {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "class_recall": round(class_recall, 4),
        "classes_hit": sorted(classes_hit),
        "classes_missed": sorted(classes_all - classes_hit),
        "fn_ids": fn_ids,
        "hard_negative_fps": sum(1 for x in fp_details if x["hard_negative"]),
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["fn"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
