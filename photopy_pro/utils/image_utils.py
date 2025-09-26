"""Image conversion utilities between PIL and Qt formats."""

import io
from PIL import Image, ImageQt
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QBuffer, QIODevice


def pil_image_to_qpixmap(pil_img: Image.Image) -> QPixmap:
    """Converts a PIL Image to a PyQt QPixmap."""
    if pil_img.mode != "RGBA":
        pil_img = pil_img.convert("RGBA")
    qim = ImageQt.ImageQt(pil_img)
    return QPixmap.fromImage(qim)


def qpixmap_to_pil_image(pix: QPixmap) -> Image.Image:
    """Converts a PyQt QPixmap to a PIL Image."""
    qimg = pix.toImage()
    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    qimg.save(buffer, "PNG")
    pil_img = Image.open(io.BytesIO(buffer.data()))
    return pil_img