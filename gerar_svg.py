import numpy as np

# Configurações do Canvas e Posição do Retrato
CANVAS_W, CANVAS_H = 1180, 610
OFFSET_X, OFFSET_Y = 86, 135

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


def criar_matriz_terminal(h, w):
    """Gera uma matriz de pontos nítidos para o símbolo do Terminal '>_'."""
    mat = np.zeros((h, w), dtype=int)
    cy, cx = h // 2, w // 2 - 15
    size = 40
    thickness = 8

    # Desenha '>'
    for t in range(-size, size):
        y = cy + t
        x = cx + (size - abs(t))
        if 0 <= y < h:
            for dx in range(-thickness, thickness):
                for dy in range(-2, 3):
                    if 0 <= x + dx < w and 0 <= y + dy < h:
                        mat[y + dy, x + dx] = 1

    # Desenha '_'
    start_x = cx + 25
    end_x = cx + 75
    y_line = cy + 32
    for x in range(start_x, end_x):
        for dy in range(-4, 5):
            if 0 <= y_line + dy < h and 0 <= x < w:
                mat[y_line + dy, x] = 1

    # Aplica padrão de pontos (grid dither)
    mask_grid = np.zeros((h, w), dtype=int)
    mask_grid[::2, ::2] = 1
    return mat * mask_grid


def criar_matriz_codigo(h, w):
    """Gera uma matriz de pontos nítidos para o símbolo de código '</>'."""
    mat = np.zeros((h, w), dtype=int)
    cy, cx = h // 2, w // 2
    size = 40
    thickness = 7

    # 1. '<'
    cx_left = cx - 50
    for t in range(-size, size):
        y = cy + t
        x = cx_left - (size - abs(t))
        if 0 <= y < h:
            for dx in range(-thickness, thickness):
                for dy in range(-2, 3):
                    if 0 <= x + dx < w and 0 <= y + dy < h:
                        mat[y + dy, x + dx] = 1

    # 2. '/'
    for t in range(-size - 10, size + 10):
        y = cy + t
        x = cx - int(t * 0.35)
        if 0 <= y < h:
            for dx in range(-thickness, thickness):
                for dy in range(-2, 3):
                    if 0 <= x + dx < w and 0 <= y + dy < h:
                        mat[y + dy, x + dx] = 1

    # 3. '>'
    cx_right = cx + 50
    for t in range(-size, size):
        y = cy + t
        x = cx_right + (size - abs(t))
        if 0 <= y < h:
            for dx in range(-thickness, thickness):
                for dy in range(-2, 3):
                    if 0 <= x + dx < w and 0 <= y + dy < h:
                        mat[y + dy, x + dx] = 1

    # Aplica padrão de pontos (grid dither)
    mask_grid = np.zeros((h, w), dtype=int)
    mask_grid[::2, ::2] = 1
    return mat * mask_grid


def matriz_para_path_d(matriz, offset_x, offset_y):
    """Converte a matriz em linhas vetoriais perfeitas."""
    h, w = matriz.shape
    segments = []

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
                    px_x = offset_x + run_start
                    px_y = offset_y + y
                    run_len = x - run_start
                    segments.append(f"M{px_x},{px_y}h{run_len}")
        if in_run:
            px_x = offset_x + run_start
            px_y = offset_y + y
            run_len = w - run_start
            segments.append(f"M{px_x},{px_y}h{run_len}")

    return " ".join(segments)


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
    h, w = matriz.shape
    mat_term = criar_matriz_terminal(h, w)
    mat_code = criar_matriz_codigo(h, w)

    path_term = matriz_para_path_d(mat_term, OFFSET_X, OFFSET_Y)
    path_code = matriz_para_path_d(mat_code, OFFSET_X, OFFSET_Y)
    path_face = matriz_para_path_d(matriz, OFFSET_X, OFFSET_Y)

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

    <g opacity="0">
      <animate attributeName="opacity" values="0; 1; 1; 0; 0" keyTimes="0.0; 0.05; 0.28; 0.33; 1.0" dur="12s" repeatCount="indefinite"/>
      <path d="{path_term}" stroke="{config_tema['dot_color']}" stroke-width="1" shape-rendering="crispEdges"/>
    </g>

    <g opacity="0">
      <animate attributeName="opacity" values="0; 0; 1; 1; 0; 0" keyTimes="0.0; 0.33; 0.38; 0.61; 0.66; 1.0" dur="12s" repeatCount="indefinite"/>
      <path d="{path_code}" stroke="{config_tema['chrome']}" stroke-width="1" shape-rendering="crispEdges"/>
    </g>

    <g opacity="0">
      <animate attributeName="opacity" values="0; 0; 1; 1; 0" keyTimes="0.0; 0.66; 0.71; 0.95; 1.0" dur="12s" repeatCount="indefinite"/>
      <path d="{path_face}" stroke="{config_tema['dot_color']}" stroke-width="1" shape-rendering="crispEdges"/>
    </g>

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