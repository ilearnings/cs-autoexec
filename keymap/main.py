import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import subprocess

import yaml

from keymap.canvas import finalize_svg, render_mouse_svg
from keymap.constants import (
    BIND_RE,
    DRAWER_CONFIG,
    IS_CI,
    KEYBOARD_ROWS,
    KEYMAP_YML,
    LAYER_NAME,
    LAYOUT_JSON,
    MAX_CJK_LABEL_LEN,
    OUTPUT_SVG,
    SOURCE_CFG,
    SYMBOL_NAMES,
    TAG_RE,
)
from keymap.label import is_cjk_like, render_key

type Binds = dict[str, str]


def warn(message: str) -> None:
    print(f"{'::warning::' if IS_CI else '警告: '}{message}")


def parse_binds() -> Binds:
    binds: Binds = {}
    with SOURCE_CFG.open(encoding="utf-8") as f:
        for raw in f:
            if not (line := raw.strip()).startswith("bind") or not (
                m := BIND_RE.match(line)
            ):
                continue
            tag = TAG_RE.search(m.group(3) or "") or TAG_RE.search(m.group(2) or "")
            if tag:
                label = tag.group(1).strip()
                if len(label) > MAX_CJK_LABEL_LEN and is_cjk_like(label):
                    warn(
                        f"标签 '{label}' 长度为 {len(label)}, 超过 {MAX_CJK_LABEL_LEN} 字, 建议拆分或缩短."
                    )
                key_str = m.group(1).lower()
                binds[SYMBOL_NAMES.get(key_str, key_str)] = label
    return binds


def export_yaml(binds: Binds) -> None:
    layer = [
        [render_key(k, binds.get(k.lower())) for k in row] for row in KEYBOARD_ROWS
    ]
    keymap = {"layers": {LAYER_NAME: layer}}
    with KEYMAP_YML.open("w", encoding="utf-8") as f:
        yaml.dump(keymap, f, allow_unicode=True, sort_keys=False)


def generate_base_svg() -> str:
    tmp_svg = KEYMAP_YML.parent / "temp.svg"
    subprocess.run(
        [
            "uv",
            "tool",
            "run",
            "--from",
            "keymap-drawer",
            "keymap",
            "-c",
            str(DRAWER_CONFIG),
            "draw",
            str(KEYMAP_YML),
            "-j",
            str(LAYOUT_JSON),
            "-o",
            str(tmp_svg),
        ],
        check=True,
    )
    svg = tmp_svg.read_text(encoding="utf-8")
    tmp_svg.unlink(missing_ok=True)
    return svg


def main() -> None:
    OUTPUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    binds = parse_binds()
    export_yaml(binds)
    print(f"已生成 {KEYMAP_YML} 文件.")

    base_svg = generate_base_svg()
    mouse_svg = render_mouse_svg(binds)
    final_svg = finalize_svg(base_svg, mouse_svg)

    OUTPUT_SVG.write_text(final_svg, encoding="utf-8")
    print(f"已为 {OUTPUT_SVG.name} 写入并合并完成.")


if __name__ == "__main__":
    main()
