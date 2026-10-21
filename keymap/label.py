from .constants import (
    DISPLAY_NAMES,
    MAX_VERTICAL_LABEL_LEN,
    SPLIT_PREFIXES,
    SPLIT_THRESHOLD,
    VERTICAL_KEYS,
)


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


def render_key(key: str, label: str | None) -> str | dict[str, str]:
    if key in VERTICAL_KEYS:
        if label and len(label) <= MAX_VERTICAL_LABEL_LEN:
            return {"t": "\n".join(label), "type": "bound"}
        return label or get_display(key)
    return {"t": split_label(label), "type": "bound"} if label else get_display(key)
