# Version and architecture choices

For a new project select a supported stable Spring Boot 4.x release and a compatible supported Java LTS; record the exact patch, source and verification date. Use Boot's dependency management, not independently selected latest versions of every Spring library. Do not use snapshots, release candidates or Java preview features by default.

Check system requirements, support availability, runtime/container JDK, Maven/Gradle wrapper, database driver, annotation processors and test tooling together. Use dependency coordinates and packages from the chosen version's documentation. Framework major changes can affect JSON libraries, starter modules, test imports and nullability; do not copy a Boot 3 snippet blindly.

For an existing project keep compatible versions unless a requested upgrade, supported-lifecycle issue or relevant vulnerability requires change. Record exceptions and regression evidence.

For a small greenfield product prefer a modular monolith when it satisfies ownership and deployment requirements. Extract services only for a concrete independent lifecycle or operational need. Keep domain boundaries testable without adding every module framework immediately.

Primary sources:
- https://docs.spring.io/spring-boot/system-requirements.html
- https://docs.spring.io/spring-boot/appendix/dependency-versions/coordinates.html
- https://spring.io/support-policy/
- https://www.oracle.com/java/technologies/java-se-support-roadmap.html
