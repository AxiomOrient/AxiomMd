# Script Patterns — Python 스크립트 작성 패턴

Codex Skills의 `scripts/` 디렉터리에 Python 스크립트를 작성하는 규범적 패턴 모음.

---

## 기본 원칙

1. **Python 3 전용** — 다른 언어 (Ruby, Bash, Node.js 등) 사용 금지.
2. **단일 책임** — 스크립트 하나는 하나의 목적만 수행한다.
3. **CLI 인터페이스** — `argparse`로 모든 인수를 정의한다.
4. **에러 핸들링** — 오류는 `stderr`로 출력하고 non-zero exit code를 반환한다.
5. **JSON 출력 권장** — Codex가 파싱할 수 있는 구조화된 출력을 사용한다.

---

## 기본 스크립트 템플릿

```python
#!/usr/bin/env python3
"""
<skill-name> 스크립트 - <한 줄 설명>.

사용법:
    python3 scripts/<script-name>.py [옵션]

예시:
    python3 scripts/validate.py --input path/to/file.yaml
    python3 scripts/validate.py --input path/to/file.yaml --json
"""

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="<스크립트 설명>",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", required=True, help="입력 파일 경로")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: 파일을 찾을 수 없음: {input_path}", file=sys.stderr)
        return 1

    # --- 핵심 로직 ---
    result = {"status": "ok", "path": str(input_path)}
    # -----------------

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[OK] {input_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## 패턴 1: 파일 검증기 (Validator)

스펙 파일이나 패킷 파일의 형식을 검증하는 스크립트.

```python
#!/usr/bin/env python3
"""
spec 검증 스크립트 - 스펙 파일이 표준을 충족하는지 확인한다.
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Workflow",
    "## Stop Conditions",
]


def validate_spec(path: Path) -> list[str]:
    """검증 실패 사유 목록을 반환한다. 빈 리스트는 통과."""
    errors = []
    content = path.read_text(encoding="utf-8")

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"Missing section: {section}")

    # frontmatter 검사
    if not content.startswith("---"):
        errors.append("Missing frontmatter")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="스펙 파일 검증")
    parser.add_argument("path", help="검증할 파일 경로")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"ERROR: {target} 존재하지 않음", file=sys.stderr)
        return 1

    errors = validate_spec(target)

    if errors:
        print(f"FAIL: {target}")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        print(f"PASS: {target}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## 패턴 2: 상태 폴러 (Poller)

외부 시스템을 주기적으로 폴링하는 스크립트. `babysit-pr`의 `gh_pr_watch.py` 패턴.

```python
#!/usr/bin/env python3
"""
상태 폴링 스크립트 - 외부 상태를 주기적으로 확인한다.
"""

import argparse
import json
import subprocess
import sys
import time


def get_status() -> dict:
    """외부 시스템 상태를 가져온다."""
    result = subprocess.run(
        ["gh", "pr", "view", "--json", "state,mergeable,statusCheckRollup"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return json.loads(result.stdout)


def classify_action(status: dict) -> list[str]:
    """상태에서 수행해야 할 액션 목록을 결정한다."""
    actions = []

    if status.get("state") in ("MERGED", "CLOSED"):
        actions.append("stop_pr_closed")
        return actions

    checks = status.get("statusCheckRollup", [])
    failing = [c for c in checks if c.get("conclusion") == "FAILURE"]

    if failing:
        actions.append("diagnose_ci_failure")
    elif all(c.get("conclusion") == "SUCCESS" for c in checks if checks):
        actions.append("idle")
    else:
        actions.append("wait")

    return actions


def main() -> int:
    parser = argparse.ArgumentParser(description="PR 상태 폴링")
    parser.add_argument("--once", action="store_true", help="한 번만 실행")
    parser.add_argument("--watch", action="store_true", help="연속 모니터링")
    parser.add_argument("--interval", type=int, default=60, help="폴링 간격 (초)")
    args = parser.parse_args()

    if not args.once and not args.watch:
        parser.error("--once 또는 --watch 중 하나를 선택하세요")

    while True:
        try:
            status = get_status()
            actions = classify_action(status)

            output = {"status": status, "actions": actions}
            print(json.dumps(output, ensure_ascii=False))
            sys.stdout.flush()

            if args.once or "stop_pr_closed" in actions:
                break

            time.sleep(args.interval)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(json.dumps({"error": str(e)}), file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## 패턴 3: YAML 패킷 처리기

YAML 입력 패킷을 읽고 검증하는 스크립트.

```python
#!/usr/bin/env python3
"""
패킷 처리기 - input.packet.yaml을 읽고 필드를 검증한다.
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML이 필요합니다: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REQUIRED_FIELDS = ["request_summary", "scope", "done_signals"]


def validate_packet(data: dict) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            errors.append(f"Missing or empty field: {field}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="입력 패킷 검증")
    parser.add_argument("path", help="input.packet.yaml 경로")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: {path} 존재하지 않음", file=sys.stderr)
        return 1

    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        print("ERROR: 유효한 YAML 딕셔너리가 아님", file=sys.stderr)
        return 1

    errors = validate_packet(data)
    if errors:
        print(f"FAIL: {path}")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## 출력 규칙

| 상황 | 출력 방식 |
|------|-----------|
| 정상 결과 | `stdout` |
| 오류 메시지 | `stderr` |
| 성공 exit code | `0` |
| 실패 exit code | `1` (또는 그 이상) |
| 검증 통과 | `PASS: <path>` |
| 검증 실패 | `FAIL: <path>` + 사유 목록 |
| JSON 모드 | `{"status": ..., "actions": [...]}` |

---

## 금지 사항

- `#!/usr/bin/env ruby` — Ruby 스크립트 금지
- `#!/bin/bash` — Bash 스크립트는 간단한 실행용으로만, 복잡한 로직 금지
- `subprocess.run("...", shell=True)` — shell=True는 보안 취약점, 피한다
- `print(...)` without flush in `--watch` mode — 스트리밍 출력 시 `flush=True` 필수
- 전역 상태 변경 — 스크립트는 파일을 쓰거나 상태를 변경할 때 SKILL.md에 명시한다
