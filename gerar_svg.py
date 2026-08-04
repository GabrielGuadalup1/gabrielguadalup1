import numpy as np

# Configurações do Canvas e Layout
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


def gerar_pontos_simbolos(num_pontos):
    """
    Gera pontos organizados no formato do Terminal (>_) e do Python.
    """
    cx, cy = OFFSET_X + 150, OFFSET_Y + 170
    pts = []
    
    # 1. Desenha o símbolo do Terminal '>_'
    n_term = num_pontos // 2
    # Parte superior do '>'
    for t in np.linspace(-50, 0, n_term // 3):
        pts.append([cx - 50 + t, cy + t])
    # Parte inferior do '>'
    for t in np.linspace(0, 50, n_term // 3):
        pts.append([cx - 100 + t, cy + t])
    # Traço '_'
    for x in np.linspace(cx - 10, cx + 50, n_term - 2 * (n_term // 3)):
        pts.append([x, cy + 50])

    # 2. Desenha a estrutura do Python (dois blocos entrelaçados)
    n_py = num_pontos - len(pts)
    # Bloco superior do Python
    for theta in np.linspace(0, np.pi, n_py // 2):
        pts.append([cx + 30 * np.cos(theta), cy - 30 + 30 * np.sin(theta)])
    # Bloco inferior do Python
    for theta in np.linspace(np.pi, 2 * np.pi, n_py - (n_py // 2)):
        pts.append([cx + 30 * np.cos(theta), cy + 10 + 30 * np.sin(theta)])

    return np.array(pts)


def gerar_morfismo_rosto_svg(matriz, config_tema, num_grupos=30):
    """
    Cria a animação SVG pura (SMIL) onde os pontos saem do formato
    Terminal/Python e navegam até o seu rosto.
    """
    y_idx, x_indices = np.where(matriz > 0)
    if len(x_indices) == 0:
        return ""

    face_pts = np.column_stack((x_indices + OFFSET_X, y_idx + OFFSET_Y))
    num_pts = len(face_pts)

    # Gera os pontos iniciais (Terminal + Python)
    start_pts = gerar_pontos_simbolos(num_pts)

    # Embaralha os índices para criar um efeito orgânico de partículas se espalhando
    np.random.seed(42)
    perm = np.random.permutation(num_pts)
    face_pts = face_pts[perm]
    start_pts = start_pts[perm]

    groups_svg = []
    batches_face = np.array_split(face_pts, num_grupos)
    batches_start = np.array_split(start_pts, num_grupos)

    for i in range(num_grupos):
        bf = batches_face[i]
        bs = batches_start[i]
        if len(bf) == 0:
            continue

        # Calcula o deslocamento (offset) do símbolo até o rosto
        dx_mean = int(np.mean(bs[:, 0] - bf[:, 0]))
        dy_mean = int(np.mean(bs[:, 1] - bf[:, 1]))

        # Monta a rota dos pontos do grupo
        path_segments = [f"M{int(px)},{int(py)}h1" for px, py in bf]
        path_d = " ".join(path_segments)

        # Animação em loop: Símbolo (offset) -> Transição -> Rosto (0 0) -> Pausa -> Volta ao Símbolo
        anim_svg = f"""    <g>
      <animateTransform attributeName="transform" type="translate"
                        values="{dx_mean} {dy_mean}; {dx_mean} {dy_mean}; 0 0; 0 0; {dx_mean} {dy_mean}"
                        keyTimes="0.0; 0.15; 0.35; 0.85; 1.0"
                        dur="12s" repeatCount="indefinite"
                        calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1"/>
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
    rosto_morfismo = gerar_morfismo_rosto_svg(matriz, config_tema)
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

  <rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#{config_tema['gid']})" stroke-width="3" opacity="0.55" filter="url(#glow8)"/>
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