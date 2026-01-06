from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTableWidget, QTableWidgetItem
)
from databases import (
    insert_laporan, get_laporan,
    update_status_laporan, delete_laporan
)

class FormLaporan(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Pelaporan Kerusakan Fasilitas Umum")
        self.setGeometry(200, 200, 800, 550)

        main_layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        self.nama = QLineEdit()
        self.lokasi = QLineEdit()
        self.jenis = QLineEdit()
        self.deskripsi = QTextEdit()

        self.btn_simpan = QPushButton("Kirim Laporan")
        self.btn_update = QPushButton("Tandai Selesai")
        self.btn_hapus = QPushButton("Hapus Laporan")

        self.btn_simpan.clicked.connect(self.simpan_data)
        self.btn_update.clicked.connect(self.update_status)
        self.btn_hapus.clicked.connect(self.hapus_data)

        form_layout.addWidget(QLabel("Nama Pelapor"))
        form_layout.addWidget(self.nama)
        form_layout.addWidget(QLabel("Lokasi"))
        form_layout.addWidget(self.lokasi)
        form_layout.addWidget(QLabel("Jenis Kerusakan"))
        form_layout.addWidget(self.jenis)
        form_layout.addWidget(QLabel("Deskripsi"))
        form_layout.addWidget(self.deskripsi)

        btn_layout.addWidget(self.btn_simpan)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_hapus)

        self.tabel = QTableWidget()
        self.tabel.setColumnCount(5)
        self.tabel.setHorizontalHeaderLabels(
            ["ID", "Nama", "Lokasi", "Jenis", "Status"]
        )
        self.tabel.cellClicked.connect(self.pilih_data)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(QLabel("Daftar Laporan"))
        main_layout.addWidget(self.tabel)

        self.setLayout(main_layout)
        self.load_data()

    # =====================
    # LOAD DATA
    # =====================
    def load_data(self):
        data = get_laporan()
        self.tabel.setRowCount(len(data))

        for row, item in enumerate(data):
            self.tabel.setItem(row, 0, QTableWidgetItem(str(item["id"])))
            self.tabel.setItem(row, 1, QTableWidgetItem(item["nama_pelapor"]))
            self.tabel.setItem(row, 2, QTableWidgetItem(item["lokasi"]))
            self.tabel.setItem(row, 3, QTableWidgetItem(item["jenis_kerusakan"]))
            self.tabel.setItem(row, 4, QTableWidgetItem(item["status"]))

    # =====================
    # INSERT
    # =====================
    def simpan_data(self):
        if not self.nama.text() or not self.lokasi.text() or not self.jenis.text():
            QMessageBox.warning(self, "Peringatan", "Data wajib diisi!")
            return

        data = {
            "nama_pelapor": self.nama.text(),
            "lokasi": self.lokasi.text(),
            "jenis_kerusakan": self.jenis.text(),
            "deskripsi": self.deskripsi.toPlainText()
        }

        status, _ = insert_laporan(data)

        if status == 201:
            QMessageBox.information(self, "Sukses", "Laporan berhasil dikirim")
            self.clear_form()
            self.load_data()
        else:
            QMessageBox.warning(self, "Error", "Gagal mengirim laporan")

    # =====================
    # PILIH DATA
    # =====================
    def pilih_data(self, row, column):
        self.selected_id = int(self.tabel.item(row, 0).text())

    # =====================
    # UPDATE STATUS
    # =====================
    def update_status(self):
        if not hasattr(self, "selected_id"):
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu")
            return

        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi",
            "Tandai laporan ini sebagai SELESAI?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if konfirmasi == QMessageBox.StandardButton.Yes:
            status = update_status_laporan(self.selected_id, "Selesai")
            if status == 204:
                QMessageBox.information(self, "Sukses", "Status diperbarui")
                self.load_data()

    # =====================
    # DELETE
    # =====================
    def hapus_data(self):
        if not hasattr(self, "selected_id"):
            QMessageBox.warning(self, "Peringatan", "Pilih data terlebih dahulu")
            return

        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi",
            "Yakin ingin menghapus laporan ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if konfirmasi == QMessageBox.StandardButton.Yes:
            status = delete_laporan(self.selected_id)
            if status == 204:
                QMessageBox.information(self, "Sukses", "Laporan dihapus")
                self.load_data()

    def clear_form(self):
        self.nama.clear()
        self.lokasi.clear()
        self.jenis.clear()
        self.deskripsi.clear()
