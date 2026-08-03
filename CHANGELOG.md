# Changelog

This file records user-visible repository changes. Dates use the commit date in Asia/Shanghai.

## [2026-08-02]

- Renamed security-lab-oriented classes, methods, routes, templates, and comments to product-facing platform terminology (`0b8f0ae`). The current names include `RequestTraceFilter`, `PassThroughHttpFirewall`, `PathPatternCheck`, and `doc_upload.html`.

## [2026-08-01]

- Reworked the repository documentation and application identifiers around the JoyChou Platform product surface, including the application artifact and database names (`bcca97e`).
- Kept `master` focused on the application: benchmark/evaluation assets and transformation scripts are not included in this branch (`bcca97e`).
- Kept the benchmark/evaluation corpus on the separate `benchmark` branch (`e2712f2`, `e61eb7f`); those files remain available there and are intentionally absent from `master`.
