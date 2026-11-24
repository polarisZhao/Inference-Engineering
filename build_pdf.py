#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a print-ready PDF from the Chinese translation Markdown.

Pipeline: Markdown -> styled HTML -> Chrome headless print-to-PDF -> footer page numbers.
Only stdlib + `markdown` + PyMuPDF are required.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import fitz  # PyMuPDF
import markdown

ROOT = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DEFAULT_MD = ROOT / "Inference-Engineering-中文全本.md"
DEFAULT_PDF = ROOT / "Inference-Engineering-中文全本.pdf"


CSS = r"""
@page {
  size: A4;
  margin: 20mm 18mm 22mm 18mm;
}
* { box-sizing: border-box; }
html { font-size: 10.5pt; }
body {
  margin: 0;
  font-family: "Songti SC", "STSong", "Noto Serif CJK SC", serif;
  line-height: 1.78;
  color: #1b1b1b;
  text-align: justify;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
p { margin: 0 0 8pt; orphans: 2; widows: 2; }
h1, h2, h3, h4 {
  font-family: "PingFang SC", "Hiragino Sans GB", "Heiti SC", sans-serif;
  color: #0b5d46;
  line-height: 1.35;
  break-after: avoid;
  page-break-after: avoid;
}
h1 {
  font-size: 21pt;
  margin: 0 0 16pt;
  padding-bottom: 8pt;
  border-bottom: 2pt solid #0b5d46;
  break-before: page;
  page-break-before: always;
}
h2 {
  font-size: 14.5pt;
  margin: 20pt 0 8pt;
  padding-left: 8pt;
  border-left: 4pt solid #2e8b6f;
}
h3 { font-size: 11.8pt; margin: 15pt 0 6pt; }
h4 { font-size: 10.8pt; margin: 12pt 0 5pt; }
ul, ol { margin: 0 0 8pt; padding-left: 1.8em; }
li { margin: 0 0 3pt; text-align: left; }
strong { font-weight: 700; }
em { font-style: italic; }
a { color: #0b5d46; text-decoration: none; }
hr {
  border: 0;
  border-top: 0.6pt solid #cfded7;
  margin: 14pt 0;
}
blockquote {
  margin: 10pt 0;
  padding: 8pt 12pt;
  background: #f3f8f5;
  border-left: 3pt solid #7fb3a0;
  color: #2a2a2a;
  font-size: 9.4pt;
  line-height: 1.65;
  break-inside: avoid;
  page-break-inside: avoid;
}
blockquote p { margin: 0 0 4pt; }
blockquote p:last-child { margin-bottom: 0; }
blockquote table { margin: 6pt 0; }
blockquote pre { margin: 6pt 0; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 10pt 0;
  font-size: 9pt;
  line-height: 1.45;
}
tr { break-inside: avoid; page-break-inside: avoid; }
th {
  background: #0b5d46;
  color: #ffffff;
  font-family: "PingFang SC", "Hiragino Sans GB", sans-serif;
  font-weight: 600;
  text-align: left;
  padding: 5pt 6pt;
  border: 0.5pt solid #0b5d46;
}
td {
  padding: 4.5pt 6pt;
  border: 0.5pt solid #b9cfc6;
  vertical-align: top;
}
tbody tr:nth-child(even) { background: #f6faf8; }
code {
  font-family: "Menlo", "SF Mono", "Courier New", monospace;
  font-size: 8.6pt;
  background: #eef2f0;
  padding: 0 2.5pt;
  border-radius: 2pt;
}
pre {
  background: #f5f8f6;
  border: 0.5pt solid #d5e2db;
  border-radius: 3pt;
  padding: 8pt 10pt;
  margin: 8pt 0;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.5;
  break-inside: avoid;
  page-break-inside: avoid;
}
pre code { background: none; padding: 0; font-size: 8.4pt; }

/* Cover */
.cover {
  height: 252mm;
  padding: 22mm 18mm;
  background-color: #0d3b2e;
  background-image:
    linear-gradient(rgba(255,255,255,0.055) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.055) 1px, transparent 1px);
  background-size: 12mm 12mm;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-radius: 2mm;
  break-after: page;
  page-break-after: always;
}
.cover .kicker {
  font-family: "Menlo", monospace;
  font-size: 9pt;
  letter-spacing: 3pt;
  color: #8fd0b8;
  margin-bottom: 8mm;
}
.cover h1 {
  font-size: 46pt;
  color: #ffffff;
  border: 0;
  margin: 0;
  padding: 0;
  letter-spacing: 3pt;
  break-before: avoid;
  page-break-before: avoid;
}
.cover .en {
  font-family: "PingFang SC", sans-serif;
  font-size: 19pt;
  letter-spacing: 1.5pt;
  color: #b9e2d2;
  margin: 3mm 0 12mm;
}
.cover .rule {
  width: 46mm;
  height: 1.2mm;
  background: #57b894;
  margin-bottom: 12mm;
}
.cover .author {
  font-family: "PingFang SC", sans-serif;
  font-size: 13pt;
  color: #ffffff;
}
.cover .scope {
  margin-top: auto;
  font-family: "PingFang SC", sans-serif;
  font-size: 9.5pt;
  color: #9fd3bf;
  letter-spacing: 0.5pt;
}

/* Info page */
.info { break-after: page; page-break-after: always; padding-top: 6mm; }
.info h2:first-child { margin-top: 0; }
.info table { font-size: 9.2pt; }
.info td { border: 0; border-bottom: 0.5pt solid #dce7e2; }
.info td:first-child { width: 28mm; color: #0b5d46; font-weight: 600; }

/* TOC */
.toc-page { break-after: page; page-break-after: always; }
.toc-page h1 {
  break-before: avoid;
  page-break-before: avoid;
}
.toc { font-family: "PingFang SC", "Hiragino Sans GB", sans-serif; }
.toc ul { list-style: none; margin: 0; padding-left: 0; }
.toc ul ul { padding-left: 1.4em; }
.toc li { margin: 2.2pt 0; font-size: 9.6pt; line-height: 1.5; }
.toc > ul > li { margin-top: 7pt; }
.toc > ul > li > a {
  font-weight: 700;
  color: #0b5d46;
  font-size: 10.6pt;
}
.toc ul ul a { color: #333333; }
.toc a { text-decoration: none; }

/* Keep figure captions readable */
blockquote strong { color: #0b5d46; }
"""


COVER = """
<section class="cover">
  <div class="kicker">INFERENCE ENGINEERING</div>
  <h1>推理工程</h1>
  <div class="en">Inference Engineering</div>
  <div class="rule"></div>
  <div class="author">Philip Kiely&nbsp;&nbsp;著</div>
  <div class="scope">中文译本 · 第 0–7 章及附录</div>
</section>
"""


INFO = """
<section class="info">
  <h2>图书信息</h2>
  <table>
    <tr><td>书名</td><td>推理工程（Inference Engineering）</td></tr>
    <tr><td>作者</td><td>Philip Kiely</td></tr>
    <tr><td>出版</td><td>Baseten Books</td></tr>
    <tr><td>版权</td><td>Copyright © 2026 Baseten Labs, Inc.</td></tr>
    <tr><td>ISBN</td><td>979-8-9943597-2-3</td></tr>
    <tr><td>原书</td><td>Inference Engineering, 259 pages</td></tr>
    <tr><td>译稿范围</td><td>第 0–7 章、附录 A、附录 B 与致谢</td></tr>
  </table>

  <h2>译稿说明</h2>
  <p>本译本力求“信、达、雅”：忠实传达原意，中文表达通顺凝练，并尽量保留原书的工程语气与叙述节奏。</p>
  <p>专有名词、产品名与关键术语（如 KV cache、prefill、decode、TTFT、TPS、compute-bound、memory-bound、kernel、token 等）按行业惯例保留英文，首次出现时酌情附中文解释。所有图号、图注、表格与公式均按原文保留并译出；原文第 3 章有一处图号重复，译本按原样保留并加注说明。</p>
  <p>本译本用于学习与研究。原书版权归作者与出版方所有。</p>

  <h2>阅读建议</h2>
  <p>第一次接触推理工程的读者，建议按第 0 章 → 第 1 章 → 第 2 章 → 第 3 章的顺序建立全局图景；已经熟悉模型与硬件的读者，可直接从第 5 章“技术”与第 7 章“生产”切入，再按需回查第 4 章与第 6 章。</p>
</section>
"""


def _convert_blockquote_fences(text: str) -> str:
    """Turn fenced code blocks nested in blockquotes into indented code blocks.

    Python-Markdown does not process fenced_code inside blockquotes, so lines
    such as ``> # comment`` would otherwise become headings (and corrupt the
    TOC). Indented code inside a blockquote is parsed correctly.
    """
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    open_re = re.compile(r"^(\s*>+\s*)```")
    while i < len(lines):
        m = open_re.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        prefix = m.group(1)
        i += 1
        code: list[str] = []
        while i < len(lines):
            mq = re.match(r"^(\s*>+\s?)(.*)$", lines[i])
            if mq and mq.group(2).lstrip().startswith("```"):
                i += 1
                break
            code.append(mq.group(2) if mq else lines[i])
            i += 1
        for cl in code:
            if cl.strip() == "":
                out.append(prefix.rstrip())
            else:
                out.append(prefix + "    " + cl)
    return "\n".join(out)


def build_html(md_path: Path, html_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    marker = "\n# 第 0 章"
    idx = text.find(marker)
    body_md = text[idx + 1 :] if idx != -1 else text
    # Drop horizontal rules used only to separate chapter files.
    body_md = re.sub(r"(?m)^---\s*$\n?", "", body_md)
    body_md = _convert_blockquote_fences(body_md)
    body_md = "[TOC]\n\n" + body_md

    md = markdown.Markdown(
        extensions=["extra", "toc", "sane_lists"],
        extension_configs={"toc": {"toc_depth": "2", "permalink": False}},
    )
    body_html = md.convert(body_md)

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>推理工程（Inference Engineering）中文译本</title>
<meta name="author" content="Philip Kiely">
<style>{CSS}</style>
</head>
<body>
{COVER}
{INFO}
<section class="toc-page">
  <h1>目录</h1>
  {body_html.split('<div class="toc">', 1)[0] if '<div class="toc">' in body_html else ''}
</section>
</body>
</html>
"""
    # The TOC div is part of body_html; splice it into the toc page rather than
    # leaving it at the top of the body. Rebuild explicitly:
    toc_start = body_html.find('<div class="toc">')
    toc_end = body_html.find("</div>", toc_start)
    if toc_start != -1 and toc_end != -1:
        toc_html = body_html[toc_start : toc_end + len("</div>")]
        body_wo_toc = body_html[:toc_start] + body_html[toc_end + len("</div>") :]
    else:
        toc_html = ""
        body_wo_toc = body_html

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>推理工程（Inference Engineering）中文译本</title>
<meta name="author" content="Philip Kiely">
<style>{CSS}</style>
</head>
<body>
{COVER}
{INFO}
<section class="toc-page">
  <h1>目录</h1>
  {toc_html}
</section>
{body_wo_toc}
</body>
</html>
"""
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")


def chrome_print(html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=15000",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if proc.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(
            "Chrome print-to-pdf failed\n"
            f"exit={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
        )


def add_toc_page_numbers(doc: fitz.Document) -> list:
    """Write page numbers beside TOC entries and return PDF outline entries."""
    outline: list[list] = []
    in_toc = False
    for page in doc:
        links = page.get_links()
        internal = [l for l in links if (l.get("page") or -1) >= 0]
        if not in_toc:
            if "目录" in page.get_text() and len(internal) >= 10:
                in_toc = True
            else:
                continue
        if len(internal) < 10:
            break
        right = page.rect.width - 51  # matches the 18 mm right margin
        for link in internal:
            target = link.get("page", -1)
            if target is None or target < 0:
                continue
            r = link["from"]
            title = page.get_textbox(r).strip().replace("\n", " ")
            if title:
                level = 1 if r.x0 < 60 else 2
                outline.append([level, title, int(target) + 1])
            number = str(target + 1)
            width = fitz.get_text_length(number, fontname="helv", fontsize=8.5)
            x = right - width
            y = r.y1 - 2.2
            # dotted leader
            try:
                page.draw_line(
                    fitz.Point(r.x1 + 5, y - 1.5),
                    fitz.Point(x - 5, y - 1.5),
                    color=(0.72, 0.76, 0.74),
                    width=0.4,
                    dashes="[1 2] 0",
                )
            except Exception:
                pass
            page.insert_text(
                (x, y),
                number,
                fontname="helv",
                fontsize=8.5,
                color=(0.30, 0.38, 0.35),
            )
    return outline


def stamp_pdf(raw_pdf: Path, out_pdf: Path) -> int:
    doc = fitz.open(raw_pdf)
    n = len(doc)
    outline = add_toc_page_numbers(doc)
    if outline:
        doc.set_toc(outline)
    for i, page in enumerate(doc):
        if i == 0:  # cover
            continue
        rect = page.rect
        box = fitz.Rect(0, rect.height - 30, rect.width, rect.height - 12)
        page.insert_textbox(
            box,
            f"第 {i + 1} 页",
            fontname="china-s",
            fontsize=8.5,
            color=(0.35, 0.35, 0.35),
            align=1,
        )
    doc.set_metadata(
        {
            "title": "推理工程（Inference Engineering）中文译本",
            "author": "Philip Kiely",
            "subject": "Inference Engineering 第 0–7 章及附录中文译本",
            "keywords": "推理工程, LLM inference, GPU, vLLM, 量化, KV cache",
            "creator": "Claude Code",
            "producer": "Chrome + PyMuPDF",
        }
    )
    doc.save(out_pdf, garbage=4, deflate=True)
    doc.close()
    return n


def main() -> None:
    md_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MD
    out_pdf = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PDF
    build_dir = ROOT / "build"
    html_path = build_dir / "book.html"
    raw_pdf = build_dir / "book_raw.pdf"

    build_html(md_path, html_path)
    chrome_print(html_path, raw_pdf)
    pages = stamp_pdf(raw_pdf, out_pdf)
    print(f"HTML: {html_path}")
    print(f"PDF : {out_pdf} ({pages} pages)")


if __name__ == "__main__":
    main()
