import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Final
from zoneinfo import ZoneInfo

import yaml

type Binds = dict[str, str]
type Key = str | dict[str, str]
type KeymapLayer = list[list[Key]]
type Keymap = dict[str, dict[str, KeymapLayer]]

HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent

SOURCE_CFG: Final[Path] = ROOT / "autoexec.cfg"
KEYMAP_YML: Final[Path] = HERE / "keymap.yml"
DRAWER_CONFIG: Final[Path] = HERE / "config.yml"
LAYOUT_JSON: Final[Path] = HERE / "layout.json"
OUTPUT_SVG: Final[Path] = ROOT / "images" / "bindings.svg"

BIND_RE: Final[re.Pattern[str]] = re.compile(
    r'bind\s+"([^"]+)"\s+"([^"]+)"(?:\s*//\s*(.*))?',
)
TAG_RE: Final[re.Pattern[str]] = re.compile(r"\^([^\^]+)\^")
META_ID: Final[str] = "svg-meta"
META_RE: Final[re.Pattern[str]] = re.compile(
    rf'<g id="{META_ID}">.*?</g>',
    re.DOTALL,
)
VIEWBOX_RE: Final[re.Pattern[str]] = re.compile(r'viewBox="([^"]+)"')

IS_CI: Final[bool] = os.environ.get("GITHUB_ACTIONS") == "true"
LAYER_NAME: Final[str] = "github.com/ilearnings/cs-autoexec"

MAX_CJK_LABEL_LEN: Final[int] = 8
MAX_VERTICAL_LABEL_LEN: Final[int] = 3
SPLIT_THRESHOLD: Final[int] = 6

STAMP_FONT_SIZE: Final[int] = 12
STAMP_LINE_HEIGHT: Final[int] = 14
STAMP_MARGIN: Final[int] = 60
STAMP_TOP_Y: Final[int] = 40

TZ: Final[ZoneInfo] = ZoneInfo("Asia/Shanghai")
VERTICAL_KEYS: Final[frozenset[str]] = frozenset({"KP_PLUS", "KP_ENTER"})
SPLIT_PREFIXES: Final[tuple[str, ...]] = ("BOT", "R Shift", "R Alt", "R Ctrl", "R Win")

DISPLAY_NAMES: Final[dict[str, str]] = {
    "ALT": "Alt",
    "BACKSPACE": "Bksp",
    "CAPSLOCK": "Caps",
    "CTRL": "Ctrl",
    "DELETE": "Del",
    "DOWN": "↓",
    "END": "End",
    "ENTER": "Enter",
    "ESC": "Esc",
    "HOME": "Home",
    "INSERT": "Ins",
    "KP_0": "0",
    "KP_1": "1",
    "KP_2": "2",
    "KP_3": "3",
    "KP_4": "4",
    "KP_5": "5",
    "KP_6": "6",
    "KP_7": "7",
    "KP_8": "8",
    "KP_9": "9",
    "KP_DEL": ".",
    "KP_DIVIDE": "/",
    "KP_ENTER": "Enter",
    "KP_MINUS": "-",
    "KP_MULTIPLY": "*",
    "KP_NUMLOCK": "Num",
    "KP_PLUS": "+",
    "LEFT": "←",
    "MENU": "Fn",
    "PAUSE": "Pause",
    "PGDN": "PgDn",
    "PGUP": "PgUp",
    "PRTSC": "PrtSc",
    "RALT": "R Alt",
    "RCTRL": "R Ctrl",
    "RIGHT": "→",
    "RSHIFT": "R Shift",
    "RWIN": "R Win",
    "SCRLK": "ScrLk",
    "SHIFT": "Shift",
    "SPACE": "Space",
    "TAB": "Tab",
    "UP": "↑",
    "WIN": "Win",
}

SYMBOL_NAMES: Final[dict[str, str]] = {
    "apostrophe": "'",
    "backslash": "\\",
    "comma": ",",
    "equal": "=",
    "grave": "`",
    "lbracket": "[",
    "minus": "-",
    "period": ".",
    "rbracket": "]",
    "semicolon": ";",
    "slash": "/",
}

KEYBOARD_ROWS: Final[list[list[str]]] = [
    [
        "ESC",
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "PRTSC",
        "SCRLK",
        "PAUSE",
    ],
    [
        "`",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "-",
        "=",
        "BACKSPACE",
        "INSERT",
        "HOME",
        "PGUP",
        "KP_NUMLOCK",
        "KP_DIVIDE",
        "KP_MULTIPLY",
        "KP_MINUS",
    ],
    [
        "TAB",
        "q",
        "w",
        "e",
        "r",
        "t",
        "y",
        "u",
        "i",
        "o",
        "p",
        "[",
        "]",
        "\\",
        "DELETE",
        "END",
        "PGDN",
        "KP_7",
        "KP_8",
        "KP_9",
        "KP_PLUS",
    ],
    [
        "CAPSLOCK",
        "a",
        "s",
        "d",
        "f",
        "g",
        "h",
        "j",
        "k",
        "l",
        ";",
        "'",
        "ENTER",
        "KP_4",
        "KP_5",
        "KP_6",
    ],
    [
        "SHIFT",
        "z",
        "x",
        "c",
        "v",
        "b",
        "n",
        "m",
        ",",
        ".",
        "/",
        "RSHIFT",
        "UP",
        "KP_1",
        "KP_2",
        "KP_3",
        "KP_ENTER",
    ],
    [
        "CTRL",
        "WIN",
        "ALT",
        "SPACE",
        "RALT",
        "RWIN",
        "MENU",
        "RCTRL",
        "LEFT",
        "DOWN",
        "RIGHT",
        "KP_0",
        "KP_DEL",
    ],
]

MOUSE_LABEL_POSITIONS: Final[dict[str, tuple[int, int, str]]] = {
    "MOUSE1": (100, 55, "middle"),
    "MOUSE2": (200, 55, "middle"),
    "MOUSE3": (150, 105, "middle"),
    "MWHEELUP": (150, 66, "middle"),
    "MWHEELDOWN": (150, 135, "middle"),
    "MOUSE4": (88, 145, "end"),
    "MOUSE5": (81, 185, "end"),
}

MOUSE_SVG_SHAPES: Final[str] = """
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#e5e5e5"/>
      <stop offset="100%" stop-color="#cccccc"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <path d="M150,12 C 110,12 75,20 60,70 C 55,90 58,120 63,140 C 65,155 65,175 64,190 C 62,210 55,230 52,250 C 48,285 70,330 110,350 C 130,365 170,365 190,350 C 230,330 252,285 248,250 C 245,230 238,210 236,190 C 235,175 235,155 237,140 C 242,120 245,90 240,70 C 225,20 190,12 150,12 Z" fill="url(#bodyGrad)" stroke="#999999" stroke-width="2"/>
  <g class="key-zone">
    <path d="M 148 12 C 110 12 75 20 60 70 C 65 95 90 112 148 112 Q 148 108 148 12 Z" fill="url(#bodyGrad)" stroke="#333333" stroke-width="1.5" />
    <path d="M 152 12 C 190 12 225 20 240 70 C 235 95 210 112 152 112 Q 152 108 152 12 Z" fill="url(#bodyGrad)" stroke="#333333" stroke-width="1.5" />
    <rect x="136" y="42" width="28" height="38" rx="6" fill="#24292E" stroke="#333333" stroke-width="1.5" />
    <path d="M 61,125 C 63,140 64,155 65,165 L 73,165 C 72,155 71,140 69,125 Z" fill="url(#bodyGrad)" stroke="#333333" stroke-width="1.5"/>
    <path d="M 64.5,175 C 64.5,185 64,195 63,203 Q 68,206 72,203 C 73,195 73,185 72.5,175 Z" fill="url(#bodyGrad)" stroke="#333333" stroke-width="1.5"/>
  </g>
"""


def is_cjk(ch: str) -> bool:
    return "\u4e00" <= ch <= "\u9fff"


def is_cjk_like(text: str) -> bool:
    return bool(text) and all(is_cjk(ch) or ch.isdigit() for ch in text)


def split_cjk_label(label: str) -> str | None:
    if not is_cjk_like(label) or (n := len(label)) < 4:
        return None
    mid = n // 2 if n % 2 == 0 else min((n + 1) // 2, 3)
    return f"{label[:mid]}\n{label[mid:]}"


def split_label(label: str) -> str:
    if "\n" in label:
        return label
    if "/" in label:
        return "/\n".join(part.strip() for part in label.split("/"))
    if "-" in label:
        a, _, b = label.partition("-")
        if a and b and is_cjk(a[-1]) and is_cjk(b[0]):
            return f"{a}\n{b}"
    for prefix in SPLIT_PREFIXES:
        if label.startswith(prefix) and len(label) > len(prefix):
            return f"{prefix}\n{label[len(prefix) :]}"
    if cjk := split_cjk_label(label):
        return cjk
    if len(label) > SPLIT_THRESHOLD:
        mid = (len(label) + 1) // 2
        return f"{label[:mid]}\n{label[mid:]}"
    return label


def get_display(key: str) -> str:
    if (upper := key.upper()) in DISPLAY_NAMES:
        return DISPLAY_NAMES[upper]
    return key.upper() if len(key) == 1 and key.isalpha() else key


def render_key(key: str, label: str | None) -> Key:
    if key in VERTICAL_KEYS:
        if label and len(label) <= MAX_VERTICAL_LABEL_LEN:
            return {"t": "\n".join(label), "type": "bound"}
        return label or get_display(key)
    return {"t": split_label(label), "type": "bound"} if label else get_display(key)


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
    keymap: Keymap = {"layers": {LAYER_NAME: layer}}
    with KEYMAP_YML.open("w", encoding="utf-8") as f:
        yaml.dump(keymap, f, allow_unicode=True, sort_keys=False)


def generate_base_svg() -> str:
    tmp_svg = HERE / "temp.svg"
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


def render_mouse_svg(binds: Binds) -> str:
    elements = [
        "  <style>",
        "    .key-zone path, .key-zone rect {",
        "      stroke: #333333; stroke-width: 1.5;",
        "    }",
        '    .mouse-label { font: bold 12px "Microsoft YaHei", "Noto Sans CJK SC", sans-serif; fill: #87CEEB; filter: url(#glow); }',
        "    .mouse-label.unbound { fill: #666; font-weight: normal; font-size: 10px; filter: none; }",
        "  </style>",
        MOUSE_SVG_SHAPES,
    ]

    wheel_up = binds.get("mwheelup", "")
    wheel_down = binds.get("mwheeldown", "")
    is_wheel_same = (wheel_up == wheel_down) and bool(wheel_up)

    for key, (mx, my, anchor) in MOUSE_LABEL_POSITIONS.items():
        text = binds.get(key.lower(), "")
        is_bound = bool(text)

        if is_wheel_same:
            if key == "MWHEELDOWN":
                continue
            if key == "MWHEELUP":
                display = "\n".join(list(text))
                my, mx, anchor = 66, 150, "middle"
                css_class = "mouse-label"
                lines = display.split("\n")
                for i, line in enumerate(lines):
                    dy = i * 14 - (len(lines) - 1) * 7
                    elements.append(
                        f'  <text class="{css_class}" x="{mx}" y="{my + dy}" text-anchor="{anchor}">{line}</text>'
                    )
                continue

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

        for i, line in enumerate(display.split("\n")):
            dy = i * 14 - (len(display.split("\n")) - 1) * 7
            elements.append(
                f'  <text class="{css_class}" x="{mx}" y="{my + dy}" text-anchor="{anchor}">{line}</text>'
            )

    return "\n".join(elements)


def finalize_svg(svg: str, mouse_block: str) -> str:
    if not (match := VIEWBOX_RE.search(svg)):
        return svg

    W, H = 1500.0, 500.0
    if len(parts := match.group(1).split()) == 4:
        W, H = float(parts[2]), float(parts[3])

    mouse_w, mouse_h = 300.0, 370.0
    new_W = W + mouse_w + 40
    new_H = max(H, mouse_h + 80)

    svg = VIEWBOX_RE.sub(f'viewBox="0 0 {new_W:g} {new_H:g}"', svg, count=1)
    svg = re.sub(r'width="[^"]+"', f'width="{new_W:g}"', svg, count=1)
    svg = re.sub(r'height="[^"]+"', f'height="{new_H:g}"', svg, count=1)

    tx = W + 20
    ty = (new_H - mouse_h) / 2

    mouse_group = f'<g transform="translate({tx:g}, {ty:g})">\n{mouse_block}\n</g>'
    svg = svg.replace("</svg>", f"{mouse_group}\n</svg>")

    now = datetime.now(TZ)
    offset = now.strftime("%z")
    stamp_text = f"{now:%Y-%m-%d %H:%M:%S} UTC{offset[:3]}:{offset[3:]}"
    x = new_W - STAMP_MARGIN
    stamp_group = (
        f'<g id="{META_ID}"><text x="{x:g}" y="{STAMP_TOP_Y}" '
        f'style="text-anchor:end" font-size="{STAMP_FONT_SIZE}" font-weight="bold" '
        f'fill="#000000" stroke="#ffffff" stroke-width="3" paint-order="stroke" stroke-linejoin="round" '
        f'font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">{stamp_text}</text></g>'
    )
    return META_RE.sub("", svg).replace("</svg>", f"{stamp_group}\n</svg>")


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
