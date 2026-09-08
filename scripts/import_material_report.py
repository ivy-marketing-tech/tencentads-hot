from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIAL_HTML = ROOT / "src" / "material-report.html"
MATERIAL_CSS = ROOT / "src" / "material-report.css"


def extract(source: str) -> tuple[str, str]:
    styles = re.findall(r"<style[^>]*>([\s\S]*?)</style>", source, flags=re.I)
    body_match = re.search(r"<body[^>]*>([\s\S]*?)</body>", source, flags=re.I)
    body = body_match.group(1) if body_match else source
    body = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", body, flags=re.I).strip()
    return body, "\n\n".join(part.strip() for part in styles if part.strip())


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("用法：import_material_report.py <新版素材HTML路径>")
    source_path = Path(sys.argv[1]).expanduser().resolve()
    source = source_path.read_text(encoding="utf-8")
    body, css = extract(source)
    if not body:
        raise RuntimeError("素材 HTML 中未找到可注入的正文内容")
    if not css:
        raise RuntimeError("素材 HTML 中未找到样式；请提供包含 <style> 的完整 HTML 文件")
    MATERIAL_HTML.write_text(body + "\n", encoding="utf-8")
    MATERIAL_CSS.write_text(css + "\n", encoding="utf-8")
    print("已更新视频号素材模块；请继续运行 build_hotspot_page.py build")


if __name__ == "__main__":
    main()
