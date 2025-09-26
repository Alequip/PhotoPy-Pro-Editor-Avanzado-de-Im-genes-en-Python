"""Image transformation utilities."""

import numpy as np
import cv2
from PIL import Image


def perspective_transform(pil_img, src_points, dst_points):
    """Performs a perspective transformation."""
    src = np.array(src_points, dtype=np.float32)
    dst = np.array(dst_points, dtype=np.float32)
    M = cv2.getPerspectiveTransform(src, dst)
    arr = np.array(pil_img.convert("RGB"))
    transformed = cv2.warpPerspective(arr, M, (pil_img.width, pil_img.height))
    return Image.fromarray(transformed).convert("RGBA")


def warp_image(pil_img, amplitude=10, frequency=0.05):
    """Applies a wave-like warp effect."""
    arr = np.array(pil_img.convert("RGB"))
    rows, cols = arr.shape[0], arr.shape[1]
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))
    dx = amplitude * np.sin(2 * np.pi * frequency * y)
    dy = amplitude * np.cos(2 * np.pi * frequency * x)
    map_x = (x + dx).astype(np.float32)
    map_y = (y + dy).astype(np.float32)
    warped = cv2.remap(arr, map_x, map_y, cv2.INTER_LINEAR)
    return Image.fromarray(warped).convert("RGBA")