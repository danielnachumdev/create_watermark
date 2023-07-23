import math
from typing import Literal
from PIL import Image, ImageDraw, ImageFont, ImageOps
from danielutils import frange
DPI: int = 300
TEXTS: list[str] = [
    "Lorem ipsum", "dolor sit"
]
OPACITY: float = 0  # value in [0,1]
FONT_NAME: str = "arial"
FONT_SIZE: int = int(DPI/3)
TEXT_COLOR: str | tuple[int, int, int] = "gray"
ANGLE: int = 45
SPACER: str = "     "
REPETITIONS: int = 8
ROW_SPACING: int = DPI*1.3
START_Y_OFFSET: int = 0


def create_image(mode: Literal["RGB", "RGBA"] = "RGBA", bg_color: tuple = (255, 255, 255, 255)) -> Image:
    AR_INCHES = (8.27, 11.69)
    A4 = (int(AR_INCHES[0]*DPI), int(AR_INCHES[1]*DPI))
    width, height = A4
    return Image.new(mode, (width, height), color=bg_color)


def to_rgba(img: Image) -> Image:
    return img.convert("RGBA")


def set_pixel(img: Image, coor: tuple[int, int], rgba: tuple[int, int, int, int]) -> None:
    pixel_access = img.load()
    x, y = coor
    pixel_access[x, y] = rgba


def set_opacity(img: Image, percentage: float, relative: bool = False) -> Image:
    tmp = to_rgba(img)
    absolute_opacity = int(255*percentage)
    data = tmp.getdata()
    new_data = []
    for item in data:
        new_data.append(
            (*item[:3], absolute_opacity if not relative else int(percentage*item[3])))
    tmp.putdata(new_data)
    return tmp


def get_font(name: str, size: int):
    return ImageFont.truetype(f"C:\\Windows\\Fonts\\{name}.ttf", size)


def draw_text(img: Image, text: str, coor: tuple[int, int], *, angle: float = 0, color: tuple[int, int, int] | str = (0, 0, 0), is_degrees: bool = True, font_name: str = "arial", font_size: int = 40):
    if not is_degrees:
        angle *= 180/math.pi
    rads = angle/180*math.pi
    font = get_font(font_name, font_size)
    bbox = ImageDraw.Draw(img).textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tmp_image = Image.new('L', (w, h+font_size))
    ImageDraw.Draw(tmp_image).text((0, 0), text,  font=font, fill=255)
    r_img = tmp_image.rotate(angle,  expand=1)
    x, y = coor
    x += (w/2 - r_img.size[0]/2)
    y += (h/2-r_img.size[1]/2)
    d_x = w/2 - w/2*math.cos(rads)
    d_y = w/2*math.sin(rads)
    pos = (int(x-d_x), int(y-d_y))
    img.paste(ImageOps.colorize(r_img, (0, 0, 0), color), pos, r_img)


def main():
    print("for different results see parameters at the top of the file")
    img = create_image(bg_color=(255, 255, 255, int(255*OPACITY)))
    text_i = 0
    for y in frange(START_Y_OFFSET, img.size[1]*2, ROW_SPACING):
        text = TEXTS[text_i]
        text = SPACER.join([text]*REPETITIONS)
        bbox = ImageDraw.Draw(img).textbbox(
            (0, 0), text, font=get_font(FONT_NAME, FONT_SIZE))
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        y_delta = 0
        # for y_delta in range(0, 1, w):
        draw_text(img, text, (y_delta, y-y_delta),
                  angle=ANGLE, font_size=FONT_SIZE, color=TEXT_COLOR)
        text_i = (text_i+1) % len(TEXTS)
    img.save(f"watermark{int(100*OPACITY)}.png")
    # for opacity in frange(0.1, 1.01, 0.1):
    #     name = f"watermark{int(opacity*100)}.png"
    #     print(f"Creating {name}")
    #     tmp = set_opacity(img, opacity)
    #     tmp.save(f"./{name}")


if __name__ == "__main__":
    main()
