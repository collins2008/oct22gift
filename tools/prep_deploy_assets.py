import os
import shutil
from PIL import Image

def prep():
    assets_dir = 'Assets'
    raw_dir = os.path.join(assets_dir, 'raw')
    os.makedirs(raw_dir, exist_ok=True)

    # Required assets actively used by index.html, style.css, script.js
    required_assets = {
        'gingham_clean.png',
        'gingham_pattern.svg',
        'flower_top_right.webp',
        'torn_paper_clean.webp',
        'heart_wallpaper.webp',
        'char_cat_shy.webp',
        'char_bubu_bouquet.webp',
        'char_cat_lying.webp',
        'tkthao219-bubududu.webp',
        'bubu-kisses-dudu-bubu-dudu.webp',
        'char_pack1_2.webp',
        'bubu-dudu.webp',
        'bubu-dudu (1).webp',
        'photo_love.webp',
        'og_preview.png',
        'favicon.png',
        'favicon.ico'
    }

    # Move non-required files in Assets/ root to Assets/raw/
    for fname in os.listdir(assets_dir):
        fpath = os.path.join(assets_dir, fname)
        if os.path.isfile(fpath):
            if fname not in required_assets and not fname.startswith('og_') and not fname.startswith('favicon'):
                target = os.path.join(raw_dir, fname)
                print(f"Moving unused asset to raw: {fname}")
                shutil.move(fpath, target)

    # Create og_preview.png (< 100 KB) for social links (WhatsApp / iMessage)
    # Use reference frame f_001.png or composite screen
    ref_frame = 'reference/final_390_s1.png'
    if not os.path.exists(ref_frame):
        ref_frame = 'reference/frames/f_001.png'
    
    if os.path.exists(ref_frame):
        im = Image.open(ref_frame).convert('RGB')
        # WhatsApp optimal OG ratio is roughly 1.91:1 or centered card
        w, h = im.size
        # Center crop square or 600x600 preview
        size = min(w, h)
        left = (w - size) // 2
        top = (h - size) // 2
        im_cropped = im.crop((left, top, left + size, top + size))
        im_resized = im_cropped.resize((480, 480), Image.Resampling.LANCZOS)
        og_path = os.path.join(assets_dir, 'og_preview.png')
        im_resized.save(og_path, 'PNG', optimize=True)
        print(f"Created og_preview.png: {os.path.getsize(og_path) / 1024:.2f} KB")

    # Create clean favicon (heart on transparent background)
    fav_im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    # Draw cute heart
    from PIL import ImageDraw
    draw = ImageDraw.Draw(fav_im)
    # Simple heart polygon / bezier or circle combo
    draw.ellipse([8, 12, 34, 38], fill=(212, 88, 122, 255))
    draw.ellipse([30, 12, 56, 38], fill=(212, 88, 122, 255))
    draw.polygon([(9, 28), (55, 28), (32, 54)], fill=(212, 88, 122, 255))
    
    fav_png_path = os.path.join(assets_dir, 'favicon.png')
    fav_im.save(fav_png_path, 'PNG', optimize=True)
    fav_ico_path = os.path.join(assets_dir, 'favicon.ico')
    fav_im.save(fav_ico_path, format='ICO')
    print("Created favicon.png and favicon.ico")

    # Strip EXIF / metadata from all assets in Assets/
    for fname in os.listdir(assets_dir):
        fpath = os.path.join(assets_dir, fname)
        if os.path.isfile(fpath) and fname.lower().endswith(('.png', '.webp', '.jpg', '.jpeg')):
            try:
                img = Image.open(fpath)
                data = list(img.getdata())
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(data)
                clean_img.save(fpath, optimize=True)
            except Exception as e:
                print(f"Skipping EXIF strip for {fname}: {e}")

    print("\nAssets preparation complete!")

if __name__ == '__main__':
    prep()
