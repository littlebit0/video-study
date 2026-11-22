"""Turn a folder of course materials into plain-text sources + an inventory.

Usage: ~/tools/.venv/bin/python extract_sources.py <materials_dir> <project_dir>
Writes <project_dir>/sources/:
  <pdf name>.txt        text per page, "=== page N ===" headers (formulas/figures are lost: render pages to PNG to read them)
  <doc name>.txt        rtf/docx/doc/txt converted with macOS textutil
  inventory.md          every file with type, pages/size, and what to do with it
The materials folder is only read, never modified.
"""
import subprocess, sys, shutil
from pathlib import Path
import pymupdf

src, proj = Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).expanduser()
out = proj / "sources"; out.mkdir(parents=True, exist_ok=True)
rows = []
for f in sorted(src.rglob("*")):
    if not f.is_file() or f.name.startswith("."):
        continue
    ext, rel = f.suffix.lower(), f.relative_to(src)
    if ext == ".pdf":
        d = pymupdf.open(f)
        text = "\n".join(f"=== page {i + 1} ===\n{p.get_text()}" for i, p in enumerate(d))
        (out / f"{f.stem}.txt").write_text(text)
        chars = len(text) / max(d.page_count, 1)
        note = "이미지 위주: 페이지를 PNG로 렌더링해서 읽기" if chars < 200 else "텍스트 추출됨 (수식 쪽은 PNG로 확인)"
        rows.append((rel, "PDF", f"{d.page_count}쪽", note))
    elif ext in (".rtf", ".rtfd", ".docx", ".doc", ".txt", ".md"):
        dst = out / f"{f.stem}.txt"
        if ext in (".txt", ".md"):
            shutil.copy(f, dst)
        else:
            subprocess.run(["textutil", "-convert", "txt", "-output", str(dst), str(f)], check=True)
        t = dst.read_text(errors="ignore")
        kind = "링크 목록" if t.count("http") >= 2 and len(t) < 3000 else ("녹음/전사" if len(t) > 20000 else "문서")
        rows.append((rel, kind, f"{len(t):,}자", "YouTube 링크면 watch 스킬로 자막·화면 수집" if kind == "링크 목록" else "주차 표시 줄(예: '6주차')로 나누기"))
    elif ext in (".png", ".jpg", ".jpeg", ".heic", ".webp"):
        rows.append((rel, "이미지", f"{f.stat().st_size // 1024}KB", "Read로 직접 보기 (LMS 주차표 등)"))
    elif ext in (".mp4", ".mov", ".m4a", ".mp3", ".wav"):
        rows.append((rel, "미디어", f"{f.stat().st_size // 1048576}MB", "watch 스킬 --input 으로 전사"))
    else:
        rows.append((rel, ext or "?", f"{f.stat().st_size // 1024}KB", "확인 필요"))

md = ["| 파일 | 종류 | 크기 | 처리 |", "|---|---|---|---|"] + [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
(out / "inventory.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
