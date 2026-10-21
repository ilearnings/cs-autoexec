import re
from datetime import datetime

from keymap.constants import (
    META_ID,
    META_RE,
    MOUSE_CSS_STYLE,
    MOUSE_HEIGHT,
    MOUSE_OFFSET_X,
    MOUSE_SVG_SHAPES,
    MOUSE_WIDTH,
    STAMP_FONT_SIZE,
    STAMP_MARGIN,
    STAMP_TOP_Y,
    TZ,
    VIEWBOX_RE,
)
from keymap.label import build_text_elems, split_label

type Binds = dict[str, str]


def render_mouse_svg(binds: Binds) -> str:
    elements = [
        MOUSE_CSS_STYLE,
        MOUSE_SVG_SHAPES,
    ]

    wheel_up = binds.get("mwheelup", "")
    wheel_down = binds.get("mwheeldown", "")
    is_wheel_same = (wheel_up == wheel_down) and bool(wheel_up)

    positions = {
        "MOUSE1": (MOUSE_WIDTH / 2 - 50, 55, "middle"),
        "MOUSE2": (MOUSE_WIDTH / 2 + 50, 55, "middle"),
        "MOUSE3": (MOUSE_WIDTH / 2, 88, "middle"),
        "MWHEELUP": (MOUSE_WIDTH / 2, 42 + 38 / 2, "middle"),
        "MOUSE4": (88, 145, "end"),
        "MOUSE5": (80, 195, "end"),
    }

    for key, (mx, my, anchor) in positions.items():
        text = binds.get(key.lower(), "")

        if is_wheel_same:
            if key == "MWHEELDOWN":
                continue
            if key == "MWHEELUP":
                display = "\n".join(list(text))
                elements.extend(
                    build_text_elems(display, mx, my, anchor, "mouse-label")
                )
                continue

        is_bound = bool(text)
        css_class = "mouse-label" if is_bound else "mouse-label unbound"

        if key == "MOUSE3":
            display = text if is_bound else key
        elif key == "MOUSE4":
            display = split_label(text) if is_bound else key
        elif key == "MOUSE5":
            display = "\n".join(list(text)) if is_bound else key
        else:
            display = split_label(text) if is_bound else key

        elements.extend(build_text_elems(display, mx, my, anchor, css_class))

    return "\n".join(elements)


def finalize_svg(svg: str, mouse_block: str) -> str:
    if not (match := VIEWBOX_RE.search(svg)):
        return svg

    w, h = 1500.0, 500.0
    if len(parts := match.group(1).split()) == 4:
        w, h = float(parts[2]), float(parts[3])

    new_w = w + MOUSE_WIDTH + MOUSE_OFFSET_X
    new_h = max(h, MOUSE_HEIGHT + 80)

    svg = VIEWBOX_RE.sub(f'viewBox="0 0 {new_w:g} {new_h:g}"', svg, count=1)
    svg = re.sub(r'width="[^"]+"', f'width="{new_w:g}"', svg, count=1)
    svg = re.sub(r'height="[^"]+"', f'height="{new_h:g}"', svg, count=1)

    tx = w + MOUSE_OFFSET_X / 2
    ty = (new_h - MOUSE_HEIGHT) / 2

    mouse_group = f'<g transform="translate({tx:g}, {ty:g})">\n{mouse_block}\n</g>'
    svg = svg.replace("</svg>", f"{mouse_group}\n</svg>")

    now = datetime.now(TZ)
    offset = now.strftime("%z")
    stamp_text = f"{now:%Y-%m-%d %H:%M:%S} UTC{offset[:3]}:{offset[3:]}"
    x = new_w - STAMP_MARGIN
    stamp_group = (
        f'<g id="{META_ID}"><text x="{x:g}" y="{STAMP_TOP_Y}" '
        f'style="text-anchor:end" font-size="{STAMP_FONT_SIZE}" font-weight="bold" '
        f'fill="#000000" stroke="#ffffff" stroke-width="3" paint-order="stroke" stroke-linejoin="round" '
        f'font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif">{stamp_text}</text></g>'
    )
    return META_RE.sub("", svg).replace("</svg>", f"{stamp_group}\n</svg>")
