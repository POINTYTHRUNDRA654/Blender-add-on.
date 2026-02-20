"""
Knowledge helpers for the advisor.
- Loads small snippets from bundled or user-provided knowledge base.
- Supports .txt/.md directly.
- PDFs: best-effort text extraction if PyPDF2 is installed.
- Video: looks for sidecar transcripts (.srt/.vtt/.txt) with the same stem.
- Keeps snippets short to avoid large prompts.
"""

import os
from pathlib import Path

from . import preferences

_DEFAULT_KB_DIR = "knowledge_base"
_TEXT_EXT = {".txt", ".md"}
_VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm"}


def _kb_root() -> Path:
    prefs = preferences.get_preferences()
    base = None
    if prefs and getattr(prefs, "knowledge_base_path", ""):
        base = Path(os.path.abspath(os.path.expanduser(prefs.knowledge_base_path)))
    else:
        base = Path(__file__).resolve().parent / _DEFAULT_KB_DIR
    return base


def _read_text_file(path: Path, max_chars: int) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        text = text.strip()
        return text[:max_chars] if text else None
    except Exception:
        return None


def _read_pdf(path: Path, max_chars: int) -> str | None:
    try:
        import PyPDF2  # optional dependency
    except Exception:
        return None
    try:
        reader = PyPDF2.PdfReader(str(path))
        parts = []
        for page in reader.pages:
            txt = page.extract_text() or ""
            if txt:
                parts.append(txt)
            if sum(len(p) for p in parts) >= max_chars:
                break
        text = "\n".join(parts).strip()
        return text[:max_chars] if text else None
    except Exception:
        return None


def _read_video_sidecar(path: Path, max_chars: int) -> str | None:
    stem = path.with_suffix("")
    for ext in (".srt", ".vtt", ".txt"):
        candidate = stem.with_suffix(ext)
        if candidate.exists():
            return _read_text_file(candidate, max_chars)
    return None


def load_snippets(max_files: int = 12, max_chars: int = 4000) -> list[str]:
    kb_dir = _kb_root()
    snippets: list[str] = []
    if not kb_dir.exists() or not kb_dir.is_dir():
        return snippets

    for path in sorted(kb_dir.glob("**/*")):
        if len(snippets) >= max_files:
            break
        if path.is_dir():
            continue
        ext = path.suffix.lower()

        text = None
        if ext in _TEXT_EXT:
            text = _read_text_file(path, max_chars)
        elif ext == ".pdf":
            text = _read_pdf(path, max_chars)
        elif ext in _VIDEO_EXT:
            text = _read_video_sidecar(path, max_chars)

        if text:
            snippets.append(text)

    return snippets


def describe_kb() -> str:
    kb_dir = _kb_root()
    if not kb_dir.exists():
        return "Knowledge base not found."
    count_txt = sum(1 for p in kb_dir.glob("**/*") if p.suffix.lower() in _TEXT_EXT)
    count_pdf = sum(1 for p in kb_dir.glob("**/*") if p.suffix.lower() == ".pdf")
    count_vid = sum(1 for p in kb_dir.glob("**/*") if p.suffix.lower() in _VIDEO_EXT)
    return f"KB at {kb_dir} (txt/md={count_txt}, pdf={count_pdf}, video={count_vid} w/ transcripts)"


def tool_status() -> dict:
    status = {
        "pypdf2": False,
        "ffmpeg": False,
        "whisper": False,
    }
    try:
        import PyPDF2  # noqa: F401
        status["pypdf2"] = True
    except Exception:
        status["pypdf2"] = False

    def _which(cmd):
        from shutil import which
        return which(cmd) is not None

    status["ffmpeg"] = _which("ffmpeg")
    status["whisper"] = _which("whisper")
    return status
