"""Main window for PhotoPy Pro application."""

import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QListWidget, QMessageBox, QToolBar,
    QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence
from PIL import Image

from ..core.constants import TOOLS_CONFIG, SUPPORTED_FORMATS, RECENT_FILES_LIMIT
from ..core.commands import CommandProcessor
from ..core.worker import ImageWorker
from .canvas import ImageCanvas


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoPy Pro - Advanced Image Editor")
        self.resize(1400, 900)
        self._current_path = None
        self.recent_files = []

        # Initialize core systems
        self.command_processor = CommandProcessor()
        self.worker_thread = None

        # Initialize data structures
        self.layers = []
        self.layer_opacities = []
        self.blend_modes = []
        self.active_layer_index = 0

        # Setup UI
        self.setup_ui()
        self.setup_actions()
        self.setup_menus()
        self.setup_toolbar()
        self.setup_shortcuts()

        # Set default state
        self.set_tool("select")
        self.update_layers_list()

    def setup_ui(self):
        """Set up the main user interface."""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - Tools
        left_panel = self.create_tools_panel()
        splitter.addWidget(left_panel)

        # Center - Canvas
        self.canvas = ImageCanvas(self)
        splitter.addWidget(self.canvas)

        # Right panel - Layers
        right_panel = self.create_layers_panel()
        splitter.addWidget(right_panel)

        # Set splitter proportions
        splitter.setSizes([200, 800, 300])
        main_layout.addWidget(splitter)

    def create_tools_panel(self):
        """Create the left tools panel."""
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        tools_group = QGroupBox("Tools")
        tools_layout = QVBoxLayout()
        self.tool_btns = {}

        for tool_id, tool_name, tooltip in TOOLS_CONFIG:
            btn = QPushButton(tool_name)
            btn.setToolTip(tooltip)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, t=tool_id: self.set_tool(t))
            tools_layout.addWidget(btn)
            self.tool_btns[tool_id] = btn

        tools_group.setLayout(tools_layout)
        left_layout.addWidget(tools_group)
        left_layout.addStretch()

        return left_panel

    def create_layers_panel(self):
        """Create the right layers panel."""
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        layers_group = QGroupBox("Layers")
        layers_layout = QVBoxLayout()

        self.layers_list = QListWidget()
        self.layers_list.currentRowChanged.connect(self.set_active_layer)
        layers_layout.addWidget(self.layers_list)

        # Layer buttons
        layers_btn_layout = QHBoxLayout()

        add_layer_btn = QPushButton("Add")
        add_layer_btn.setToolTip("Add new layer")
        add_layer_btn.clicked.connect(self.add_layer)

        remove_layer_btn = QPushButton("Remove")
        remove_layer_btn.setToolTip("Remove current layer")
        remove_layer_btn.clicked.connect(self.remove_layer)

        layers_btn_layout.addWidget(add_layer_btn)
        layers_btn_layout.addWidget(remove_layer_btn)
        layers_layout.addLayout(layers_btn_layout)

        layers_group.setLayout(layers_layout)
        right_layout.addWidget(layers_group)
        right_layout.addStretch()

        return right_panel

    def setup_actions(self):
        """Create actions for menus and toolbars."""
        # File actions
        self.new_action = QAction("&New", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction("&Open", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction("&Save", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction("Save &As...", self)
        self.save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.save_as_action.triggered.connect(self.save_as_file)

        # Edit actions
        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.triggered.connect(self.undo)

        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.triggered.connect(self.redo)

    def setup_menus(self):
        """Set up the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)

    def setup_toolbar(self):
        """Set up the toolbar."""
        toolbar = self.addToolBar("Main")
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.undo_action)
        toolbar.addAction(self.redo_action)

    def setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        pass  # Already handled in actions

    def set_tool(self, tool_name):
        """Set the active tool."""
        # Clear all tool button selections
        for btn in self.tool_btns.values():
            btn.setChecked(False)

        # Set the selected tool
        if tool_name in self.tool_btns:
            self.tool_btns[tool_name].setChecked(True)

        # Update canvas tool
        if hasattr(self.canvas, 'set_tool'):
            self.canvas.set_tool(tool_name)

    def update_layers_list(self):
        """Update the layers list widget."""
        self.layers_list.clear()
        for i, layer in enumerate(self.layers):
            self.layers_list.addItem(f"Layer {i+1}")

        if self.layers:
            self.layers_list.setCurrentRow(self.active_layer_index)

    def add_layer(self):
        """Add a new layer."""
        if hasattr(self.canvas, 'pil_image') and self.canvas.pil_image:
            # Create empty layer same size as canvas
            new_layer = Image.new("RGBA", self.canvas.pil_image.size, (255, 255, 255, 0))
            self.layers.append(new_layer)
            self.layer_opacities.append(100)
            self.blend_modes.append("normal")
            self.active_layer_index = len(self.layers) - 1
            self.update_layers_list()

    def remove_layer(self):
        """Remove the active layer."""
        if self.layers and len(self.layers) > 1:
            self.layers.pop(self.active_layer_index)
            self.layer_opacities.pop(self.active_layer_index)
            self.blend_modes.pop(self.active_layer_index)
            self.active_layer_index = min(self.active_layer_index, len(self.layers) - 1)
            self.update_layers_list()

    def set_active_layer(self, index):
        """Set the active layer."""
        if 0 <= index < len(self.layers):
            self.active_layer_index = index

    def new_file(self):
        """Create a new file."""
        # For now, just clear the canvas
        if hasattr(self.canvas, 'clear'):
            self.canvas.clear()
        self._current_path = None

    def open_file(self):
        """Open an image file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            f"Images ({SUPPORTED_FORMATS})"
        )

        if file_path:
            try:
                if hasattr(self.canvas, 'load_image'):
                    self.canvas.load_image(file_path)
                    self._current_path = file_path
                    self.setWindowTitle(f"PhotoPy Pro - {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open image: {str(e)}")

    def save_file(self):
        """Save the current file."""
        if not self._current_path:
            self.save_as_file()
        else:
            self.save_image(self._current_path)

    def save_as_file(self):
        """Save the file with a new name."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            f"Images ({SUPPORTED_FORMATS})"
        )

        if file_path:
            self.save_image(file_path)
            self._current_path = file_path
            self.setWindowTitle(f"PhotoPy Pro - {os.path.basename(file_path)}")

    def save_image(self, file_path):
        """Save the image to the specified path."""
        try:
            if hasattr(self.canvas, 'save_image'):
                self.canvas.save_image(file_path)
            else:
                QMessageBox.warning(self, "Warning", "No image to save")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save image: {str(e)}")

    def undo(self):
        """Undo the last operation."""
        if hasattr(self.canvas, 'undo'):
            self.canvas.undo()

    def redo(self):
        """Redo the last undone operation."""
        if hasattr(self.canvas, 'redo'):
            self.canvas.redo()