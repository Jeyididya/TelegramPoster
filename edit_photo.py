import textwrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageColor


class COLOR:
    def __init__(self, color):
        self.color = color
        self.composite = ""

    def rgb2hex(self, color):
        return '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])

    def get_composite(self):
        """Get Composote
        """
        _color = self.color
        if _color[0] == "#":
            _color = _color[1:]
        if len(_color) == 3:
            _color = _color[0] + _color[0] + _color[1] + \
                _color[1] + _color[2] + _color[2]
        if len(_color) != 6:
            print("INVALID color")
        r = 255-int(_color[0:2], 16)
        g = 255-int(_color[2:4], 16)
        b = 255-int(_color[4:6], 16)

        self.composite = self.rgb2hex((r, g, b))
        return self.composite


class EDIT_IMAGE:
    """
    Class To Edit Image

    """

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(self.image_path)
        self.image_width, self.image_height = self.image.size
        self.image_color = ""
        self.get_image_color()

    def get_image_color(self):
        color_code = self.image_path.split("_")[1].split(".")[0]
        # print("color->",color_code)
        self.image_color = color_code

    def get_image_brightness(self):
        """
        Get the overall brightness of the image.
        Returns a value between 0 (black) and 255 (white).
        """
        image_grayscale = self.image.convert("L")
        histogram = image_grayscale.histogram()
        pixels = sum(histogram)
        brightness = scale = len(histogram)

        for index in range(0, scale):
            ratio = histogram[index] / pixels
            brightness += ratio * (-scale + index)

        return 255 * brightness // scale

    def get_text_color(self):
        # Calculate the overall brightness of the image
        image_brightness = self.get_image_brightness()

        # Set a threshold to decide between black and white text
        threshold = 128

        # If the image is bright, use black text; otherwise, use white text
        if image_brightness > threshold:
            return "#000000"  # Black
        else:
            return "#FFFFFF"  # White

    def get_stroke_color(self, color):
        r, g, b = ImageColor.getcolor(color, "RGB")  # type: ignore
        if (r * 0.299 + g * 0.587 + b * 0.114) > 186:
            return '#000000'
        else:
            return '#FFFFFF'

    def add_text(self, text, author):
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype(
            "./fonts/ugly_betty.ttf", self.image_width//32)
        lines = textwrap.fill(text, 56).split('\n')

        text_y = self.image_height//2+self.image_height//6

        for line in lines:
            # width, height = draw.textsize(line, font=font)
            width = font.getmask(line).getbbox()[
                2] - font.getmask(line).getbbox()[0]
            height = font.getmask(line).getbbox()[
                3] - font.getmask(line).getbbox()[1]

            text_x = (self.image_width-width)//2

            draw.text((text_x, text_y), line, font=font, fill=self.get_text_color(),
                      stroke_fill=self.get_stroke_color(self.image_color), stroke_width=5, align="center")
            text_y += height

        # draw author
        print(author)
        author_text_width = font.getmask(author).getbbox()[
            2] - font.getmask(author).getbbox()[0]
        author_text_height = font.getmask(author).getbbox()[
            3] - font.getmask(author).getbbox()[1]
        # width, height = draw.textsize("-"+str(author), font=font)

        author_text_x = (self.image_width-author_text_width)//2
        author_text_y = self.image_height // 8

        draw.text((author_text_x, author_text_y), "-"+str(author), font=font, fill=self.get_text_color(),
                  stroke_fill=self.get_stroke_color(self.image_color), stroke_width=5)  # type: ignore
        file_name = self.save_image()

        return file_name

    def save_image(self):
        # print("name->",self.image_path.split("/")[-1])
        self.image.save("./photos/EDIT "+self.image_path.split("/")[-1])
        return ("./photos/EDIT "+self.image_path.split("/")[-1])
        # print("saved")

# text="Why do I keep repeating harmful behaviors/habits when I know they are bad for me?” Because they give you pleasure or help you avoid discomfort. And you are too weak to let go of a little pleasure or to bear a little discomfort"
# auth="sir me and i"

# im=EDIT_IMAGE("Black-haired Boy Crying by Kat Smith_#2F2F2F.jpg")
# im.add_text(text,auth)
