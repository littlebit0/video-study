---
name: video-study
description: 강의자료 폴더(PDF 슬라이드, 녹음 전사, 유튜브 영상강의 링크, LMS 주차표 스크린샷, 시험지·해설)를 모두 대조해서 유튜브처럼 재미있고 쉬운 한국어 설명 영상 시리즈(3Blue1Brown 스타일 Manim 애니메이션 + 한국어 TTS 나레이션 + 자막)를 만든다. 단원별 영상과 시험 해설 영상을 따로 만들고, 시험 범위·정답률 낮은 문제를 반영한다. 사용자가 "강의자료로 영상 만들어줘", "공부 영상", "설명 영상", "시험 해설 영상", "video-study" 등을 요청할 때 사용한다. notes-to-video·watch 스킬, 병렬 에이전트, edge-tts, manim, ffmpeg 를 묶은 작업 절차다.
---

# video-study: 강의자료 → 공부용 설명 영상 시리즈

notes-to-video(영상 엔진), watch(유튜브 영상강의 수집), 병렬 에이전트(내용 정리·제작), 검증·빌드 스크립트를 하나의 절차로 묶었다.
처음 만든 사례: `~/Documents/Codex/linear-algebra-videos/` (선형대수학 5편 + 중간고사 해설, 2026-11-22). 막히면 그 폴더의 코드를 참고 구현으로 본다.

스킬 경로를 `$VS = ~/.claude/skills/video-study` 로 부른다. 파이썬은 항상 `~/tools/.venv/bin/python` (`$PY`).

## 0. 환경 확인
```bash
bash $VS/scripts/check_env.sh
python3 $VS/scripts/patch_validator.py   # 한 번만: 검사기 오탐(대각선 선) 보정
```
missing 이 있으면 `references/setup.md` 를 보고, **무엇을 어디에 설치할지 사용자에게 물은 뒤** 설치한다(질문·버튼은 한국어). 유튜브 링크가 없으면 yt-dlp 는 필요 없다.

## 1. 자료 파악 (원자료 폴더는 읽기만)
1. 프로젝트 폴더를 정한다: `~/Documents/Codex/<과목>-videos/` (사용자가 다른 곳을 말하면 그곳).
2. 첫 영상 뼈대와 공용 코드를 만든다: `python3 $VS/scripts/new_video.py <project> v1_<name>` (이후 편도 같은 명령).
3. 자료 목록·텍스트 추출: `$PY $VS/scripts/extract_sources.py <자료폴더> <project>` → `sources/inventory.md`.
4. 스크린샷(LMS 주차표 등)은 Read 로 직접 보고 **주차 ↔ 자료 ↔ 학습목표** 표를 만든다. 시험 날짜·범위도 여기서 확인한다.
5. 긴 녹음 전사는 주차 표시 줄로 나눈다: `python3 $VS/scripts/split_by_marker.py <전사.txt> <project>/sources` → `rec_wNN.txt`. 표시가 다르면 정규식을 셋째 인자로.
6. 유튜브 영상강의 링크가 있으면 watch 스킬로 수집한다(사용자 허락 후, 영상은 임시 폴더):
   ```bash
   bash ~/.claude/skills/watch/scripts/prepare_video.sh --url "<URL>" --workdir <tmp>/vN --languages "ko,en" --max-frames 40
   python3 $VS/scripts/vtt_to_txt.py <tmp>/vN/subtitles.ko.vtt <project>/sources/yt_wNN_<주제>.txt
   ```
   `transcript=unavailable` 이어도 `subtitles.ko.vtt` 가 있으면 변환하면 된다. `frames-selected/` 와 `scene_index.csv` 는 `sources/yt_frames/<이름>/` 로 복사하고, **받은 영상 파일은 분석 후 지운다.** 여러 링크를 셸 배열로 돌릴 때 zsh 배열은 1부터 시작한다(파일 이름이 한 칸씩 밀린 적이 있다).

## 2. 시리즈 구성
- 주차 표를 보고 단원별로 3~5주 분량씩 묶어 편을 나눈다(편당 9~12분). 시험 해설은 **별도 편**.
- 사용자에게 이미 정해진 것은 다시 묻지 않는다. 기본값: 1080p 24fps, 편당 9~12분, Edge-TTS `ko-KR-InJoonNeural`, 자막 `.srt` + 영상에 넣은 버전. 다른 요구가 있으면 그대로 따른다.
- 시험 범위(예: 기말 전범위), 정답률 낮아 다시 나올 수 있는 문제("앵콜")를 모든 편의 마지막 "시험 대비 포인트"에 반영한다.
- 아직 자료가 없는 주차는 만들지 않고, 자료가 나오면 이어서 만든다고 알린다.

## 3. 내용 정리 (병렬 에이전트)
편마다 brief 에이전트 1개씩, 한 메시지에서 동시에 띄운다. 지시문은 `references/agent_prompts.md` 1번 템플릿(model sonnet). 녹음·영상강의가 기준이고 슬라이드는 보조라는 점, 다른 편이 맡는 범위, 실습 유무를 채운다.
- 영상강의 자막은 나중에 도착해도 SendMessage 로 해당 에이전트에 경로를 보내 brief 를 갱신하게 한다.
- brief 가 오면 "불확실" 표시와 자료 간 불일치를 훑어보고 제작 지시에 반영한다.

## 4. 제작
1. **첫 편은 직접 만든다**(보통 시험 해설 편이나 가장 brief 가 빨리 온 편). 템플릿(`video_<name>.py`, `part_<name>_narration.py`, `generate_tts_<name>.py`)을 채우고 `PRODUCTION_GUIDE.md` 순서대로: 나레이션 → TTS → validate 0건 → `--screenshots` + `frame_sheet.py dir` 로 전부 보기 → `build.py`.
   이 편이 나머지 편의 참고 구현이 된다. 여기서 발견한 공통 문제는 `PRODUCTION_GUIDE.md` 에 규칙으로 추가한다.
2. 나머지 편은 제작 에이전트로 병렬 진행(`references/agent_prompts.md` 2번, build `--jobs 2`). 진행 중 공통 규칙이 바뀌면 가이드를 고치고 각 에이전트에 SendMessage.
3. 공용 코드(`intermediate/common/`)는 에이전트가 아니라 나만 고친다. 고치면 이미 끝난 편은 `build.py <slug> --captions-only` 로 다시 합친다(재렌더 없음).

디자인 바닥 규칙(`references/design-floor.md`, Hallmark 를 Manim 영상에 옮긴 것: 색 토큰, 이모지 아이콘 금지, 지어낸 숫자 금지, 화면 글자 80 단어 이하)을 지킨다. 장면을 쓴 뒤 `python3 $VS/scripts/lint_scene.py src/video_<name>.py` 가 FAIL 0 이어야 한다. 배너 색은 `ui.py` 의 `BANNER_GOLD/GREEN/RED/SLATE` 를 쓴다.

## 5. 검수 (에이전트 보고를 믿지 말고 직접)
편마다:
- `$PY $VS/scripts/frame_sheet.py video final/<slug>/<slug>_captioned.mp4 <scratch>/sheet.png 6` → Read 로 보기: 겹침, 잘림, 자막이 내용을 가리는지, 그림과 수치가 맞는지.
- 화면에 나온 계산을 손이나 numpy 로 다시 검산한다(보고서 요약과 실제 화면이 다를 수 있다 — 화면 기준으로 판단).
- `tail -3 final/<slug>/<slug>.srt` 의 마지막 끝 시각 ≈ `ffprobe` 영상 길이(자막 밀림 확인).

## 6. 전달
- 완성되는 대로 한 편씩 `SendUserFile`(`_captioned.mp4`, display render, 한 줄 설명)로 보낸다.
- 마지막에 표로 정리: 편, 내용, 길이, 파일 경로. 자료 간 불일치를 어떻게 처리했는지, 확인하지 못한 것(특히 TTS 발음은 귀로 듣지 않았음)을 적는다.
- 폴더를 열어 달라고 하면 `open <project>/final`.
- 프로젝트 상태(완성 편, 남은 주차)를 메모리에 project 로 기록한다.

## 7. 홍보 릴스 (선택, 사용자가 원할 때)
시리즈를 소개하는 세로 릴스·숏츠(30초 안팎)는 이 스킬의 `promo/` 로 만든다. **`promo/PROMO.md` 를 처음부터 읽고 따른다.** Remotion 으로 `reel.json` 하나만 고쳐 렌더한다(음성 InJoon, 카라오케 자막, 터미널 데모, 좋아요·팔로우 엔딩).
- 먼저 Remotion 공식 스킬 `~/.claude/skills/remotion-best-practices/`(라우터 → remotion-markup, remotion-captions, remotion-render)를 읽는다. 없으면 설치 전에 사용자에게 묻는다(`npx skills add remotion-dev/remotion`).
- `npm install` 은 약 400 MB 라서 사용자 OK 를 먼저 받는다. 렌더는 설치된 Chrome, `--concurrency=2`.
- 화면 디자인은 `promo/references/design-floor.md` 를 지킨다.
- 소개 웹페이지(랜딩, README 상단 시각 자료)를 만들 때만 [Hallmark](https://github.com/Nutlope/hallmark) 스킬(`npx skills add nutlope/hallmark -g`)을 쓴다. 영상 제작에는 필요 없다.
- 업로드·게시는 하지 않는다.

## 겪어 본 함정
| 증상 | 원인 | 해결 |
|---|---|---|
| pip 로 manim 설치 실패 (pycairo) | cairo/pkg-config 없음 | micromamba conda-forge (`setup.md`) |
| 영상 뒤로 갈수록 자막이 말보다 빠름 | 장면 영상이 오디오보다 몇 프레임 짧은데 자막은 오디오 길이로 계산 | `build.py` 가 실제 장면 길이로 계산 (이미 반영) |
| 아래 배너가 자막에 가림 | 배너를 buff 0.5 에 둠 | `bottom()` = buff 1.15, 내용은 y > -2.85 |
| 모서리 태그가 OOB | buff 0.4 | `corner_tag()` = buff 0.7 |
| 점선 대각선이 line-cross 실패 | 선이 숫자를 관통 | 원소마다 SurroundingRectangle |
| 회색 글씨가 안 보임 | 스킬 기본 DIMMED #555555 | ui.py 에서 #9AA0A6 |
| 음성·화면 어긋남 | 세그먼트 끝 0.5초 fade 누락, 애니메이션이 오디오보다 김 | `Seg.end()` 사용, build 출력의 `WARNING` 0개 |
| watch 스킬 transcript=unavailable | vtt 변환 실패 | `vtt_to_txt.py` 로 직접 변환 |
| TinyTeX 스크립트가 끝에서 멈춤 | `--no-path` 를 폴더로 착각 | 설치는 완료됨, 링크만 직접 |
| 대각선 간선 옆 숫자가 전부 `LINE-CROSS 100%` | 기본 검사기는 선의 외곽 상자(bbox)만 비교해서 대각선 옆 글자를 오탐 | `python3 $VS/scripts/patch_validator.py` 로 직선을 실제 선분으로 검사하게 패치 (멱등) |
| 목소리가 기계적이라는 피드백 | 기본 음성 + 속도 올림 | 같은 문장을 여러 Edge 목소리로 만든 샘플을 `SendUserFile` 로 보내 고르게 한다. 속도는 올리지 않는다 (`+32%` 는 더 기계적으로 들림) |
| 글 폭이 원 안/카드 안에서 넘침 | CText 폭을 예측 못 함 | `TEXT-OVERFLOW` 경고가 나오면 글자 크기를 줄이거나 컨테이너 키우기 |
| 에이전트 보고의 수치가 화면과 다름 | 요약 과정의 착오 | 화면·소스 코드로 확인 |

## 하지 않는 것
- 원자료 폴더를 수정하지 않는다. 받은 영상은 분석 후 지운다.
- 교수·학생 이름, 제3자 사진·캐릭터 이미지를 영상에 넣지 않는다(도식은 Manim 으로 다시 그린다).
- 소프트웨어 설치, 외부 다운로드는 사용자 허락 없이 하지 않는다.
- 검산하지 않은 수치, brief 의 (불확실) 항목을 단정하지 않는다.
