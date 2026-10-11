import cv2
import numpy as np
import os
import sys

def process_sticker_sheet(image_path, output_dir):
    print(f"Processing {image_path}...")
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error reading {image_path}")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Assume background is white or close to white. 
    # Let's get the background color from the corners.
    h, w = gray.shape
    corners = [gray[0,0], gray[0,w-1], gray[h-1,0], gray[h-1,w-1]]
    bg_color = np.median(corners)
    
    # Thresholding: Assuming stickers are darker than the background (if bg is white).
    # We use a simple binary threshold.
    # If bg is white (>200), we threshold to find darker regions.
    if bg_color > 128:
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    else:
        _, thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)
        
    # Dilate slightly to connect components of a single sticker
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    min_area = 500  # Minimum area to be considered a sticker
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    count = 0
    for i, contour in enumerate(contours):
        if cv2.contourArea(contour) < min_area:
            continue
            
        # Get bounding box
        x, y, w_box, h_box = cv2.boundingRect(contour)
        
        # Add some padding
        pad = 10
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(w, x + w_box + pad)
        y2 = min(h, y + h_box + pad)
        
        sticker = img[y1:y2, x1:x2]
        
        # Save sticker
        out_name = f"{base_name}_sticker_{count+1}.png"
        out_path = os.path.join(output_dir, out_name)
        cv2.imwrite(out_path, sticker)
        print(f"  Saved {out_name}")
        count += 1
        
    print(f"Found {count} stickers in {image_path}")

if __name__ == '__main__':
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        print("Assets folder not found")
        sys.exit(1)
        
    for file in os.listdir(assets_dir):
        if file.startswith("sticker pack") and file.lower().endswith(('.png', '.jpg', '.jpeg')):
            process_sticker_sheet(os.path.join(assets_dir, file), assets_dir)
