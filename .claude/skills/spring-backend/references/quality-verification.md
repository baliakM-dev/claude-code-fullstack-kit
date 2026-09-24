# Verifying design quality with real evidence

Use for backend verification setup and changes to a material contract/module boundary. Reuse approved tooling and the chosen build. This reference is a workflow, not installed application tooling: the kit contains no Maven/Gradle build, ArchUnit tests or application CI until bootstrap creates them.

## Choose checks by purpose
| Purpose | Evidence to configure or reuse | What it does not prove |
| --- | --- | --- |
| Consistent source formatting | One compatible formatter/style check selected for the project's JVM language and invoked by CI. Do not use whole-repository auto-format in a bounded feature task. | Domain correctness or a sound abstraction. |
| Likely implementation defects | A compatible static analyzer (for example SpotBugs for Java) with reviewed findings and narrow justified suppressions. Verify the selected JDK/bytecode/tool combination. | Freedom from null failures, vulnerabilities or all logic bugs. |
| Module direction and cycles | A few ArchUnit rules, or existing module verification such as Spring Modulith if already selected, protecting actual project boundaries. | Complete SOLID compliance, runtime authorization or financial correctness. |
| Behavior and substitutability | Unit/contract tests against requirements; shared contract cases for real interchangeable implementations. | Database/proxy behavior when those are mocked. |
| Framework/data behavior | Relevant HTTP, transaction, PostgreSQL, concurrency or OIDC tests against the actual mechanism. | Every other deployment or untested profile. |

Choose a minimal complementary set, not every available quality plugin. Record exact compatible dependencies, commands and CI wiring only after creating them. Do not fabricate a Maven goal, npm script, coverage number or CI result. Follow test-verification for execution, evidence and environment constraints.

## Architecture checks: meaningful boundaries only
1. Read the actual module/package layout and agreed dependency direction. State the invariant before writing a test. Do not introduce layers only to give a test something to check.
2. Select the production classes to import and explicitly identify excluded test/generated/bootstrap code when applicable. Confirm the relevant selection contains the expected real classes; a passing test on an empty or wrong package is not evidence.
3. For a layered use case, check that the application/domain does not depend on HTTP controllers. For a deliberately pure calculation core, check independence from transport, persistence and external I/O. Check cross-module cycles once multiple modules actually exist. Do not impose framework independence on every existing JPA model.
4. Prove new/custom rules can detect the forbidden relation using isolated synthetic positive and negative fixtures with assertions on the rule outcome. Do not introduce intentional defects into the user's application, overwrite working files or perform Git restore/reset as part of this check. Fixtures do not replace checking real production classes.
5. Keep test discovery visible: verify that the architecture test actually ran in the chosen test engine and that CI runs the same check. Do not silence failure by allowing empty class selections, excluding a whole module or disabling a gate.
6. When a boundary does not yet exist, record NOT_APPLICABLE plus the concrete activation trigger. For example, enable the pure-calculation boundary when that module is created. Do not add fake classes or claim the future boundary passed.
7. Read-only reviewers inspect rules, target selection, fixtures and supplied execution evidence. Only the authorized writer/tester runs checks in the permitted isolated environment.

## Bootstrap and later changes
For task 000 (or an equivalent new-project task), establish the minimal formatter/static-analysis/test command set, documenting compatibility or a precise blocker. Add architecture checks for already real boundaries. Explicitly record absent boundaries and their activation triggers rather than adding an empty test suite.

When the first application/domain module or pure calculator is added, implement its now-relevant architecture test in the same scoped task and wire it into the existing build/CI. For an existing project, preserve working tools and avoid a tool migration during a feature change. Get explicit scope for new tooling or justified suppressions; never modify agents or permissions to make a check pass.

## Evidence and completion
Record check, command and directory, checked revision/file manifest, observed result, relevant test count/selection and remaining limitation. Mark a required unexecuted check NOT_RUN. A known violation requires correction or an explicitly accepted scoped exception; an environment blocker requires PARTIALLY_VERIFIED, not removing the check. No universal coverage/complexity threshold establishes senior-level quality.

Keep non-blocking style suggestions separate. Pass the original acceptance criteria and sanitized evidence to an independent reviewer where the risk policy requires one. This process supplements, not replaces, behavior tests and human approval for financial rules.

## Primary references
Definitions of project boundaries and the evidence requirements above are this kit's policy. Verify APIs/tool compatibility for the project's selected versions. Sources accessed: 2026-09-23.

- [ArchUnit rules, cycles and empty selections](https://www.archunit.org/userguide/html/000_Index.html)
- [Spring Modulith verification](https://docs.spring.io/spring-modulith/reference/verification.html)
- [SpotBugs purpose and limitations](https://spotbugs.readthedocs.io/en/stable/introduction.html)
