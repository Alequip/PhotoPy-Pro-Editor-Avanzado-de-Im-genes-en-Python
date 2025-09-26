"""Blend modes and layer compositing utilities."""

from PIL import Image, ImageChops


def blend_images(base_img, top_img, blend_mode):
    """Blends two images using various blend modes."""
    # Ensure images have the same size and mode
    if base_img.size != top_img.size:
        top_img = top_img.resize(base_img.size, Image.Resampling.LANCZOS)

    base_img = base_img.convert("RGBA")
    top_img = top_img.convert("RGBA")

    if blend_mode == "normal":
        return Image.alpha_composite(base_img, top_img)

    # Blending functions from Pillow
    if blend_mode == "multiply":
        blended = ImageChops.multiply(base_img, top_img)
    elif blend_mode == "screen":
        blended = ImageChops.screen(base_img, top_img)
    elif blend_mode == "overlay":
        blended = ImageChops.overlay(base_img, top_img)
    elif blend_mode == "add":
        blended = ImageChops.add(base_img, top_img, 1.0, 0)
    elif blend_mode == "subtract":
        blended = ImageChops.subtract(base_img, top_img, 1.0, 0)
    elif blend_mode == "difference":
        blended = ImageChops.difference(base_img, top_img)
    elif blend_mode == "darker":
        blended = ImageChops.darker(base_img, top_img)
    elif blend_mode == "lighter":
        blended = ImageChops.lighter(base_img, top_img)
    else:
        blended = base_img

    # Preserve alpha from top image
    if top_img.mode == "RGBA":
        alpha = top_img.split()[-1]
        blended.putalpha(alpha)

    return blended