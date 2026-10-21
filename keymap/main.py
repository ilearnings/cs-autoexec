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
WIDTH_RE: Final[re.Pattern[str]] = re.compile(r'width="([^"]+)"')

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

# 坐标调整：飞行/标记放滚轮中心，滚轮描述放原飞行/标记位置；侧键竖排
MOUSE_LABEL_POSITIONS: Final[dict[str, tuple[int, int, str]]] = {
    "MOUSE1": (100, 55, "middle"),
    "MOUSE2": (200, 55, "middle"),
    "MOUSE3": (150, 66, "middle"),
    "MWHEELUP": (150, 105, "middle"),
    "MWHEELDOWN": (150, 135, "middle"),
    "MOUSE4": (76, 145, "end"),
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
  <path d="M150,12 C 110,12 75,20 60,70 C 55,90 58,120 63,140 C 65,155 65,175 64,190 C 62,210 55,230 52,250 C 48,285 70,330 110,350 C 130,365 170,365 190,350 C 230,330 252,285 248,250 C 245,230 238,210 236,190 C 235,175 235,155 237,140 C 242,120 245,90 240,70 C 225,20 190,12 150,12 Z" fill="url(#bodyGrad)" stroke="#999" stroke-width="2"/>
  <g class="key-zone">
    <path d="M 148 12 C 110 12 75 20 60 70 C 65 95 90 112 146 112 Q 148 108 148 12 Z" fill="#111111" stroke="#333" stroke-width="1.5" />
    <path d="M 152 12 C 190 12 225 20 240 70 C 235 95 210 112 154 112 Q 152 108 152 12 Z" fill="#111111" stroke="#333" stroke-width="1.5" />
    <rect x="136" y="42" width="28" height="38" rx="6" fill="url(#bodyGrad)" stroke="#333" stroke-width="1.5" />
    <rect x="144" y="47" width="12" height="28" rx="4" fill="#00d4ff" opacity="0.8"/>
    <path d="M 61,125 C 63,140 64,155 65,165 L 73,165 C 72,155 71,140 69,125 Z" fill="#111111" stroke="#333" stroke-width="1.5"/>
    <path d="M 64.5,175 C 64.5,185 64,195 63,203 Q 68,206 72,203 C 73,195 73,185 72.5,175 Z" fill="#111111" stroke="#333" stroke-width="1.5"/>
  </g>
"""


def parse_binds() -> Binds:
    binds: Binds = {}
    with SOURCE_CFG.open(encoding="utf-8") as f:
        for raw in f:
            if not (line := raw.strip()).startswith("bind"):
                continue
            if not (match := BIND_RE.match(line)):
                continue
            tag = TAG_RE.search(match.group(3) or "") or TAG_RE.search(
                match.group(2) or ""
            )
            if tag:
                label = tag.group(1).strip()
                if len(label) > MAX_CJK_LABEL_LEN and is_cjk_like(label):
                    warn(
                        f"标签 '{label}' 长度为 {len(label)}, "
                        f"超过 {MAX_CJK_LABEL_LEN} 字, 建议拆分或缩短."
                    )
                key_str = match.group(1).lower()
                binds[SYMBOL_NAMES.get(key_str, key_str)] = label
    return binds


def build_keymap(binds: Binds) -> Keymap:
    return {"layers": {LAYER_NAME: build_layer(binds)}}


def build_layer(binds: Binds) -> KeymapLayer:
    return [
        [render_key(k, binds.get(k.lower()), False) for k in row]
        for row in KEYBOARD_ROWS
    ]


def render_key(key: str, label: str | None, is_mouse: bool = False) -> Key:
    key_type = "mouse" if is_mouse else "bound"
    if key in VERTICAL_KEYS:
        if label and len(label) <= MAX_VERTICAL_LABEL_LEN:
            return {"t": "\n".join(label), "type": key_type}
        return label or get_display(key)
    return {"t": split_label(label), "type": key_type} if label else get_display(key)


def get_display(key: str) -> str:
    if (upper := key.upper()) in DISPLAY_NAMES:
        return DISPLAY_NAMES[upper]
    return key.upper() if len(key) == 1 and key.isalpha() else key


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


def split_cjk_label(label: str) -> str | None:
    if not is_cjk_like(label) or (n := len(label)) < 4:
        return None
    mid = n // 2 if n % 2 == 0 else min((n + 1) // 2, 3)
    return f"{label[:mid]}\n{label[mid:]}"


def is_cjk(ch: str) -> bool:
    return "\u4e00" <= ch <= "\u9fff"


def is_cjk_like(text: str) -> bool:
    return bool(text) and all(is_cjk(ch) or ch.isdigit() for ch in text)


def export_yaml(keymap: Keymap) -> None:
    with KEYMAP_YML.open("w", encoding="utf-8") as f:
        yaml.dump(keymap, f, allow_unicode=True, sort_keys=False)


def warn(message: str) -> None:
    prefix = "::warning::" if IS_CI else "警告: "
    print(f"{prefix}{message}")


def run_drawer(binds: Binds) -> None:
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
    merge_svg(tmp_svg, OUTPUT_SVG, binds)
    tmp_svg.unlink(missing_ok=True)


def merge_svg(src: Path, dst: Path, binds: Binds) -> None:
    svg = src.read_text(encoding="utf-8")
    match = VIEWBOX_RE.search(svg)
    W, H = 1500.0, 500.0
    if match and len(parts := match.group(1).split()) == 4:
        W, H = float(parts[2]), float(parts[3])

    mouse_w, mouse_h = 300.0, 370.0
    new_W = W + mouse_w + 40
    new_H = max(H, mouse_h + 80)

    svg = VIEWBOX_RE.sub(f'viewBox="0 0 {new_W:g} {new_H:g}"', svg, count=1)
    svg = re.sub(r'width="[^"]+"', f'width="{new_W:g}"', svg, count=1)
    svg = re.sub(r'height="[^"]+"', f'height="{new_H:g}"', svg, count=1)

    tx = W + 20
    ty = (new_H - mouse_h) / 2

    elements = [
        f'<g transform="translate({tx:g}, {ty:g})">',
        "  <style>",
        "    .key-zone path, .key-zone rect {",
        "      stroke: #555; stroke-width: 1;",
        "    }",
        '    .mouse-label { font: bold 12px "Microsoft YaHei", "Noto Sans CJK SC", sans-serif; fill: #FFE4A0; filter: url(#glow); }',
        "    .mouse-label.unbound { fill: #666; font-weight: normal; font-size: 10px; filter: none; }",
        "  </style>",
        MOUSE_SVG_SHAPES,
    ]

    wheel_up_label = binds.get("mwheelup", "")
    wheel_down_label = binds.get("mwheeldown", "")
    is_wheel_same = (wheel_up_label == wheel_down_label) and bool(wheel_up_label)

    for key, (mx, my, anchor) in MOUSE_LABEL_POSITIONS.items():
        text = binds.get(key.lower(), "")
        is_bound = bool(text)

        if is_wheel_same:
            if key == "MWHEELDOWN":
                continue
            elif key == "MWHEELUP":
                # 滚轮键描述横向排列
                display = text
                my = 105
                mx = 150
                anchor = "middle"
                css_class = "mouse-label"

                lines = [display]
                for i, line in enumerate(lines):
                    dy = i * 14 - (len(lines) - 1) * 7
                    elements.append(
                        f'  <text class="{css_class}" x="{mx}" y="{my + dy}" '
                        f'text-anchor="{anchor}">{line}</text>'
                    )
                continue

        css_class = "mouse-label" if is_bound else "mouse-label unbound"

        if key in ("MOUSE3", "MOUSE4", "MOUSE5"):
            # 强制竖向排列
            display = "\n".join(list(text)) if is_bound else key
        else:
            display = split_label(text) if is_bound else key

        lines = display.split("\n")
        for i, line in enumerate(lines):
            dy = i * 14 - (len(lines) - 1) * 7
            elements.append(
                f'  <text class="{css_class}" x="{mx}" y="{my + dy}" '
                f'text-anchor="{anchor}">{line}</text>'
            )

    elements.append("</g>")
    mouse_block = "\n".join(elements)

    svg = svg.replace("</svg>", f"{mouse_block}\n</svg>")
    dst.write_text(svg, encoding="utf-8")


def add_metadata(target: Path) -> list[str]:
    svg = META_RE.sub("", target.read_text(encoding="utf-8"))
    lines = collect_metadata()
    target.write_text(
        svg.replace("</svg>", build_group(lines, get_width(svg)) + "\n</svg>"),
        encoding="utf-8",
    )
    return lines


def build_group(lines: list[str], width: float | None) -> str:
    x = f"{width - STAMP_MARGIN:g}" if width is not None else "99%"
    texts = "".join(
        f'<text x="{x}" y="{STAMP_TOP_Y + i * STAMP_LINE_HEIGHT}" '
        f'style="text-anchor:end" '
        f'font-size="{STAMP_FONT_SIZE}" font-weight="bold" fill="#000000" '
        f'stroke="#ffffff" stroke-width="3" paint-order="stroke" stroke-linejoin="round" '
        f'font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">{line}</text>'
        for i, line in enumerate(lines)
    )
    return f'<g id="{META_ID}">{texts}</g>'


def collect_metadata() -> list[str]:
    now = datetime.now(TZ)
    offset = now.strftime("%z")
    return [f"{now:%Y-%m-%d %H:%M:%S} UTC{offset[:3]}:{offset[3:]}"]


def get_width(svg: str) -> float | None:
    if (match := VIEWBOX_RE.search(svg)) and len(parts := match.group(1).split()) >= 3:
        try:
            return float(parts[2])
        except ValueError:
            pass
    if match := WIDTH_RE.search(svg):
        try:
            return float(match.group(1))
        except ValueError:
            pass
    return None


def main() -> None:
    OUTPUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    binds = parse_binds()

    export_yaml(build_keymap(binds))
    print(f"已生成 {KEYMAP_YML} 文件.")

    run_drawer(binds)
    for line in add_metadata(OUTPUT_SVG):
        print(f"已为 {OUTPUT_SVG.name} 写入: {line}")


if __name__ == "__main__":
    main()
