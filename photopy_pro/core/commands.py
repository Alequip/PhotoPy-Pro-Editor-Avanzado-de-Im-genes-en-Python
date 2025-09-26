"""Command pattern implementation for undo/redo functionality."""

import io
from PIL import Image
from .constants import MAX_HISTORY_STEPS


class EditCommand:
    """Encapsulates an edit operation for undo/redo functionality."""

    def __init__(self, layer_index, operation, before, after, bounds=None):
        self.layer_index = layer_index
        self.operation = operation
        self.bounds = bounds or (0, 0, before.width, before.height)
        self.before = self._compress_image(before.crop(self.bounds))
        self.after = self._compress_image(after.crop(self.bounds))

    def _compress_image(self, image):
        """Compress image to save memory in history."""
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", optimize=True, compress_level=9)
        return buffer.getvalue()

    def undo(self, current_image):
        """Apply the undo operation."""
        return self._apply_patch(current_image, self.before)

    def redo(self, current_image):
        """Apply the redo operation."""
        return self._apply_patch(current_image, self.after)

    def _apply_patch(self, image, patch_data):
        """Apply a compressed patch to the image."""
        buffer = io.BytesIO(patch_data)
        patch = Image.open(buffer)
        image.paste(patch, self.bounds)
        return image


class CommandProcessor:
    """Manages the undo/redo stack for edit commands."""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def execute(self, command):
        """Execute a command and add it to history."""
        self.undo_stack.append(command)
        if len(self.undo_stack) > MAX_HISTORY_STEPS:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self, current_state):
        """Undo the last operation."""
        if not self.undo_stack:
            return None
        command = self.undo_stack.pop()
        self.redo_stack.append(command)

        new_state = current_state.copy()
        return command.undo(new_state)

    def redo(self, current_state):
        """Redo the last undone operation."""
        if not self.redo_stack:
            return None
        command = self.redo_stack.pop()
        self.undo_stack.append(command)

        new_state = current_state.copy()
        return command.redo(new_state)

    def can_undo(self):
        """Check if undo is available."""
        return bool(self.undo_stack)

    def can_redo(self):
        """Check if redo is available."""
        return bool(self.redo_stack)

    def clear(self):
        """Clear the command history."""
        self.undo_stack.clear()
        self.redo_stack.clear()