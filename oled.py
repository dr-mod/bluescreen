import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from observer import Observer


class OledDisplay(Observer):
    def __init__(self, observable):
        Observer.__init__(self, observable)
        self.__display = self.__init_display()
        self.__font = ImageFont.load_default()

    @staticmethod
    def __init_display():
        display = Adafruit_SSD1306.SSD1306_128_64(rst=24)
        display.begin()
        display.clear()
        display.display()
        return display

    def update(self, device):
        self.__display.clear()

        width = self.__display.width
        height = self.__display.height
        image = Image.new('1', (width, height))

        draw = ImageDraw.Draw(image)

        draw.text((0, 0), '{:8s} {:2.2f} {}'.format(*device), font=self.__font, fill=255)

        self.__display.image(image)
        self.__display.display()

