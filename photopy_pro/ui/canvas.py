"""Image canvas for displaying and editing images."""

from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PIL import Image

from ..utils.image_utils import pil_image_to_qpixmap, qpixmap_to_pil_image
from ..tools.selection import SelectionManager


class ImageCanvas(QGraphicsView):
    """Main image editing canvas."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        # Graphics scene setup
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Image data
        self.pil_image = None
        self.pixmap_item = None

        # Tools and interaction
        self.current_tool = "select"
        self.selection_manager = SelectionManager(self)

        # Canvas settings
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setRenderHints(self.renderHints() |
                          self.renderHints().Antialiasing |
                          self.renderHints().SmoothPixmapTransform)

    def load_image(self, file_path):
        """Load an image from file path."""
        try:
            self.pil_image = Image.open(file_path).convert("RGBA")
            self.display_image()

            # Initialize layers in parent window
            if hasattr(self.parent_window, 'layers'):
                self.parent_window.layers = [self.pil_image.copy()]
                self.parent_window.layer_opacities = [100]
                self.parent_window.blend_modes = ["normal"]
                self.parent_window.active_layer_index = 0
                self.parent_window.update_layers_list()

        except Exception as e:
            raise Exception(f"Failed to load image: {str(e)}")

    def display_image(self):
        """Display the current PIL image on the canvas."""
        if not self.pil_image:
            return

        # Clear existing items
        self.scene.clear()

        # Convert and display
        pixmap = pil_image_to_qpixmap(self.pil_image)
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)

        # Fit in view
        self.fitInView(self.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def save_image(self, file_path):
        """Save the current image."""
        if not self.pil_image:
            raise Exception("No image to save")

        # Determine format from extension
        file_format = file_path.split('.')[-1].upper()
        if file_format == 'JPG':
            file_format = 'JPEG'

        # Convert to RGB if saving as JPEG
        save_image = self.pil_image
        if file_format == 'JPEG':
            save_image = self.pil_image.convert('RGB')

        save_image.save(file_path, format=file_format)

    def set_tool(self, tool_name):
        """Set the active tool."""
        self.current_tool = tool_name

        # Update selection manager mode
        tool_mode_map = {
            "select_rect": SelectionManager.MODE_RECTANGLE,
            "select_ellipse": SelectionManager.MODE_ELLIPSE,
            "select_free": SelectionManager.MODE_FREEHAND,
            "select_wand": SelectionManager.MODE_MAGIC_WAND,
        }

        if tool_name in tool_mode_map:
            self.selection_manager.current_mode = tool_mode_map[tool_name]

        # Clear selection if switching away from selection tools
        if not tool_name.startswith("select"):
            self.selection_manager.clear_selection()

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if self.current_tool.startswith("select"):
            self.selection_manager.mouse_press(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move events."""
        if self.current_tool.startswith("select"):
            self.selection_manager.mouse_move(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        if self.current_tool.startswith("select"):
            self.selection_manager.mouse_release(event)
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        """Handle zoom with mouse wheel."""
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        # Set anchor point to mouse position
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        # Zoom
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        self.scale(zoom_factor, zoom_factor)

    def clear(self):
        """Clear the canvas."""
        self.scene.clear()
        self.pil_image = None
        self.pixmap_item = None

        # Clear parent window layers
        if hasattr(self.parent_window, 'layers'):
            self.parent_window.layers.clear()
            self.parent_window.layer_opacities.clear()
            self.parent_window.blend_modes.clear()
            self.parent_window.active_layer_index = 0
            self.parent_window.update_layers_list()

    def undo(self):
        """Undo the last operation."""
        if hasattr(self.parent_window, 'command_processor'):
            if self.pil_image and self.parent_window.command_processor.can_undo():
                result = self.parent_window.command_processor.undo(self.pil_image)
                if result:
                    self.pil_image = result
                    self.display_image()

    def redo(self):
        """Redo the last undone operation."""
        if hasattr(self.parent_window, 'command_processor'):
            if self.pil_image and self.parent_window.command_processor.can_redo():
                result = self.parent_window.command_processor.redo(self.pil_image)
                if result:
                    self.pil_image = result
                    self.display_image()