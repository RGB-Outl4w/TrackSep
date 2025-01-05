from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import pyqtSlot

class LogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.expanded = False

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        
        # Header with expand button
        header_layout = QHBoxLayout()
        self.expand_button = QPushButton("▶")  # Right arrow
        self.expand_button.setFixedWidth(30)
        self.expand_button.clicked.connect(self.toggle_expansion)
        header_layout.addWidget(self.expand_button)
        header_layout.addWidget(QLabel("Logs"))
        header_layout.addStretch()
        self.layout.addLayout(header_layout)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        self.log_text.hide()
        self.layout.addWidget(self.log_text)
        
    def toggle_expansion(self):
        self.expanded = not self.expanded
        self.expand_button.setText("▼" if self.expanded else "▶")
        self.log_text.setVisible(self.expanded)
        
    @pyqtSlot(str)
    def append_log(self, message):
        self.log_text.append(message)
        self.log_text.moveCursor(QTextCursor.End)
