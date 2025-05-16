from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6.QtGui import QPainter, QColor, QImage, QPen
from PyQt6.QtCore import Qt, QPoint
from tools import ToolType, Tool
from PIL import Image
import numpy as np

class PixelCanvas(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.zoom = 10  # Facteur de zoom initial
        self.pan_offset = QPoint(0, 0)
        self.last_pan_pos = None
        self.current_color = QColor(Qt.GlobalColor.black)
        self.current_tool = Tool(ToolType.PENCIL)
        
        # Création de l'image
        self.image = QImage(width, height, QImage.Format.Format_ARGB32)
        self.image.fill(Qt.GlobalColor.white)
        
        # Configuration du widget
        self.setMinimumSize(400, 400)
        self.setMouseTracking(True)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Appliquer le pan
        painter.translate(self.pan_offset)
        
        # Dessiner l'image zoomée
        scaled_width = self.width * self.zoom
        scaled_height = self.height * self.zoom
        painter.drawImage(0, 0, self.image.scaled(scaled_width, scaled_height))
        
        # Dessiner la grille
        painter.setPen(QPen(QColor(200, 200, 200)))
        for x in range(0, scaled_width + 1, self.zoom):
            painter.drawLine(x, 0, x, scaled_height)
        for y in range(0, scaled_height + 1, self.zoom):
            painter.drawLine(0, y, scaled_width, y)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = self.pixelPos(event.pos())
            if 0 <= pos.x() < self.width and 0 <= pos.y() < self.height:
                if self.current_tool.tool_type == ToolType.PICKER:
                    color = self.getPixel(pos.x(), pos.y())
                    self.current_color = color
                else:
                    self.current_tool.use(self, pos.x(), pos.y(), self.current_color)
                self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            pos = self.pixelPos(event.pos())
            if 0 <= pos.x() < self.width and 0 <= pos.y() < self.height:
                self.setPixel(pos.x(), pos.y(), QColor(Qt.GlobalColor.white))
                self.update()
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.last_pan_pos = event.pos()
            
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            pos = self.pixelPos(event.pos())
            if 0 <= pos.x() < self.width and 0 <= pos.y() < self.height:
                if self.current_tool.tool_type == ToolType.PENCIL:
                    self.current_tool.use(self, pos.x(), pos.y(), self.current_color)
                    self.update()
        elif event.buttons() & Qt.MouseButton.MiddleButton and self.last_pan_pos:
            delta = event.pos() - self.last_pan_pos
            self.pan_offset += delta
            self.last_pan_pos = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.last_pan_pos = None
            
    def wheelEvent(self, event):
        # Zoom avec la molette
        if event.angleDelta().y() > 0 and self.zoom < 50:
            self.zoom += 1
        elif event.angleDelta().y() < 0 and self.zoom > 1:
            self.zoom -= 1
        self.update()
        
    def pixelPos(self, pos):
        """Convertit une position écran en position pixel"""
        x = int((pos.x() - self.pan_offset.x()) / self.zoom)
        y = int((pos.y() - self.pan_offset.y()) / self.zoom)
        return QPoint(x, y)
        
    def setCurrentColor(self, color):
        self.current_color = color
        
    def setTool(self, tool_type):
        self.current_tool = Tool(tool_type)
        
    def setPixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.image.setPixelColor(x, y, color)
            
    def getPixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.image.pixelColor(x, y)
        return QColor(Qt.GlobalColor.white)
        
    def clearCanvas(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update()
        
    def exportToPNG(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter en PNG",
            "",
            "PNG Files (*.png)"
        )
        
        if file_path:
            # Convertir QImage en PIL Image
            buffer = self.image.bits().asarray(self.width * self.height * 4)
            arr = np.frombuffer(buffer, dtype=np.uint8).reshape(
                self.height, self.width, 4
            )
            img = Image.fromarray(arr, 'RGBA')
            
            # Sauvegarder l'image
            img.save(file_path, format='PNG') 