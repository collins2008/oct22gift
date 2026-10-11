#!/bin/bash
# Image Optimization script for Open When project
# Run this inside a bash environment to process new assets

INPUT_DIR="Assets/raw"
OUTPUT_DIR="Assets"

echo "Optimizing assets..."

if [ ! -d "$INPUT_DIR" ]; then
  echo "No raw assets directory found at $INPUT_DIR. Please place raw images there."
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Convert all JPEGs, PNGs, and AVIFs to compressed WEBP
for img in "$INPUT_DIR"/*.{jpg,jpeg,png,avif}; do
  if [ -f "$img" ]; then
    filename=$(basename -- "$img")
    name="${filename%.*}"
    
    echo "Processing $name..."
    # Example command using cwebp (requires webp package)
    # cwebp -q 75 -resize 300 0 "$img" -o "$OUTPUT_DIR/${name}.webp"
    
    # Example using ffmpeg
    ffmpeg -i "$img" -vcodec libwebp -qscale:v 75 -filter:v scale="300:-1" -y "$OUTPUT_DIR/${name}.webp"
  fi
done

echo "Done! Optimized assets are in $OUTPUT_DIR"
