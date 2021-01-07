from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random


class ValidCodeImg:
    def __init__(self, width=140, height=35, code_count=5, font_size=32, point_count=20, line_count=3,
                 img_format='png'):
        self.width = width
        self.height = height
        self.code_count = code_count
        self.font_size = font_size
        self.point_count = point_count
        self.line_count = line_count
        self.img_format = img_format

    def getRandomColor(self):
        c1 = random.randint(0, 255)
        c2 = random.randint(0, 255)
        c3 = random.randint(0, 255)
        return c1, c2, c3

    def getRandomStr(self):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        return random_char

    def getValidCodeImg(self):
        image = Image.new('RGB', (self.width, self.height), self.getRandomColor())

        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype("GIGI.TTF", size=self.font_size)

        valid_str = ''
        for i in range(self.code_count):
            random_char = self.getRandomStr()

            draw.text((10 + i * 30, -2), random_char, self.getRandomColor(), font=font)

            valid_str += random_char

        for i in range(self.line_count):
            x1 = random.randint(0, self.width)
            x2 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            y2 = random.randint(0, self.height)
            draw.line((x1, y1, x2, y2), fill=self.getRandomColor())

        for i in range(self.point_count):
            draw.point([random.randint(0, self.width), random.randint(0, self.height)], fill=self.getRandomColor())
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.getRandomColor())

        f = BytesIO()
        image.save(f, self.img_format)

        return f, valid_str
