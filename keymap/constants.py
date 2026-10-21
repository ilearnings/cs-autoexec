import os
import re
from pathlib import Path
from typing import Final
from zoneinfo import ZoneInfo

HERE: Final[Path] = Path(__file__).resolve().parent
ROOT: Final[Path] = HERE.parent

SOURCE_CFG: Final[Path] = ROOT / "autoexec.cfg"
KEYMAP_YML: Final[Path] = HERE / "keymap.yml"
DRAWER_CONFIG: Final[Path] = HERE / "config.yml"
LAYOUT_JSON: Final[Path] = HERE / "layout.json"
OUTPUT_SVG: Final[Path] = ROOT / "images" / "bindings.svg"

BIND_RE: Final[re.Pattern[str]] = re.compile(
    r'bind\s+"([^"]+)"\s+"([^"]+)"(?:\s*//\s*(.*))?'
)
TAG_RE: Final[re.Pattern[str]] = re.compile(r"\^([^\^]+)\^")
META_ID: Final[str] = "svg-meta"
META_RE: Final[re.Pattern[str]] = re.compile(rf'<g id="{META_ID}">.*?</g>', re.DOTALL)
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

COLOR_MOUSE_BODY: Final[str] = "#f0f0f0"
COLOR_KEY_FILL: Final[str] = "#111111"
COLOR_WHEEL_FILL: Final[str] = "#f0f0f0"
COLOR_KEY_BORDER: Final[str] = "#333333"

COLOR_LABEL_BOUND: Final[str] = "#ffffff"
COLOR_LABEL_UNBOUND: Final[str] = "#ffffff"

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

MOUSE_CSS_STYLE: Final[str] = f"""
  <style>
    .key-zone path, .key-zone rect {{
      stroke: {COLOR_KEY_BORDER}; stroke-width: 1.5;
    }}
    .mouse-label {{ font: bold 12px "Microsoft YaHei", "Noto Sans CJK SC", sans-serif; fill: {COLOR_LABEL_BOUND}; }}
    .mouse-label.unbound {{ fill: {COLOR_LABEL_UNBOUND}; font-weight: normal; font-size: 10px; }}
  </style>
"""

MOUSE_SVG_SHAPES: Final[str] = f"""
  <path d="M150,12 C 110,12 75,20 60,70 C 55,90 58,120 63,140 C 65,155 65,175 64,190 C 62,210 55,230 52,250 C 48,285 70,330 110,350 C 130,365 170,365 190,350 C 230,330 252,285 248,250 C 245,230 238,210 236,190 C 235,175 235,155 237,140 C 242,120 245,90 240,70 C 225,20 190,12 150,12 Z" fill="{COLOR_MOUSE_BODY}" stroke="none"/>
  <g class="key-zone">
    <path d="M 148 12 C 110 12 75 20 60 70 C 65 95 90 112 148 112 Q 148 108 148 12 Z" fill="{COLOR_KEY_FILL}" stroke="{COLOR_KEY_BORDER}" stroke-width="1.5" />
    <path d="M 152 12 C 190 12 225 20 240 70 C 235 95 210 112 152 112 Q 152 108 152 12 Z" fill="{COLOR_KEY_FILL}" stroke="{COLOR_KEY_BORDER}" stroke-width="1.5" />
    <rect x="136" y="42" width="28" height="38" rx="6" fill="{COLOR_WHEEL_FILL}" stroke="{COLOR_KEY_BORDER}" stroke-width="1.5" />
    <path d="M 61,125 C 63,140 64,155 65,165 L 73,165 C 72,155 71,140 69,125 Z" fill="{COLOR_KEY_FILL}" stroke="{COLOR_KEY_BORDER}" stroke-width="1.5"/>
    <path d="M 64.5,175 C 64.5,185 64,195 63,203 Q 68,206 72,203 C 73,195 73,185 72.5,175 Z" fill="{COLOR_KEY_FILL}" stroke="{COLOR_KEY_BORDER}" stroke-width="1.5"/>
  </g>
"""
