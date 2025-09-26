"""Artistic effects and creative filters."""

import numpy as np
import cv2
from PIL import Image


def apply_oil_painting(pil_img, brush_size=7, roughness=4):
    """Applies a simple oil painting effect."""
    arr = np.array(pil_img.convert("RGB"))
    h, w, _ = arr.shape
    out = np.zeros_like(arr)

    for y in range(h):
        for x in range(w):
            y1, y2 = max(0, y - brush_size), min(h, y + brush_size + 1)
            x1, x2 = max(0, x - brush_size), min(w, x + brush_size + 1)
            region = arr[y1:y2, x1:x2]

            # Using reshape and unique for more robust common color finding
            colors, counts = np.unique(region.reshape(-1, 3), axis=0, return_counts=True)
            most_common = colors[np.argmax(counts)]

            if roughness > 0:
                noise = np.random.randint(-roughness, roughness + 1, 3)
                most_common = np.clip(most_common + noise, 0, 255)
            out[y, x] = most_common

    return Image.fromarray(out).convert("RGBA")


def apply_watercolor(pil_img):
    """Applies a simple watercolor effect."""
    arr = np.array(pil_img.convert("RGB"))
    blurred = cv2.GaussianBlur(arr, (15, 15), 0)
    edges = cv2.Canny(arr, 100, 200)
    edges = cv2.dilate(edges, None, iterations=1)
    edges = cv2.erode(edges, None, iterations=1)

    # Convert edges to 3-channel and create mask
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    mask = edges_bgr.astype(bool)

    # Combine original and blurred based on edge mask
    result = np.where(mask, arr, blurred)
    return Image.fromarray(result).convert("RGBA")