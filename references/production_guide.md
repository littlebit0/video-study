# 강의 설명 영상 제작 가이드 (이 프로젝트의 모든 편 공통)

목표: 강의자료·녹음·영상강의를 바탕으로, 유튜브처럼 재미있고 쉬운 3Blue1Brown 스타일 Manim 애니메이션 + 한국어 나레이션 영상.
시험 정보(범위, 앵콜 문제 등)는 프로젝트 첫 편의 brief 와 사용자 요청을 따른다.

## 따라야 할 스킬
- `~/.claude/skills/notes-to-video/SKILL.md` 를 처음부터 끝까지 읽고 규칙(큐 마커 동기화, 겹침 방지, 검증 필수, 스크린샷 검토 필수)을 따른다. 아래와 다르면 이 문서를 따른다.

## 고정 설정 (사용자와 합의됨, 다시 묻지 말 것)
- 1080p, 24fps. 자막은 `.srt` + 영상에 넣은 버전 둘 다(빌드 스크립트가 처리).
- 음성: Edge-TTS `ko-KR-SunHiNeural` (`intermediate/common/ko_setup.py` 의 `VOICE`). 약 230음절/분(공백 제외) → 10분 ≈ 2,300음절. 나레이션 텍스트는 Microsoft TTS 서버로 전송된다.
- 한글 글꼴: `ko_setup.py` import 시 Text 기본 글꼴이 Apple SD Gothic Neo. MathTex 안에 한글 금지.
- 공용 코드: `intermediate/common/` — `ui.py`(corner_tag, bottom, banner, tag, bullet_list, fit, 색 WARN/OK/BLUE_3B/DIMMED), `seg.py`(Seg 시간 관리), `build.py`(렌더·합치기·자막).
- 파이썬은 반드시 `~/tools/.venv/bin/python`.

## 파일 규칙
폴더 `intermediate/vN_<name>/`, `src/video_<name>.py`, `src/part_<name>_narration.py`, `src/generate_tts_<name>.py`, 오디오 `audio/video_<name>/`. 새 편은 `python3 ~/.claude/skills/video-study/scripts/new_video.py <project> vN_<name>` 으로 만든다(템플릿 포함).

## 작업 순서
1. 자기 편 `brief.md` 를 읽는다. 필요하면 `sources/` 와 원자료(읽기만)를 확인.
2. `plan.md`: 6~9개 장면, 장면당 2~5세그먼트, 총 9~12분. 첫 장면 = 다루는 주차 + "오늘의 질문". 마지막 장면 = 시험 대비 체크리스트.
3. 나레이션 → `generate_tts_<name>.py` 실행 → 총 길이 확인. 목표를 벗어나면 나레이션 수정, `audio/video_<name>/` 삭제 후 재생성.
4. 장면 작성 → `~/tools/.venv/bin/python ~/tools/video_utils/validate_scenes.py src/video_<name>.py` 0건이 될 때까지 → `--screenshots` 후 `frame_sheet.py dir review/video_<name> review/sheet` 로 묶어 **모든 스크린샷을 직접 본다**. 출력의 `WARNING` (시간 초과·자막 영역)도 0개여야 한다.
5. 빌드: `~/tools/.venv/bin/python intermediate/common/build.py vN_<name> --quality h --jobs 2` (여러 편 동시 진행이면 jobs 2, 혼자면 4~5). 1080p 10분 렌더는 보통 1~3분.
6. 완성본 확인: `frame_sheet.py video final/vN_<name>/vN_<name>_captioned.mp4 <out.png> 6` 로 프레임을 보고, srt 마지막 자막 끝 시각이 영상 길이와 맞는지 본다.

## 화면 배치 규칙
- 안전 영역 x ∈ [-6.5, 6.5], y ∈ [-2.85, 3.5]. **y < -2.85 는 자막 자리**(최대 2줄). 아래 배너는 `bottom(...)` (= `to_edge(DOWN, buff=1.15)`).
- 모서리 태그는 `corner_tag(...)` (buff 0.7). buff 0.4 면 검사기가 범위 밖으로 잡는다.
- 점선·화살표가 글자를 지나가면 검사기가 실패시킨다. 대각선 강조는 선 대신 각 원소에 `SurroundingRectangle`.
- 같은 자리에 새 내용을 넣을 때는 이전 것을 FadeOut 하면서 FadeIn.
- 회색 보조글은 `DIMMED`(#9AA0A6). 스킬 기본값 #555555 는 어두운 배경에서 안 보인다.
- 라벨이 화살표 사이에 들어가야 하면 상자 간격을 넓힌다(라벨 폭 > 간격이면 겹친다).

## 내용 규칙
- 말투: 친근한 유튜브 강의체 존댓말("~해요", "~죠"). 짧은 문장, 질문 던지기, 일상 비유. 수식은 화면에, 설명은 말로.
- TTS용 문장: 기호와 약어를 한글로 풀어 쓴다 ("A x = b" → "에이 엑스는 비", "3x3" → "3 곱하기 3", "λ" → "람다", "det" → "행렬식", "x'" → "엑스 프라임"). 화면 텍스트는 원래 표기 그대로.
- **녹음·영상강의가 기준, 슬라이드는 보조.** 녹음에서 다룬 내용을 중심으로, 슬라이드에만 있고 수업에서 안 다룬 내용은 짧게 언급하거나 뺀다.
- 수학 사실은 brief 에서 검산된 것만. (불확실) 표시는 단정하지 않는다. 계산 예제는 numpy 로 다시 검산한다.
- 자료끼리 어긋나면(슬라이드 오타, 표기 차이) 영상에서 한 번 짚고, 헷갈리지 않는 표현(부등식 등)을 쓴다.
- 교수 강조점·시험 힌트는 "교수님이 강조하신" 식으로. 교수 이름과 학생 이름은 넣지 않는다.
- 시험 문항과 연결되는 개념이 나오면 "중간 서술 N번" 같은 꼬리표를 붙인다.
- 그림은 Manim 으로 다시 그린다. 제3자 사진·캐릭터 이미지는 넣지 않는다.

## 끝나면 보고
최종 파일 경로, 영상 길이, 장면 목록(한 줄씩), 검증 결과, 일부러 뺀 내용과 이유, 확인하지 못한 것(특히 TTS 발음은 귀로 확인하지 않았다는 점).
