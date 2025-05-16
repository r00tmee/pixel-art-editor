from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QColorDialog
from PyQt6.QtGui import QColor
from PyQt6.QtCore import pyqtSignal

class ColorButton(QPushButton):
    def __init__(self, color: QColor, parent=None):
        super().__init__(parent)
        self.setColor(color)
        self.setFixedSize(30, 30)
        
    def setColor(self, color: QColor):
        self.color = color
        self.setStyleSheet(
            f"background-color: {color.name()}; "
            "border: none; "
            "border-radius: 4px;"
        )

class ColorPalette(QWidget):
    colorSelected = pyqtSignal(QColor)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)
        
        # Couleurs de base
        default_colors = [
            "#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF",
            "#FFFF00", "#FF00FF", "#00FFFF", "#808080", "#800000",
            "#008000", "#000080", "#808000", "#800080", "#008080",
            "#C0C0C0"
        ]
        
        # Création des boutons de couleur
        row, col = 0, 0
        for color_hex in default_colors:
            color = QColor(color_hex)
            btn = ColorButton(color)
            btn.clicked.connect(lambda checked, c=color: self.onColorClicked(c))
            layout.addWidget(btn, row, col)
            col += 1
            if col > 3:  # 4 couleurs par ligne
                col = 0
                row += 1
                
        # Bouton pour ajouter une couleur personnalisée
        custom_btn = QPushButton("+")
        custom_btn.setFixedSize(30, 30)
        custom_btn.clicked.connect(self.addCustomColor)
        layout.addWidget(custom_btn, row, col)
        
    def onColorClicked(self, color: QColor):
        self.colorSelected.emit(color)
        
    def addCustomColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.colorSelected.emit(color) 