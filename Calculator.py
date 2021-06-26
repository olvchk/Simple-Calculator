from PyQt5.QtCore import QEvent, QObject, QPoint, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QPainterPath, QRegion, QResizeEvent, QScreen
from PyQt5.QtWidgets import QApplication, QBoxLayout, QDesktopWidget, QGridLayout, QLabel, QPushButton, QWidget
import sys
import operator

ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,  # use operator.div for Python 2
    '%' : operator.mod,
}

class Calculator(QWidget):
  def __init__(self):
    super().__init__()
    self.pressing = False
    self.topnumber = ''
    self.botnumber = ''
    self.operator = ''
    self.init_component()
    self.init_window()
    self.show()

  

  def init_window(self):
    screen = QDesktopWidget().screenGeometry()
    self.maxHeight, self.maxWidth = screen.height(), screen.width()
    self.top, self.left = self.maxHeight // 2 - self.height() // 2, self.maxWidth // 2 - self.width() // 2
    self.setWindowTitle('Simple Calculator - Oiko')
    self.setGeometry(self.left, self.top, self.width(), self.height())
  
  def init_component(self):

    titlebar = TitleBar(self)

    btn_size = 20
    title = QLabel('Minimalistic Simple Calculator - Oiko')
    title.setObjectName('title')
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    exit_btn = QPushButton(titlebar)
    exit_btn.setObjectName('ExitBtn')
    exit_btn.setFixedSize(btn_size, btn_size)
    exit_btn.setCursor(QCursor(Qt.PointingHandCursor))
    exit_btn.clicked.connect(lambda: self.close())
  
    min_btn = QPushButton(titlebar)
    min_btn.setObjectName('MinBtn')
    min_btn.setFixedSize(btn_size, btn_size)
    min_btn.setCursor(QCursor(Qt.PointingHandCursor))
    min_btn.clicked.connect(lambda: self.showMinimized())
 
    max_btn = QPushButton(titlebar)
    max_btn.setObjectName('MaxBtn')
    max_btn.setFixedSize(btn_size, btn_size)
    max_btn.setCursor(QCursor(Qt.PointingHandCursor))
    max_btn.clicked.connect(lambda: self.showMaximized() if self.width() != self.maxWidth and self.height() != self.maxHeight else self.showNormal())

    btnlayout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
    btnlayout.addWidget(exit_btn)
    btnlayout.addWidget(max_btn)
    btnlayout.addWidget(min_btn)

    titlebar.layout.addLayout(btnlayout)
    titlebar.layout.addWidget(title)

    topnumber = QLabel(self.topnumber)
    topnumber.setObjectName('TopNumber')
    topnumber.setAlignment(Qt.AlignmentFlag.AlignRight)

    botnumber = QLabel(self.botnumber)
    botnumber.setObjectName('BotNumber')
    botnumber.setAlignment(Qt.AlignmentFlag.AlignRight)

    topframe = QWidget(self)
    topframe.setObjectName('TopFrame')
    topframe.setMaximumHeight(200)
    topframelayout = QBoxLayout(QBoxLayout.Direction.Down, topframe)
    topframelayout.setContentsMargins(40, 10, 40, 30)
    topframelayout.setSpacing(10)
    topframelayout.addWidget(topnumber)
    topframelayout.addWidget(botnumber)

    ac = QLabel('ac')
    plusminus = QLabel('+/-')
    persen = QLabel('%')
    divide = QLabel('/')
    multiply = QLabel('*')
    minus = QLabel('-')
    plus = QLabel('+')
    equal = QLabel('=')
    coma = QLabel('.')
    one = QLabel('1')
    two = QLabel('2')
    three = QLabel('3')
    four = QLabel('4')
    five = QLabel('5')
    six = QLabel('6')
    seven = QLabel('7')
    eight = QLabel('8')
    nine = QLabel('9')
    zero = QLabel('0')
    botWidgets = [ac, plusminus, persen, divide, multiply, minus, plus, equal, coma, one, two, three, four, five, six, seven, eight, nine, zero]

    def addnumber(widget):
      num = widget.text()
      if self.operator == '=':
        self.botnumber = ''
        botnumber.setText(self.botnumber)
        self.operator = ''
      if len(self.botnumber) == 1 and self.botnumber == '0' and num != '.':
        self.botnumber = ''
      self.botnumber += num
      botnumber.setText(self.botnumber)
    
    def calculate(widget):
      operator = widget.text()
      if self.topnumber != '' and self.operator != '' and self.botnumber != '' and operator != '=':
        self.botnumber = str(ops[self.operator](float(self.topnumber), float(self.botnumber)))
        self.botnumber = self.botnumber[:-2] if self.botnumber.endswith('.0') else self.botnumber[:15]
        self.topnumber = self.botnumber
        self.botnumber = ''
        self.operator = operator
        topnumber.setText(f'{self.topnumber} {self.operator} ')
        botnumber.setText(self.botnumber)
        return
      if operator == '=':
        if self.operator == '' or self.topnumber == '' or self.botnumber == '':
          return
        self.botnumber = str(ops[self.operator](float(self.topnumber), float(self.botnumber)))
        self.botnumber = self.botnumber[:-2] if self.botnumber.endswith('.0') else self.botnumber[:15]
        self.topnumber = ''
        topnumber.setText(self.topnumber)
        botnumber.setText(self.botnumber)
        self.operator = '='
        return

      self.operator = operator
      if self.operator == '+/-':
        if self.botnumber.find('-') == -1:
          self.botnumber = f'-{self.botnumber}'
        else:
          self.botnumber = self.botnumber.strip('-')
        botnumber.setText(self.botnumber)
        return
      if self.operator == 'ac':
        self.botnumber = ''
        self.topnumber = ''
        self.operator = ''
        topnumber.setText(self.topnumber)
        botnumber.setText(self.botnumber)
        return
      if self.topnumber == '':
        self.topnumber = self.botnumber
        self.botnumber = ''
        topnumber.setText(f'{self.topnumber} {self.operator} ')
        botnumber.setText(self.botnumber)
        return
      topnumber.setText(f'{self.topnumber} {self.operator} ')

      
      


    for widget in botWidgets:
      widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
      widget.setFixedSize(80, 80)
      if widget.text() in "0123456789.":
        widget.mousePressEvent = lambda a, x = widget: addnumber(x)
        widget.setObjectName('number')
      else:
        widget.mousePressEvent = lambda a, x = widget: calculate(x)
        widget.setObjectName('operator')

    botframe = QWidget(self)
    botframe.setObjectName('BotFrame')
  
    botframe.setContentsMargins(10, 30, 10, 30)
    botframelayout = QGridLayout(botframe)
    botframelayout.addWidget(ac, 0, 0)
    botframelayout.addWidget(plusminus, 0, 1)
    botframelayout.addWidget(persen, 0, 2)
    botframelayout.addWidget(divide, 0, 3)
    botframelayout.addWidget(seven, 1, 0)
    botframelayout.addWidget(eight, 1, 1)
    botframelayout.addWidget(nine, 1, 2)
    botframelayout.addWidget(multiply, 1, 3)
    botframelayout.addWidget(four, 2, 0)
    botframelayout.addWidget(five, 2, 1)
    botframelayout.addWidget(six, 2, 2)
    botframelayout.addWidget(minus, 2, 3)
    botframelayout.addWidget(one, 3, 0)
    botframelayout.addWidget(two, 3, 1)
    botframelayout.addWidget(three, 3, 2)
    botframelayout.addWidget(plus, 3, 3)
    botframelayout.addWidget(zero, 4, 1)
    botframelayout.addWidget(coma, 4, 2)
    botframelayout.addWidget(equal, 4, 3)
    
    defaultlayout = QBoxLayout(QBoxLayout.Direction.Down)
    defaultlayout.setContentsMargins(0, 0, 0, 0)
    defaultlayout.setSpacing(0)
    defaultlayout.addWidget(titlebar)
    defaultlayout.addWidget(topframe)
    defaultlayout.addWidget(botframe)
    defaultlayout.setStretch(2, 1)
    self.setLayout(defaultlayout)

    # path = QPainterPath()
    # print(self.rect())
    # path.addRoundedRect(QRectF(self.rect()), 20, 20)
    # mask = QRegion(path.toFillPolygon().toPolygon())
    # self.setMask(mask)

    self.setFixedSize(500, 650)
    self.setWindowFlag(Qt.FramelessWindowHint)
    self.adjustSize()
    self.setContentsMargins(2, 2, 2, 2)
    self.setObjectName('Calculator')
    self.setStyleSheet(css)
    print(self.width(), self.height())

class TitleBar(QWidget):
  def __init__(self, parent):
    super(TitleBar, self).__init__()
    self.start = QPoint(0, 0)
    self.pressing = False
    self.parent = parent
    self.setFixedHeight(50)
    self.setContentsMargins(0, 0, 0, 0)
    self.layout = QBoxLayout(QBoxLayout.Direction.LeftToRight, self)
    self.layout.setContentsMargins(15, 0, 15, 0)

  def mousePressEvent(self, event):
    self.start = self.mapToGlobal(event.pos())
    self.pressing = True
  
  def mouseMoveEvent(self, event):
    if self.pressing:
      if self.parent.width() == self.parent.maxWidth and self.parent.height() == self.parent.maxHeight:
        self.parent.showNormal()
      self.end = self.mapToGlobal(event.pos())
      self.movement = self.end-self.start
      self.parent.setGeometry(self.parent.mapToGlobal(self.movement).x(), self.parent.mapToGlobal(self.movement).y(), self.parent.width(), self.parent.height())
      self.start = self.end
  
  def mouseReleaseEvent(self, QMouseEvent):
    self.pressing = False
css = """
#Calculator {
  background-color: #FEFEFF; 
  border-radius: 20%;
}
#BotFrame {
  background-color: #28272d; 
}
#TopFrame {
  background-color: #FEFEFF; 
}
#TopNumber {
  color: #D7D7D7; 
  font-size: 25px; 
  font-family: 'Poppins' sans-serif; 
}
#BotNumber {
  color: #28272d; 
  font-size: 50px; 
  font-family: 'Poppins' sans-serif; 
} 
#MinBtn {
  background-color: #9BE044; 
  border-radius: 10px;
  border: 2px solid #D0F1A7;
}
#MinBtn:pressed {
  background-color: #78C11F; 
  border-radius: 10px;
}
#MaxBtn {
  background-color: #F0D264; 
  border-radius: 10px;
  border: 2px solid #F9EFC7;
}
#MaxBtn:pressed {
  background-color: #E9BD20; 
  border-radius: 10px;
}
#ExitBtn {
  background-color: #F34A5C; 
  border-radius: 10px;
  border: 2px solid #FAB2B9
}
#ExitBtn:pressed {
  background-color: #E60F24; 
  border-radius: 10px;
}
#title {
  font-family: 'Poppins' sans-serif;
  font-size: 17px;
}
#TitleBar{
  background: #FEFEFF;
}
#number {
  color: #FEFEFF; 
  font-size: 35px; 
  font-family: 'Poppins' sans-serif; 
  font-weight: 500; 
}

#operator {
  color: #929196; 
  font-family: 'Poppins' sans-serif; 
  font-size: 35px; 
  font-weight: 500; 
}
"""

app = QApplication(sys.argv)
calculator = Calculator()
sys.exit(app.exec_())