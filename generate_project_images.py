"""
Generate professional project showcase images with modern design.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def create_project_image(filename, title, subtitle, color1, color2, accent_color):
    """Create a professional project showcase image with modern design."""
    width, height = 800, 500

    # Create image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Draw subtle gradient background
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    for y in range(height):
        r = int(r1 + (r2 - r1) * (y / height))
        g = int(g1 + (g2 - g1) * (y / height))
        b = int(b1 + (b2 - b1) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add subtle grid pattern for tech feel
    grid_spacing = 40
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 8), width=1)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill=(255, 255, 255, 8), width=1)

    # Add floating glass-morphism cards (decorative elements)
    # Top-right card
    card1_x, card1_y = 580, 50
    card1_w, card1_h = 180, 100
    draw.rounded_rectangle([card1_x, card1_y, card1_x + card1_w, card1_y + card1_h], 
                          radius=12, fill=(255, 255, 255, 30))
    draw.rounded_rectangle([card1_x, card1_y, card1_x + card1_w, card1_y + card1_h], 
                          radius=12, outline=(255, 255, 255, 60), width=2)
    
    # Bottom-left card
    card2_x, card2_y = 40, 360
    card2_w, card2_h = 140, 90
    draw.rounded_rectangle([card2_x, card2_y, card2_x + card2_w, card2_y + card2_h], 
                          radius=12, fill=(255, 255, 255, 25))
    draw.rounded_rectangle([card2_x, card2_y, card2_x + card2_w, card2_y + card2_h], 
                          radius=12, outline=(255, 255, 255, 50), width=2)

    # Add decorative circles
    draw.ellipse([700, 380, 780, 460], fill=accent_color + (40,))
    draw.ellipse([50, 60, 120, 130], fill=accent_color + (30,))

    # Add accent line at top
    draw.rectangle([0, 0, width, 6], fill=accent_color)

    # Add title text (centered, prominent)
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 48)
    except:
        font_title = ImageFont.load_default()

    try:
        font_subtitle = ImageFont.truetype("arial.ttf", 24)
    except:
        font_subtitle = ImageFont.load_default()

    # Draw title with better positioning
    bbox = draw.textbbox((0, 0), title, font=font_title)
    text_width = bbox[2] - bbox[0]
    title_x = (width - text_width) // 2
    title_y = 150

    # Add subtle shadow for title
    for offset in [3, 2, 1]:
        draw.text((title_x + offset, title_y + offset), title, fill=(0, 0, 0, 40), font=font_title)
    
    # Main title text
    draw.text((title_x, title_y), title, fill='white', font=font_title)

    # Draw subtitle (centered)
    bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    text_width = bbox[2] - bbox[0]
    subtitle_x = (width - text_width) // 2
    subtitle_y = 230
    draw.text((subtitle_x, subtitle_y), subtitle, fill=(235, 235, 235), font=font_subtitle)

    # Add elegant separator line
    line_width = 100
    line_y = subtitle_y + 50
    line_x = (width - line_width) // 2
    draw.line([(line_x, line_y), (line_x + line_width, line_y)], fill=(255, 255, 255, 180), width=2)
    
    # Add small accent dots
    dot_size = 3
    draw.ellipse([line_x - 15 - dot_size, line_y - dot_size, line_x - 15 + dot_size, line_y + dot_size], fill=(255, 255, 255, 200))
    draw.ellipse([line_x + line_width + 15 - dot_size, line_y - dot_size, line_x + line_width + 15 + dot_size, line_y + dot_size], fill=(255, 255, 255, 200))

    # Save image
    img.save(filename, 'PNG', quality=95)
    print(f"✓ Created: {filename}")

# Define project configurations with professional color schemes
projects = [
    {
        'filename': 'project_ecommerce.png',
        'title': 'E-Commerce Platform',
        'subtitle': 'Full-Stack Online Shopping Experience',
        'color1': (79, 70, 229),      # Deep indigo
        'color2': (124, 58, 237),     # Rich purple
        'accent_color': (236, 72, 153),  # Pink accent
    },
    {
        'filename': 'project_taskmanager.png',
        'title': 'Task Management App',
        'subtitle': 'Collaborative Productivity Tool',
        'color1': (13, 148, 136),     # Deep teal
        'color2': (20, 184, 166),     # Bright teal
        'accent_color': (6, 182, 212),   # Cyan accent
    },
    {
        'filename': 'project_apigateway.png',
        'title': 'API Gateway Service',
        'subtitle': 'Microservices Architecture',
        'color1': (220, 38, 38),      # Deep red
        'color2': (239, 68, 68),      # Bright red
        'accent_color': (251, 146, 60),  # Orange accent
    }
]

# Create media/projects directory if it doesn't exist
media_dir = os.path.join(os.path.dirname(__file__), 'media', 'projects')
os.makedirs(media_dir, exist_ok=True)

# Generate all project images
for project in projects:
    filepath = os.path.join(media_dir, project['filename'])
    create_project_image(
        filename=filepath,
        title=project['title'],
        subtitle=project['subtitle'],
        color1=project['color1'],
        color2=project['color2'],
        accent_color=project['accent_color']
    )

print(f"\n✓ All {len(projects)} professional project images created successfully!")
print(f"Location: {media_dir}")
