#!/usr/bin/env python3
"""
NÍVEL 3: Processador de Visão Computacional
FUNÇÃO: Higienização e formatação de fotos de perfil (LinkedIn Style).
CONCEITOS: Pillow, Máscara Alpha, Organização de Data/output_images.
"""

import sys
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

# --- BOOTSTRAP: CONEXÃO COM O SETTINGS ---
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from Config.settings import DIRS
    # Origem: Assets | Destino: Data/output_images
    ASSETS_DIR = BASE_DIR / "Assets"
    OUTPUT_DIR = DIRS["DATA"] / "output_images"
except ImportError:
    ASSETS_DIR = BASE_DIR / "Assets"
    OUTPUT_DIR = BASE_DIR / "Data" / "output_images"

# Garante que as pastas de organização existam
ASSETS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def criar_foto_linkedin(nome_arquivo):
    caminho_in = ASSETS_DIR / nome_arquivo
    # O resultado vai para a pasta de OUTPUT com o prefixo 'perfil_'
    caminho_out = OUTPUT_DIR / f"perfil_{caminho_in.stem}.png"

    if not caminho_in.exists():
        print(f"❌ Erro: '{nome_arquivo}' não encontrado em {ASSETS_DIR}")
        return

    try:
        print(f"🖼️  Lendo original de Assets: {caminho_in.name}")
        img = Image.open(caminho_in)
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGBA")
        
        # Sua lógica de design (Zoom 0.20 e Foco nos olhos 0.35)
        fator_zoom = 0.20 
        borda = int(min(img.size) * fator_zoom)
        img_com_borda = ImageOps.expand(img, border=borda, fill='white')

        min_lado = min(img_com_borda.size)
        tamanho_quadrado = (min_lado, min_lado)
        img_quadrada = ImageOps.fit(img_com_borda, tamanho_quadrado, centering=(0.5, 0.35))
        
        mascara = Image.new('L', tamanho_quadrado, 0)
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0) + tamanho_quadrado, fill=255)
        img_quadrada.putalpha(mascara)

        img_final = img_quadrada.resize((500, 500), Image.Resampling.LANCZOS)

        # Salva o arquivo na pasta organizada de saída
        img_final.save(caminho_out, "PNG", optimize=True, compress_level=9)
        
        print(f"✅ SUCESSO! Foto processada disponível em: {caminho_out}")

    except Exception as e:
        print(f"❌ Falha no processamento: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        criar_foto_linkedin(sys.argv[1])
    else:
        print("--- ToolBox Vision v3.0 ---")
        print(f"Uso: python3 vision_processor.py foto.jpg")
        print(f"Nota: Coloque a foto em {ASSETS_DIR}")