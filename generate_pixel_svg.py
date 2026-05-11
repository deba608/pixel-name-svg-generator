#!/usr/bin/env python3
"""
Generate a GitHub-profile-style animated pixel name SVG.

Examples:
  python generate_pixel_svg.py --name DEBASHISH --subtitle "AI ENGINEER | DEVELOPER"
  python generate_pixel_svg.py --name RAHUL --subtitle "FULL STACK DEVELOPER" --out rahul.svg
"""

from __future__ import annotations

import argparse
import html
import random
import re
from pathlib import Path


WIDE_FONT = {
    "A": [".##.", "#..#", "####", "#..#", "#..#"],
    "B": ["###.", "#..#", "###.", "#..#", "###."],
    "C": [".###", "#...", "#...", "#...", ".###"],
    "D": ["###.", "#..#", "#..#", "#..#", "###."],
    "E": ["####", "#...", "###.", "#...", "####"],
    "F": ["####", "#...", "###.", "#...", "#..."],
    "G": [".###", "#...", "#.##", "#..#", ".###"],
    "H": ["#..#", "#..#", "####", "#..#", "#..#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"],
    "J": ["..##", "...#", "...#", "#..#", ".##."],
    "K": ["#..#", "#.#.", "##..", "#.#.", "#..#"],
    "L": ["#...", "#...", "#...", "#...", "####"],
    "M": ["#...#", "##.##", "#.#.#", "#...#", "#...#"],
    "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "O": [".##.", "#..#", "#..#", "#..#", ".##."],
    "P": ["###.", "#..#", "###.", "#...", "#..."],
    "Q": [".##.", "#..#", "#..#", "#.##", ".###"],
    "R": ["###.", "#..#", "###.", "#.#.", "#..#"],
    "S": ["####", "#...", "###.", "...#", "####"],
    "T": ["#####", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#..#", "#..#", "#..#", "#..#", ".##."],
    "V": ["#...#", "#...#", ".#.#.", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
    "Y": ["#...#", ".#.#.", "..#..", "..#..", "..#.."],
    "Z": ["####", "...#", "..#.", ".#..", "####"],
    "0": [".##.", "#..#", "#..#", "#..#", ".##."],
    "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["###.", "...#", ".##.", "#...", "####"],
    "3": ["###.", "...#", ".##.", "...#", "###."],
    "4": ["#..#", "#..#", "####", "...#", "...#"],
    "5": ["####", "#...", "###.", "...#", "###."],
    "6": [".###", "#...", "###.", "#..#", ".##."],
    "7": ["####", "...#", "..#.", ".#..", ".#.."],
    "8": [".##.", "#..#", ".##.", "#..#", ".##."],
    "9": [".##.", "#..#", ".###", "...#", "###."],
    "&": [".##.", "#.#.", ".#..", "#.#.", ".###"],
    "-": ["....", "....", "###.", "....", "...."],
    "_": ["....", "....", "....", "....", "####"],
    ".": ["..", "..", "..", "..", "#."],
    " ": ["...", "...", "...", "...", "..."],
}

COMPACT_FONT = {
    "A": [".#.", "#.#", "###", "#.#", "#.#"],
    "B": ["##.", "#.#", "##.", "#.#", "##."],
    "C": [".##", "#..", "#..", "#..", ".##"],
    "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"],
    "F": ["###", "#..", "##.", "#..", "#.."],
    "G": [".##", "#..", "#.#", "#.#", ".##"],
    "H": ["#.#", "#.#", "###", "#.#", "#.#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"],
    "J": ["..#", "..#", "..#", "#.#", ".#."],
    "K": ["#.#", "##.", "#..", "##.", "#.#"],
    "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#.#", "###", "###", "#.#", "#.#"],
    "N": ["#.#", "###", "###", "#.#", "#.#"],
    "O": ["###", "#.#", "#.#", "#.#", "###"],
    "P": ["##.", "#.#", "##.", "#..", "#.."],
    "Q": ["###", "#.#", "#.#", "###", "..#"],
    "R": ["##.", "#.#", "##.", "##.", "#.#"],
    "S": ["###", "#..", "###", "..#", "###"],
    "T": ["###", ".#.", ".#.", ".#.", ".#."],
    "U": ["#.#", "#.#", "#.#", "#.#", "###"],
    "V": ["#.#", "#.#", "#.#", "#.#", ".#."],
    "W": ["#.#", "#.#", "###", "###", "#.#"],
    "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "Y": ["#.#", "#.#", ".#.", ".#.", ".#."],
    "Z": ["###", "..#", ".#.", "#..", "###"],
    "0": ["###", "#.#", "#.#", "#.#", "###"],
    "1": [".#.", "##.", ".#.", ".#.", "###"],
    "2": ["##.", "..#", ".#.", "#..", "###"],
    "3": ["##.", "..#", ".#.", "..#", "##."],
    "4": ["#.#", "#.#", "###", "..#", "..#"],
    "5": ["###", "#..", "##.", "..#", "##."],
    "6": [".##", "#..", "##.", "#.#", ".#."],
    "7": ["###", "..#", ".#.", ".#.", ".#."],
    "8": [".#.", "#.#", ".#.", "#.#", ".#."],
    "9": [".#.", "#.#", ".##", "..#", "##."],
    "&": [".#.", "#..", ".#.", "#.#", ".##"],
    "-": ["...", "...", "###", "...", "..."],
    "_": ["...", "...", "...", "...", "###"],
    ".": [".", ".", ".", ".", "#"],
    " ": ["..", "..", "..", "..", ".."],
}


def build_matrix(text: str, min_cols: int = 49) -> list[str]:
    text = text.upper().strip()
    if not text:
        raise ValueError("Name cannot be empty.")

    unsupported = sorted({ch for ch in text if ch not in WIDE_FONT})
    if unsupported:
        raise ValueError(f"Unsupported character(s): {', '.join(unsupported)}")

    rows = [""] * 5
    for index, ch in enumerate(text):
        glyph = WIDE_FONT[ch]
        for row_index in range(5):
            rows[row_index] += glyph[row_index]
            if index != len(text) - 1:
                rows[row_index] += "."

    cols = max(min_cols, len(rows[0]))
    left = (cols - len(rows[0])) // 2
    right = cols - len(rows[0]) - left
    return ["." * left + row + "." * right for row in rows]


def default_output_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"{slug or 'name'}-animation.svg"


def make_svg(name: str, subtitle: str) -> str:
    matrix = build_matrix(name)
    active = [(x, y) for y, row in enumerate(matrix) for x, value in enumerate(row) if value == "#"]
    colors = ["#40c463", "#9be9a8", "#30a14e", "#2ea043", "#216e39"]
    width = len(matrix[0]) * 16 + 60
    center_x = width // 2

    seed = sum(ord(ch) for ch in f"{name}|{subtitle}") + len(active) * 17
    rng = random.Random(seed)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="190" viewBox="0 0 {width} 190">',
        "<style>",
    ]

    for index in range(len(active)):
        rotation = rng.choice((-1, 1)) * rng.randint(18, 720)
        color = colors[index % len(colors)]
        lines.append(
            f"@keyframes a{index}"
            + "{0%{transform:rotate("
            + f"{rotation}deg"
            + ");opacity:0}50%{transform:rotate(0deg);opacity:1}100%{fill:"
            + color
            + ";transform:rotate(0deg);opacity:1}}"
        )

    lines.extend(
        [
            ".sub{font-family:'Segoe UI',Ubuntu,'Helvetica Neue',sans-serif;font-size:14px;fill:#8b949e;letter-spacing:2px;}",
            "</style>",
            '<rect width="100%" height="100%" fill="#0d1117" rx="8"/>',
            "<g>",
        ]
    )

    active_index = 0
    for row_index, row in enumerate(matrix):
        y = 30 + row_index * 16
        for col_index, value in enumerate(row):
            x = 30 + col_index * 16
            if value == "#":
                color = colors[active_index % len(colors)]
                delay = col_index * 0.04 + row_index * 0.02
                lines.append(
                    f'<rect x="{x}" y="{y}" width="12" height="12" rx="2" ry="2" '
                    f'fill="{color}" style="animation:a{active_index} 3s ease-in-out {delay:.2f}s infinite;'
                    f'transform-origin:{x + 6}px {y + 6}px;"/>'
                )
                active_index += 1
            else:
                lines.append(
                    f'<rect x="{x}" y="{y}" width="12" height="12" rx="2" ry="2" '
                    'fill="#161b22" opacity="0.4"/>'
                )

    lines.extend(
        [
            "</g>",
            f'<text x="{center_x}" y="145" text-anchor="middle" class="sub">{html.escape(subtitle.upper())}</text>',
            "</svg>",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an animated pixel name SVG.")
    parser.add_argument("--name", help="Name to render in pixel letters, for example DEBASHISH.")
    parser.add_argument(
        "--subtitle",
        default="AI ENGINEER | DEVELOPER",
        help='Subtitle below the pixel name. Default: "AI ENGINEER | DEVELOPER".',
    )
    parser.add_argument("--out", help="Output SVG path. Default: <name>-animation.svg")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    name = args.name or input("Name: ").strip()
    subtitle = args.subtitle or input("Subtitle: ").strip()
    out = Path(args.out or default_output_name(name))

    svg = make_svg(name, subtitle)
    out.write_text(svg, encoding="utf-8")

    print(f"Created: {out.resolve()}")


if __name__ == "__main__":
    main()
