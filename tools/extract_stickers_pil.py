import os
import sys
import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects, binary_closing, binary_fill_holes

def extract_stickers(image_path, output_dir):
    print(f"Processing {image_path}...")
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return

    # Convert to grayscale numpy array
    gray_img = img.convert("L")
    gray = np.array(gray_img)
    
    h, w = gray.shape
    
    # Estimate background from corners
    corners = [gray[0, 0], gray[0, w-1], gray[h-1, 0], gray[h-1, w-1]]
    bg_color = np.median(corners)
    
    print(f"Background color estimated as: {bg_color}")
    
    if bg_color > 128:
        mask = gray < (bg_color - 15)
    else:
        mask = gray > (bg_color + 15)
        
    struct = np.ones((5, 5), dtype=bool)
    mask = binary_closing(mask, structure=struct, iterations=2)
    
    labeled_array, num_features = label(mask)
    print(f"Found {num_features} potential components.")
    
    slices = find_objects(labeled_array)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    min_area = 1000  # Minimum pixels to be considered a sticker
    count = 0
    img_array = np.array(img)
    
    for i, slice_tuple in enumerate(slices):
        if slice_tuple is None:
            continue
            
        y_slice, x_slice = slice_tuple
        
        box_h = y_slice.stop - y_slice.start
        box_w = x_slice.stop - x_slice.start
        
        img_area = h * w
        if box_h * box_w < min_area or box_h < 20 or box_w < 20 or (box_h * box_w > 0.9 * img_area):
            continue
            
        # Extract the component mask
        comp_mask = (labeled_array[y_slice, x_slice] == (i + 1))
        
        # Fill holes in the mask so white interior parts of stickers aren't transparent
        filled_mask = binary_fill_holes(comp_mask)
        
        pad = 10
        y_start = max(0, y_slice.start - pad)
        y_stop = min(h, y_slice.stop + pad)
        x_start = max(0, x_slice.start - pad)
        x_stop = min(w, x_slice.stop + pad)
        
        # Extract sticker image with padding
        sticker_array = img_array[y_start:y_stop, x_start:x_stop].copy()
        
        # We also need to get a padded mask matching sticker_array's size
        pad_y_top = y_slice.start - y_start
        pad_y_bottom = y_stop - y_slice.stop
        pad_x_left = x_slice.start - x_start
        pad_x_right = x_stop - x_slice.stop
        
        padded_mask = np.pad(filled_mask, ((pad_y_top, pad_y_bottom), (pad_x_left, pad_x_right)), mode='constant', constant_values=False)
        
        # Set alpha channel to 0 where mask is False
        sticker_array[~padded_mask, 3] = 0
        
        sticker_img = Image.fromarray(sticker_array)
        
        out_name = f"{base_name}_sticker_{count+1}.png"
        out_path = os.path.join(output_dir, out_name)
        sticker_img.save(out_path)
        count += 1
        
    print(f"Successfully extracted {count} transparent stickers from {image_path}")

if __name__ == '__main__':
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        print("Assets folder not found")
        sys.exit(1)
        
    for file in os.listdir(assets_dir):
        if file.startswith("sticker pack") and "_sticker_" not in file and file.lower().endswith(('.png', '.jpg', '.jpeg')):
            extract_stickers(os.path.join(assets_dir, file), assets_dir)
