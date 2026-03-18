# Condition Grammar (Pipeline Stage)

현재 실행기는 side-effect 없이 텍스트 조건식만 파싱합니다.

- 허용 형식(단항):
  - `<artifact> == <string|number|true|false|null>`
  - `<artifact> != <string|number|true|false|null>`
  - `<artifact> is not null`
  - `<artifact> is null`

- 조합:
  - `and`, `or` 로 연결된 조건식
  - 예시: `route.decision.yaml.route == "framing-first" and readiness-report.md.status != "ready"`

- 제약:
  - 현재는 파이프라인 플래닝 단계에서의 정합성 점검용이므로 산술 연산/함수/그룹 연산자(`(...)`)는 지원하지 않습니다.
  - 추후 확장 시 안전한 AST evaluator를 도입해 연산 범위를 제한할 계획입니다.
