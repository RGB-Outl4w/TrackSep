import logging
from PyQt5.QtCore import Q_ARG, QMetaObject, Qt

class LogHandler(logging.Handler):
    def __init__(self, widget):
        """
        Initialize the log handler.

        Args:
            widget (QWidget): A PyQt5 widget that implements an `append_log` method.
        """
        super().__init__()
        self.widget = widget
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        """
        Emit a log record to the attached PyQt5 widget.

        Args:
            record (LogRecord): The log record to process.
        """
        msg = self.format(record)
        # Thread-safe update of UI via Qt
        QMetaObject.invokeMethod(
            self.widget, 
            "append_log",
            Qt.QueuedConnection,
            Q_ARG(str, msg)
        )
