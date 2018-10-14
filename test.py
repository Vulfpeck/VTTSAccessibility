try:
        from PIL import Image
except ImportError:
        import Image
import pytesseract

im = Image.open("screen_region.jpg")
print(pytesseract.image_to_string(im, lang='eng',config='--psm 1'))