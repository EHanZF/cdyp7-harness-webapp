# Copilot instructions for this repository

Purpose
- Give GitHub Copilot clear, repository-specific guidance so sessions produce consistent, minimal, and correct changes.

1) Build, test, and lint commands (fill in for this repo)
- Primary build/test/lint commands (paste exact commands used in CI):
  - Build: npm ci
  - Test (full): npm run test:e2e
  - Lint: npm run lint (fix: npm run lint:fix). Format: npm run format

- Single-file lint example: npx eslint tests/e2e/example.spec.ts --ext .ts
- Auto-fix single file: npx eslint tests/e2e/example.spec.ts --ext .ts --fix
- How to run a single test (examples — replace with the project-specific form):
  - Node (Jest/Mocha): npm test -- tests/path/to/testfile.test.js  OR npx jest tests/path/to/testfile.test.js -t "test name"
  - Python (pytest): pytest tests/test_module.py::test_name -q
  - Java (Maven): mvn -Dtest=ClassName#testMethod test
  - Gradle: ./gradlew test --tests "com.example.ClassTest.testMethod"
  - .NET: dotnet test --filter "FullyQualifiedName=Namespace.Class.TestMethod"
  - Go: go test ./pkg -run TestName

2) High-level architecture (brief, cross-file overview)
- Languages/frameworks: <e.g. TypeScript backend, React frontend, Python worker>
- Runtime topology: list services, libraries, and how they interact (API -> worker -> DB / frontend -> API)
- Repos/monorepo layout: note packages, shared libs, and where to find entrypoints
- Data stores & external dependencies: DB types, queues, caching, 3rd-party APIs
- CI/CD: where pipeline definitions live (e.g. .github/workflows/*), deploy targets

(Replace placeholders above with a 3–5 sentence summary that Copilot can use to reason about cross-file changes.)

3) Key conventions (project-specific)
- Source layout: e.g. source lives under `src/`, tests under `tests/` or `src/**/__tests__/`.
- Test naming: e.g. `*.test.js`, `*Spec.kt`, `*Test.java` — Copilot should follow the repo's pattern.
- Configuration: central config files and environment variable files (list paths).
- API schema/versioning: where OpenAPI/GraphQL schema lives and how to update it.
- Code generation: note any codegen tools (openapi-generator, protobuf, tsc --build) and generated paths to avoid editing.
- Formatting/linting: preferred formatter (prettier/black/dotnet-format) and autofix command.

4) Helpful patterns for Copilot sessions
- Make the smallest change that satisfies the tests/issue and update related files (docs, changelogs, version files) in same PR.
- If adding dependencies, update lockfile and CI matrix.
- For refactors: add tests covering behavior before changing public APIs.
- When touching multiple packages, run the full test suite and include a brief summary in the PR.

5) Files for other assistants / integration
- If present, merge important bits from: README.md, CONTRIBUTING.md, CLAUDE.md, AGENTS.md, CONVENTIONS.md, AIDER_CONVENTIONS.md
- Check for assistant config files and their locations so Copilot can reuse rules:
  - Claude/OpenCode: CLAUDE.md
  - Cursor: .cursorrules, .cursor/rules/
  - Codex/Jules/OpenCode: AGENTS.md
  - Windsurf: .windsurfrules
  - Aider: CONVENTIONS.md, AIDER_CONVENTIONS.md
  - Cline: .clinerules, .cline_rules

6) Where to add missing info
- Update the Build/Test/Lint section with exact commands and a brief example for running a single test.
- Populate High-level architecture with a 3–5 sentence summary listing services and data stores.
- Populate Key conventions with concrete patterns (test filename patterns, package boundaries, and codegen locations).

7) Quick checklist for PRs Copilot should create
- Minimal, well-scoped changes
- Add/update tests demonstrating behavior
- Run linters and tests locally; include CI status in PR description
- Update docs or README if public behavior changes

---

Notes for maintainers
- Replace placeholder lines above with the project-specific commands and paths so future Copilot sessions can synthesize accurate changes.
