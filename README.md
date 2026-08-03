# JoyChou Platform

Internal Spring Boot web platform used for account login, content APIs, file/document handling, background jobs, and third-party resource integration.

[中文文档](./README_zh.md)

[Recent changes](./CHANGELOG.md)

## Features

- Spring Security form login with remember-me
- User query and MyBatis data access
- File / picture upload
- Office document and XML import
- HTTP resource proxy and outbound fetch helpers
- Background job and expression evaluation endpoints
- JWT token issue / parse
- JSONP callback APIs
- Swagger UI (optional)
- WebSocket channel registration
- Spring Boot Actuator endpoints

## Tech stack

| Component | Version / notes |
|---|---|
| Java | 8+ |
| Spring Boot | 1.5.1.RELEASE |
| Spring Security | via starter |
| MyBatis | MySQL mapper |
| Thymeleaf | server-side pages |
| Packaging | executable JAR |

## Requirements

- JDK 8+
- Maven 3.x
- MySQL 5.7 / 8.x for local runs (Docker Compose starts the application and MySQL services)

Create database (local run):

```sql
CREATE DATABASE joychou_platform DEFAULT CHARACTER SET utf8mb4;
```

Default datasource (`src/main/resources/application.properties`):

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/joychou_platform?allowPublicKeyRetrieval=true&useSSL=false&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=woshishujukumima
```

Adjust credentials for your environment before starting the app.

The checked-in schema bootstrap is `src/main/resources/create_db.sql`. Its `USE` statement still targets `java_sec_code`; change that database name to `joychou_platform` (or to your configured schema) before running it with the default datasource above. The script inserts `admin` and `joychou` rows.

## Quick start

### Docker

```bash
docker-compose pull
docker-compose up
```

Stop:

```bash
docker-compose down
```

### IDEA

1. Open the project in IntelliJ IDEA
2. Ensure MySQL is running and `application.properties` is correct
3. Run `org.joychou.Application`

### Maven package

```bash
mvn clean package -DskipTests
java -jar target/joychou-platform-1.0.0.jar
```

Application base URL: `http://localhost:8080`

Docker Compose publishes the application on `8080`, the JDWP debug port on `8000`, and the MySQL service on `3306`.

## Login

| Username | Password |
|---|---|
| admin | admin123 |
| joychou | joychou123 |

- Login: `http://localhost:8080/login`
- Logout: `http://localhost:8080/logout`
- Home: `http://localhost:8080/index`
- App info: `http://localhost:8080/appInfo`
- Swagger: `http://localhost:8080/swagger-ui.html` (when enabled)

Remember-me cookie extends the session beyond Tomcat’s default 30-minute idle timeout (default about 2 weeks).

## Project structure

```text
.
├── CHANGELOG.md
├── docker-compose.yml
├── pom.xml
└── src/main
    ├── java/org/joychou
    │   ├── Application.java
    │   ├── config/          # CORS, domains, swagger, websocket
    │   ├── controller/      # HTTP APIs and page controllers
    │   ├── dao/             # entities
    │   ├── filter/          # servlet filters
    │   ├── mapper/          # MyBatis mappers
    │   ├── security/        # Spring Security & helpers
    │   ├── service/
    │   └── util/
    └── resources
        ├── application.properties
        ├── create_db.sql
        ├── mapper/
        ├── templates/
        └── url/             # domain allowlists
```

## Main modules

| Module | Path prefix | Description |
|---|---|---|
| Auth / login | `/login`, `/logout` | Form login |
| User query | `/query` | JDBC / MyBatis user lookups |
| Content | `/content` | Content render / cookie store demo |
| Assets | `/assets` | File read helpers |
| Upload | `/file` | Multipart upload |
| Proxy | `/proxy` | Server-side URL fetch |
| Jobs | `/job` | Runtime / script / yaml job entrypoints |
| XML import | `/xml` | Multiple XML parser integrations |
| Office | `/office/*` | OOXML / XLSX readers |
| Object store | `/object` | Object restore APIs |
| JSON API | `/jsonapi` | Fastjson parse endpoints |
| Rules | `/rules` | QLExpress rule evaluation |
| Expr | `/expr` | SpEL evaluation |
| Templates | `/tpl` | Velocity templates |
| Token | `/token` | JWT create / parse |
| Session | `/session` | Session cookie restore |
| Domain gate | `/domain` | URL allowlist checks |
| Navigation | `/nav` | Redirect helpers |
| Callback | `/callback` | JSONP style responses |
| Cross-domain | `/crossdomain` | CORS related handlers |
| Client IP | `/clientip` | Client address resolution |
| Logger | `/applog` | Application logging sample |
| Tools | `/tools/file` | Host / path utility endpoints |

Exact routes are defined on each controller under `src/main/java/org/joychou/controller/`.

The `master` branch contains the product-facing application, build/deployment files, and documentation. Evaluation-only assets are not part of this branch.

## Configuration notes

- CSRF checking can be toggled with `joychou.security.csrf.enabled`
- Login-exempt URL patterns: `joychou.no.need.login.url`
- JSONP callback parameter names: `joychou.business.callback` / `joychou.security.jsonp.callback`
- Safe domain lists live under `src/main/resources/url/`
- Actuator security is controlled by `management.security.enabled`

## Development

```bash
# compile
mvn -DskipTests compile

# package
mvn clean package -DskipTests
```

For remote debug with the Docker image, port `8000` is exposed for JDWP.

## Contributors

- [JoyChou](https://github.com/JoyChou93)
- [liergou9981](https://github.com/liergou9981)
- [lightless](https://github.com/lightless233)
- [Anemone95](https://github.com/Anemone95)
- [waderwu](https://github.com/waderwu)

Pull requests are welcome.

## License

See repository license terms. Use only in environments you are authorized to run.
