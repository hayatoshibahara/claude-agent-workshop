"""単一のハーネスと二重のハーネスの英語版の図（figure/single-harness.en.drawio.svg、figure/double-harness.en.drawio.svg）を作る。

日本語版（harness_layers.py）と同じ形で、文字だけを英語にしている。

draw.io の XML を content 属性に埋め込んだ SVG を書き出すので、draw.io（VS Code の Draw.io Integration を含む）で開けば編集できる。
draw.io で編集したあとは、このスクリプトを回し直さない（上書きされる）。

    uv run --no-project python figure/harness_layers_en.py   # slide/ で
"""

from html import escape
from pathlib import Path

HERE = Path(__file__).parent

INK = "#141413"
ORANGE = "#d97757"
BLUE = "#4a78a8"
CARD = "#e8e6dc"
IVORY = "#faf9f5"
PALE_ORANGE = "#f6e3dc"
PALE_BLUE = "#eef3f9"
FONT = "Noto Sans JP, Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif"


class Figure:
    """箱・枠・矢印を並べ、SVG と draw.io の XML を同じ定義から書き出す。"""

    def __init__(self, name: str, w: int, h: int):
        self.name, self.w, self.h = name, w, h
        self.svg: list[str] = []
        self.cells: list[str] = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
        self.n = 0

    def _id(self) -> str:
        self.n += 1
        return f"c{self.n}"

    def frame(self, x, y, w, h, title, stroke, fill):
        """見出しを左上に置く大きな枠。"""
        self.svg.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'
            f'<text x="{x + 16}" y="{y + 24}" dominant-baseline="central" font-size="17" font-weight="bold" '
            f'fill="{stroke}">{escape(title)}</text>'
        )
        self.cells.append(
            f'<mxCell id="{self._id()}" value="{escape(title)}" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;'
            f"fillColor={fill};strokeColor={stroke};strokeWidth=2.5;verticalAlign=top;align=left;spacingLeft=12;"
            f'fontStyle=1;fontSize=17;fontColor={stroke};" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )

    def box(self, x, y, w, h, lines, fill, stroke, bold_first=True):
        """1〜2 行の文字を中央に置く箱。"""
        cx = x + w / 2
        n = len(lines)
        parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>']
        for i, line in enumerate(lines):
            ty = y + h / 2 + (i - (n - 1) / 2) * 22
            weight = ' font-weight="bold"' if (i == 0 and bold_first) else ""
            size = 18 if i == 0 else 15
            if fill == stroke:  # 札（塗りつぶしの小さな箱）
                size = 13
            parts.append(
                f'<text x="{cx}" y="{ty}" text-anchor="middle" dominant-baseline="central" font-size="{size}"{weight}'
                f'{" fill=\"#ffffff\"" if fill == stroke else ""}>'
                f"{escape(line)}</text>"
            )
        self.svg.append("".join(parts))
        value = "<br/>".join((f"<b>{escape(t)}</b>" if (i == 0 and bold_first) else escape(t)) for i, t in enumerate(lines))
        self.cells.append(
            f'<mxCell id="{self._id()}" value="{escape(value)}" style="rounded=1;whiteSpace=wrap;html=1;'
            f'fillColor={fill};strokeColor={stroke};strokeWidth=2;fontSize=16;arcSize=14;" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )

    def arrow(self, points, color=INK, dashed=False, label=None, label_at=None):
        """折れ線の矢印。points の最後が矢じり。"""
        (x1, y1), (x2, y2) = points[-2], points[-1]
        dx, dy = x2 - x1, y2 - y1
        length = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / length, dy / length
        bx, by = x2 - ux * 10, y2 - uy * 10
        px, py = -uy * 6, ux * 6
        line = points[:-1] + [(bx, by)]
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        self.svg.append(
            f'<polyline points="{" ".join(f"{x},{y}" for x, y in line)}" fill="none" stroke="{color}" stroke-width="2"{dash}/>'
            f'<polygon points="{x2},{y2} {bx + px},{by + py} {bx - px},{by - py}" fill="{color}"/>'
        )
        if label:
            lx, ly = label_at
            self.svg.append(
                f'<text x="{lx}" y="{ly}" dominant-baseline="central" font-size="15" font-weight="bold" '
                f'fill="{color}">{escape(label)}</text>'
            )
        pts = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in points[1:-1])
        style = f"endArrow=block;endFill=1;html=1;strokeColor={color};strokeWidth=2;fontSize=15;fontColor={color};"
        if dashed:
            style += "dashed=1;"
        self.cells.append(
            f'<mxCell id="{self._id()}" value="{escape(label or "")}" style="{style}" edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry"><mxPoint x="{points[0][0]}" y="{points[0][1]}" as="sourcePoint"/>'
            f'<mxPoint x="{points[-1][0]}" y="{points[-1][1]}" as="targetPoint"/>'
            f'<Array as="points">{pts}</Array></mxGeometry></mxCell>'
        )

    def write(self):
        model = "".join(self.cells)
        mx = (
            f'<mxfile host="drawio"><diagram name="{self.name}" id="d0">'
            f'<mxGraphModel dx="{self.w}" dy="{self.h}" grid="1" gridSize="10" page="0"><root>{model}</root></mxGraphModel>'
            f"</diagram></mxfile>"
        )
        out = HERE / f"{self.name}.en.drawio.svg"
        out.write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
            f'font-family="{FONT}" fill="{INK}" content="{escape(mx)}">{"".join(self.svg)}</svg>\n',
            encoding="utf-8",
        )
        print(out)


def single():
    f = Figure("single-harness", 600, 540)
    f.frame(10, 10, 580, 440, "Harness: designed by people", ORANGE, IVORY)
    stages = [
        ("Writer agent", "Writes the script"),
        ("Language agent", "Reviews the script"),
        ("Producer agent", "Makes the video"),
        ("Director agent", "Reviews the video"),
        ("Poster agent", "Posts the video"),
    ]
    x, w, h, gap, top = 40, 400, 56, 22, 56
    ys = [top + i * (h + gap) for i in range(len(stages))]
    for (name, what), y in zip(stages, ys):
        fill = PALE_ORANGE if "Reviews" in what else IVORY
        f.box(x, y, w, h, [name, what], fill, ORANGE)
        f.box(x + w - 112, y - 10, 104, 24, ["Agent SDK"], ORANGE, ORANGE)
    for y0, y1 in zip(ys, ys[1:]):
        f.arrow([(x + w / 2, y0 + h), (x + w / 2, y1)])
    right, xo = x + w, x + w + 40
    for src, dst in [(1, 0), (3, 2)]:
        ya, yb = ys[src] + h / 2, ys[dst] + h / 2
        f.arrow([(right, ya), (xo, ya), (xo, yb), (right, yb)], color=ORANGE, dashed=True,
                label="Send back", label_at=(xo + 8, (ya + yb) / 2))
    f.box(150, 490, 300, 40, ["People fix the harness from results"], CARD, INK)
    f.arrow([(300, 490), (300, 450)], dashed=True)
    f.write()


def double():
    f = Figure("double-harness", 600, 540)
    f.frame(10, 10, 580, 450, "Outer loop: improves the harness automatically", BLUE, PALE_BLUE)
    x, w, h, gap, top = 40, 400, 64, 26, 60
    ys = [top + i * (h + gap) for i in range(4)]
    f.box(x, ys[0], w, h, ["Proposer", "Reads the log and rewrites the harness"], IVORY, BLUE)
    f.box(x, ys[1], w, h, ["Inner harness", "Solves tasks with the candidate"], PALE_ORANGE, ORANGE)
    f.box(x + w - 112, ys[1] - 10, 104, 24, ["Agent SDK"], ORANGE, ORANGE)
    f.box(x, ys[2], w, h, ["Evaluator", "Scores it and keeps the better one"], IVORY, BLUE)
    f.box(x, ys[3], w, h, ["Log", "Candidates, scores, failures"], IVORY, BLUE)
    for y0, y1 in zip(ys, ys[1:]):
        f.arrow([(x + w / 2, y0 + h), (x + w / 2, y1)])
    right, xo = x + w, x + w + 40
    ya, yb = ys[3] + h / 2, ys[0] + h / 2
    f.arrow([(right, ya), (xo, ya), (xo, yb), (right, yb)], color=BLUE, label="Repeat",
            label_at=(xo + 8, (ya + yb) / 2))
    f.box(200, 490, 200, 40, ["Improved harness"], CARD, INK)
    f.arrow([(300, 460), (300, 490)])
    f.write()


if __name__ == "__main__":
    single()
    double()
