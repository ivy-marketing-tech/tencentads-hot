from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PAGE = ROOT / "src" / "hotspot-shell.html"
MATERIAL_HTML = ROOT / "src" / "material-report.html"
MATERIAL_CSS = ROOT / "src" / "material-report.css"
DEPLOY_PAGE = ROOT / "index.html"

TEMPLATE_BLOCK = re.compile(
    r'    <template id="materialTemplate">\n([\s\S]*?)\n    </template>\n'
    r'    <script type="text/plain" id="materialStyles">\n([\s\S]*?)\n    </script>',
    re.M,
)


def initialize() -> None:
    html = DEPLOY_PAGE.read_text(encoding="utf-8")
    match = TEMPLATE_BLOCK.search(html)
    if not match:
        raise RuntimeError("未找到可拆分的视频号素材模块")
    MATERIAL_HTML.write_text(match.group(1).rstrip() + "\n", encoding="utf-8")
    MATERIAL_CSS.write_text(match.group(2).rstrip() + "\n", encoding="utf-8")
    shell = TEMPLATE_BLOCK.sub(
        "    <!-- MATERIAL_TEMPLATE -->\n    <!-- MATERIAL_STYLES -->",
        html,
        count=1,
    )
    SOURCE_PAGE.write_text(shell, encoding="utf-8")
    print("已从部署页面拆出热点壳与视频号素材模块")


def build() -> None:
    shell = SOURCE_PAGE.read_text(encoding="utf-8")
    material_html = MATERIAL_HTML.read_text(encoding="utf-8").rstrip()
    material_css = MATERIAL_CSS.read_text(encoding="utf-8").rstrip()
    if "<!-- MATERIAL_TEMPLATE -->" not in shell or "<!-- MATERIAL_STYLES -->" not in shell:
        raise RuntimeError("热点壳文件缺少素材注入标记")
    output = shell.replace(
        "<!-- MATERIAL_TEMPLATE -->",
        '<template id="materialTemplate">\n' + material_html + '\n</template>',
    ).replace(
        "<!-- MATERIAL_STYLES -->",
        '<script type="text/plain" id="materialStyles">\n' + material_css + '\n</script>',
    )
    DEPLOY_PAGE.write_text(output, encoding="utf-8")
    print(f"已构建部署页面：{DEPLOY_PAGE}")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "build"
    if command == "init":
        initialize()
    elif command == "build":
        build()
    else:
        raise SystemExit("用法：build_hotspot_page.py [init|build]")
