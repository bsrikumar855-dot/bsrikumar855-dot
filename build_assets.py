"""Generate the animated profile SVGs in GitHub's light and dark palettes."""
import math
import random
from xml.sax.saxutils import escape

# GitHub Primer palettes
DARK = dict(
    name="dark",
    bg="#0d1117",          # canvas.default
    grid="#161b22",        # canvas.subtle
    border="#30363d",      # border.default
    text="#e6edf3",        # fg.default
    muted="#7d8590",       # fg.muted
    accent="#58a6ff",      # accent.fg
    levels=["#0e4429", "#006d32", "#26a641", "#39d353"],
)
LIGHT = dict(
    name="light",
    bg="#ffffff",
    grid="#f6f8fa",
    border="#d0d7de",
    text="#1f2328",
    muted="#59636e",
    accent="#0969da",
    levels=["#9be9a8", "#40c463", "#30a14e", "#216e39"],
)

PHRASES = [
    "agents that read, decide and act",
    "grading that can explain itself",
    "compliance that never stops watching",
    "build. ship. learn. repeat.",
]
CHIPS = ["Python", "FastAPI", "React", "OpenCV", "LangChain", "Docker"]

CH, TX, TY = 9.6, 46, 176
PROMPT_W = 2 * CH
SLOT, TYPE_DUR, HOLD_END = 5.0, 2.2, 4.5
CYCLE = SLOT * len(PHRASES)


def frame(p, W, H, pal):
    """Background, grid and corner brackets."""
    p.append(f'<rect width="{W}" height="{H}" rx="6" fill="{pal["bg"]}"/>')
    for x in range(0, W, 40):
        p.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{pal["grid"]}" stroke-width="1"/>')
    for y in range(0, H, 40):
        p.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{pal["grid"]}" stroke-width="1"/>')
    for cx, cy, sx, sy in [(22, 22, 1, 1), (W - 22, 22, -1, 1), (22, H - 22, 1, -1), (W - 22, H - 22, -1, -1)]:
        p.append(f'<path d="M{cx} {cy + 18 * sy} L{cx} {cy} L{cx + 18 * sx} {cy}" '
                 f'stroke="{pal["accent"]}" stroke-width="1.5" fill="none" opacity=".8"/>')


def banner(pal):
    random.seed(7)  # stable across both themes
    W, H = 1000, 285
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Shreekumar B, AI builder">']
    frame(p, W, H, pal)

    # activity matrix, coloured with the contribution-graph scale
    cell, gap, x0, y0, cols, rows = 12, 4, 640, 40, 21, 8
    mw = cols * (cell + gap)
    for r in range(rows):
        for c in range(cols):
            if c > r + 13:
                continue
            x, y = x0 + c * (cell + gap), y0 + r * (cell + gap)
            lvl = random.randrange(len(pal["levels"]))
            nxt = min(lvl + 1, len(pal["levels"]) - 1)
            beg = (r * 0.11 + c * 0.05) % 4.0
            p.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{pal["levels"][lvl]}">'
                     f'<animate attributeName="fill" values="{pal["levels"][lvl]};{pal["levels"][nxt]};{pal["levels"][lvl]}" '
                     f'dur="4s" begin="{beg:.2f}s" repeatCount="indefinite"/></rect>')
    p.append(f'<rect y="{y0 - 4}" width="26" height="{rows * (cell + gap)}" fill="{pal["accent"]}" opacity=".14">'
             f'<animate attributeName="x" values="{x0 - 30};{x0 + mw}" dur="3.6s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;.16;.16;0" dur="3.6s" repeatCount="indefinite"/></rect>')

    p.append(f'<text x="46" y="86" font-family="Georgia,\'Times New Roman\',serif" font-size="46" '
             f'font-weight="700" fill="{pal["text"]}">Shreekumar B</text>')
    p.append(f'<rect x="46" y="100" width="0" height="2" fill="{pal["accent"]}">'
             f'<animate attributeName="width" values="0;250" dur=".9s" fill="freeze"/></rect>')
    p.append(f'<circle cx="52" cy="128" r="4" fill="{pal["levels"][-1]}">'
             f'<animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>')
    p.append(f'<text x="64" y="132" font-family="ui-monospace,Consolas,monospace" font-size="11.5" '
             f'letter-spacing="1.6" fill="{pal["muted"]}">AI BUILDER  ·  AI &amp; DATA SCIENCE  ·  INDIA</text>')

    for i, phrase in enumerate(PHRASES):
        n = len(phrase)
        s = i * SLOT / CYCLE
        he = (i * SLOT + HOLD_END) / CYCLE
        if i == 0:
            ov, ok = ["1", "0", "0"], ["0", f"{he:.4f}", "1"]
        else:
            ov, ok = ["0", "1", "0", "0"], ["0", f"{s:.4f}", f"{he:.4f}", "1"]
        kt, vv = ["0", f"{s:.4f}"], ["0", f"{PROMPT_W:.1f}"]
        for j in range(1, n + 1):
            kt.append(f"{s + (j / n) * (TYPE_DUR / CYCLE):.4f}")
            vv.append(f"{PROMPT_W + j * CH:.1f}")
        kt.append("1")
        vv.append(f"{PROMPT_W + n * CH:.1f}")

        p.append(f'<clipPath id="tw{i}"><rect x="{TX}" y="{TY - 18}" width="0" height="26">'
                 f'<animate attributeName="width" values="{";".join(vv)}" keyTimes="{";".join(kt)}" '
                 f'calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/></rect></clipPath>')
        p.append(f'<g><animate attributeName="opacity" values="{";".join(ov)}" keyTimes="{";".join(ok)}" '
                 f'calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/>')
        p.append(f'<g clip-path="url(#tw{i})" font-family="ui-monospace,Consolas,monospace" font-size="16">'
                 f'<text x="{TX}" y="{TY}" fill="{pal["accent"]}">$ </text>'
                 f'<text x="{TX + PROMPT_W:.1f}" y="{TY}" fill="{pal["muted"]}">{escape(phrase)}</text></g>')
        p.append(f'<rect y="{TY - 14}" width="9" height="18" fill="{pal["accent"]}" x="{TX + PROMPT_W:.1f}">'
                 f'<animate attributeName="x" values="{";".join(str(TX + float(v)) for v in vv)}" '
                 f'keyTimes="{";".join(kt)}" calcMode="discrete" dur="{CYCLE}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="1;1;0;1" dur="1s" repeatCount="indefinite"/></rect>')
        p.append('</g>')

    cx = 46
    for i, c in enumerate(CHIPS):
        w = len(c) * 7.3 + 20
        p.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur=".5s" '
                 f'begin="{1.0 + i * 0.14:.2f}s" fill="freeze"/>'
                 f'<rect x="{cx}" y="{TY + 26}" width="{w:.0f}" height="23" rx="11.5" fill="none" '
                 f'stroke="{pal["border"]}" stroke-width="1"/>'
                 f'<text x="{cx + w / 2:.0f}" y="{TY + 41}" text-anchor="middle" '
                 f'font-family="ui-monospace,Consolas,monospace" font-size="10.5" '
                 f'fill="{pal["muted"]}">{escape(c)}</text></g>')
        cx += w + 9

    p.append('</svg>')
    return "\n".join(p)


def capabilities(pal):
    """Radial capability map."""
    W, H, CX, CY = 1000, 380, 500, 186
    RX, RY = 332, 124
    NODE_R, GAP = 6, 20
    domains = [
        ("AI Agents",       "routing · tool use · RAG"),
        ("LLM Engineering", "OpenAI · Gemini · LangChain"),
        ("Backend & APIs",  "FastAPI · Node · SQL"),
        ("Computer Vision", "OpenCV · OCR · detection"),
        ("Full Stack",      "React · TypeScript"),
        ("Automation",      "GitHub Actions · Python"),
    ]
    n = len(domains)
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Capability map: AI agents, LLM engineering, backend and APIs, '
         f'computer vision, full stack, automation">']
    frame(p, W, H, pal)

    nodes = []
    for i, (name, sub) in enumerate(domains):
        a = -math.pi / 2 + i * (2 * math.pi / n)
        x, y = CX + RX * math.cos(a), CY + RY * math.sin(a)
        nodes.append((x, y, a, name, sub))
        d = math.hypot(x - CX, y - CY)
        ex, ey = CX + (x - CX) * (d - GAP) / d, CY + (y - CY) * (d - GAP) / d
        p.append(f'<line x1="{CX}" y1="{CY}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{pal["accent"]}" '
                 f'stroke-width="1" opacity=".42" stroke-dasharray="5 6">'
                 f'<animate attributeName="stroke-dashoffset" values="22;0" dur="1.6s" '
                 f'begin="{i * 0.22:.2f}s" repeatCount="indefinite"/></line>')

    p.append(f'<circle cx="{CX}" cy="{CY}" r="40" fill="{pal["bg"]}" stroke="{pal["accent"]}" stroke-width="1.4"/>')
    p.append(f'<circle cx="{CX}" cy="{CY}" r="40" fill="none" stroke="{pal["accent"]}" stroke-width="1">'
             f'<animate attributeName="r" values="40;64" dur="3.2s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values=".55;0" dur="3.2s" repeatCount="indefinite"/></circle>')
    p.append(f'<text x="{CX}" y="{CY - 2}" text-anchor="middle" font-family="Georgia,serif" font-size="17" '
             f'font-weight="700" fill="{pal["text"]}">build</text>')
    p.append(f'<text x="{CX}" y="{CY + 15}" text-anchor="middle" font-family="ui-monospace,monospace" '
             f'font-size="8" letter-spacing="1.6" fill="{pal["muted"]}">THEN VERIFY</text>')

    for i, (x, y, a, name, sub) in enumerate(nodes):
        col = pal["levels"][-1]
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{NODE_R}" fill="{col}">'
                 f'<animate attributeName="r" values="{NODE_R};{NODE_R + 2.5};{NODE_R}" dur="2.8s" '
                 f'begin="{i * 0.35:.2f}s" repeatCount="indefinite"/></circle>')
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{NODE_R}" fill="none" stroke="{col}" stroke-width="1">'
                 f'<animate attributeName="r" values="{NODE_R};18" dur="2.8s" begin="{i * 0.35:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values=".7;0" dur="2.8s" begin="{i * 0.35:.2f}s" '
                 f'repeatCount="indefinite"/></circle>')

        c = math.cos(a)
        if abs(c) < 0.3:
            anchor, lx = "middle", x
            ly = y - 24 if y < CY else y + 32
        elif c > 0:
            anchor, lx, ly = "start", x + 16, y + 4
        else:
            anchor, lx, ly = "end", x - 16, y + 4
        p.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-family="Georgia,serif" '
                 f'font-size="15" font-weight="600" fill="{pal["text"]}">{escape(name)}</text>')
        p.append(f'<text x="{lx:.1f}" y="{ly + 15:.1f}" text-anchor="{anchor}" '
                 f'font-family="ui-monospace,monospace" font-size="9" fill="{pal["muted"]}">{escape(sub)}</text>')

    p.append('</svg>')
    return "\n".join(p)


def pipeline(pal):
    """How a graded script actually flows: extract -> ground -> reason -> validate."""
    W, H = 1000, 300
    MID = 146
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Pipeline: answer sheet, extraction, rubric, reasoning, evidence, '
         f'confidence, validator, released mark, with a repair loop">']
    frame(p, W, H, pal)

    lanes = [("Rubric", 56), ("Reasoning", 108), ("Evidence", 160), ("Confidence", 212)]
    EX_X, EX_W, EX_H = 366, 120, 36

    def box(x, y, w, h, title, sub=None, strong=False):
        stroke = pal["accent"] if strong else pal["border"]
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{pal["bg"]}" '
                 f'stroke="{stroke}" stroke-width="1.2"/>')
        ty = y + h / 2 + (0 if sub else 4)
        p.append(f'<text x="{x + w/2}" y="{ty:.0f}" text-anchor="middle" font-family="Georgia,serif" '
                 f'font-size="13.5" font-weight="600" fill="{pal["text"]}">{escape(title)}</text>')
        if sub:
            p.append(f'<text x="{x + w/2}" y="{ty + 13:.0f}" text-anchor="middle" '
                     f'font-family="ui-monospace,monospace" font-size="8" '
                     f'fill="{pal["muted"]}">{escape(sub)}</text>')

    # connectors, drawn first so boxes sit on top
    for i, (_, ey) in enumerate(lanes):
        d = f"M316,{MID} L{EX_X},{ey} M{EX_X+EX_W},{ey} L556,{MID}"
        p.append(f'<path d="{d}" fill="none" stroke="{pal["accent"]}" stroke-width="1" opacity=".35" '
                 f'stroke-dasharray="4 5">'
                 f'<animate attributeName="stroke-dashoffset" values="18;0" dur="1.4s" '
                 f'begin="{i*0.18:.2f}s" repeatCount="indefinite"/></path>')
    for x1, x2 in ((146, 186), (686, 746)):
        p.append(f'<path d="M{x1},{MID} L{x2},{MID}" stroke="{pal["accent"]}" stroke-width="1" '
                 f'opacity=".45" stroke-dasharray="4 5">'
                 f'<animate attributeName="stroke-dashoffset" values="18;0" dur="1.4s" repeatCount="indefinite"/></path>')

    # repair loop: validator drops back to the reasoning lane
    LOOP_Y = 258
    loop = (f"M621,{MID+24} L621,{LOOP_Y} L340,{LOOP_Y} "
            f"L340,{lanes[1][1]} L{EX_X},{lanes[1][1]}")
    p.append(f'<path d="{loop}" fill="none" stroke="{pal["levels"][-1]}" stroke-width="1" opacity=".5" '
             f'stroke-dasharray="4 5">'
             f'<animate attributeName="stroke-dashoffset" values="0;18" dur="1.4s" repeatCount="indefinite"/></path>')
    p.append(f'<circle r="3.5" fill="{pal["levels"][-1]}" opacity="0">'
             f'<animateMotion path="{loop}" dur="2.6s" begin="1.2s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" '
             f'dur="2.6s" begin="1.2s" repeatCount="indefinite"/></circle>')
    p.append(f'<text x="500" y="{LOOP_Y - 8}" text-anchor="middle" font-family="ui-monospace,monospace" '
             f'font-size="8.5" letter-spacing="1.1" fill="{pal["muted"]}">'
             f'CAN&#8217;T JUSTIFY IT  &#8594;  REPAIR  &#8594;  RE-RUN</text>')

    box(36, MID-22, 110, 44, "Script", "SCANNED")
    box(186, MID-24, 130, 48, "Extract", "VISION + OCR", strong=True)
    for name, ey in lanes:
        box(EX_X, ey - EX_H/2, EX_W, EX_H, name)
    box(556, MID-24, 130, 48, "Validate", "AGAINST RUBRIC", strong=True)
    box(746, MID-22, 120, 44, "Mark", "EXPLAINED")

    # packets travelling the full route, one per lane, staggered
    CYC = 4.0
    for i, (_, ey) in enumerate(lanes):
        route = (f"M146,{MID} L316,{MID} L{EX_X},{ey} L{EX_X+EX_W},{ey} "
                 f"L556,{MID} L746,{MID}")
        p.append(f'<circle r="4" fill="{pal["levels"][-1]}" opacity="0">'
                 f'<animateMotion path="{route}" dur="{CYC}s" begin="{i*0.5:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.06;0.94;1" '
                 f'dur="{CYC}s" begin="{i*0.5:.2f}s" repeatCount="indefinite"/></circle>')

    p.append(f'<text x="{W/2}" y="{H-14}" text-anchor="middle" font-family="ui-monospace,monospace" '
             f'font-size="9" letter-spacing="1.5" fill="{pal["muted"]}">'
             f'EXTRACT  ·  GROUND  ·  REASON  ·  VALIDATE  ·  RELEASE</text>')
    p.append('</svg>')
    return "\n".join(p)


if __name__ == "__main__":
    for pal in (DARK, LIGHT):
        for stem, fn in (("banner", banner), ("capabilities", capabilities), ("pipeline", pipeline)):
            path = f"{stem}-{pal['name']}.svg"
            open(path, "w", encoding="utf-8").write(fn(pal))
            print("wrote", path)
