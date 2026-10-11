#!/usr/bin/env python3
"""
tools/optimize.py
Production image optimizer for "Open When" website:
- Resizes to max 2x retina display size
- Converts static assets to clean WebP with alpha transparency preserved
- Strips metadata
- Reports before and after file sizes
"""

import os
from PIL import Image

ASSETS_DIR = 'Assets'

# Targeted optimizations for production site assets
SPECS = {
    'flower_top_right.png': {'out': 'flower_top_right.webp', 'max_w': 280, 'q': 82},
    'torn_paper_clean.png': {'out': 'torn_paper_clean.webp', 'max_w': 420, 'q': 80},
    'heart_wallpaper.png': {'out': 'heart_wallpaper.webp', 'max_w': 720, 'q': 76},
    'sticker pack 3_sticker_8.png': {'out': 'char_cat_shy.webp', 'max_w': 180, 'q': 82},
    'bubu_dudu_bouquet.png': {'out': 'char_bubu_bouquet.webp', 'max_w': 180, 'q': 82},
    'mochi_cat_pleading_lying.png': {'out': 'char_cat_lying.webp', 'max_w': 180, 'q': 82},
    'sticker pack 1_sticker_2.png': {'out': 'char_pack1_2.webp', 'max_w': 180, 'q': 82},
    'sticker pack 2_sticker_1.png': {'out': 'photo_love.webp', 'max_w': 260, 'q': 80},
}

def optimize():
    total_before = 0
    total_after = 0
    print(f"{'Source Asset':35} | {'Before (KB)':11} | {'Output Asset':25} | {'After (KB)':10} | {'Saved %'}")
    print("-" * 95)

    for src_name, cfg in SPECS.items():
        src_path = os.path.join(ASSETS_DIR, src_name)
        if not os.path.exists(src_path):
            continue

        size_before = os.path.getsize(src_path)
        total_before += size_before

        out_name = cfg['out']
        out_path = os.path.join(ASSETS_DIR, out_name)

        im = Image.open(src_path)
        w, h = im.size
        if w > cfg['max_w']:
            ratio = cfg['max_w'] / float(w)
            new_h = int(h * ratio)
            im = im.resize((cfg['max_w'], new_h), Image.Resampling.LANCZOS)

        im.save(out_path, 'WEBP', quality=cfg['q'], method=6)
        size_after = os.path.getsize(out_path)
        total_after += size_after

        savings = ((size_before - size_after) / size_before) * 100
        print(f"{src_name:35} | {size_before/1024:9.2f} KB | {out_name:25} | {size_after/1024:8.2f} KB | {savings:5.1f}%")

    print("-" * 95)
    print(f"{'TOTAL':35} | {total_before/1024:9.2f} KB | {'':25} | {total_after/1024:8.2f} KB | {((total_before-total_after)/total_before)*100:5.1f}%")

if __name__ == '__main__':
    optimize()
