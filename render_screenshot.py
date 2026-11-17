import os
import sys
from PIL import Image, ImageDraw, ImageFont

def render_terminal_screenshot(text_path, output_png_path, title="Terminal Output"):
    raw_bytes = open(text_path, "rb").read()
    if raw_bytes.startswith(b'\xff\xfe') or raw_bytes.startswith(b'\xfe\xff'):
        content = raw_bytes.decode('utf-16', errors='replace')
    else:
        try:
            content = raw_bytes.decode('utf-8')
        except UnicodeDecodeError:
            content = raw_bytes.decode('latin-1', errors='replace')
    lines = content.splitlines(keepends=True)

    # Font setup
    font_path = "C:\\Windows\\Fonts\\consola.ttf"
    if not os.path.exists(font_path):
        font_path = "C:\\Windows\\Fonts\\lucon.ttf"
    
    font_size = 15
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        font = ImageFont.load_default()

    # Calculate dimensions
    max_line_len = max([len(line.rstrip('\r\n')) for line in lines] + [len(title) + 10, 60])
    char_width = 9.2
    line_height = 22
    
    padding_x = 24
    padding_y = 20
    header_height = 40
    
    img_width = int(max(max_line_len * char_width + padding_x * 2, 650))
    img_height = int(len(lines) * line_height + padding_y * 2 + header_height)

    # Background color (Dark terminal theme)
    bg_color = (30, 30, 30)
    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    # Window title bar
    bar_color = (45, 45, 48)
    draw.rectangle([0, 0, img_width, header_height], fill=bar_color)

    # Window controls (macOS/modern style dots)
    dot_y = header_height // 2
    draw.ellipse([16, dot_y - 6, 28, dot_y + 6], fill=(255, 95, 86))    # Red
    draw.ellipse([36, dot_y - 6, 48, dot_y + 6], fill=(255, 189, 46))   # Yellow
    draw.ellipse([56, dot_y - 6, 68, dot_y + 6], fill=(39, 201, 63))    # Green

    # Window Title
    title_font_size = 13
    try:
        title_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", title_font_size)
    except Exception:
        title_font = font
    draw.text((80, dot_y - 8), title, fill=(200, 200, 200), font=title_font)

    # Content
    y = header_height + padding_y
    for line in lines:
        raw_line = line.rstrip('\r\n')
        # Simple color highlighting for headers / errors / successes
        text_color = (220, 220, 220)
        if "ERROR" in raw_line or "Exception" in raw_line or "Fail" in raw_line or "Cause" in raw_line:
            text_color = (255, 110, 110)
        elif "SUCCESS" in raw_line or "PASS" in raw_line or "Saved" in raw_line or "Seats sold" in raw_line:
            text_color = (130, 240, 130)
        elif "===" in raw_line or "---" in raw_line or "[" in raw_line and "]" in raw_line:
            text_color = (100, 180, 255)
        
        draw.text((padding_x, y), raw_line, fill=text_color, font=font)
        y += line_height

    img.save(output_png_path, "PNG")
    print(f"Rendered: {output_png_path}")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        title = sys.argv[3] if len(sys.argv) > 3 else "Terminal Output"
        render_terminal_screenshot(sys.argv[1], sys.argv[2], title)
