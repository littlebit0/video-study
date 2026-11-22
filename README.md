# video-study

강의자료 폴더(PDF 슬라이드, 녹음 전사, 유튜브 영상강의 링크, LMS 주차표 스크린샷, 시험지·해설)를 대조해서 **유튜브처럼 쉬운 한국어 설명 영상 시리즈**를 만드는 [Claude Code](https://claude.com/claude-code) 스킬입니다.
3Blue1Brown 스타일 Manim 애니메이션 + 한국어 TTS 나레이션 + 자막(`.srt`, 영상에 넣은 버전)으로, 단원별 영상과 시험 해설 영상을 따로 만듭니다.

## 하는 일

1. 환경 점검 (`scripts/check_env.sh`)
2. 자료 파악: PDF/rtf 텍스트 추출, 녹음 전사를 주차별로 나누기, 유튜브 영상강의 자막·화면 수집
3. 시리즈 구성: 단원별 편 + 시험 해설 편, 시험 범위·정답률 낮은 문제 반영
4. 편마다 내용 정리 에이전트를 병렬로 실행 (녹음·영상강의가 기준, 슬라이드는 보조)
5. 첫 편을 직접 만들어 참고 구현으로 삼고, 나머지 편은 제작 에이전트가 병렬로 제작
6. 검수: 프레임 시트, 수치 재검산, 자막 시간 확인
7. 완성되는 대로 전달

자세한 절차는 [`SKILL.md`](SKILL.md), 제작 규칙은 [`references/production_guide.md`](references/production_guide.md)에 있습니다.

## 설치

```bash
git clone https://github.com/littlebit0/video-study ~/.claude/skills/video-study
bash ~/.claude/skills/video-study/scripts/check_env.sh
```

필요한 것 (빠진 항목은 [`references/setup.md`](references/setup.md) 참고, macOS 기준):

- [notes-to-video](https://github.com/cymcymcymcym/notes-to-video) 스킬과 `~/tools/video_utils`
- `~/tools/.venv` 파이썬 3.10+ 환경: manim, edge-tts, pydub, pymupdf, Pillow (micromamba conda-forge 권장)
- PATH 의 ffmpeg/ffprobe (libass 포함), LaTeX + dvisvgm (TinyTeX)
- 선택: watch 스킬 + yt-dlp (유튜브 영상강의), macOS `textutil` (rtf/docx)

## 사용

Claude Code 에서:

```
/video-study ~/Downloads/<과목 자료 폴더>
```

또는 "강의자료로 공부 영상 만들어줘"처럼 요청하면 됩니다.

## 구성

```
SKILL.md                     작업 절차, 겪어 본 함정
references/
  production_guide.md        프로젝트마다 복사되는 제작 규칙
  agent_prompts.md           내용 정리·제작 에이전트 지시문 템플릿
  setup.md                   환경 설치 (Homebrew 없이)
assets/common/               ko_setup.py(한글 글꼴·음성), ui.py, seg.py(나레이션 동기화), build.py(렌더·합치기·자막)
assets/template/             새 편 템플릿 (나레이션, TTS, 장면)
scripts/                     check_env.sh, new_video.py, extract_sources.py, split_by_marker.py, vtt_to_txt.py, frame_sheet.py
```

## 참고

- 나레이션은 Edge-TTS 로 만들기 때문에 대본 텍스트가 Microsoft TTS 서비스로 전송됩니다.
- 강의자료와 녹음은 각자 수강 과목의 개인 학습용으로만 사용하세요.
