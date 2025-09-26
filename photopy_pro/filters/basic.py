"""Basic image filters and adjustments."""

import numpy as np
import cv2
from PIL import Image, ImageFilter, ImageChops


def apply_lut_to_pil(pil_img: Image.Image, lut_r, lut_g, lut_b):
    """Applies a lookup table (LUT) to an image."""
    arr = np.array(pil_img.convert("RGBA"), dtype=np.uint8)
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
    r2 = lut_r[r]
    g2 = lut_g[g]
    b2 = lut_b[b]
    out = np.stack([r2, g2, b2, a], axis=-1).astype(np.uint8)
    return Image.fromarray(out, mode="RGBA")


def apply_brightness_contrast(pil_img, brightness, contrast):
    """Applies brightness and contrast adjustments."""
    arr = np.array(pil_img.convert("RGBA"), dtype=np.float32)

    # Brightness (simple linear shift)
    arr[..., :3] += brightness * 2.55

    # Contrast (factor calculation from GIMP)
    f = 131 * (contrast + 127) / (127 * (131 - contrast)) if contrast != -127 else 0
    arr[..., :3] = (arr[..., :3] - 127.5) * f + 127.5

    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def apply_saturation(pil_img, saturation):
    """Applies saturation adjustment."""
    arr = np.array(pil_img.convert("HSV"))
    arr[:, :, 1] = np.clip(arr[:, :, 1] * (1 + saturation / 100), 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "HSV").convert("RGBA")


def apply_blur(pil_img, radius):
    """Applies a Gaussian blur filter."""
    return pil_img.filter(ImageFilter.GaussianBlur(radius))


def apply_sharpen(pil_img, factor):
    """Applies an unsharp mask filter."""
    return pil_img.filter(ImageFilter.UnsharpMask(radius=2, percent=factor, threshold=3))


def edge_detection(pil_img):
    """Performs edge detection using the Sobel operator."""
    gray = pil_img.convert("L")
    gray_arr = np.array(gray)
    sobel_x = cv2.Sobel(gray_arr, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_arr, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    magnitude = magnitude / magnitude.max() * 255 if magnitude.max() > 0 else magnitude
    magnitude = 255 - magnitude.astype(np.uint8)
    return Image.fromarray(magnitude).convert("RGBA")


def apply_sepia(pil_img):
    """Applies a sepia tone filter."""
    arr = np.array(pil_img.convert("RGB"), dtype=np.float32)
    r = arr[..., 0] * 0.393 + arr[..., 1] * 0.769 + arr[..., 2] * 0.189
    g = arr[..., 0] * 0.349 + arr[..., 1] * 0.686 + arr[..., 2] * 0.168
    b = arr[..., 0] * 0.272 + arr[..., 1] * 0.534 + arr[..., 2] * 0.131
    arr[..., 0] = np.clip(r, 0, 255)
    arr[..., 1] = np.clip(g, 0, 255)
    arr[..., 2] = np.clip(b, 0, 255)
    return Image.fromarray(arr.astype(np.uint8)).convert("RGBA")


def apply_posterize(pil_img, bits):
    """Reduces the number of bits for each color channel."""
    arr = np.array(pil_img.convert("RGB"), dtype=np.uint8)
    mask = 0xFF << (8 - bits)
    arr = (arr & mask) | (arr >> (8 - bits))
    return Image.fromarray(arr).convert("RGBA")


def remove_background(pil_img):
    """Simple background removal using flood fill on corners."""
    arr = np.array(pil_img.convert("RGBA"))
    h, w = arr.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # Fill from corners
    cv2.floodFill(arr, mask, (0, 0), (0, 0, 0, 0), flags=cv2.FLOODFILL_FIXED_RANGE)
    cv2.floodFill(arr, mask, (w-1, 0), (0, 0, 0, 0), flags=cv2.FLOODFILL_FIXED_RANGE)
    cv2.floodFill(arr, mask, (0, h-1), (0, 0, 0, 0), flags=cv2.FLOODFILL_FIXED_RANGE)
    cv2.floodFill(arr, mask, (w-1, h-1), (0, 0, 0, 0), flags=cv2.FLOODFILL_FIXED_RANGE)

    return Image.fromarray(arr, "RGBA")


def apply_grayscale(pil_img):
    """Converts the image to grayscale."""
    return pil_img.convert("L").convert("RGBA")


def apply_invert(pil_img):
    """Inverts the colors of the image."""
    return ImageChops.invert(pil_img.convert("RGB")).convert("RGBA")


def apply_emboss(pil_img):
    """Applies an emboss filter."""
    return pil_img.filter(ImageFilter.EMBOSS)


def apply_sketch(pil_img):
    """Applies a contour (sketch) filter."""
    return pil_img.filter(ImageFilter.CONTOUR)