import numpy as np

# Configurações do Canvas e Posição do Retrato
CANVAS_W, CANVAS_H = 1180, 610
OFFSET_X, OFFSET_Y = 86, 150

# Cores por tema
THEMES = {
    "dark": {
        "bg": "#0A101F",
        "chrome": "#22D3EE",
        "accent": "#A78BFA",
        "accent2": "#7C3AED",
        "text_sub": "#94A3B8",
        "text_main": "#F8FAFC",
        "dot_color": "#A78BFA",
        "file_out": "dark.svg",
        "gid": "accent_dark",
    },
    "light": {
        "bg": "#F8FAFC",
        "chrome": "#0891B2",
        "accent": "#7C3AED",
        "accent2": "#059669",
        "text_sub": "#475569",
        "text_main": "#0F172A",
        "dot_color": "#7C3AED",
        "file_out": "light.svg",
        "gid": "accent_light",
    },
}

# Dados do Painel SYSTEM.INFO
INFO_ROWS = [
    ("Subject", "Gabriel Guadalup"),
    ("Role", "Estudante de IA & Dev"),
    ("Origin", "Macapa, Amapa, Brasil"),
    ("Education", "Bacharelado em IA (IFAP)"),
    ("Status", "Building & Learning"),
    ("ToolChain", "VS Code, Git, Python, GitHub"),
    ("Core.Lang", "Python, JavaScript, TypeScript"),
    ("Core.Frontend", "HTML5, CSS3, JavaScript"),
    ("Core.Backend", "Python Scripts & APIs"),
    ("Core.AI", "NumPy, Pandas, Scikit-Learn"),
    ("Grid.Mail", "gabrielguadalup.dev@gmail.com"),
    ("Grid.LinkedIn", "gabriel-guadalup-78351329a"),
    ("Grid.GitHub", "@GabrielGuadalup1"),
]


def gerar_pontos_terminal(N):
    """Gera N pontos formando o símbolo do Terminal '>_'."""
    cx, cy = OFFSET_X + 150, OFFSET_Y + 170
    pts = []

    n1 = N // 3
    # Topo do '>'
    for t in np.linspace(0, 1, n1):
        pts.append([(cx - 70) + t * 50, (cy - 60) + t * 50])
    # Baixo do '>'
    for t in np.linspace(0, 1, n1):
        pts.append([(cx - 20) - t * 50, (cy - 10) + t * 50])
    # Traço '_'
    n3 = N - 2 * n1
    for t in np.linspace(0, 1, n3):
        pts.append([cx + 10 + t * 55, cy + 40])

    return np.array(pts)


def gerar_pontos_codigo(N):
    """Gera N pontos formando a tag de código '</>'."""
    cx, cy = OFFSET_X + 150, OFFSET_Y + 170
    pts = []

    n_seg = N // 5
    # '<' superior
    for t in np.linspace(0, 1, n_seg):
        pts.append([(cx - 40) - t * 45, (cy - 50) + t * 50])
    # '<' inferior
    for t in np.linspace(0, 1, n_seg):
        pts.append([(cx - 85) + t * 45, cy + t * 50])

    # Barra '/'
    n_slash = N // 5
    for t in np.linspace(0, 1, n_slash):
        pts.append([(cx + 15) - t * 30, (cy - 55) + t * 110])

    # '>' superior
    n_rem = (N - 2 * n_seg - n_slash) // 2
    for t in np.linspace(0, 1, n_rem):
        pts.append([(cx + 40) + t * 45, (cy - 50) + t * 50])
    # '>' inferior
    n_last = N - 2 * n_seg - n_slash - n_rem
    for t in np.linspace(0, 1, n_last):
        pts.append([(cx + 85) - t * 45, cy + t * 50])

    return np.array(pts)


def matriz_para_runs(matriz, offset_x, offset_y):
    h, w = matriz.shape
    runs = []
    for y in range(h):
        in_run = False
        run_start = 0
        for x in range(w):
            if matriz[y, x] > 0:
                if not in_run:
                    in_run = True
                    run_start = x
            else:
                if in_run:
                    in_run = False
                    runs.append((offset_x + run_start, offset_y + y, x - run_start))
        if in_run:
            runs.append((offset_x + run_start, offset_y + y, w - run_start))
    return runs


def gerar_morfismo_3_etapas(matriz, config_tema, num_grupos=40):
    """
    Agrupa partículas e calcula a interpolação para transição
    Terminal (>_) -> Código (</>) -> Rosto -> Repete.
    """
    runs = matriz_para_runs(matriz, OFFSET_X, OFFSET_Y)
    if not runs:
        return ""

    N = len(runs)
    term_pts = gerar_pontos_terminal(N)
    code_pts = gerar_pontos_codigo(N)

    runs_sorted = sorted(runs, key=lambda r: (r[1], r[0]))

    batches_face = np.array_split(runs_sorted, num_grupos)
    batches_term = np.array_split(term_pts, num_grupos)
    batches_code = np.array_split(code_pts, num_grupos)

    groups_svg = []
    for i in range(num_grupos):
        bf = batches_face[i]
        bt = batches_term[i]
        bc = batches_code[i]
        if len(bf) == 0:
            continue

        mean_fx = np.mean([r[0] for r in bf])
        mean_fy = np.mean([r[1] for r in bf])

        mean_tx = np.mean(bt[:, 0])
        mean_ty = np.mean(bt[:, 1])

        mean_cx = np.mean(bc[:, 0])
        mean_cy = np.mean(bc[:, 1])

        dx_term = int(mean_tx - mean_fx)
        dy_term = int(mean_ty - mean_fy)

        dx_code = int(mean_cx - mean_fx)
        dy_code = int(mean_cy - mean_fy)

        path_segments = [f"M{x},{y}h{length}" for x, y, length in bf]
        path_d = " ".join(path_segments)

        anim_svg = f"""    <g>
      <animateTransform attributeName="transform" type="translate"
                        values="{dx_term} {dy_term}; {dx_term} {dy_term}; {dx_code} {dy_code}; {dx_code} {dy_code}; 0 0; 0 0; {dx_term} {dy_term}"
                        keyTimes="0.0; 0.22; 0.33; 0.55; 0.66; 0.88; 1.0"
                        dur="14s" repeatCount="indefinite"
                        calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1"/>
      <path d="{path_d}" stroke="{config_tema['dot_color']}" stroke-width="1" shape-rendering="crispEdges"/>
    </g>"""
        groups_svg.append(anim_svg)

    return "\n".join(groups_svg)


def gerar_linhas_info_animadas(config_tema, start_y=162, spacing=23):
    """Gera os textos da direita surgindo linha por linha."""
    rows_svg = []
    begin_base = 0.50

    for i, (label, val) in enumerate(INFO_ROWS):
        y = start_y + (i * spacing)
        begin_time = begin_base + (i * 0.08)
        val_xml = val.replace("&", "&amp;")

        row_str = f"""    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{begin_time:.2f}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="{begin_time:.2f}s" fill="freeze"/>
      <text x="470" y="{y}" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve"><tspan fill="{config_tema['chrome']}">{label} </tspan><tspan fill="rgba(148,163,184,0.35)">................................................................</tspan><tspan fill="{config_tema['text_main']}" font-weight="600"> {val_xml}</tspan></text>
    </g>"""
        rows_svg.append(row_str)

    return "\n".join(rows_svg)


def gerar_svg_tema(matriz, config_tema):
    rosto_morfismo = gerar_morfismo_3_etapas(matriz, config_tema)
    info_svg = gerar_linhas_info_animadas(config_tema)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Gabriel Guadalup — profile.sh --live">
  <defs>
    <linearGradient id="{config_tema['gid']}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{config_tema['accent2']}"><animate attributeName="stop-color" values="{config_tema['accent2']};{config_tema['chrome']};#10B981;{config_tema['accent2']}" dur="10s" repeatCount="indefinite"/></stop>
      <stop offset="0.5" stop-color="{config_tema['chrome']}"><animate attributeName="stop-color" values="{config_tema['chrome']};#10B981;{config_tema['accent2']};{config_tema['chrome']}" dur="10s" repeatCount="indefinite"/></stop>
      <stop offset="1" stop-color="#10B981"><animate attributeName="stop-color" values="#10B981;{config_tema['accent2']};{config_tema['chrome']};#10B981" dur="10s" repeatCount="indefinite"/></stop>
    </linearGradient>
    <filter id="glow8" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
    <filter id="glow3" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>
    <filter id="txtGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="0.9" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="winClip"><rect x="2" y="2" width="1176" height="606" rx="18"/></clipPath>
  </defs>

  <rect x="2" y="2" width="1176" height="606" rx="18" fill="{config_tema['bg']}"/>
  <g clip-path="url(#winClip)">
    <rect x="2" y="2" width="1176" height="606" fill="{config_tema['bg']}"/>
    <rect x="2" y="2" width="1176" height="46" fill="#0B1222"/>
    <line x1="2" y1="48" x2="1178" y2="48" stroke="rgba(255,255,255,0.10)"/>

    <circle cx="30" cy="25.0" r="5.5" fill="#ff5f56"/>
    <circle cx="50" cy="25.0" r="5.5" fill="#ffbd2e"/>
    <circle cx="70" cy="25.0" r="5.5" fill="#27c93f"/>
    <text x="590.0" y="29.0" text-anchor="middle" font-size="12" fill="#94A3B8">gabrielguadalup.dev@gmail.com - % ./profile.sh --live</text>

    <text x="38" y="74" font-size="10" letter-spacing="3" fill="#475569">VISUAL.MAP</text>
    <rect x="36" y="84" width="400" height="492" rx="10" fill="none" stroke="{config_tema['chrome']}" stroke-width="2" opacity="0.45" filter="url(#glow3)"/>
    <rect x="36" y="84" width="400" height="492" rx="10" fill="{config_tema['bg']}" stroke="rgba(34,211,238,0.35)"/>

    {rosto_morfismo}

    <text x="470" y="106" font-size="13" letter-spacing="2" fill="{config_tema['chrome']}" filter="url(#txtGlow)">SYSTEM.INFO</text>
    <line x1="566" y1="102" x2="1061" y2="102" stroke="rgba(255,255,255,0.10)"/>
    <text x="1125" y="106" text-anchor="end" font-size="12" fill="#F87171" font-weight="700"><tspan>&#9679;</tspan> LIVE<animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></text>

    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.4s" fill="freeze"/>
      <rect x="470" y="122" width="280" height="20" rx="4" fill="#4C1D95"/>
      <text x="479" y="136" font-size="13" font-weight="700" fill="#E9D5FF">gabrielguadalup.dev@gmail.com</text>
      <line x1="760" y1="130" x2="1125" y2="130" stroke="rgba(255,255,255,0.10)"/>
    </g>

    {info_svg}

    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.80s" fill="freeze"/>
      <text x="470" y="550" font-size="14" fill="#94A3B8">&#9656; Aprendendo em publico. Projetos abaixo no README &#8595; <tspan fill="{config_tema['chrome']}">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
    </g>
  </g>

  <rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#{config_tema['gid']})" strokse-width="3" opacity="0.55" filter="url(#glow8)"/>
  <rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#{config_tema['gid']})" stroke-width="1.6"/>
</svg>"""

    with open(config_tema["file_out"], "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Gerado com sucesso: {config_tema['file_out']}")


if __name__ == "__main__":
    pontos_claro = np.load("pontos.npy")
    pontos_escuro = np.load("pontos_escuro.npy")

    gerar_svg_tema(pontos_escuro, THEMES["dark"])
    gerar_svg_tema(pontos_claro, THEMES["light"])