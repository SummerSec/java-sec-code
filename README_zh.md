# Java AI Benchmark（评测分支）

本分支在应用源码之上附带 **AI / SAST 代码审计评测资产**。

| 分支 | 内容 |
|---|---|
| [`master`](https://github.com/SummerSec/java-sec-code/tree/master) | 仅应用代码 — 产品向 README，不含答案 |
| **`benchmark`（当前分支）** | 应用代码 + `benchmark/` 标注 + `scripts/` 辅助脚本 |

## 推荐流程

### 1. 盲测（给模型的上下文）

只使用 **master**。不要把本分支的 `benchmark/` 目录交给模型。

```bash
git clone https://github.com/SummerSec/java-sec-code.git
cd java-sec-code
git checkout master
# 将 src/（可选 pom.xml）提供给模型
```

### 2. 打分（仅评测方）

```bash
git show benchmark:benchmark/ground-truth.json > ground-truth.json
git show benchmark:benchmark/score.py > score.py
python score.py findings.json
```

或：

```bash
git checkout benchmark
python benchmark/score.py findings.json
```

## 本分支目录

```text
.
├── src/
├── benchmark/
│   ├── ground-truth.json
│   ├── classes.json
│   ├── EVALUATION.md
│   ├── NAME_MAP.md
│   ├── prompts/static_audit.md
│   └── score.py
└── scripts/
```

## 指标

详见 `benchmark/EVALUATION.md`。

```text
class_recall = |至少命中 1 条 TP 的类别| / |类别总数|
```

实例级 P/R/F1 使用 `benchmark/score.py`。

## 说明

- Controller 使用业务化命名（如 `UserQuery`、`/proxy`）。对照表：`benchmark/NAME_MAP.md`。
- `/sec`、`/safe` 加固实现不应被报为问题（hard negatives）。
- 声称 zero-shot 时，请勿把 `benchmark/` 放入训练或 few-shot 上下文。

## 产品文档

安装、登录、模块与 Docker 说明见 **master** README：

https://github.com/SummerSec/java-sec-code/blob/master/README.md
