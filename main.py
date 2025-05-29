import os
from math import ceil
from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)

#ASCII characters mapped by intensity (ordered darkest to lightest)
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " ", "░", "▒", "▓", "█"]

IMAGE_PATH = "./Anime.jpg"

PIL_WIDTH_INDEX = 0
PIL_HEIGHT_INDEX = 1

#font path - macOS
FONT_FILENAMES = [
    '/System/Library/Fonts/Menlo.ttc'  #modify as per your OS
]

def resize_image(image, new_width=350):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height))

def open_image(image_path):
    try:
        return Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"Error opening image: {e}")

def image_to_ascii_colored(image, new_width=350):
    image = resize_image(image, new_width)
    pixels = list(image.getdata())  
    width = image.width

    ascii_data = []
    for i, pixel in enumerate(pixels):
        r, g, b = pixel[:3]
        gray = int((r + g + b) / 3)
        char = ASCII_CHARS[gray * len(ASCII_CHARS) // 256]
        ascii_data.append((char, (r, g, b)))

    ascii_lines = []
    for i in range(0, len(ascii_data), width):
        ascii_lines.append(ascii_data[i:i + width])

    return ascii_lines 

def ascii_to_image_colored(ascii_lines, output_image_path):
    font = None
    font_size = 16  #adjust size as needed

    for font_filename in FONT_FILENAMES:
        try:
            font = ImageFont.truetype(font_filename, font_size)
            print(f'Using font "{font_filename}".')
            break
        except IOError:
            print(f'Could not load font "{font_filename}". Trying next.')

    if font is None:
        font = ImageFont.load_default()
        print('Using default font.')

    line_height = font.getbbox("A")[3]
    char_width = font.getbbox("A")[2]
    padding = 10

    max_line_length = max(len(line) for line in ascii_lines)
    image_width = max_line_length * char_width + 2 * padding
    image_height = len(ascii_lines) * line_height + 2 * padding

    #create transparent background image
    image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    for i, line in enumerate(ascii_lines):
        for j, (char, color) in enumerate(line):
            x = padding + j * char_width
            y = padding + i * line_height
            draw.text((x, y), char, font=font, fill=color + (255,))  # RGBA

    image.save(output_image_path, "PNG")
    print(f"Colored ASCII art saved as image: {output_image_path}")

def main():
    img = open_image(IMAGE_PATH)
    if img:
        ascii_colored = image_to_ascii_colored(img)
        ascii_to_image_colored(ascii_colored, './ascii_art_colored.png')

if __name__ == "__main__":
    main()
