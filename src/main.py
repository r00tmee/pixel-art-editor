#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QToolBar, QLabel)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

from canvas import PixelCanvas
from color_palette import ColorPalette
from tools import ToolType

class PixelEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pixel Art Editor")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Création du canvas
        self.canvas = PixelCanvas(32, 32)  # Grille 32x32 par défaut
        
        # Création de la palette de couleurs
        self.color_palette = ColorPalette()
        self.color_palette.colorSelected.connect(self.canvas.setCurrentColor)
        
        # Layout principal
        canvas_layout = QVBoxLayout()
        canvas_layout.addWidget(self.canvas)
        
        # Ajout des widgets au layout principal
        layout.addLayout(canvas_layout, stretch=4)
        layout.addWidget(self.color_palette, stretch=1)
        
        self.createToolbar()
        self.createMenuBar()
        
    def createToolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Outil Crayon
        pencil_action = QAction("Crayon", self)
        pencil_action.setCheckable(True)
        pencil_action.setChecked(True)
        pencil_action.triggered.connect(lambda: self.canvas.setTool(ToolType.PENCIL))
        toolbar.addAction(pencil_action)
        
        # Outil Remplissage
        fill_action = QAction("Remplir", self)
        fill_action.setCheckable(True)
        fill_action.triggered.connect(lambda: self.canvas.setTool(ToolType.FILL))
        toolbar.addAction(fill_action)
        
        # Outil Pipette
        picker_action = QAction("Pipette", self)
        picker_action.setCheckable(True)
        picker_action.triggered.connect(lambda: self.canvas.setTool(ToolType.PICKER))
        toolbar.addAction(picker_action)
        
        # Groupe d'actions pour les outils
        self.tool_actions = [pencil_action, fill_action, picker_action]
        for action in self.tool_actions:
            action.triggered.connect(lambda checked, a=action: self.updateToolActions(a))
            
    def createMenuBar(self):
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        
        export_action = QAction("Exporter PNG...", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.canvas.exportToPNG)
        file_menu.addAction(export_action)
        
        # Menu Edition
        edit_menu = menubar.addMenu("Edition")
        
        clear_action = QAction("Effacer tout", self)
        clear_action.setShortcut("Ctrl+N")
        clear_action.triggered.connect(self.canvas.clearCanvas)
        edit_menu.addAction(clear_action)
        
    def updateToolActions(self, triggered_action):
        for action in self.tool_actions:
            if action != triggered_action:
                action.setChecked(False)

def main():
    app = QApplication(sys.argv)
    editor = PixelEditor()
    editor.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 