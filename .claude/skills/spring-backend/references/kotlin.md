# Kotlin alternative, not automatic migration

Use this reference only when Kotlin is selected or the user asks to evaluate it. Keep Java as a valid choice. Kotlin nullability does not establish authorization or financial correctness.

Align Kotlin/compiler plugins, Spring and JSON serialization with the exact Boot release. Verify spring/all-open and JPA no-arg requirements rather than disabling proxies or adding arbitrary open modifiers. Review Java platform types and boundary nullability. Do not normalize repeated !! assertions into the style guide.

Use immutable data classes for suitable DTOs. Do not automatically make mutable JPA entities data classes: identity, equality, lazy associations and generated methods need deliberate choices. Verify annotation use-site targets for validation and persistence with the compiler version. Do not assume Java Lombok/processor conventions carry across.

Compile and test the exact combination before calling it supported.

Primary source: https://docs.spring.io/spring-boot/reference/features/kotlin.html
