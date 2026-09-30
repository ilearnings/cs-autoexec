from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Final

import yaml

Binds = dict[str, str]
KeymapRow = list[Any]
KeymapLayer = list[KeymapRow]
Keymap = dict[str, dict[str, KeymapLayer]]

_HERE: Final[Path] = Path(__file__).resolve().parent
DEFAULT_SOURCE: Final[Path] = _HERE.parent / "autoexec.cfg"
DEFAULT_OUTPUT: Final[Path] = _HERE / "keymap.yml"

LAYER_NAME: str = "github.com/ilearnings/cs-autoexec"

SPLIT_PREFIXES: tuple[str, ...] = ("BOT", "R Shift", "R Alt", "R Ctrl", "R Win")
SPLIT_THRESHOLD: int = 6
MAX_CJK_LABEL_LEN: int = 8
VERTICAL_KEYS: set[str] = {"KP_PLUS", "KP_ENTER"}

IS_CI: bool = os.environ.get("GITHUB_ACTIONS") == "true"


def warn(message: str) -> None:
    if IS_CI:
        print(f"::warning::{message}")
    else:
        print(f"⚠️  警告: {message}")


SYMBOL_NAMES: dict[str, str] = {
    "semicolon": ";", "apostrophe": "'", "comma": ",",
    "period": ".", "slash": "/", "backslash": "\\",
    "lbracket": "[", "rbracket": "]", "grave": "`",
    "equal": "=", "minus": "-",
}

DISPLAY_NAMES: dict[str, str] = {
    "ESC": "Esc",
    "PRTSC": "PrtSc", "SCRLK": "ScrLk", "PAUSE": "Pause",
    "INSERT": "Ins", "HOME": "Home", "PGUP": "PgUp",
    "DELETE": "Del", "END": "End", "PGDN": "PgDn",
    "UP": "↑", "DOWN": "↓", "LEFT": "←", "RIGHT": "→",
    "BACKSPACE": "Bksp", "CAPSLOCK": "Caps", "ENTER": "Enter",
    "SHIFT": "Shift", "RSHIFT": "R Shift",
    "CTRL": "Ctrl", "RCTRL": "R Ctrl",
    "WIN": "Win", "RWIN": "R Win",
    "ALT": "Alt", "RALT": "R Alt",
    "MENU": "Fn", "SPACE": "Space", "TAB": "Tab",
    "KP_NUMLOCK": "Num", "KP_DIVIDE": "/", "KP_MULTIPLY": "*",
    "KP_MINUS": "-", "KP_PLUS": "+", "KP_ENTER": "Enter",
    "KP_DEL": ".", "KP_0": "0", "KP_1": "1", "KP_2": "2",
    "KP_3": "3", "KP_4": "4", "KP_5": "5", "KP_6": "6",
    "KP_7": "7", "KP_8": "8", "KP_9": "9",
}

KEYBOARD_ROWS: list[list[str]] = [
    ["ESC", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
     "PRTSC", "SCRLK", "PAUSE"],
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "BACKSPACE",
     "INSERT", "HOME", "PGUP",
     "KP_NUMLOCK", "KP_DIVIDE", "KP_MULTIPLY", "KP_MINUS"],
    ["TAB", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\",
     "DELETE", "END", "PGDN",
     "KP_7", "KP_8", "KP_9", "KP_PLUS"],
    ["CAPSLOCK", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "ENTER",
     "KP_4", "KP_5", "KP_6"],
    ["SHIFT", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "RSHIFT",
     "UP",
     "KP_1", "KP_2", "KP_3", "KP_ENTER"],
    ["CTRL", "WIN", "ALT", "SPACE", "RALT", "RWIN", "MENU", "RCTRL",
     "LEFT", "DOWN", "RIGHT",
     "KP_0", "KP_DEL"],
]

MOUSE_ROW: list[str] = ["MOUSE1", "MWHEELUP", "MOUSE2",
                        "MOUSE5", "MOUSE3",
                        "MOUSE4", "MWHEELDOWN"]

BIND_RE: re.Pattern[str] = re.compile(r'bind\s+"([^"]+)"\s+"([^"]+)"(?:\s*//\s*(.*))?')
TAG_RE: re.Pattern[str] = re.compile(r'\^([^\^]+)\^')


def parse_binds(
    path: str | Path = DEFAULT_SOURCE,
    symbols: dict[str, str] | None = None,
) -> Binds:
    symbols = symbols or SYMBOL_NAMES
    binds: Binds = {}
    with Path(path).open(encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line.startswith("bind"):
                continue
            m = BIND_RE.match(line)
            if not m:
                continue
            key = m.group(1).lower()
            key = symbols.get(key, key)
            tag = TAG_RE.search(m.group(3) or "") or TAG_RE.search(m.group(2) or "")
            if tag:
                label = tag.group(1).strip()
                if len(label) > MAX_CJK_LABEL_LEN and is_cjk_like(label):
                    warn(
                        f"标签 '{label}' 长度为 {len(label)}, "
                        f"超过 {MAX_CJK_LABEL_LEN} 字, 建议拆分或缩短."
                    )
                binds[key] = label
    return binds


def is_cjk(ch: str) -> bool:
    return "\u4e00" <= ch <= "\u9fff"


def is_cjk_label_char(ch: str) -> bool:
    return is_cjk(ch) or ch.isdigit()


def is_cjk_like(text: str) -> bool:
    return bool(text) and all(is_cjk_label_char(ch) for ch in text)


def split_cjk_label(label: str) -> str | None:
    if not is_cjk_like(label):
        return None
    n = len(label)
    if n < 4:
        return None
    if n % 2 == 0:
        mid = n // 2
    else:
        mid = min((n + 1) // 2, 3)
    return f"{label[:mid]}\n{label[mid:]}"


def split_label(
    label: str,
    prefixes: tuple[str, ...] = SPLIT_PREFIXES,
    threshold: int = SPLIT_THRESHOLD,
) -> str:
    if "\n" in label:
        return label
    if "/" in label:
        return "/\n".join(part.strip() for part in label.split("/"))
    if "-" in label:
        a, _, b = label.partition("-")
        if a and b and is_cjk(a[-1]) and is_cjk(b[0]):
            return f"{a}\n{b}"
    for prefix in prefixes:
        if label.startswith(prefix) and len(label) > len(prefix):
            return f"{prefix}\n{label[len(prefix):]}"
    cjk_split = split_cjk_label(label)
    if cjk_split:
        return cjk_split
    if len(label) > threshold:
        mid = (len(label) + 1) // 2
        return f"{label[:mid]}\n{label[mid:]}"
    return label


def get_display(key: str, names: dict[str, str] | None = None) -> str:
    names = names or DISPLAY_NAMES
    upper = key.upper()
    if upper in names:
        return names[upper]
    if len(key) == 1 and key.isalpha():
        return key.upper()
    return key


def render_key(
    key: str,
    label: str | None,
    is_mouse: bool = False,
    vertical: set[str] | None = None,
    names: dict[str, str] | None = None,
    prefixes: tuple[str, ...] = SPLIT_PREFIXES,
    threshold: int = SPLIT_THRESHOLD,
) -> str | dict[str, str]:
    vertical = VERTICAL_KEYS if vertical is None else vertical
    key_type = "mouse" if is_mouse else "bound"

    if key in vertical:
        text = label or get_display(key, names)
        return {"t": "\n".join(text), "type": key_type} if label else "\n".join(text)

    if label:
        return {"t": split_label(label, prefixes, threshold), "type": key_type}

    return get_display(key, names)


def build_layer(
    binds: Binds,
    keyboard_rows: list[list[str]] | None = None,
    mouse_row: list[str] | None = None,
    **kwargs: Any,
) -> KeymapLayer:
    keyboard_rows = KEYBOARD_ROWS if keyboard_rows is None else keyboard_rows
    mouse_row = MOUSE_ROW if mouse_row is None else mouse_row

    def render(key: str, is_mouse: bool) -> str | dict[str, str]:
        return render_key(key, binds.get(key.lower()), is_mouse, **kwargs)

    rows: KeymapLayer = [[render(k, False) for k in row] for row in keyboard_rows]
    if mouse_row:
        rows.append([render(k, True) for k in mouse_row])
    return rows


def build_keymap(
    binds: Binds,
    layer_name: str = LAYER_NAME,
    **kwargs: Any,
) -> Keymap:
    return {"layers": {layer_name: build_layer(binds, **kwargs)}}


def export_yaml(keymap: Keymap, path: str | Path = DEFAULT_OUTPUT) -> None:
    with Path(path).open("w", encoding="utf-8") as f:
        yaml.dump(keymap, f, allow_unicode=True, sort_keys=False)


def main(
    source: str | Path = DEFAULT_SOURCE,
    output: str | Path = DEFAULT_OUTPUT,
) -> None:
    binds = parse_binds(source)
    export_yaml(build_keymap(binds), output)
    print(f"已生成 {output} 文件.")


if __name__ == "__main__":
    main()