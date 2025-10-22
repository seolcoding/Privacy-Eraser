"""Generate app icon for Privacy Eraser

Creates a simple icon with a broom and shield design.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# App color (Primary color from UI)
PRIMARY_COLOR = "#2563EB"
BG_COLOR = "#FFFFFF"


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_icon(size):
    """Create a simple icon with eraser + lock design

    Args:
        size: Icon size (width and height)

    Returns:
        PIL Image object
    """
    # Create image with white background
    img = Image.new('RGB', (size, size), hex_to_rgb(BG_COLOR))
    draw = ImageDraw.Draw(img)

    # Convert colors
    primary = hex_to_rgb(PRIMARY_COLOR)

    # Calculate sizes relative to canvas
    margin = size // 8
    center_x, center_y = size // 2, size // 2

    # Draw shield (background shape)
    shield_top = margin
    shield_bottom = size - margin
    shield_left = margin
    shield_right = size - margin

    # Shield outline
    shield_points = [
        (center_x, shield_top),  # Top point
        (shield_right, shield_top + margin),  # Top right
        (shield_right, center_y),  # Right middle
        (center_x, shield_bottom),  # Bottom point
        (shield_left, center_y),  # Left middle
        (shield_left, shield_top + margin),  # Top left
    ]

    # Fill shield
    draw.polygon(shield_points, fill=primary, outline=primary)

    # Draw broom handle (white line)
    broom_start_y = shield_top + margin * 2
    broom_end_y = shield_bottom - margin
    broom_x = center_x + margin // 2

    line_width = max(2, size // 32)
    draw.line(
        [(broom_x, broom_start_y), (broom_x, broom_end_y)],
        fill=BG_COLOR,
        width=line_width
    )

    # Draw broom bristles (white triangular shape)
    bristle_width = margin
    bristle_height = margin * 2
    bristle_top = shield_bottom - margin * 3

    bristle_points = [
        (broom_x - bristle_width // 2, bristle_top),
        (broom_x + bristle_width // 2, bristle_top),
        (broom_x, bristle_top + bristle_height),
    ]
    draw.polygon(bristle_points, fill=BG_COLOR, outline=BG_COLOR)

    return img


def main():
    """Generate all icon sizes"""
    print("Generating Privacy Eraser icons...")

    # Icon sizes
    sizes = [16, 32, 64, 128, 256]

    # Output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'icons')
    os.makedirs(output_dir, exist_ok=True)

    # Generate PNG icons for each size
    images = []
    for size in sizes:
        img = create_icon(size)
        png_path = os.path.join(output_dir, f'app_icon_{size}.png')
        img.save(png_path, 'PNG')
        print(f"  Created: {png_path}")
        images.append(img)

    # Save largest as main PNG icon
    main_icon = create_icon(256)
    main_png_path = os.path.join(output_dir, 'app_icon.png')
    main_icon.save(main_png_path, 'PNG')
    print(f"  Created: {main_png_path}")

    # Create ICO file with multiple sizes (Windows)
    ico_path = os.path.join(output_dir, 'app_icon.ico')
    main_icon.save(ico_path, format='ICO', sizes=[(s, s) for s in sizes])
    print(f"  Created: {ico_path}")

    print("\n✓ Icon generation complete!")
    print(f"  Location: {output_dir}")
    print("\nNext steps:")
    print("  1. Review the generated icons")
    print("  2. Replace with custom-designed icons if desired")
    print("  3. Icons are already integrated into the app")


if __name__ == '__main__':
    main()
