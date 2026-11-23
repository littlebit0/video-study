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

## 준비할 자료

과목마다 폴더 하나를 만들고 아래 자료를 넣습니다. 폴더 안 파일은 읽기만 하고 수정하지 않습니다.

```
~/Downloads/선형대수학/
├── [01] Linear Algebra.pdf            강의자료 (주차·장 번호를 파일 이름 앞에)
├── [02] Transformation.pdf
├── [실습02] ....pdf                    실습자료
├── 녹음본.rtf                          수업 녹음 전사 (여러 주차를 한 파일에)
├── 4,5주차 영상강의 유튜브 링크.rtf      영상강의 링크
├── 스크린샷 ... .png                   LMS 주차별 강의계획 화면
├── (정답)중간고사.pdf                   시험지 + 정답
└── 중간고사 해설.rtf                    시험 해설 수업 녹음 전사
```

| 자료 | 필수 | 형식 | 준비 요령 |
|---|---|---|---|
| 강의자료 | 필수 | PDF | 수업에서 쓴 슬라이드 원본. 스캔본이나 그림 위주 PDF도 되지만 쪽마다 이미지로 읽어 시간이 더 걸립니다. |
| 수업 녹음 전사 | 강력 권장 | rtf, docx, txt | **영상 내용의 기준**입니다. 교수님이 강조한 점·시험 힌트를 여기서 찾습니다. 클로바노트 등에서 내보낸 텍스트(“참석자 1 00:45” 형식)도 그대로 됩니다. 여러 주차를 한 파일에 넣을 때는 각 주차가 시작하는 곳에 `2주차`, `3주차`처럼 **한 줄짜리 표시**를 넣어 주세요. 이 줄로 주차를 나눕니다. |
| 영상강의 링크 | 있으면 | rtf, txt | 주차별로 유튜브 주소를 적습니다(예: `4주차` 아래에 링크 목록). 자막(자동 자막 포함)이 있는 공개·일부 공개 영상만 됩니다. 로그인이 필요한 LMS 영상은 영상 파일을 직접 넣어 주세요. |
| 주차별 강의계획 | 권장 | 스크린샷 png | LMS의 주차·학습목표·게시 자료가 보이는 화면. 어느 주차에 어떤 자료로 수업했는지, 시험 주차가 언제인지 이걸로 맞춥니다. 길면 여러 장으로 나눠 찍으세요. |
| 시험지·정답 | 해설 영상에 필수 | PDF | 정답이 표시된 시험지. 배점이 보이면 좋습니다. |
| 시험 해설 수업 | 해설 영상에 권장 | rtf, txt | 교수님이 문제를 풀어 준 수업의 녹음 전사. 정답률 낮은 문제, 감점 기준, 다음 시험 힌트를 여기서 찾습니다. |
| 실습 코드 | 있으면 | py, txt, PDF | 실습 문제가 시험에 코드 빈칸 등으로 나올 때 도움이 됩니다. |

요청할 때 함께 알려 주면 좋은 것:

- 다음 시험 날짜와 범위 (예: "기말은 전범위")
- 따로 만들 영상 (예: "중간고사 해설은 별도로")
- 원하는 영상 길이, 목소리, 자막 방식이 기본값(편당 9~12분, 여성 목소리, 자막 두 가지)과 다르면 그 내용

참고: 녹음 전사에 나오는 학생 이름과 교수 이름은 영상에 넣지 않습니다.

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
promo/                       Remotion 릴스 템플릿·절차 (PROMO.md)
scripts/                     lint_scene.py, patch_validator.py, check_env.sh, new_video.py, extract_sources.py, split_by_marker.py, vtt_to_txt.py, frame_sheet.py
```

## 디자인 규칙과 홍보 릴스

- **디자인 바닥 규칙**: [Hallmark](https://github.com/Nutlope/hallmark) 의 Floor 규칙(색 토큰, 이모지 아이콘 금지, 지어낸 숫자 금지 등)을 Manim 영상에 옮겼습니다. `references/design-floor.md`, 검사는 `scripts/lint_scene.py`.
- **홍보 릴스**: [Remotion](https://github.com/remotion-dev/remotion) 으로 시리즈 소개용 세로 영상(30초 안팎)을 만드는 템플릿과 절차가 `promo/` 에 들어 있습니다. `promo/PROMO.md` 참고. 필요하면 Remotion 공식 스킬(`npx skills add remotion-dev/remotion`)을 함께 설치하세요.

## 참고

- 나레이션은 Edge-TTS 로 만들기 때문에 대본 텍스트가 Microsoft TTS 서비스로 전송됩니다.
- 강의자료와 녹음은 각자 수강 과목의 개인 학습용으로만 사용하세요.

## 라이선스

MIT — [`LICENSE`](LICENSE)
