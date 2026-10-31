"""ショート動画の制作と投稿の流れの図（figure/short-video-flow.drawio.svg）を作る。

draw.io の XML を content 属性に埋め込んだ SVG を書き出すので、draw.io（VS Code の Draw.io Integration を含む）で開けば編集できる。
draw.io で編集したあとは、このスクリプトを回し直さない（上書きされる）。

    uv run --no-project python figure/short_video_flow.py   # slide/ で
"""

from html import escape
from pathlib import Path

OUT = Path(__file__).with_name("short-video-flow.drawio.svg")

INK = "#141413"
ORANGE = "#d97757"
CARD = "#e8e6dc"
IVORY = "#faf9f5"
FONT = "Noto Sans JP, Noto Sans CJK JP, Hiragino Sans, Meiryo, sans-serif"

BOX_X, BOX_W, BOX_H, GAP, TOP = 20, 380, 64, 28, 20
# (id, 1 行目, 2 行目, 種類)。種類: input は人の入力、agent は作る役、review は評価する役
STEPS = [
    ("topic", "お題を入力", "例：もし AI が進歩したら？", "input"),
    ("writer", "作家エージェント", "台本を作成", "agent"),
    ("japanese", "日本語エージェント", "台本を評価", "review"),
    ("producer", "制作エージェント", "動画を作成", "agent"),
    ("director", "監督エージェント", "動画を評価", "review"),
    ("poster", "投稿エージェント", "動画を投稿", "agent"),
]
# 差し戻し（評価の段 → 1 つ前の段）
RETURNS = [("japanese", "writer"), ("director", "producer")]
W = 600
H = TOP * 2 + len(STEPS) * BOX_H + (len(STEPS) - 1) * GAP
STYLE = {
    "input": (CARD, INK),
    "agent": (IVORY, ORANGE),
    "review": ("#f6e3dc", ORANGE),
}


def box_y(i: int) -> int:
    return TOP + i * (BOX_H + GAP)


def mxfile() -> str:
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
    for i, (cid, l1, l2, kind) in enumerate(STEPS):
        fill, stroke = STYLE[kind]
        value = escape(f"<b>{l1}</b><br/>{l2}")
        cells.append(
            f'<mxCell id="{cid}" value="{value}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};'
            f'strokeColor={stroke};strokeWidth=2;fontSize=16;arcSize=14;" vertex="1" parent="1">'
            f'<mxGeometry x="{BOX_X}" y="{box_y(i)}" width="{BOX_W}" height="{BOX_H}" as="geometry"/></mxCell>'
        )
    for (a, _, _, _), (b, _, _, _) in zip(STEPS, STEPS[1:]):
        cells.append(
            f'<mxCell id="e-{a}-{b}" style="endArrow=block;endFill=1;html=1;strokeColor={INK};strokeWidth=2;" '
            f'edge="1" parent="1" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )
    for a, b in RETURNS:
        cells.append(
            f'<mxCell id="r-{a}-{b}" value="差し戻し" style="endArrow=block;endFill=1;html=1;strokeColor={ORANGE};'
            f"strokeWidth=2;dashed=1;fontSize=15;fontColor={ORANGE};labelBackgroundColor={IVORY};"
            f'edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.5;entryX=1;entryY=0.5;" edge="1" parent="1" '
            f'source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )
    model = "".join(cells)
    return (
        f'<mxfile host="drawio"><diagram name="short-video-flow" id="d0">'
        f'<mxGraphModel dx="{W}" dy="{H}" grid="1" gridSize="10" page="0"><root>{model}</root></mxGraphModel>'
        f"</diagram></mxfile>"
    )


def svg() -> str:
    idx = {cid: i for i, (cid, *_) in enumerate(STEPS)}
    parts = []
    for i, (cid, l1, l2, kind) in enumerate(STEPS):
        fill, stroke = STYLE[kind]
        y = box_y(i)
        cx = BOX_X + BOX_W / 2
        parts.append(
            f'<rect x="{BOX_X}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="10" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="2"/>'
            f'<text x="{cx}" y="{y + 25}" text-anchor="middle" dominant-baseline="central" font-size="19" '
            f'font-weight="bold">{escape(l1)}</text>'
            f'<text x="{cx}" y="{y + 46}" text-anchor="middle" dominant-baseline="central" font-size="16">'
            f"{escape(l2)}</text>"
        )
    # ↓ でつなぐ
    for i in range(len(STEPS) - 1):
        x = BOX_X + BOX_W / 2
        y0, y1 = box_y(i) + BOX_H, box_y(i + 1)
        parts.append(
            f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1 - 9}" stroke="{INK}" stroke-width="2"/>'
            f'<polygon points="{x},{y1} {x - 6},{y1 - 10} {x + 6},{y1 - 10}" fill="{INK}"/>'
        )
    # 差し戻し: 評価の段の右から出て、1 つ前の段の右に入る
    right = BOX_X + BOX_W
    for a, b in RETURNS:
        ya = box_y(idx[a]) + BOX_H / 2
        yb = box_y(idx[b]) + BOX_H / 2
        xo = right + 40
        parts.append(
            f'<polyline points="{right},{ya} {xo},{ya} {xo},{yb} {right + 9},{yb}" fill="none" '
            f'stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6 4"/>'
            f'<polygon points="{right},{yb} {right + 10},{yb - 6} {right + 10},{yb + 6}" fill="{ORANGE}"/>'
            f'<text x="{xo + 10}" y="{(ya + yb) / 2}" dominant-baseline="central" font-size="17" '
            f'font-weight="bold" fill="{ORANGE}">差し戻し</text>'
        )
    body = "".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="{FONT}" fill="{INK}" content="{escape(mxfile())}">{body}</svg>\n'
    )


if __name__ == "__main__":
    OUT.write_text(svg(), encoding="utf-8")
    print(OUT)
