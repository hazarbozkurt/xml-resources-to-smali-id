import re
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from qt_material import apply_stylesheet

class XMLAEROSmali(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        apply_stylesheet(self, theme='dark_pink.xml')
        self.format_etiket = QtWidgets.QLabel("Yeni format:")
        self.format_giris = QtWidgets.QTextEdit()
        self.format_giris.setText("{isim} {kimlik}")
        self.format_giris.setAcceptRichText(False)
        self.format_giris.setTabChangesFocus(False)
        self.format_giris.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.format_giris.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.format_giris.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.dosya_sec = QtWidgets.QPushButton("XML dosyası seç")
        self.dosya_sec.clicked.connect(self.dosya_secme)
        self.dosya_isle = QtWidgets.QPushButton("XML dosyasını işle")
        self.dosya_isle.clicked.connect(self.dosya_isleme)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.format_etiket)
        hbox.addWidget(self.format_giris)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.dosya_sec)
        vbox.addLayout(hbox)
        vbox.addWidget(self.dosya_isle)
        self.setLayout(vbox)
        self.xml_dosya = None
        
    def dosya_secme(self):
        secenekler = QtWidgets.QFileDialog.Options()
        self.xml_dosya, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Lütfen bir XML dosyası seçin",
            "",
            "XML Dosyaları (*.xml);;Tüm Dosyalar (*)",
            options=secenekler
        )
        
    def dosya_isleme(self):
        if not self.xml_dosya:
            QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen bir XML dosyası seçin.")
            return

        yeni_satir_formati = self.format_giris.toPlainText()

        cikti_dosyasi = "cikti.smali"
        with open(self.xml_dosya, "r") as f_in, open(cikti_dosyasi, "w") as f_out:
            for satir in f_in:
                eslesmeler = re.findall(r'name="(.+?)" id="(.+?)"', satir)
                if eslesmeler:
                    isim, tanimlayici = eslesmeler[0]
                    try:
                        yeni_satir = yeni_satir_formati.format(isim=isim.replace('{', '{{').replace('}', '}}').replace('"', '\\"').replace("'", "\\'"), kimlik=tanimlayici.replace('{', '{{').replace('}', '}}').replace('"', '\\"').replace("'", "\\'"))
                    except ValueError:
                        QtWidgets.QMessageBox.warning(self, "Hata", "Geçersiz karakter girdiniz.")
                        return
                    print(yeni_satir, file=f_out, end='\n')

if __name__ == "__main__":
    uygulama = QtWidgets.QApplication([])
    pencere = XMLAEROSmali()
    pencere.setWindowTitle("Public XML - Smali ID dönüştürücü")
    pencere.setGeometry(100, 100, 800, 600)
    pencere.show()
    uygulama.exec_()
