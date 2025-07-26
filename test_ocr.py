import pytesseract
from PIL import Image

# Test OCR on the image
image = Image.open('test_invoice.png')
print(f"Image mode: {image.mode}")
print(f"Image size: {image.size}")

# Convert to RGB if necessary
if image.mode != 'RGB':
    image = image.convert('RGB')

# Test different OCR settings
print("\n=== Testing OCR Settings ===")

text1 = pytesseract.image_to_string(image, config='--oem 3 --psm 3')
print(f"PSM 3: '{repr(text1)}' (length: {len(text1)})")

text2 = pytesseract.image_to_string(image, config='--oem 3 --psm 6')
print(f"PSM 6: '{repr(text2)}' (length: {len(text2)})")

text3 = pytesseract.image_to_string(image)
print(f"Basic: '{repr(text3)}' (length: {len(text3)})")

# Test if any of them work
for i, text in enumerate([text1, text2, text3], 1):
    if text.strip() and len(text.strip()) > 2:
        print(f"\nSuccess with method {i}!")
        print(f"Extracted text: {text[:200]}...")
        break
else:
    print("\nAll OCR methods failed to extract meaningful text")
