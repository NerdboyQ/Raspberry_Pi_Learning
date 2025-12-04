import sys
import random
import time
from enum import Enum
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, Slot, QRect, QTimer, QParallelAnimationGroup, QPoint, QPropertyAnimation, QSequentialAnimationGroup
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

        self.spacing = spacing
        self.layout.setSpacing(self.spacing)
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
        rand_color = random.randint(0, len(dflt_QtColors)-1)
        rand_color = dflt_QtColors[rand_color]
        print("Random color selected:", rand_color)

        for v in lst:
            # n = NodeWidget(height//4,color=rand_color,text=v)
            n = NodeWidget(height//4, text=v)
            self.add_node(n)

    def swap_node_data(self, i1, i2):
        self.nodes[i1],self.nodes[i2] = self.nodes[i2],self.nodes[i1]

    def print_values(self, arr = None):
        if arr is None: arr = [int(i.text) for i in self.nodes]
        print("[",end='')
        for node in self.nodes:
            if node == self.nodes[0]: print(node.text, end='')
            else: print(f",{node.text}", end='')
        print("]")

    def swap_nodes(self, i1: int, i2: int, finishedHandler, duration: int = 500):
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
        # self.groupAnim2.start()

        self.animGroup = QParallelAnimationGroup()
        self.animGroup.addAnimation(self.groupAnim1)
        self.animGroup.addAnimation(self.groupAnim2)

        # 1. Once animations are done, perform the logical swap in the list
        self.animGroup.finished.connect(lambda: self.swap_node_data(i1, i2))
        
        # 2. Connect the final handler (from MyWidget) to continue the step sequence
        self.animGroup.finished.connect(finishedHandler)
        self.animGroup.start()
        

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
    class AnimationOpt(Enum):
        """
        Animation Options
        """
        COMPARE = 0,
        SWAP = 1

    def __init__(self):
        """
        Constructor for Custom widget basics
        """
        super().__init__()
        self.currentAnimStep_Idx = 0
        self.animSteps = []
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
        self.arrow1.setParent(self)
        self.arrow1.move(0,0)
        self.arrow1.show()
        self.arrow1_i1 = 0

        self.arrow2 = ArrowWidget(height=30, width=30, color=QColor('orange'))
        self.arrow2.setParent(self)
        self.arrow2.move(0,0)
        self.arrow2.show()
        self.arrow1_i2 = 1

        self.holderWidget.print_values()

        self.animGroup = None
        self.animStep = 0
        self.animMaxSteps = 1   # forces the animation to only run once
        
        self.button.clicked.connect(self.bubble_sort)

    def _run_single_anim_step(self):
        if self.currentAnimStep_Idx >= len(self.animSteps):
            print(" -- Animation Complete -- ")
            return

        op, i1, i2 = self.animSteps[self.currentAnimStep_Idx]
        self.currentAnimStep_Idx+=1

        if op == self.AnimationOpt.COMPARE:
            self.moveArrows(i1,i2,500,nextAction=self.animStepDone)
        else:
            self.holderWidget.swap_nodes(i1,i2,self.animStepDone)

    @Slot()
    def animStepDone(self):
        if self.animGroup and self.animGroup.finished:
            self.animGroup.finished.disconnect(self.animStepDone)

        PAUSE_MS = 500

        QTimer.singleShot(PAUSE_MS, self._run_single_anim_step)

    def moveArrows(self, i1: int = -1, i2: int = -1, duration: int = 100, nextAction = None):
        if i1 < 0: i1 = self.arrow1_i1
        if i2 < 0: i2 = self.arrow1_i2
        
        spc = self.holderWidget.spacing
        self.animGroup = QParallelAnimationGroup()
        
        # n1, n2 = self.holderWidget.nodes[i1], self.holderWidget.nodes[i2]
        # --- Arrow 1 Animation --- #
        anim1 = QPropertyAnimation(self.arrow1, b"pos") # object to move/animate and the movement type?

        x,y = self.start_ref_pos
        x += i1*(self.holderWidget.nodes[0].width() + spc)
        print(f"n1[{i1}], x: {x}, y: {y} - ", end="")
        anim1.setEndValue(QPoint(x-self.arrow1.width//2,y))
        anim1.setDuration(duration) # in ms
        
        # --- Arrow 2 Animation --- #
        x,y = self.start_ref_pos
        x += i2*(self.holderWidget.nodes[0].width() + spc)
        print(f"n2[{i2}]",x,y)
        anim2 = QPropertyAnimation(self.arrow2, b"pos") # object to move/animate and the movement type?
        anim2.setEndValue(QPoint(x-self.arrow1.width//2,y))
        anim2.setDuration(duration) # in ms
        
        self.animGroup.addAnimation(anim1)
        self.animGroup.addAnimation(anim2)

        if nextAction: self.animGroup.finished.connect(nextAction)

        self.animGroup.start()


    # > NOTE: The show event is called once the widget has already rendered, and 
    #         positions (coordinates) can be referenced.
    def showEvent(self, event):
        print("Arrow original position:", self.arrow1.pos()) # return (0,0), appears relative to default location.
        print("Arrow geometry:", self.arrow1.geometry())
        x,y = self.start_ref_pos = getWidgetPosRef(self.holderWidget.nodes[0],RefDirection.DIR_DOWN,self)
        print(x,y) 
        self.arrow1.move(x-self.arrow1.width//2, y)
        self.arrow2.move(x+2*(self.holderWidget.nodes[0].width()//2+self.holderWidget.spacing//2)-self.arrow1.width//2, y)

    @Slot()
    def bubble_sort(self):
        """
        Updates text for text widget
        
        :param self: Description
        """
        self.animSteps = []
        temp_data = [int(n.text) for n in self.holderWidget.nodes]
        print("Clicked")
        # self.text.setText(random.choice(self.hello))
        N = len(self.holderWidget.nodes)
        print("Before:", end='')
        self.holderWidget.print_values()

        for i in range(N-1):
            for j in range(N-1-i):
                self.animSteps.append((self.AnimationOpt.COMPARE, j, j+1))
                n1, n2 = temp_data[j], temp_data[j+1]
                if n1 > n2:
                    temp_data[j], temp_data[j+1] = temp_data[j+1], temp_data[j]
                    self.animSteps.append((self.AnimationOpt.SWAP, j, j+1))
                    # self.holderWidget.nodes[j], self.holderWidget.nodes[j+1] = self.holderWidget.nodes[j+1], self.holderWidget.nodes[j]

                    print(f"\t\tafter swap:", end='')
                    self.holderWidget.print_values()

            print(f"\tafter iteration[{i+1}]:", end='')
            self.holderWidget.print_values(arr=temp_data)

        print("Done sorting, final array:", end='')
        self.holderWidget.print_values(arr=temp_data)

        for x in self.animSteps:
            print("\t-",x)
        self.currentAnimStep_Idx = 0
        self._run_single_anim_step()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())