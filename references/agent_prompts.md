# 에이전트 지시문 템플릿

`<...>` 를 채워서 Agent 도구로 보낸다. 여러 편이면 한 메시지에 여러 Agent 호출 → 병렬 실행.
Agent 결과는 보고서일 뿐이다. 반드시 직접 확인(수치 검산, 프레임 시트)한 뒤 사용자에게 보낸다.

## 1. 내용 정리(brief) 에이전트 — model: sonnet, run_in_background: true

```
You are preparing a content brief (in Korean) for a 3Blue1Brown-style Korean explainer video for a university <과목> course. The video will be made later with Manim; your job is ONLY to extract accurate, exam-relevant content. Do not write code or narration.

VIDEO <vN> topic: <주제> (course weeks <주차>).

Sources (read-only; never modify the materials folder):
- PDF(s): <절대경로들> — cover only <범위>. <다른 편이 맡는 범위가 있으면 명시>
- Extracted PDF text: <project>/sources/*.txt. Text extraction loses formulas; for formula/figure pages render to PNG and look:
  `~/tools/.venv/bin/python -c "import pymupdf,sys;d=pymupdf.open(sys.argv[1]);d[int(sys.argv[2])-1].get_pixmap(dpi=110).save(sys.argv[3])" <pdf> <page> <out.png>` (PNGs to <project>/intermediate/<slug>/pages/), then Read the PNG.
- Professor transcript(s) (noisy Korean STT; English terms transliterated): <project>/sources/rec_wNN.txt. The recording is the primary basis: what was taught and emphasized there matters most.
- Video lecture subtitles (if any): <project>/sources/yt_*.txt with key frames in sources/yt_frames/.
- Earlier student summaries (may contain errors, verify): <경로 또는 없음>

Write <project>/intermediate/<slug>/brief.md with sections:
1. 개념 순서 (teaching order, PDF page numbers)
2. 정의·공식 (exact LaTeX in the slides' notation)
3. 예제 (numeric examples from slides/lecture, fully worked and verified by hand; cross-check with ~/tools/.venv/bin/python + numpy)
4. 교수 강조점·시험 힌트 (paraphrase with approximate timestamps)
5. 직관/비유 (what to animate)
6. 흔한 실수 / 슬라이드·녹음·정리본 불일치
7. 영상에 넣을 그림 후보 (PDF + page)
8. <실습이 있으면: 실습 핵심 (code idea, outputs, shapes)>
9. 시험 대비 포인트 (<시험 범위 정보>; connections to earlier/later topics)

Accuracy over completeness; mark uncertain items (불확실). Do not include student names. Under ~600 lines. Final message: 10-line summary plus the brief path.
```

시험 해설 편은 섹션을 바꾼다: 1 시험 개요(문항·배점·주제) / 2 문제별(문제, 정답, 검산한 풀이, 교수 설명 요지, 많이 틀린 점·감점, 관련 슬라이드) / 3 교수가 말한 다음 시험 관련 발언 / 4 영상 구성 제안(정답률 낮은 문제에 시간 집중). 시험지 PDF는 모든 쪽을 PNG로 보게 한다.

## 2. 제작 에이전트 — model: 기본(상속), run_in_background: true

```
Produce one Korean 3Blue1Brown-style explainer video for a <과목> course, end to end, using the installed notes-to-video skill.

Your video: <vN> "<제목>" (<주차>). Folder: <project>/intermediate/<slug>/ (name = "<name>", so files are src/video_<name>.py, src/part_<name>_narration.py, src/generate_tts_<name>.py, audio/video_<name>/). The scaffold and template are already there. Content brief (already researched and verified): <project>/intermediate/<slug>/brief.md. Key points: <brief 에서 꼭 살릴 3~6개: 시험 함정, 표기 충돌 처리, 빼야 할 불확실 내용>.

Read and follow <project>/PRODUCTION_GUIDE.md exactly — fixed settings, reference implementation (<완성된 편이 있으면 그 src 경로, 없으면 템플릿>), step order, layout and content rules, and what to report. Other agents may be producing sibling videos in parallel; do not touch their folders, intermediate/common/, or the materials folder (read-only). If something in common/ seems broken, don't edit it — work around it in your own src/ and mention it in your report.

Target 9–12 minutes. Work until the final files exist in <project>/final/<slug>/ and you have checked frames from the finished video. Final message: the report described in the guide.
```

진행 중 공통 규칙이 바뀌면 PRODUCTION_GUIDE.md 를 고치고 SendMessage 로 각 에이전트에 한 단락으로 알린다.
