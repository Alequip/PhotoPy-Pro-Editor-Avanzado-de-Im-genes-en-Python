"""Constants and configurations for PhotoPy Pro."""

from PyQt6.QtGui import QColor

MAX_HISTORY_STEPS = 50
SUPPORTED_FORMATS = "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"
RECENT_FILES_LIMIT = 5
DEFAULT_BRUSH_SIZE = 3
DEFAULT_BRUSH_COLOR = QColor(0, 0, 0)

TOOL_ICONS = {
    "select": "icons/select.svg",
    "crop": "icons/crop.svg",
    "text": "icons/text.svg",
    "brush": "icons/brush.svg",
    "eraser": "icons/eraser.svg",
    "fill": "icons/fill.svg",
    "clone": "icons/clone.svg",
    "select_rect": "icons/select_rect.svg",
    "select_ellipse": "icons/select_ellipse.svg",
    "select_free": "icons/select_free.svg",
    "select_wand": "icons/select_wand.svg",
    "line": "icons/line.svg",
    "rect": "icons/rect.svg",
    "ellipse": "icons/ellipse.svg",
    "perspective": "icons/perspective.svg"
}

TOOLS_CONFIG = [
    ("select", "Selection", "Select objects"),
    ("crop", "Crop", "Crop image"),
    ("text", "Text", "Add text"),
    ("brush", "Brush", "Draw with brush"),
    ("eraser", "Eraser", "Erase parts of image"),
    ("fill", "Fill", "Fill area with color"),
    ("clone", "Clone", "Clone image areas"),
    ("select_rect", "Rect Select", "Rectangular selection"),
    ("select_ellipse", "Ellipse Select", "Elliptical selection"),
    ("select_free", "Free Select", "Freehand selection"),
    ("select_wand", "Magic Wand", "Select similar colors"),
    ("line", "Line", "Draw straight lines"),
    ("rect", "Rectangle", "Draw rectangles"),
    ("ellipse", "Ellipse", "Draw ellipses"),
    ("perspective", "Perspective", "Perspective transformation")
]