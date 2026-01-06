import sys
from PyQt6.QtWidgets import QApplication
from ui import FormLaporan

app = QApplication(sys.argv)
window = FormLaporan()
window.show()
sys.exit(app.exec())
