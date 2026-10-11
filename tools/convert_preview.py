from PIL import Image
img = Image.open(r'Assets/a pink crumpled heart paper texture')
img.save(r'Assets/heart_paper_preview.png')
print("Saved heart_paper_preview.png")
