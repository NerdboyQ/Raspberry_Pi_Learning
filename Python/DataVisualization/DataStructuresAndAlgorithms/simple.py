import sys
import random
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, Slot, QRect
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont

class NodeWidget(QWidget):
    """
    Placeholder for base class for lists, linked lists, trees, & graphs/matrices
    """
    def __init__(self, diameter, color, border_color = None, text="", text_color=QColor('white')):
        """
        Constructor for Custom Node Widget
        
        :param self: Description
        :param diameter: Description
        :param color: Description
        :param border_color: Description
        :param text: Description
        :param text_color: Description
        """
        super().__init__()
        self.diameter = diameter
        self.border_width = self.diameter*.01 # force border to be 1% of the diameter
        self.color = color
        if border_color == None: self.border_color = QColor(self.color)
        else: self.border_color = QColor(border_color)
        # print(self.border_color,type(self.border_color))
        self.text = str(text)
        self.text_color = text_color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(self.border_color, self.border_width)
        painter.setPen(pen)

        brush = QBrush(self.color)
        painter.setBrush(brush)

        offset = self.border_width // 2
        rect =  QRect(
            offset, offset,
            self.diameter - self.border_width,
            self.diameter - self.border_width)
        
        painter.drawEllipse(rect)

        painter.setPen(self.text_color)
        font_size = int(self.diameter * 0.25)
        font = QFont("Arial", font_size, QFont.Weight.Bold)
        painter.setFont(font)

        text_rect = QRect(0,0, self.diameter, self.diameter)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.text)  
    
    def set_fill_color(self, color):
        """Change the fill color and redraw"""
        self.fill_color = color
        self.update()
    
    def set_border_color(self, color):
        """Change the border color and redraw"""
        self.border_color = color
        self.update()

    def set_text(self, text):
        """Update the text displayed in the circle"""
        self.text = text
        self.update()

class NodeHolderWidget(QWidget):
    """
    Holder for Lists
    """
    def __init__(self, lst, orientation='horizontal', spacing=2, padding=5):
        """
        Constructor: creates node holder widget instance
        """
        super().__init__()

        self.nodes = []
        self.spacing = spacing
        self.padding = padding
        self.border_width = 2
        self.bg_color = QColor('transparent')
        self.border_color = QColor('white')

        if orientation == 'horizontal': self.layout = QHBoxLayout(self)
        elif orientation == 'vertical': self.layout = QVBoxLayout(self)

        self.layout.setSpacing(spacing)
        self.layout.setContentsMargins(padding, padding, padding, padding)

        # Create custom circle widgets
        dflt_QtColors = QColor.colorNames() # gets default QtColors as list of strings
        """
        [
         'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 
         'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 
         'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 
         'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 
         'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 
         'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 
         'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 
         'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 
         'gray', 'green', 'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 
         'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 
         'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 
         'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 
         'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 
         'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 
         'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 
         'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 
         'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 
         'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 
         'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 
         'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 
         'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 
         'teal', 'thistle', 'tomato', 'transparent', 'turquoise', 'violet', 'wheat', 'white', 
         'whitesmoke', 'yellow', 'yellowgreen']
        """
        rand_color = random.randint(0, len(dflt_QtColors))
        rand_color = dflt_QtColors[rand_color]
        print("Random color selected:", rand_color)

        for v in lst:
            self.add_node(
                NodeWidget(80,color=rand_color,text=v)
            )

    def add_node(self, node):
        """
        Add node to holder
        
        :param self: Description
        :param node: Description
        """
        self.nodes.append(node)
        self.layout.addWidget(node)
        return node

    def add_stretch(self):
        """
        Docstring for add_stretch
        
        :param self: Description
        """
        self.layout.addStretch()
    
    def clear_nodes(self):
        """
        Docstring for clear_nodes
        
        :param self: Description
        """
        for node in self.nodes:
            self.layout.removeWidget(node)
            node.deleteLater()
        
        self.nodes.clear()
    
    def get_node(self, index):
        """
        Docstring for get_node
        
        :param self: Description
        """
        if 0 <= index < len(self.nodes):
            return self.nodes[index]
        
        return None
    
    def paintEvent(self, event):
        """
        Docstring for paintEvent
        
        :param self: Description
        :param event: Description
        """
        painter  = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        brush = QBrush(self.bg_color)
        painter.setBrush(brush)

        pen = QPen(self.border_color, self.border_width)
        painter.setPen(pen)

        rect = self.rect().adjusted(
            self.border_width // 2,
            self.border_width // 2,
            -self.border_width // 2,
            -self.border_width // 2
        )
        painter.drawRoundedRect(rect, 10, 10)

class MyWidget(QWidget):
    """
    Demo custom widget class: MyWidget
    """
    def __init__(self):
        """
        Constructor for Custom widget basics
        """
        super().__init__()

        self.hello = ["Hello", "blah", "hah", "my nigga"]

        self.button = QtWidgets.QPushButton("Click Me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        holderWidget = NodeHolderWidget([ random.randint(1,100) for _ in range(5) ])
        self.layout.addWidget(holderWidget)

        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self):
        """
        Updates text for text widget
        
        :param self: Description
        """
        self.text.setText(random.choice(self.hello))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())