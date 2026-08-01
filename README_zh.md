# JoyChou Platform

基于 Spring Boot 的内部 Web 平台，覆盖账号登录、内容接口、文件/文档处理、后台任务与第三方资源集成等能力。

[English](./README.md)

## 功能概览

- Spring Security 表单登录与记住我
- 用户查询与 MyBatis 数据访问
- 文件 / 图片上传
- Office 文档与 XML 导入
- HTTP 资源代理与外联请求工具
- 后台任务与表达式执行接口
- JWT 签发与解析
- JSONP 回调接口
- 可选 Swagger UI
- WebSocket 通道注册
- Spring Boot Actuator 端点

## 技术栈

| 组件 | 说明 |
|---|---|
| Java | 8+ |
| Spring Boot | 1.5.1.RELEASE |
| Spring Security | starter 集成 |
| MyBatis | MySQL Mapper |
| Thymeleaf | 服务端页面 |
| 打包方式 | 可执行 JAR |

## 环境要求

- JDK 8+
- Maven 3.x
- MySQL 5.7 / 8.x（使用自带数据库的 Docker 镜像时可省略）

本地建库示例：

```sql
CREATE DATABASE joychou_platform DEFAULT CHARACTER SET utf8mb4;
```

默认数据源（`src/main/resources/application.properties`）：

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/joychou_platform?allowPublicKeyRetrieval=true&useSSL=false&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=woshishujukumima
```

启动前请按实际环境修改账号密码。

## 快速启动

### Docker

```bash
docker-compose pull
docker-compose up
```

停止：

```bash
docker-compose down
```

### IDEA

1. 用 IntelliJ IDEA 打开项目  
2. 确认 MySQL 已启动且 `application.properties` 配置正确  
3. 运行 `org.joychou.Application`

### Maven 打包

```bash
mvn clean package -DskipTests
java -jar target/joychou-platform-1.0.0.jar
```

默认访问地址：`http://localhost:8080`

## 登录

| 用户名 | 密码 |
|---|---|
| admin | admin123 |
| joychou | joychou123 |

- 登录：`http://localhost:8080/login`
- 登出：`http://localhost:8080/logout`
- 首页：`http://localhost:8080/index`
- 应用信息：`http://localhost:8080/appInfo`
- Swagger：`http://localhost:8080/swagger-ui.html`（开启时）

Remember-me 会在 Tomcat 默认 30 分钟空闲超时之外延长会话（默认约两周）。

## 目录结构

```text
.
├── docker-compose.yml
├── pom.xml
└── src/main
    ├── java/org/joychou
    │   ├── Application.java
    │   ├── config/          # CORS、域名、Swagger、WebSocket
    │   ├── controller/      # HTTP 接口与页面
    │   ├── dao/
    │   ├── filter/
    │   ├── mapper/
    │   ├── security/
    │   ├── service/
    │   └── util/
    └── resources
        ├── application.properties
        ├── mapper/
        ├── templates/
        └── url/             # 域名白名单配置
```

## 主要模块

| 模块 | 路径前缀 | 说明 |
|---|---|---|
| 登录认证 | `/login`、`/logout` | 表单登录 |
| 用户查询 | `/query` | JDBC / MyBatis 查询 |
| 内容 | `/content` | 内容展示 / Cookie 示例 |
| 资源文件 | `/assets` | 文件读取辅助 |
| 上传 | `/file` |  multipart 上传 |
| 代理 | `/proxy` | 服务端 URL 拉取 |
| 任务 | `/job` | 运行时 / 脚本 / YAML 入口 |
| XML 导入 | `/xml` | 多种 XML 解析集成 |
| Office | `/office/*` | OOXML / XLSX 读取 |
| 对象存储 | `/object` | 对象还原相关接口 |
| JSON 接口 | `/jsonapi` | Fastjson 解析 |
| 规则引擎 | `/rules` | QLExpress 规则执行 |
| 表达式 | `/expr` | SpEL 求值 |
| 模板 | `/tpl` | Velocity 模板 |
| 令牌 | `/token` | JWT 签发 / 解析 |
| 会话 | `/session` | 会话 Cookie 还原 |
| 域名门禁 | `/domain` | URL 白名单校验 |
| 导航跳转 | `/nav` | 重定向辅助 |
| 回调 | `/callback` | JSONP 风格响应 |
| 跨域 | `/crossdomain` | CORS 相关处理 |
| 客户端 IP | `/clientip` | 客户端地址解析 |
| 日志 | `/applog` | 应用日志示例 |
| 工具 | `/tools/file` | 主机 / 路径工具接口 |

完整路由以 `src/main/java/org/joychou/controller/` 下各 Controller 为准。

## 配置说明

- CSRF：`joychou.security.csrf.enabled`
- 免登录路径：`joychou.no.need.login.url`
- JSONP 回调参数：`joychou.business.callback` / `joychou.security.jsonp.callback`
- 安全域名列表：`src/main/resources/url/`
- Actuator：`management.security.enabled`

## 开发命令

```bash
mvn -DskipTests compile
mvn clean package -DskipTests
```

Docker 环境暴露 `8000` 端口用于 JDWP 远程调试。

## 贡献者

- [JoyChou](https://github.com/JoyChou93)
- [liergou9981](https://github.com/liergou9981)
- [lightless](https://github.com/lightless233)
- [Anemone95](https://github.com/Anemone95)
- [waderwu](https://github.com/waderwu)

欢迎提交 PR。

## 使用说明

请在已获授权的环境中部署与使用本项目。
