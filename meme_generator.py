from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

TEMPLATE_DIR = "templates"
FONT_PATH = os.path.join(TEMPLATE_DIR, "DejaVuSans-Bold.ttf")


def get_dynamic_font(draw, line, image_width, font_path, initial_size=40, margin=40, stroke_width=2):
    font_size = initial_size
    while font_size > 12:
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=stroke_width)
        line_width = bbox[2] - bbox[0]
        if line_width + margin * 2 < image_width:
            return font
        font_size -= 2
    return ImageFont.truetype(font_path, 12)


def draw_text(draw, text, y, image_width, font_path, fill="white", stroke_fill="black", stroke_width=2, margin=40):
    lines = []
    fonts = []
    total_height = 0

    for paragraph in text.split('\n'):
        # Choose a starting font size
        base_font = get_dynamic_font(draw, paragraph, image_width, font_path, initial_size=int(image_width / 10), margin=margin, stroke_width=stroke_width)

        # Estimate wrap width from font size
        wrap_width = max(10, image_width // (base_font.size // 2))
        wrapped = textwrap.wrap(paragraph, width=wrap_width)

        for line in wrapped:
            font = get_dynamic_font(draw, line, image_width, font_path, initial_size=base_font.size, margin=margin, stroke_width=stroke_width)
            fonts.append(font)
            lines.append(line)
            bbox = draw.textbbox((0, 0), line, font=font, stroke_width=stroke_width)
            height = bbox[3] - bbox[1]
            total_height += height + 5

    # Draw centered lines
    y_start = y
    for i, line in enumerate(lines):
        font = fonts[i]
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=stroke_width)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        x = (image_width - line_width) // 2
        draw.text((x, y_start), line, font=font, fill=stroke_fill, stroke_width=stroke_width)
        draw.text((x, y_start), line, font=font, fill=fill)
        y_start += line_height + 5


def create_meme(template_filename: str, top_text: str, bottom_text: str, output_path="output_meme.jpg"):
    template_path = os.path.join(TEMPLATE_DIR, template_filename)
    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    image_width, image_height = img.size

    # Uppercase for meme style
    top_text = top_text.strip().upper()
    bottom_text = bottom_text.strip().upper()
    margin = int(image_height * 0.05)

    # Draw top text
    draw_text(
        draw,
        top_text,
        y=margin,
        image_width=image_width,
        font_path=FONT_PATH,
        margin=margin,
    )

    # Measure and wrap bottom text to calculate vertical space
    bottom_lines = []
    bottom_fonts = []
    total_text_height = 0
    for paragraph in bottom_text.split('\n'):
        base_font = get_dynamic_font(draw, paragraph, image_width, FONT_PATH, int(image_width / 10), margin)
        wrap_width = max(10, image_width // (base_font.size // 2))
        wrapped = textwrap.wrap(paragraph, width=wrap_width)
        for line in wrapped:
            font = get_dynamic_font(draw, line, image_width, FONT_PATH, base_font.size, margin)
            bottom_fonts.append(font)
            bottom_lines.append(line)
            bbox = draw.textbbox((0, 0), line, font=font, stroke_width=2)
            total_text_height += (bbox[3] - bbox[1]) + 5

    bottom_y = image_height - total_text_height - margin

    draw_text(
        draw,
        bottom_text,
        y=bottom_y,
        image_width=image_width,
        font_path=FONT_PATH,
        margin=margin,
    )

    img.save(output_path)
    return output_path
