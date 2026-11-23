# 디자인 바닥 규칙 (Hallmark 를 Manim 강의 영상에 옮긴 것)

[Nutlope/hallmark](https://github.com/Nutlope/hallmark) v2 의 Floor 규칙 중 영상에 맞는 것만 가져왔다. 웹 전용(focus, overflow, 1280 첫 화면)은 뺐다. 괄호 번호는 hallmark `references/gates.md` 게이트 번호. 세로 홍보 릴스용은 `promo/references/design-floor.md`.

## 지킨다 (예외 없음)
- **색은 토큰으로** (48): 장면 파일에 `"#RRGGBB"` 를 직접 쓰지 않는다. 모듈 맨 위 `NAME = "#..."` 상수나 `ui.py` 에 두고 이름으로 쓴다. `scripts/lint_scene.py` 가 검사한다.
- **이모지를 아이콘으로 쓰지 않는다** (30a): ✔ ✗ ★ 대신 Manim 도형(`Cross`, `Line` 등)이나 글자.
- **보라→파랑 그라디언트 금지** (2a).
- **지어낸 숫자·후기·점수 금지** (46a): 자료에 없는 통계, 합격률, "대부분 학생이" 같은 말을 화면과 나레이션에 넣지 않는다.
- **손으로 그린 창 틀 금지** (47a): 코드 화면은 둥근 사각형 + 글자. 빨강·노랑·초록 점이나 가짜 주소창을 그리지 않는다.
- **한 화면 글자 약 80 단어 이하** (58): 설명은 말로, 수식과 그림은 화면에. 넘으면 장면을 나눈다.

## 피한다 (이유가 있으면 예외, 보고에 적는다)
- **글로우** (29): 글자 주위 색 번짐. 강조는 `Indicate`, 색 대비, `SurroundingRectangle`.
- **꾸밈 글자** (66): 의미 없는 버전 배지·장식 숫자.
- **같은 구도 반복**: 연속 장면이 전부 "제목 + 불릿 3개"면 그림이나 표로 바꾼다.

## 확인 순서
`validate_scenes.py` 0건 → `python3 $VS/scripts/lint_scene.py src/video_<name>.py` FAIL 0 → 스크린샷 시트 확인.
