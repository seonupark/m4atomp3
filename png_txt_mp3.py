from moviepy.editor import *
import os
from PIL import Image, ImageDraw, ImageFont

FONT_SIZE = 80
LINE_SPACING = int(FONT_SIZE * 0.5)
MAX_CHARS_PER_LINE = 24

def read_text_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            return txt_file.read()
    except FileNotFoundError:
        return "내용이 없습니다."

def create_black_image(width, height):
    return Image.new("RGB", (width, height), "black")

def draw_text(draw, text, position, font, fill,LINE_SPACING):
    draw.text(position, text, font=font, fill=fill, spacing=LINE_SPACING)

def wrap_text(text, max_chars_per_line=MAX_CHARS_PER_LINE):
    lines = []
    current_line = ""

    for char in text:
        if char == "-" or len(current_line) == max_chars_per_line:
            lines.append(current_line)
            current_line = "" if char == "-" else char
        else:
            current_line += char

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)

def process_file(file):
    if not file.endswith(".m4a"):
        return

    base_name, ext = os.path.splitext(file)

    # Read content from text file
    text_content = read_text_content(base_name + ".txt")

    # Create image and draw text
    im = create_black_image(1920, 1080)
    draw = ImageDraw.Draw(im)

    # Add the file name to the top of the image
    font = ImageFont.truetype("HMKMRHD.TTF", FONT_SIZE)
    draw_text(draw, base_name, ((im.width - draw.textsize(base_name, font)[0]) // 2, 50), font, (173, 216, 230),LINE_SPACING)

    # Automatic line break (every 20 characters or when "-" is encountered)
    wrapped_text = wrap_text(text_content)
    draw_text(draw, wrapped_text, (100, 250), font, (255, 255, 224),LINE_SPACING)

    im.save(base_name + ".png")

    # Create video clip
    audio = AudioFileClip(base_name + ".m4a")
    video = ImageClip(base_name + ".png", duration=audio.duration)
    video = video.set_audio(audio)

    # Create video file
    video.write_videofile(base_name + ".mp4", fps=24, codec="libx264")

if __name__ == "__main__":
    file_list = [file for file in os.listdir() if file.endswith(".m4a")]

    for file in file_list:
        process_file(file)