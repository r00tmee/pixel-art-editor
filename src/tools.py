from enum import Enum, auto

class ToolType(Enum):
    PENCIL = auto()
    FILL = auto()
    PICKER = auto()

class Tool:
    def __init__(self, tool_type: ToolType):
        self.tool_type = tool_type
        
    def use(self, canvas, x, y, color):
        if self.tool_type == ToolType.PENCIL:
            canvas.setPixel(x, y, color)
        elif self.tool_type == ToolType.FILL:
            self._flood_fill(canvas, x, y, color)
        elif self.tool_type == ToolType.PICKER:
            return canvas.getPixel(x, y)
            
    def _flood_fill(self, canvas, x, y, new_color):
        """Algorithme de remplissage par diffusion"""
        target_color = canvas.getPixel(x, y)
        if target_color == new_color:
            return
            
        def fill(x, y):
            if (x < 0 or x >= canvas.width or 
                y < 0 or y >= canvas.height or 
                canvas.getPixel(x, y) != target_color):
                return
                
            canvas.setPixel(x, y, new_color)
            
            # Remplir récursivement dans les 4 directions
            fill(x + 1, y)
            fill(x - 1, y)
            fill(x, y + 1)
            fill(x, y - 1)
            
        fill(x, y) 