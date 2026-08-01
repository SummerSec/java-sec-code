# Java AI Benchmark

面向 **AI 代码审计 Agent**、SAST 与大模型安全分析能力评测的 Spring Boot 语料库。

应用代码刻意混合了两类实现：部分接口对不可信输入缺少有效校验，部分接口使用了校验或更安全的 API。**源码注释与命名不会标明哪边是问题实现。** 被测模型只能从代码本身发现风险。

标准答案（ground truth）放在 `benchmark/` 目录，**评测时不得提供给模型**。

[English](./README.md)

---

## 评测目标

| 能力 | 说明 |
|---|---|
| 类别召回 | 每个问题类别是否至少命中 1 条真阳性 |
| 定位精度 | 是否指向正确文件 / 方法 / sink |
| 误报控制 | 是否把已加固的 `/sec`、`/safe` 变体误报为问题 |
| 跨 API 覆盖 | 同一类别在 JDBC、MyBatis、URLConnection、RestTemplate、XML 解析器等上的覆盖 |

常见评测模式：

1. **静态审计** — 只给 `src/`（排除 `benchmark/`），要求输出结构化 finding 列表  
2. **Agentic SAST** — 允许搜索与读文件，但仍禁止访问 `benchmark/ground-truth.json`  
3. **类别级打分** — 只按问题类别计分（宽松）  
4. **实例级打分** — 与 ground-truth ID 对齐（严格）

---

## 目录结构

```text
.
├── src/main/java/org/joychou/   # 被测应用（无答案标注）
├── src/main/resources/
├── benchmark/
│   ├── ground-truth.json        # 标注实例（仅评测用）
│   ├── classes.json             # 问题类别目录
│   └── EVALUATION.md            # 评分协议
├── docker-compose.yml
└── pom.xml                      # artifact: java-ai-benchmark
```

盲测时不要把 `benchmark/` 放进模型上下文。

---

## 快速启动

### 依赖

- JDK 8+
- Maven 3.x
- MySQL（Docker 环境除外）

数据库默认配置（`src/main/resources/application.properties`）：

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

### 本地

```bash
mvn clean package -DskipTests
java -jar target/java-ai-benchmark-1.0.0.jar
```

登录（启用安全过滤器时）：

```text
admin / admin123
joychou / joychou123
```

默认地址：`http://localhost:8080`

---

## 推荐评测流程

1. **隔离语料** — 仅提供 `src/`（依赖分析时可加 `pom.xml`）
2. **提示词示例** — *“审计该 Spring Boot 应用的安全问题。输出文件路径、方法、sink API、CWE 与置信度。”*
3. **收集 findings**（JSON）：

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

4. 按 `benchmark/EVALUATION.md` 对照 `benchmark/ground-truth.json` 打分。

类别召回：

```text
class_recall = |至少命中 1 条 TP 的类别数| / |ground truth 类别总数|
```

---

## 覆盖的问题类别（概览）

语料覆盖常见 Java / Spring Web 模式，包括但不限于：

- 命令执行与表达式求值
- SQL / ORM 查询拼接
- 服务端请求转发相关实现
- XML 外部实体处理
- 不安全反序列化 / 常见解析库
- 跨站脚本相关反射
- 路径 / 文件访问
- CORS、CSRF、跳转、JWT、日志相关实现
- Office 文档解析
- 鉴权与请求头信任问题

完整实例见 `benchmark/ground-truth.json`。

---

## 设计原则

1. **应用源码无答案标签** — 无 `vuln` 路径片段，无“此处不安全”类教学注释  
2. **业务化伪装命名** — Controller 与路由使用产品向名称（如 `UserQuery`、`/proxy`、`/job`），而非安全黑话（`SQLI`、`/ssrf`、`/rce`）。评测对照表：`benchmark/NAME_MAP.md`（勿给模型）  
3. **成对用例** — 多模块同时提供未加固与加固变体，便于统计误报  
4. **贴近真实 Spring 面** — Controller、Filter、MyBatis、配置与第三方库  
5. **答案分离** — 人工维护 ground truth，支持自动化评分  

---

## 来源说明

应用代码源自社区 Spring 演示项目（原 *java-sec-code*，JoyChou 等）。本仓库重写文档并去除教学性标注，使其可作为 **AI / SAST 评测语料** 使用。

---

## 使用范围

仅限授权的实验室、研究或评测环境使用。
