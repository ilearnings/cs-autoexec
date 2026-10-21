import re
from datetime import datetime

from .constants import (
    META_ID,
    META_RE,
    STAMP_FONT_SIZE,
    STAMP_MARGIN,
    STAMP_TOP_Y,
    TZ,
    VIEWBOX_RE,
)


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
