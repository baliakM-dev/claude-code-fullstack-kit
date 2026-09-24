# Java null contracts and build-time verification

Select this reference for Java nullability, NPE fixes, boundary DTOs, JSpecify or checker setup.
Use the existing language, build and Framework version. For new Framework 7 code prefer
JSpecify; an unrelated feature is not permission to migrate all legacy annotations.

## Make absence explicit
- Use `@NullMarked` in each intended package (package defaults do not cascade to subpackages).
  Use `@Nullable` for an actual optional value, not to silence an unexplained warning.
- Distinguish a nullable container from nullable elements: `@Nullable List<String>` versus
  `List<@Nullable String>`. For arrays, `String @Nullable []` permits an absent array, while
  `@Nullable String[]` permits absent elements. Preserve this distinction in overrides.
- Treat deserialized input, legacy APIs, reflection/JPA lifecycle and external results as
  boundaries requiring validation. An annotation is not a runtime validation constraint.
- Use a DTO's `@NotNull`/other validation only when required by the API contract. A numeric
  range constraint alone may accept null. Preserve missing versus explicit null for PATCH.
- Do not replace missing financial inputs with zero or absent text with an empty string.
  Define not-found, optional and invalid-input behavior separately.
- Keep JPA-generated ID/version nullability honest before persistence. Do not use a fake ID,
  fake version or broad suppression to make initialization warnings disappear.
- Do not add Optional to every field, parameter or entity; use it when it expresses the
  operation's absence contract. Do not use unguarded `get()` as a replacement for handling absence.

Illustrative Framework 7 syntax, not a compiled template in this kit:
```java
// package-info.java, in EACH selected package
@org.jspecify.annotations.NullMarked
package example.catalog;
```
```java
// A nullable result needs an explicit branch; no runtime enforcement comes from the annotation.
static int lengthOrZero(@org.jspecify.annotations.Nullable String text) {
    return text == null ? 0 : text.length(); // valid only for this example's stated text contract
}
```

## Enforce only what has actually been configured
1. Inspect the exact JDK, compiler, annotation processors, Boot BOM and existing static checks.
   Declare the JSpecify dependency; use its managed version if the selected BOM supplies one.
2. Choose a compatible NullAway/Error Prone configuration or an existing equivalent checker.
   Keep the current build tool. Record checked packages, generated-code exclusions and commands.
3. Start with checked null-marked application packages. Spring documents `OnlyNullMarked=true`;
   use the chosen checker's actual options. Enable full JSpecify mode only after verifying its
   JDK/version requirements and generic/array limitations. Do not blindly copy a compiler flag.
4. In an isolated negative fixture, dereference a nullable result and prove the configured
   checker fails with the expected diagnostic. The repaired fixture must pass. Prove the real
   application's selected packages run through that same check, not a disconnected sample.
5. Keep suppressions local, justified and test-covered. Never silently downgrade a failing
   check, exclude the domain package or hide unhandled nulls with casts/defaults.
6. Report CHECKER_VERIFIED, PARTIALLY_VERIFIED or NOT_RUN with exact command and limitation.
   JSpecify dependency presence, a green javac build or IDE highlighting alone is not evidence
   that a nullness checker ran, and a checker is not proof that NPEs are impossible.

For Kotlin keep Kotlin nullability and review platform types; do not introduce Java tools
as a substitute for the Kotlin compiler. Consult the existing kotlin reference only as needed.

Adapted selectively from [upstream null-safety](https://github.com/rrezartprebreza/spring-boot-skills/blob/f0c06a01b0b7571b519cd43e16692b2483a24514/skills/spring-boot-4/null-safety/SKILL.md).
Retain [upstream MIT notice](../LICENSE-UPSTREAM.txt). Primary checks, accessed 2026-09-23:
[Spring null-safety](https://docs.spring.io/spring-framework/reference/core/null-safety.html),
[JSpecify semantics](https://jspecify.dev/docs/user-guide/).
