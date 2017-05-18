import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from observer import Observer


class OledDisplay(Observer):

    STEP = 16
    TEXT_OFFSET = 3

    AWAKE = Image.open('img/sun2.ppm').convert('1')
    ASLEEP = Image.open('img/moon.ppm').convert('1')

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

    def update(self, devices):
        width = self.__display.width
        height = self.__display.height
        image = Image.new('1', (width, height))

        draw = ImageDraw.Draw(image)

        img_x = self.__display.width - 16
        for idx, device in enumerate(devices):
            y = OledDisplay.STEP * idx
            draw.text((0, y + OledDisplay.TEXT_OFFSET), '{:8s} {:2.2f}'.format(device[0], device[1]), font=self.__font, fill=255)
            if device[2] is not None:
                status_image = OledDisplay.AWAKE if device[2] else OledDisplay.ASLEEP
                image.paste(status_image, (img_x, y))

        self.__display.clear()
        self.__display.image(image)
        self.__display.display()

