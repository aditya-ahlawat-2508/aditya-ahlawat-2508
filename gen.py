import math, random, heapq, os

OUT = "assets"
os.makedirs(OUT, exist_ok=True)

NAVY = "#0F1E33"
ROAD = "#22385A"
ROAD2 = "#2E4A73"
TEXT = "#F2F5F9"
MUTED = "#8FA3BF"
SAFFRON = "#FFB020"
CYAN = "#3FD0C9"
PINK = "#F0648C"
WHITE = "#FFFFFF"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ------------------------------------------------------------------
# HERO: a street graph where three friends' shortest paths converge
# ------------------------------------------------------------------
def hero():
    random.seed(11)
    Wd, Ht = 1200, 420
    cols, rows = 17, 8
    x0, y0, dx, dy = 470, 30, 44, 50
    nodes = {}
    for c in range(cols):
        for r in range(rows):
            nodes[(c, r)] = (x0 + c * dx + random.uniform(-12, 12), y0 + r * dy + random.uniform(-10, 10))
    edges = set()
    for (c, r) in nodes:
        for dc, dr in [(1, 0), (0, 1)]:
            n2 = (c + dc, r + dr)
            if n2 in nodes and random.random() > 0.14:
                edges.add(((c, r), n2))
        if (c + 1, r + 1) in nodes and random.random() < 0.12:
            edges.add(((c, r), (c + 1, r + 1)))
    adj = {n: [] for n in nodes}
    for a, b in edges:
        w = math.dist(nodes[a], nodes[b]) * random.uniform(0.9, 1.25)
        adj[a].append((b, w)); adj[b].append((a, w))

    def dijkstra(src):
        dist = {src: 0}; prev = {}
        pq = [(0, src)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                if d + w < dist.get(v, 1e18):
                    dist[v] = d + w; prev[v] = u; heapq.heappush(pq, (d + w, v))
        return dist, prev

    origins = [(4, 1), (15, 0), (13, 7)]
    runs = [dijkstra(o) for o in origins]
    best = min(nodes, key=lambda n: max(r[0].get(n, 1e18) for r in runs))
    paths = []
    for (dist, prev), o in zip(runs, origins):
        p = [best]
        while p[-1] != o:
            p.append(prev[p[-1]])
        paths.append(list(reversed(p)))

    road_d = " ".join(f"M{nodes[a][0]:.1f},{nodes[a][1]:.1f}L{nodes[b][0]:.1f},{nodes[b][1]:.1f}" for a, b in edges)
    cols_ = [SAFFRON, CYAN, PINK]
    route_svg = []
    for i, (p, col) in enumerate(zip(paths, cols_)):
        pts = [nodes[n] for n in p]
        L = sum(math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1))
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        route_svg.append(
            f'<path class="route r{i}" d="{d}" stroke="{col}" style="--len:{L:.0f};stroke-dasharray:{L:.0f};stroke-dashoffset:{L:.0f}"/>')
        ox, oy = pts[0]
        route_svg.append(f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="6" fill="{col}"/>'
                         f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="11" fill="none" stroke="{col}" stroke-opacity=".45"/>')
    mx, my = nodes[best]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {Ht}" width="{Wd}" height="{Ht}" role="img" aria-label="Aditya Ahlawat. Three shortest paths across a city street graph converge on one fair meeting point.">
<title>Aditya Ahlawat</title>
<style>
  .route {{ fill:none; stroke-width:3.2; stroke-linecap:round; stroke-linejoin:round; animation: draw 8s ease-in-out infinite; }}
  .r1 {{ animation-delay:.25s }} .r2 {{ animation-delay:.5s }}
  .meet {{ opacity:0; animation: meet 8s ease-in-out infinite; }}
  @keyframes draw {{ 0%{{stroke-dashoffset:var(--len)}} 38%{{stroke-dashoffset:0}} 86%{{stroke-dashoffset:0;opacity:1}} 100%{{stroke-dashoffset:0;opacity:0}} }}
  @keyframes meet {{ 0%,40%{{opacity:0}} 48%,86%{{opacity:1}} 100%{{opacity:0}} }}
  @media (prefers-reduced-motion: reduce) {{ .route{{animation:none;stroke-dashoffset:0}} .meet{{animation:none;opacity:1}} }}
</style>
<defs>
  <linearGradient id="fade" x1="0" x2="1">
    <stop offset="0" stop-color="{NAVY}" stop-opacity="1"/>
    <stop offset=".42" stop-color="{NAVY}" stop-opacity="1"/>
    <stop offset=".62" stop-color="{NAVY}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="{Wd}" height="{Ht}" rx="14" fill="{NAVY}"/>
<path d="{road_d}" stroke="{ROAD}" stroke-width="1.6" fill="none" stroke-linecap="round"/>
{''.join(route_svg)}
<g class="meet">
  <circle cx="{mx:.1f}" cy="{my:.1f}" r="9" fill="{WHITE}"/>
  <circle cx="{mx:.1f}" cy="{my:.1f}" r="9" fill="none" stroke="{WHITE}" stroke-width="2">
    <animate attributeName="r" values="9;30" dur="1.6s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values=".9;0" dur="1.6s" repeatCount="indefinite"/>
  </circle>
  <rect x="{mx + 16:.1f}" y="{my - 30:.1f}" width="178" height="24" rx="5" fill="{NAVY}" stroke="{ROAD2}"/>
  <text x="{mx + 26:.1f}" y="{my - 13.5:.1f}" font-family="{MONO}" font-size="12.5" fill="{TEXT}">worst commute minimised</text>
</g>
<rect width="{Wd}" height="{Ht}" rx="14" fill="url(#fade)" pointer-events="none"/>
<text x="56" y="168" font-family="{SANS}" font-size="64" font-weight="800" fill="{TEXT}" letter-spacing="-1.5">Aditya Ahlawat</text>
<text x="58" y="214" font-family="{SANS}" font-size="22" fill="{TEXT}">I build AI agents that have to be right,</text>
<text x="58" y="244" font-family="{SANS}" font-size="22" fill="{TEXT}">and the graph engines underneath them.</text>
<text x="58" y="296" font-family="{SANS}" font-size="15" fill="{MUTED}">B.Tech Information Technology, Delhi Technological University, class of 2027</text>
<g font-family="{SANS}" font-size="13" fill="{MUTED}">
  <circle cx="64" cy="352" r="5" fill="{SAFFRON}"/><circle cx="80" cy="352" r="5" fill="{CYAN}"/><circle cx="96" cy="352" r="5" fill="{PINK}"/>
  <text x="112" y="356.5">Three friends, one city. Where should they meet?</text>
</g>
</svg>'''
    open(f"{OUT}/hero.svg", "w").write(svg)


# ------------------------------------------------------------------
# PROJECT CARDS
# ------------------------------------------------------------------
def wrap(text, width_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width_chars:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines


def glyph_graph(col):
    return f'''<g stroke="{ROAD2}" stroke-width="1.4" fill="none">
<path d="M20,30 L60,22 L100,34 L126,20 M20,30 L28,70 L62,62 L100,74 L128,66 M60,22 L62,62 L66,104 M100,34 L100,74 L96,112 M28,70 L24,110 L66,104 L96,112 L130,106 M126,20 L128,66 L130,106"/></g>
<path d="M20,30 L28,70 L62,62" stroke="{SAFFRON}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
<path d="M126,20 L100,34 L100,74 L62,62" stroke="{CYAN}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
<path d="M96,112 L66,104 L62,62" stroke="{PINK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
<circle cx="62" cy="62" r="6" fill="#fff"/>'''


def glyph_agents(col):
    n = [(20, 66, "in"), (58, 30, "✈"), (58, 66, "▣"), (58, 102, "☀"), (100, 66, "▤"), (134, 66, "✓")]
    s = f'<g stroke="{ROAD2}" stroke-width="1.6" fill="none">'
    for a, b in [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4), (4, 5)]:
        s += f'<path d="M{n[a][0]},{n[a][1]} L{n[b][0]},{n[b][1]}"/>'
    s += "</g>"
    for i, (x, y, _) in enumerate(n):
        c = col if i in (4, 5) else ("#fff" if i == 0 else ROAD2)
        s += f'<circle cx="{x}" cy="{y}" r="{9 if i else 6}" fill="{c}"/>'
    return s


def glyph_bars(col):
    hs = [80, 88, 72, 94, 60, 44, 36]
    s = ""
    for i, h in enumerate(hs):
        c = col if i >= 4 else ROAD2
        s += f'<rect x="{16 + i * 17}" y="{118 - h}" width="11" height="{h}" rx="2" fill="{c}"/>'
    s += f'<path d="M84,20 L138,56" stroke="#fff" stroke-width="2" fill="none" stroke-dasharray="4 4"/><path d="M138,56 l-10,-1 l5,-8z" fill="#fff"/>'
    return s


def glyph_funnel(col):
    s = ""
    random.seed(4)
    for i in range(14):
        x, y = 18 + (i % 7) * 18, 22 + (i // 7) * 16
        s += f'<rect x="{x}" y="{y}" width="12" height="10" rx="2" fill="{ROAD2}"/>'
    s += f'<path d="M14,58 L140,58 L96,86 L58,86 Z" fill="none" stroke="{ROAD2}" stroke-width="1.6"/>'
    for i in range(3):
        s += f'<rect x="{56 + i * 16}" y="96" width="12" height="10" rx="2" fill="{col}"/>'
    s += f'<rect x="72" y="114" width="12" height="10" rx="2" fill="#fff"/>'
    return s


CARDS = [
    ("meeting-point", "Fair Meeting-Point Finder", "In progress", SAFFRON, glyph_graph,
     "One-to-many Dijkstra over Delhi's OSM road graph, compares who's fair to everyone against who's simply fastest to reach.",
     "1.6 ms per source on a 32k-node OSM road graph",
     "C++20 / libosmium / pybind11 / FastAPI / MapLibre"),
    ("tripmate", "TripMate AI", "Becoming a SaaS", CYAN, glyph_agents,
     "Five LangGraph agents share one Postgres-checkpointed state. I adversarially tested it and it was inventing flight prices with total confidence, fixing that before this is real.",
     "MCP tool layer for flights, hotels and weather",
     "LangGraph / MCP / FastAPI / Groq / PostgreSQL"),
    ("cost-optimizer", "AWS Cost Optimizer", "Becoming a SaaS", PINK, glyph_bars,
     "Real Cost Explorer billing plus live EC2, RDS and S3 inventory. An LLM advisor turns that into resource-level savings instead of generic right-sizing advice.",
     "Serverless backend provisioned end to end with Terraform",
     "Terraform / Lambda / boto3 / LangGraph / GPT-4o"),
    ("rag", "FEAT RAG Chatbot", "Shipped", "#8B9CFF", glyph_funnel,
     "Hybrid retrieval plus cross-encoder reranking, with an LLM-as-judge step that checks each answer against retrieved context before it ships.",
     "BM25 + ChromaDB retrieval with groundedness scoring",
     "LangChain / ChromaDB / BM25 / cross-encoders"),
]


def card(slug, title, status, col, glyph, desc, proof, stack):
    Wd, Ht = 600, 250
    lines = wrap(desc, 50)
    desc_svg = "".join(f'<text x="196" y="{96 + i * 21}" font-family="{SANS}" font-size="14.5" fill="{TEXT}">{esc(l)}</text>' for i, l in enumerate(lines))
    y_proof = 96 + len(lines) * 21 + 10
    pw = len(status) * 7.4 + 22
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {Ht}" width="{Wd}" height="{Ht}" role="img" aria-label="{esc(title)}: {esc(desc)}">
<title>{esc(title)}</title>
<defs><clipPath id="c-{slug}"><rect width="{Wd}" height="{Ht}" rx="12"/></clipPath></defs>
<g clip-path="url(#c-{slug})"><rect width="{Wd}" height="{Ht}" fill="{NAVY}"/><rect x="0" y="0" width="6" height="{Ht}" fill="{col}"/></g>
<g transform="translate(24,34)">{glyph(col)}</g>
<text x="196" y="56" font-family="{SANS}" font-size="23" font-weight="700" fill="{TEXT}">{esc(title)}</text>
<rect x="{100 - pw / 2}" y="{Ht - 42}" width="{pw}" height="24" rx="12" fill="none" stroke="{col}"/>
<text x="100" y="{Ht - 25.5}" font-family="{SANS}" font-size="12" fill="{col}" text-anchor="middle">{esc(status)}</text>
{desc_svg}
<text x="196" y="{y_proof}" font-family="{SANS}" font-size="13" fill="{col}">{esc(proof)}</text>
<line x1="196" y1="{Ht - 44}" x2="{Wd - 20}" y2="{Ht - 44}" stroke="{ROAD}"/>
<text x="196" y="{Ht - 20}" font-family="{MONO}" font-size="12.5" fill="{MUTED}">{esc(stack)}</text>
</svg>'''
    open(f"{OUT}/card-{slug}.svg", "w").write(svg)


# ------------------------------------------------------------------
# ROUTE SO FAR: credentials as stations on one transit line
# ------------------------------------------------------------------
def route():
    Wd, Ht = 1200, 200
    stations = [
        ("JEE Main", "99.31 percentile, 1.1M+ candidates", SAFFRON),
        ("JEE Advanced", "All India Rank 8947", SAFFRON),
        ("Samsung Solve for Tomorrow", "Top 40 of 20,000+ teams, pitched at IIT Delhi", CYAN),
        ("Research paper", "Co-author, SCCTT-2025 (CEUR)", CYAN),
        ("AI Developer Intern, FEAT", "RAG chatbot + attendance system", PINK),
        ("LeetCode Knight", "Rating 1862, 650+ problems", PINK),
    ]
    x0, x1, y = 130, 960, 100
    step = (x1 - x0) / (len(stations) - 1)
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {Ht}" width="{Wd}" height="{Ht}" role="img" aria-label="Milestones: JEE Main 99.31 percentile; JEE Advanced AIR 8947; Samsung Solve for Tomorrow top 40 of 20,000+ teams; SCCTT-2025 paper; AI Developer Intern at FEAT; LeetCode Knight 1862 with 650+ problems; open to 2027 SDE and AI/ML roles.">
<title>The route so far</title>
<rect width="{Wd}" height="{Ht}" rx="14" fill="{NAVY}"/>
<defs><linearGradient id="line" x1="0" x2="1"><stop offset="0" stop-color="{SAFFRON}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/></linearGradient></defs>
<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="url(#line)" stroke-width="8" stroke-linecap="round"/>
<line x1="{x1}" y1="{y}" x2="1090" y2="{y}" stroke="{PINK}" stroke-width="8" stroke-dasharray="2 14" stroke-linecap="round"/>
'''
    for i, (name, sub, col) in enumerate(stations):
        x = x0 + i * step
        up = i % 2 == 0
        ty = y - 52 if up else y + 48
        s += f'<circle cx="{x:.1f}" cy="{y}" r="11" fill="{NAVY}" stroke="{col}" stroke-width="5"/>'
        s += f'<line x1="{x:.1f}" y1="{y + (-14 if up else 14)}" x2="{x:.1f}" y2="{y + (-30 if up else 28)}" stroke="{ROAD2}" stroke-width="1.5"/>'
        s += f'<text x="{x:.1f}" y="{ty}" font-family="{SANS}" font-size="15" font-weight="700" fill="{TEXT}" text-anchor="middle">{esc(name)}</text>'
        s += f'<text x="{x:.1f}" y="{ty + 19}" font-family="{SANS}" font-size="12.5" fill="{MUTED}" text-anchor="middle">{esc(sub)}</text>'
    s += f'''<circle cx="1100" cy="{y}" r="15" fill="#fff"><animate attributeName="r" values="13;16;13" dur="2.4s" repeatCount="indefinite"/></circle>
<text x="1100" y="{y - 52}" font-family="{SANS}" font-size="15" font-weight="700" fill="{TEXT}" text-anchor="middle">Next stop</text>
<text x="1100" y="{y - 33}" font-family="{SANS}" font-size="12.5" fill="{MUTED}" text-anchor="middle">SDE / AI-ML, 2027</text>
</svg>'''
    open(f"{OUT}/route-so-far.svg", "w").write(s)




hero()
for c in CARDS:
    card(*c)
route()
print(sorted(os.listdir(OUT)))