# 홍보 릴스 (promo)

30초 안팎 세로(1080x1920, 30fps) 소개 영상을 `src/reel.json` 하나로 만든다. 구조와 근거는 `references/reel-structure.md`, 화면 디자인 바닥 규칙은 `references/design-floor.md`, 사용자가 거절한 것은 `references/lessons.md`, 완성 예시는 `references/examples/video-study.reel.json`.

## 먼저
- Remotion 공식 스킬(remotion-dev/remotion `packages/skills`, 4.0.545)을 읽는다: `~/.claude/skills/remotion-best-practices/SKILL.md`(라우터) → `remotion-markup/SKILL.md`(애니메이션·미디어) → 자막을 고치면 `remotion-captions/`, 렌더 옵션은 `remotion-render/SKILL.md`. 없으면 만들기 전에 사용자에게 알린다.
- Composition.tsx를 고치거나 새 장면을 만들면 `references/design-floor.md`(hallmark 바닥 규칙의 영상판)를 지킨다. 원본은 `~/.claude/skills/hallmark/`.
- 스킬 경로: `~/.claude/skills/video-study/promo/` (아래 `$RM`).

## 흐름
1. **사실 수집**: 사용자가 준 사실만 쓴다. 점수·"완벽"·"누구나" 같은 주장, 개인정보(이름, 학교, 과목 코드)는 넣지 않는다. 검증 안 되는 숫자는 쓰지 않는다.
2. **스크립트**: 7개 장면(hook, pain, reveal, demo, proof, feat, cta)에 문장을 쓴다. 해요체, 짧게, 수사 질문 훅. 길면 속도를 올리지 말고 문구를 줄인다(목표 26~35초).
3. **목소리 고르기**: `python $RM/scripts/make_voice_samples.py <폴더> [문장] [--say-yuna]`(venv: `~/tools/.venv/bin/python`)로 샘플을 만들어 SendUserFile로 보내고 사용자가 고르게 한다. 기본값은 `ko-KR-InJoonNeural`, 속도 0%(최대 +8%, tts.py가 assert).
4. **스캐폴드**: `bash $RM/scripts/new_reel.sh <dest> --link-modules <기존 Remotion 프로젝트>` 또는 `--install`. **npm install은 약 400 MB를 받으므로 사용자 OK를 먼저 받는다.**
5. **reel.json 편집**: 줄(`lines`), 후크 큰 글씨, 고통 카드, 터미널 단계, 증거 숫자·클립, 필(pill), CTA, 커버. 터미널/필의 `at`은 `[줄 id, 구절 번호]`(구절은 rows의 `|` 단위). 클립은 `public/clips/`에 ffmpeg로 2~3초, 폭 960 이하로 잘라 넣고, 원본 자막·개인정보가 없는 프레임만 쓴다.
6. **빌드**: `cd <dest> && npm run build:voice -- [음성이름]` (TTS → timeline.json → 렌더 → out/cover.png). 음성만 바꿔 다시 만들 때도 같은 명령.
7. **검사**: `python $RM/scripts/check_reel.py <dest>/out/video-study-reel.mp4 sheet.png 16` 후 시트를 Read로 본다. 안전 영역(세로 10~75%, 가로 90%), 겹침, 자막 위치(약 70%), 클립과 자막 일치, CTA(하트+팔로우+멘트)를 확인한다. 소리는 들을 수 없으니 못 확인했다고 보고한다.
8. **전달**: 파일 경로와 길이·용량을 알리고 SendUserFile로 보낸다. 업로드·게시는 하지 않는다.

## 규칙
- 렌더는 설치된 Chrome으로(`remotion.config.ts`의 `Config.setBrowserExecutable`), `--concurrency=2`. remotion-render 스킬은 번들 브라우저를 권하지만 사용자 규칙이 우선한다. Remotion이 브라우저를 받으려 하면 멈추고 사용자에게 묻는다.
- 오디오·영상은 `@remotion/media`의 `<Audio>`/`<Video>`(Html5Audio·OffthreadVideo 아님). 움직임은 `interpolate`/`spring`과 `transform`·`scale`·`translate`·`opacity`만, `top`·`height` 같은 레이아웃 값은 애니메이션하지 않는다. CSS transition/animation 금지(렌더에 안 잡힘).
- 모션은 차분하게: 화면 흔들림, 번쩍임, 팝/휙/클릭 효과음 없음. 음성만(아주 조용한 부드러운 비트는 선택).
- 터미널 화면은 "예시 화면"으로 표시. 하트·팔로우는 일반 도형, 플랫폼 로고·UI 복제 금지.
- Remotion은 개인 무료, 회사는 라이선스 조건이 있다(remotion.dev/license, `remotion-license` 스킬) — 보고에 한 줄 적는다. 키가 있으면 `REMOTION_LICENSE_KEY`로 넘긴다(build.sh가 `--license-key`로 전달).
- 자막 줄은 16자 이하(tts.py가 검사), 최대 2줄. 장면 7개 구조는 코드에 고정이다. 다른 구조는 Composition.tsx를 고친다.

## 구성
`template/`(Remotion 프로젝트, node_modules 없음) · `scripts/`(new_reel.sh, make_voice_samples.py, check_reel.py) · `references/`
