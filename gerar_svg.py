import numpy as np

# Configurações do Canvas e Layout
CANVAS_W, CANVAS_H = 1180, 610
PORTRAIT_W, PORTRAIT_H = 300, 340
OFFSET_X, OFFSET_Y = 90, 150

# Cores por tema
THEMES = {
    "dark": {
        "bg": "#0A101F",
        "chrome": "#22D3EE",
        "accent": "#A78BFA",
        "text_sub": "#94A3B8",
        "text_main": "#F8FAFC",
        "dot_color": "#A78BFA",
        "file_out": "dark.svg"
    },
    "light": {
        "bg": "#F8FAFC",
        "chrome": "#089182",
        "accent": "#7C3AED",
        "text_sub": "#64748B",
        "text_main": "#0F172A",
        "dot_color": "#7C3AED",
        "file_out": "light.svg"
    }
}

# Dados do Painel SYSTEM.INFO
INFO_ROWS = [
    ("Subject", "Gabriel Guadalup"),
    ("Role", "Estudante de IA & Desenvolvedor"),
    ("Origin", "Macapa, Amapa, Brasil"),
    ("Education", "Bacharelado em IA (IFAP)"),
    ("Status", "Building & Learning"),
    ("Core.Lang", "Python, JavaScript, TypeScript"),
    ("Core.Tools", "Git, GitHub, VS Code"),
    ("Grid.LinkedIn", "gabriel-guadalup-78351329a"),
    ("Grid.GitHub", "GabrielGuadalup1")
]


def matriz_para_path_d(matriz, offset_x, offset_y):
    """
    Converte a matriz de pontos (1s) em rotas otimizadas <path d="...">
    usando corridas horizontais para reduzir o tamanho do arquivo SVG.
    """
    h, w = matriz.shape
    segments = []
    
    for y in range(h):
        in_run = False
        run_start = 0
        for x in range(w):
            if matriz[y, x] == 1:
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


def gerar_svg_tema(matriz, config_tema):
    """Gera a estrutura SVG completa para um tema (dark/light)."""
    path_d = matriz_para_path_d(matriz, OFFSET_X, OFFSET_Y)
    
    # Construção das linhas de dados com tratamento do caractere '&'
    rows_svg = []
    start_y = 160
    spacing = 38
    
    for i, (label, val) in enumerate(INFO_ROWS):
        y = start_y + (i * spacing)
        
        # Converte & para &amp; para não quebrar o parser XML
        val_xml = val.replace("&", "&amp;")
        
        row_str = f"""
        <!-- Row: {label} -->
        <text x="490" y="{y}" fill="{config_tema['text_sub']}" font-family="JetBrains Mono, monospace" font-size="13" font-weight="600">{label}</text>
        <path d="M630,{y-4} h330" stroke="{config_tema['text_sub']}" stroke-dasharray="2 6" stroke-width="1" opacity="0.4" />
        <text x="1110" y="{y}" fill="{config_tema['text_main']}" font-family="JetBrains Mono, monospace" font-size="13" font-weight="600" text-anchor="end">{val_xml}</text>
        """
        rows_svg.append(row_str)
        
    info_content = "\n".join(rows_svg)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" width="{CANVAS_W}" height="{CANVAS_H}">
    <defs>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&amp;family=JetBrains+Mono:wght@400;600;700&amp;display=swap');
        </style>
    </defs>

    <rect width="{CANVAS_W}" height="{CANVAS_H}" fill="{config_tema['bg']}" rx="10" />

    <!-- Janela Terminal Chrome -->
    <rect x="20" y="20" width="1140" height="570" fill="none" stroke="{config_tema['chrome']}" stroke-width="1.5" rx="8" opacity="0.6" />
    <circle cx="45" cy="42" r="5" fill="#FF5F56" />
    <circle cx="62" cy="42" r="5" fill="#FFBD2E" />
    <circle cx="79" cy="42" r="5" fill="#27C93F" />
    <text x="590" y="46" fill="{config_tema['text_sub']}" font-family="JetBrains Mono, monospace" font-size="12" text-anchor="middle" opacity="0.8">profile.sh — live</text>
    <line x1="20" y1="62" x2="1160" y2="62" stroke="{config_tema['chrome']}" stroke-width="1" opacity="0.3" />

    <!-- PAINEL ESQUERDO: VISUAL.MAP -->
    <rect x="45" y="85" width="390" height="475" fill="none" stroke="{config_tema['chrome']}" stroke-width="1" opacity="0.3" rx="4" />
    <text x="60" y="112" fill="{config_tema['chrome']}" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" letter-spacing="1">VISUAL.MAP</text>

    <!-- Moldura e Retrato Pontilhado -->
    <rect x="{OFFSET_X-5}" y="{OFFSET_Y-5}" width="{PORTRAIT_W+10}" height="{PORTRAIT_H+10}" fill="none" stroke="{config_tema['chrome']}" stroke-width="1" stroke-dasharray="4 4" opacity="0.4" />
    <path d="{path_d}" stroke="{config_tema['dot_color']}" stroke-width="1" shape-rendering="crispEdges" />

    <!-- PAINEL DIREITO: SYSTEM.INFO -->
    <rect x="460" y="85" width="675" height="475" fill="none" stroke="{config_tema['chrome']}" stroke-width="1" opacity="0.3" rx="4" />
    <text x="490" y="112" fill="{config_tema['chrome']}" font-family="JetBrains Mono, monospace" font-size="12" font-weight="700" letter-spacing="1">SYSTEM.INFO</text>

    <!-- Indicador LIVE -->
    <circle cx="1070" cy="108" r="4" fill="#EF4444" />
    <text x="1082" y="112" fill="#EF4444" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700">LIVE</text>

    {info_content}

</svg>"""

    with open(config_tema["file_out"], "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Gerado com sucesso: {config_tema['file_out']}")


if __name__ == "__main__":
    pontos_claro = np.load("pontos.npy")
    pontos_escuro = np.load("pontos_escuro.npy")

    gerar_svg_tema(pontos_escuro, THEMES["dark"])
    gerar_svg_tema(pontos_claro, THEMES["light"])