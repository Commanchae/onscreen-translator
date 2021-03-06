from PIL import Image, ImageFilter, ImageDraw, ImageGrab, ImageOps
import pytesseract
from pytesseract import Output
from googletrans import Translator, constants

import time
import cv2

# In implementation, try putting this into the folder as well.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OnscreenTranslator():
    def __init__(self):
        currentImage = None

    def getImage(self, imageName: str):
        return Image.open(imageName)
    
    def getTesseractDataFromImage(self, image, language="chi_sim", output_type = Output.DICT):
        return pytesseract.image_to_data(image, lang = language, output_type = output_type)
    
    def getBoundingBoxes(self, image):
        imageData = self.getTesseractDataFromImage(image)
        bounding_boxes = [[imageData["left"][i], imageData["top"][i], imageData["left"][i]+ imageData["width"][i],  imageData["top"][i]+imageData["height"][i]] for i in range(len(imageData["level"])) if imageData["conf"][i] != "-1"]
        return bounding_boxes

    def drawBoundingBoxesOnImage(self, image):
        image_copy = image.copy()
        bounding_boxes = self.getBoundingBoxes(image_copy)
        for box_dict in bounding_boxes:
            draw = ImageDraw.Draw(image_copy)
            draw.rectangle(box_dict, fill = None, outline="red")
        return image_copy

if __name__ == "__main__":
    time.sleep(2)
    ost = OnscreenTranslator()
    img = ImageGrab.grab()
    img = ImageOps.grayscale(img)
    im2 = ost.drawBoundingBoxesOnImage(img)
    im2.show()


'''
osT = OnscreenTranslator()


translator = Translator()
for i in range(len(data["text"])):
    if translator.detect(data["text"][i]).confidence > 0.5:
        print(data["text"][i], ": CONF: ", translator.detect(data["text"][i]))
'''
#translator = Translator()
#translated_text = translator.translate(transcribed_text)


# Do something that allows you to select which text to transcribe.
# Make it so that it detects chinese chars and uses that instead.