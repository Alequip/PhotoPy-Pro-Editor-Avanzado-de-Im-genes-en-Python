"""Background worker thread for heavy image processing tasks."""

from PyQt6.QtCore import QThread, pyqtSignal


class ImageWorker(QThread):
    """Worker thread for processing heavy operations without blocking UI."""

    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, task_fn, *args, **kwargs):
        super().__init__()
        self.task_fn = task_fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Execute the task in background thread."""
        try:
            result = self.task_fn(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))