# 환경 설치 (macOS, Homebrew 없음 기준)

`scripts/check_env.sh` 에서 missing 이 나온 항목만 설치한다. **설치 전 사용자에게 무엇을 어디에 설치하는지 묻는다.** 관리자 비밀번호가 필요한 방법은 쓰지 않는다.

## 1. notes-to-video 스킬과 video_utils
GitHub `cymcymcymcym/notes-to-video` 를 임시 폴더에 clone → 코드 검토 → 복사. `npx` 는 쓰지 않는다(npm 버전이 GitHub 과 다를 수 있음).
```bash
cp -R <clone>/skills/notes-to-video ~/.claude/skills/
mkdir -p ~/tools && cp -R <clone>/video_utils ~/tools/
```

## 2. 파이썬 환경 ~/tools/.venv (manim + ffmpeg)
시스템 python3 는 3.9 라 안 된다. pip 로 manim 을 깔면 pycairo 빌드가 실패한다(cairo/pkg-config 없음). conda-forge 미리 빌드본을 micromamba 로 받는다.
```bash
mkdir -p ~/tools/mm && cd ~/tools
curl -fsSL https://micro.mamba.pm/api/micromamba/osx-arm64/latest -o mm.tar.bz2
tar -xjf mm.tar.bz2 -C mm bin/micromamba && rm mm.tar.bz2
MAMBA_ROOT_PREFIX=~/tools/mamba ./mm/bin/micromamba create -y -p ~/tools/.venv -c conda-forge python=3.12 manim ffmpeg pip
~/tools/.venv/bin/python -m pip install edge-tts pydub pymupdf yt-dlp
ln -sf ~/tools/.venv/bin/ffmpeg ~/.local/bin/ffmpeg
ln -sf ~/tools/.venv/bin/ffprobe ~/.local/bin/ffprobe
ln -sf ~/tools/.venv/bin/yt-dlp ~/.local/bin/yt-dlp
```
`~/.local/bin` 이 PATH 에 있는지 확인한다. C 라이브러리가 필요한 패키지를 더 넣을 때도 micromamba `-c conda-forge` 를 쓴다.

## 3. LaTeX (MathTex 용, TinyTeX ~360MB)
공식 스크립트를 받아 **읽어 본 뒤** `--no-path` 로 실행(관리자 비밀번호·`/etc/paths.d` 회피). 스크립트가 `--no-path` 를 폴더로 착각해 마지막 mv 에서 멈추지만 설치 자체는 끝난다. 남은 tar.xz 는 `$TMPDIR` 에서 지운다.
```bash
curl -fsSL https://yihui.org/tinytex/install-bin-unix.sh -o install.sh   # 읽어 보기
sh install.sh --no-path
B=~/Library/TinyTeX/bin/universal-darwin
for x in latex pdflatex xelatex dvisvgm tlmgr kpsewhich; do ln -sf $B/$x ~/.local/bin/$x; done
tlmgr install standalone preview doublestroke ms everysel setspace rsfs relsize ragged2e fundus-calligra microtype wasysym physics dvisvgm jknapltx wasy cm-super babel-english gnu-freefont mathastext cbfonts-fd
```

## 4. watch 스킬 (YouTube 영상강의)
`~/.claude/skills/watch` 가 있으면 yt-dlp 만 있으면 된다(2번에서 설치). Whisper 는 자막 없는 영상에만 필요하다.

## 확인
```bash
bash ~/.claude/skills/video-study/scripts/check_env.sh
```
마지막으로 한국어 테스트: 템플릿으로 `new_video.py` → TTS → validate → `build.py --quality l` 이 끝까지 되는지 본다.
