import sys
import random
from enum import Enum
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, Slot, QRect, QAnimationGroup, QParallelAnimationGroup, QPoint, QPropertyAnimation, QSequentialAnimationGroup
from PySide6.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor, QFont

class RefDirection(Enum):
    DIR_LEFT = 0,
    DIR_UP = 1,
    DIR_RIGHT = 2,
    DIR_DOWN = 3,
    DIR_DIAG_UP_RIGHT = 4,
    DIR_DIAG_UP_LEFT = 5,
    DIR_DIAG_DOWN_LEFT = 6,
    DIR_DIAG_DOWN_RIGHT = 7,

# > NOTE: This required a reference image as the position needs coordinates in referece to the 
#         eldest widget (main window in most cases)
def getWidgetPosRef(widget: QWidget, widgetPos: RefDirection=None, relativeTo: QWidget = None) -> tuple:
    """
    Retrieves the position of a widget and returns the reference position
    to focus on

    @param widget: the widget to consider
    @param widgetPos: suggested reference position of the widget

    @return tuple for x,y reference position
    """
    if relativeTo: pos = widget.mapTo(relativeTo, QPoint(0,0))
    else: pos = widget.pos()
    x,y = pos.x(), pos.y()
    w,h = widget.width(), widget.height()
    if widgetPos == None: return (x+w//2, y+h//2)
    elif widgetPos == RefDirection.DIR_DOWN: return (x+w//2, y+h)    # Center of widget
    elif widgetPos == RefDirection.DIR_DIAG_DOWN_RIGHT: return (x+w, y+h)
    elif widgetPos == RefDirection.DIR_DIAG_DOWN_LEFT: return (x, y+h)
    elif widgetPos == RefDirection.DIR_DIAG_UP_RIGHT: return (x+w, y)
    elif widgetPos == RefDirection.DIR_DIAG_UP_LEFT: return (x, y)
    elif widgetPos == RefDirection.DIR_UP: return (x+w//2, y)
    elif widgetPos == RefDirection.DIR_LEFT: return (x, y+h//2)
    elif widgetPos == RefDirection.DIR_RIGHT: return (x+w, y+h//2)

class ArrowWidget(QWidget):
    """
    Arrow widget for index pointing
    """
    def __init__(self, height, width, color=QColor('white'), direction=RefDirection.DIR_UP):
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
    def __init__(self, diameter, color=QColor('white'), border_color = QColor('black'), text="", text_color=QColor('black')):
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
    def __init__(self, lst, orientation='horizontal', spacing=1, padding=10, height=200):
        """
        Constructor: creates node holder widget instance
        """
        super().__init__()
        
        self.nodes = []
        self.border_width = 2
        self.bg_color = QColor('transparent')
        self.border_color = QColor('white')

        self.setFixedHeight(height)

        if orientation == 'horizontal': self.layout = QHBoxLayout(self)
        elif orientation == 'vertical': self.layout = QVBoxLayout(self)

        self.layout.setSpacing(spacing)
        self.layout.setContentsMargins(padding, padding, padding, padding)
        # the line below helped avoid the horizontal and veritcal alignment
        # > NOTE: This must be set after the contents margins has been set
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
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
            # n = NodeWidget(height//4,color=rand_color,text=v)
            n = NodeWidget(height//4, text=v)
            self.add_node(n)

    def print_values(self):
        print("[",end='')
        for node in self.nodes:
            if node == self.nodes[0]: print(node.text, end='')
            else: print(f",{node.text}", end='')
        print("]")

    def swap_nodes(self, i1: int, i2: int):
        n1 = self.nodes[i1]
        n2 = self.nodes[i2]
        print(f"Swapping {n1.text} & {n2.text}")
        print("Before:", end='')
        self.print_values()

        x1,y1 = getWidgetPosRef(n1, RefDirection.DIR_DIAG_UP_LEFT,relativeTo=self)
        x2,y2 = getWidgetPosRef(n2, RefDirection.DIR_DIAG_UP_LEFT,relativeTo=self)

        # handle animation
        self.anim_a1 = QPropertyAnimation(n1, b"pos") # object to move/animate and the movement type?
        self.anim_a2 = QPropertyAnimation(n1, b"pos")
        self.anim_a3 = QPropertyAnimation(n1, b"pos")
        y1_n = y1-n1.height()*2
        print(f"({x1},{y1}) => ({x1},{y1_n})")
        self.anim_a1.setEndValue(QPoint(x1,y1_n))
        self.anim_a1.setDuration(500) # in ms
        self.anim_a2.setEndValue(QPoint(x2,y1_n))
        self.anim_a2.setDuration(500) # in ms
        self.anim_a3.setEndValue(QPoint(x2,y1))
        self.anim_a3.setDuration(500) # in ms
        # self.anim.start()
        self.groupAnim1 = QSequentialAnimationGroup()
        self.groupAnim1.addAnimation(self.anim_a1)
        self.groupAnim1.addAnimation(self.anim_a2)
        self.groupAnim1.addAnimation(self.anim_a3)
        self.groupAnim1.start()

        
        self.anim_b1 = QPropertyAnimation(n2, b"pos") # object to move/animate and the movement type?
        self.anim_b2 = QPropertyAnimation(n2, b"pos")
        self.anim_b3 = QPropertyAnimation(n2, b"pos")
        y2_n = y2-n2.height()
        print(f"({x2},{y2}) => ({x2},{y2_n})")
        self.anim_b1.setEndValue(QPoint(x2,y2_n))
        self.anim_b1.setDuration(500) # in ms
        self.anim_b2.setEndValue(QPoint(x1,y2_n))
        self.anim_b2.setDuration(500) # in ms
        self.anim_b3.setEndValue(QPoint(x1,y1))
        self.anim_b3.setDuration(500) # in ms

        self.groupAnim2 = QSequentialAnimationGroup()
        self.groupAnim2.addAnimation(self.anim_b1)
        self.groupAnim2.addAnimation(self.anim_b2)
        self.groupAnim2.addAnimation(self.anim_b3)
        self.groupAnim2.start()

        self.nodes[i1], self.nodes[i2] = self.nodes[i2], self.nodes[i1]
        print("After:", end='')
        self.print_values()

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

    def showEvent(self, event):
        # Removes nodes from layout and converts them to absolute positioning.
        # This is done once the widgets are fully rendered and shown to get 
        # the exact x,y position.
        for node in self.nodes:
            x2,y2 = getWidgetPosRef(node, RefDirection.DIR_DIAG_UP_LEFT,relativeTo=self)
            self.layout.removeWidget(node)
            node.setParent(self)
            node.move(x2,y2)
            node.show()

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

        self.text = QtWidgets.QLabel("Hello World", alignment=Qt.AlignmentFlag.AlignCenter)
        """
        self.button = QtWidgets.QPushButton("Run Bubble Sort!")
        self.layout = QtWidgets.QVBoxLayout(self)
        """
        self.layout.addWidget(self.text)
        """
        self.layout.addWidget(self.button)
        self.holderWidget = NodeHolderWidget(
            [ random.randint(1,100) for _ in range(5) ],
            spacing=5,
            height=300
        )
        self.layout.addWidget(self.holderWidget)

        self.arrow1 = ArrowWidget(height=30, width=30, color=QColor('green'))
        self.layout.addWidget(self.arrow1)
        self.arrow2 = ArrowWidget(height=30, width=30, color=QColor('orange'))
        self.layout.addWidget(self.arrow2)

        self.holderWidget.print_values()
        
        self.button.clicked.connect(self.magic)

    # > NOTE: The show event is called once the widget has already rendered, and 
    #         positions (coordinates) can be referenced.
    def showEvent(self, event):
        print("Arrow original position:", self.arrow1.pos()) # return (0,0), appears relative to default location.
        print("Arrow geometry:", self.arrow1.geometry())
        # animation working, TODO: trigger repeatedly 
        self.anim = QPropertyAnimation(self.arrow1, b"pos") # object to move/animate and the movement type?

        x,y = getWidgetPosRef(self.holderWidget.nodes[0], RefDirection.DIR_DOWN, self)
        print(x,y)
        self.anim.setEndValue(QPoint(x-self.arrow1.width//2,y))
        self.anim.setDuration(2000) # in ms
        self.anim.start()
        
        x,y = getWidgetPosRef(self.holderWidget.nodes[2], RefDirection.DIR_DOWN, self)
        self.anim2 = QPropertyAnimation(self.arrow2, b"pos") # object to move/animate and the movement type?
        self.anim2.setEndValue(QPoint(x-self.arrow1.width//2,y))
        self.anim2.setDuration(2000) # in ms
        self.anim2.start()

    @Slot()
    def magic(self):
        """
        Updates text for text widget
        
        :param self: Description
        """
        print("Clicked")
        # self.text.setText(random.choice(self.hello))
        self.holderWidget.swap_nodes(0,1)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())