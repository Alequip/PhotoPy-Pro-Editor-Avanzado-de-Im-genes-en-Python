"""Selection tools and management."""

import numpy as np
import cv2
from PIL import Image, ImageDraw
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor, QPainterPath
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsPathItem, QGraphicsPixmapItem
from PyQt6.QtGui import QImage, QPixmap
from ..utils.image_utils import qpixmap_to_pil_image


class SelectionManager:
    """Manages different types of selections in the image editor."""

    MODE_RECTANGLE = 0
    MODE_ELLIPSE = 1
    MODE_FREEHAND = 2
    MODE_MAGIC_WAND = 3

    def __init__(self, canvas):
        self.canvas = canvas
        self.current_mode = self.MODE_RECTANGLE
        self.selection_item = None
        self.feather = 5
        self.tolerance = 15

        self.start_point = None
        self.current_path = None

    def clear_selection(self):
        """Clear the current selection."""
        if self.selection_item:
            self.canvas.scene.removeItem(self.selection_item)
            self.selection_item = None

    def mouse_press(self, event):
        """Handle mouse press events for selection tools."""
        self.start_point = self.canvas.mapToScene(event.pos())
        self.clear_selection()

        if self.current_mode == self.MODE_FREEHAND:
            self.current_path = QPainterPath(self.start_point)
            self.selection_item = QGraphicsPathItem(self.current_path)
        elif self.current_mode != self.MODE_MAGIC_WAND:
            from PyQt6.QtCore import QRectF
            self.selection_item = QGraphicsRectItem(QRectF(self.start_point, self.start_point))

        if self.selection_item:
            pen = QPen(QColor(255, 255, 255, 150), 1, Qt.PenStyle.DashLine)
            pen.setDashPattern([3, 3])
            self.selection_item.setPen(pen)
            self.canvas.scene.addItem(self.selection_item)
            self.selection_item.setZValue(10)

    def mouse_move(self, event):
        """Handle mouse move events for selection tools."""
        if not self.start_point or not self.selection_item:
            return

        current_pos = self.canvas.mapToScene(event.pos())

        if self.current_mode == self.MODE_RECTANGLE:
            from PyQt6.QtCore import QRectF
            rect = QRectF(self.start_point, current_pos).normalized()
            self.selection_item.setRect(rect)
        elif self.current_mode == self.MODE_ELLIPSE:
            from PyQt6.QtCore import QRectF
            rect = QRectF(self.start_point, current_pos).normalized()
            self.selection_item.setRect(rect)
        elif self.current_mode == self.MODE_FREEHAND:
            self.current_path.lineTo(current_pos)
            self.selection_item.setPath(self.current_path)

    def mouse_release(self, event):
        """Handle mouse release events for selection tools."""
        if self.current_mode == self.MODE_MAGIC_WAND:
            point = self.canvas.mapToScene(event.pos())
            self.magic_wand_selection(point)

        self.start_point = None
        self.current_path = None

    def magic_wand_selection(self, point):
        """Create a selection using magic wand (flood fill) algorithm."""
        pil_img = self.canvas.pil_image
        if not pil_img:
            return

        img_array = np.array(pil_img)
        x, y = int(point.x()), int(point.y())

        # Check boundaries
        if not (0 <= x < pil_img.width and 0 <= y < pil_img.height):
            return

        target_color = tuple(img_array[y, x, :3])

        mask = np.zeros((img_array.shape[0] + 2, img_array.shape[1] + 2), dtype=np.uint8)

        # Use floodFill to get the selection mask
        cv2.floodFill(
            image=img_array,
            mask=mask,
            seedPoint=(x, y),
            newVal=(0, 0, 0),
            loDiff=(self.tolerance,)*3,
            upDiff=(self.tolerance,)*3,
            flags=4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY
        )

        mask = mask[1:-1, 1:-1]

        if self.feather > 0:
            mask = cv2.GaussianBlur(mask, (self.feather*2+1, self.feather*2+1), 0)

        qimage = QImage(mask.data, mask.shape[1], mask.shape[0], QImage.Format.Format_Grayscale8)
        self.selection_item = QGraphicsPixmapItem(QPixmap.fromImage(qimage))
        self.canvas.scene.addItem(self.selection_item)
        self.selection_item.setZValue(10)

    def get_selection_mask(self):
        """Get the selection as a PIL mask image."""
        pil_img = self.canvas.pil_image
        if not pil_img or not self.selection_item:
            return Image.new("L", (1, 1), 255)

        mask = Image.new("L", pil_img.size, 0)
        draw = ImageDraw.Draw(mask)

        if isinstance(self.selection_item, QGraphicsRectItem):
            rect = self.selection_item.rect().normalized()
            if self.current_mode == self.MODE_RECTANGLE:
                draw.rectangle((rect.x(), rect.y(), rect.right(), rect.bottom()), fill=255)
            elif self.current_mode == self.MODE_ELLIPSE:
                draw.ellipse((rect.x(), rect.y(), rect.right(), rect.bottom()), fill=255)
        elif isinstance(self.selection_item, QGraphicsPathItem):
            # For freehand selections, we'd need to convert the path
            # This is a simplified version - full implementation would require path conversion
            pass
        elif isinstance(self.selection_item, QGraphicsPixmapItem):
            # Already a mask, just convert
            return qpixmap_to_pil_image(self.selection_item.pixmap()).convert("L")

        return mask

    def has_selection(self):
        """Check if there is an active selection."""
        return self.selection_item is not None