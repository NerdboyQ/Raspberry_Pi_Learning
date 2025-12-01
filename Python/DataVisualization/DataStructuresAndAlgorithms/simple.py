import sys
import random
from enum import Enum
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, Slot, QRect, QAnimationGroup, QParallelAnimationGroup, QPoint, QPropertyAnimation
from PySide6.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor, QFont

class ArrowDirection(Enum):
    DIR_ARROW_LEFT = 0,
    DIR_ARROW_UP = 1,
    DIR_ARROW_RIGHT = 2,
    DIR_ARROW_DOWN = 3,
    DIR_ARROW_DIAG_UP_RIGHT = 4,
    DIR_ARROW_DIAG_UP_LEFT = 5,
    DIR_ARROW_DIAG_DOWN_LEFT = 6,
    DIR_ARROW_DIAG_DOWN_RIGHT = 7

class ArrowWidget(QWidget):
    """
    Arrow widget for index pointing
    """
    def __init__(self, height, width, color=QColor('white'), direction=ArrowDirection.DIR_ARROW_UP):
        super().__init__()
        self.height = height
        if width <= 0: self.width = self.height
        else: self.width = width

        self.color = color

        self.setMaximumHeight = height
        self.setMaximumWidth = self.width

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # drawing path
        path = QPainterPath()
        center_x ,start_y = self.width//2, self.height
        # outline of arrow using points
        path.moveTo(center_x-self.width//4, start_y)                    # left middle
        path.lineTo(center_x-self.width//4, start_y-self.height//4*2)   # line to arrow head base
        path.lineTo(center_x-self.width//2, start_y-self.height//4*2)   # left corner of arrow head
        path.lineTo(center_x, start_y-self.height)                      # point of arrow
        path.lineTo(center_x+self.width//2, start_y-self.height//4*2)   # right corner of arrow head
        path.lineTo(center_x+self.width//4, start_y-self.height//4*2)   # back to line
        path.lineTo(center_x+self.width//4, start_y)                    # complete the base
        path.closeSubpath()                                             # close the path

        painter.fillPath(path, QBrush(self.color))  # fill the arrow with the desired color
        painter.setPen(QPen(QColor('gray'), 1))     # set outline color and size
        painter.drawPath(path)                      # draw the arrow

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

        # needed for correct layout spacing
        self.setFixedSize(diameter, diameter)

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
    def __init__(self, lst, orientation='horizontal', spacing=1, padding=10):
        """
        Constructor: creates node holder widget instance
        """
        super().__init__()

        self.nodes = []
        self.border_width = 2
        self.bg_color = QColor('transparent')
        self.border_color = QColor('white')

        self.setFixedHeight(200)

        if orientation == 'horizontal': self.layout = QHBoxLayout(self)
        elif orientation == 'vertical': self.layout = QVBoxLayout(self)

        self.layout.setSpacing(spacing)
        self.layout.setContentsMargins(padding, padding, padding, padding)
        # the line below helped avoid the horizontal and veritcal alignment
        # > NOTE: This must be set after the contents margins has been set
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
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
        """
        self.hello = ["Hello", "blah", "hah", "my nigga"]

        self.button = QtWidgets.QPushButton("Click Me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=Qt.AlignmentFlag.AlignCenter)
        """
        self.layout = QtWidgets.QVBoxLayout(self)
        """
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        """
        self.holderWidget = NodeHolderWidget(
            [ random.randint(1,100) for _ in range(5) ],
            spacing=5
        )
        self.layout.addWidget(self.holderWidget)

        self.arrow = ArrowWidget(height=30, width=30)
        self.layout.addWidget(self.arrow)

        print("Arrow original position:", self.arrow.pos()) # return (0,0), appears relative to default location.
        # animation working, TODO: trigger repeatedly 
        self.anim = QPropertyAnimation(self.arrow, b"pos") # object to move/animate and the movement type?
        self.anim.setEndValue(QPoint(400,400))
        self.anim.setDuration(2000) # in ms
        self.anim.start()
        # self.button.clicked.connect(self.magic)

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