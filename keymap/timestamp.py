from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Final
from zoneinfo import ZoneInfo

MetadataLines = list[str]

_HERE: Final[Path] = Path(__file__).resolve().parent
DEFAULT_SVG: Final[Path] = _HERE.parent / "images" / "key-bindings.svg"

TZ: ZoneInfo = ZoneInfo("Asia/Shanghai")
META_ID: str = "svg-meta"
FONT_SIZE: int = 12
LINE_HEIGHT: int = 14
TOP_Y: int = 40
MARGIN: int = 60

META_RE: re.Pattern[str] = re.compile(
    rf'<g id="{META_ID}">.*?</g>', re.DOTALL,
)
VIEWBOX_RE: re.Pattern[str] = re.compile(r'viewBox="([^"]+)"')
WIDTH_RE: re.Pattern[str] = re.compile(r'width="([\d.]+)')


def collect_metadata() -> MetadataLines:
    now = datetime.now(TZ)
    stamp = now.strftime("%Y-%m-%d %H:%M:%S")
    offset = now.strftime("%z")
    tz_str = f"UTC{offset[:3]}:{offset[3:]}"
    return [f"{stamp} {tz_str}"]


def get_width(svg: str) -> float | None:
    m = VIEWBOX_RE.search(svg)
    if m:
        parts = m.group(1).split()
        if len(parts) >= 3:
            try:
                return float(parts[2])
            except ValueError:
                pass
    m = WIDTH_RE.search(svg)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    return None


def build_group(lines: MetadataLines, width: float | None) -> str:
    x: str = f"{width - MARGIN:g}" if width is not None else "99%"
    texts: list[str] = []
    y = TOP_Y
    for line in lines:
        texts.append(
            f'<text x="{x}" y="{y}" style="text-anchor:end" '
            f'font-size="{FONT_SIZE}" font-weight="bold" fill="#000000" '
            f'font-family="monospace">{line}</text>'
        )
        y += LINE_HEIGHT
    return f'<g id="{META_ID}">' + "".join(texts) + "</g>"


def add_metadata(svg_path: str | Path = DEFAULT_SVG) -> MetadataLines:
    path = Path(svg_path)
    svg = path.read_text(encoding="utf-8")
    svg = META_RE.sub("", svg)
    lines = collect_metadata()
    group = build_group(lines, get_width(svg))
    svg = svg.replace("</svg>", group + "\n</svg>")
    path.write_text(svg, encoding="utf-8")
    return lines


def main(svg_path: str | Path = DEFAULT_SVG) -> None:
    lines = add_metadata(svg_path)
    for line in lines:
        print(f"已写入: {line}")


if __name__ == "__main__":
    main()