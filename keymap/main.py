import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import subprocess

import yaml

from keymap.canvas import finalize_svg
from keymap.constants import (
    BIND_RE,
    DRAWER_CONFIG,
    IS_CI,
    KEYBOARD_ROWS,
    KEYMAP_YML,
    LAYER_NAME,
    LAYOUT_JSON,
    MAX_CJK_LABEL_LEN,
    MOUSE_CSS_STYLE,
    MOUSE_LABEL_POSITIONS,
    MOUSE_SVG_SHAPES,
    OUTPUT_SVG,
    SOURCE_CFG,
    SYMBOL_NAMES,
    TAG_RE,
)
from keymap.label import is_cjk_like, render_key, split_label

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


def build_text_elems(
    display: str, mx: int, my: int, anchor: str, css_class: str
) -> list[str]:
    lines = display.split("\n")
    elems = []
    for i, line in enumerate(lines):
        dy = i * 14 - (len(lines) - 1) * 7
        elems.append(
            f'  <text class="{css_class}" x="{mx}" y="{my + dy}" text-anchor="{anchor}">{line}</text>'
        )
    return elems


def render_mouse_svg(binds: Binds) -> str:
    elements = [
        MOUSE_CSS_STYLE,
        MOUSE_SVG_SHAPES,
    ]

    wheel_up = binds.get("mwheelup", "")
    wheel_down = binds.get("mwheeldown", "")
    is_wheel_same = (wheel_up == wheel_down) and bool(wheel_up)

    for key, (mx, my, anchor) in MOUSE_LABEL_POSITIONS.items():
        text = binds.get(key.lower(), "")

        if is_wheel_same:
            if key == "MWHEELDOWN":
                continue
            if key == "MWHEELUP":
                display = "\n".join(list(text))
                elements.extend(
                    build_text_elems(display, 150, 66, "middle", "mouse-label")
                )
                continue

        is_bound = bool(text)
        css_class = "mouse-label" if is_bound else "mouse-label unbound"

        if key == "MOUSE3":
            display = text if is_bound else key
            mx, my, anchor = 150, 105, "middle"
        elif key == "MOUSE4":
            display = split_label(text) if is_bound else key
        elif key == "MOUSE5":
            display = "\n".join(list(text)) if is_bound else key
        else:
            display = split_label(text) if is_bound else key

        elements.extend(build_text_elems(display, mx, my, anchor, css_class))

    return "\n".join(elements)


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
