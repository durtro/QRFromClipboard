import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QWidget, QLabel, QPushButton, QTextEdit)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, Qt
from io import BytesIO
import qrcode

class QRMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QRFromClipboard Generator")
        self.setGeometry(100, 100, 800, 700)
        
        self.clipboard = QApplication.clipboard()
        self.last_text = self.clipboard.text()
        
        self.qr_label = None  # Für QR-Bild
        self.setup_ui()
        self.start_clipboard_monitor()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Text-Anzeige
        self.text_display = QTextEdit()
        self.text_display.setMaximumHeight(100)
        layout.addWidget(self.text_display)
        
        # Buttons
        btn = QPushButton("📱 QR aus Zwischenablage generieren")
        btn.clicked.connect(self.generate_qr)
        layout.addWidget(btn)

        # QR-Bild-Label
        self.qr_label = QLabel("Kein QR-Code vorhanden")
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setStyleSheet("border: 2px dashed gray; min-height: 300px;")
        self.qr_label.setMinimumSize(400, 400)
        layout.addWidget(self.qr_label)
    
    def start_clipboard_monitor(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(500)  # Alle 500ms
    
    def check_clipboard(self):
        if not len(self.clipboard.text()) > 2000:
            current = self.clipboard.text()
            if current != self.last_text:
                self.last_text = current
                self.text_display.setText(f"{current}")
        else:
            self.text_display.setText(f"Text too long")
    
    def generate_qr(self):
        #text = self.clipboard.text()
        text = self.text_display.toPlainText()
        if not text:
            self.qr_label.setText("❌ Zwischenablage leer!")
            return
        
        # QR-Code erzeugen
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        
        # Als QPixmap konvertieren
        qt_pixmap = QPixmap()
        qt_pixmap.loadFromData(img_bytes, "PNG")

        # Skalieren und anzeigen
        scaled = qt_pixmap.scaled(
            400, 400, 
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.qr_label.setPixmap(scaled)
        self.setWindowTitle(f"QR Code from Clipboard - {len(text)} characters")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRMonitor()
    window.show()
    sys.exit(app.exec())
