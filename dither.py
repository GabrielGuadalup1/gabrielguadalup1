"""
Gera o retrato pontilhado do banner.
Etapa 1: preparo da imagem + dithering + segmentacao de fundo.
O SVG vem depois, a partir da matriz que este script produz.
"""

import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from scipy import ndimage

# Nome do arquivo da sua foto (deve estar na mesma pasta do script)
ENTRADA = "IMG_4783.JPG"
LARG, ALT = 300, 340


def preparar(caminho):
    """Abre, corta na proporcao certa e ajusta contraste."""
    im = Image.open(caminho).convert("L")
    w, h = im.size

    # corta para a proporcao 300:340, tirando da base (a cabeca fica no topo)
    alvo = LARG / ALT
    if w / h < alvo:
        nova_h = int(w / alvo)
        im = im.crop((0, 0, w, nova_h))
    else:
        nova_w = int(h * alvo)
        im = im.crop((0, 0, nova_w, h))

    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Contrast(im).enhance(1.3)
    im = im.resize((LARG, ALT), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    return im


def dither(im):
    """Floyd-Steinberg 1 bit, em serpentina.

    Serpentina = percorre uma linha da esquerda para a direita e a
    seguinte no sentido contrario. Isso evita que o erro se acumule
    sempre para o mesmo lado e crie listras verticais.
    """
    a = np.asarray(im).astype(np.float64)
    h, w = a.shape
    saida = np.zeros((h, w), dtype=np.uint8)

    for y in range(h):
        esquerda_para_direita = (y % 2 == 0)
        xs = range(w) if esquerda_para_direita else range(w - 1, -1, -1)
        d = 1 if esquerda_para_direita else -1

        for x in xs:
            antigo = a[y, x]
            novo = 255.0 if antigo > 127.5 else 0.0
            saida[y, x] = 1 if novo == 0.0 else 0  # 1 = ponto de tinta
            erro = antigo - novo

            if 0 <= x + d < w:
                a[y, x + d] += erro * 7 / 16
            if y + 1 < h:
                if 0 <= x - d < w:
                    a[y + 1, x - d] += erro * 3 / 16
                a[y + 1, x] += erro * 5 / 16
                if 0 <= x + d < w:
                    a[y + 1, x + d] += erro * 1 / 16

    return saida


def separar_fundo(im, tolerancia=28):
    """Marca o que e sujeito e o que e parede.

    O fundo aqui e quase uma cor chapada, entao basta olhar a
    distancia de cada pixel ate o tom medio das bordas.
    """
    a = np.asarray(im).astype(np.float64)
    borda = np.concatenate([a[:6, :].ravel(), a[-6:, :].ravel(),
                            a[:, :6].ravel(), a[:, -6:].ravel()])
    tom_fundo = np.median(borda)

    sujeito = np.abs(a - tom_fundo) > tolerancia
    sujeito = ndimage.binary_closing(sujeito, np.ones((5, 5)))
    sujeito = ndimage.binary_fill_holes(sujeito)

    # fica so com a maior mancha conectada, descarta respingo solto
    rotulos, n = ndimage.label(sujeito)
    if n > 1:
        tamanhos = ndimage.sum(sujeito, rotulos, range(1, n + 1))
        sujeito = rotulos == (np.argmax(tamanhos) + 1)

    return sujeito


def salvar_preview(matriz, caminho, escala=2, fundo=255, tinta=0):
    """Grava um PNG ampliado para inspecao visual."""
    img = np.where(matriz == 1, tinta, fundo).astype(np.uint8)
    Image.fromarray(img).resize(
        (matriz.shape[1] * escala, matriz.shape[0] * escala), Image.NEAREST
    ).save(caminho)


if __name__ == "__main__":
    im = preparar(ENTRADA)
    sujeito = separar_fundo(im)

    # modo claro: fundo fica, pontos desenham as partes ESCURAS da foto
    pontos = dither(im)
    salvar_preview(pontos, "preview_claro.png", fundo=255, tinta=0)

    # modo escuro: fundo sai, pontos desenham as partes CLARAS (o que a luz pega)
    im_inv = ImageOps.invert(im)
    pontos_escuro = dither(im_inv) & sujeito

    # limpa a franja
    borda = sujeito & ~ndimage.binary_erosion(sujeito, np.ones((3, 3)))
    pontos_escuro = pontos_escuro & ~borda

    salvar_preview(pontos_escuro, "preview_escuro.png", fundo=10, tinta=167)
    salvar_preview(sujeito.astype(np.uint8), "preview_mascara.png",
                   fundo=255, tinta=60)

    np.save("pontos.npy", pontos)
    np.save("pontos_escuro.npy", pontos_escuro)
    np.save("sujeito.npy", sujeito)

    total = int(pontos.sum())
    print(f"pontos no modo claro:  {total}")
    print(f"pontos no modo escuro: {int(pontos_escuro.sum())}")
    print(f"cobertura de tinta:    {total / pontos.size * 100:.1f}%")
    print(f"area do sujeito:       {sujeito.sum() / sujeito.size * 100:.1f}%")