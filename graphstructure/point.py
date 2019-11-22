from PyQt5.QtCore import *
class point:
    def __init__(self,x,y):
        self.x=x if x>0 else 0
        self.y=y if y>0 else 0
        self.color=Qt.red
    def __eq__(self,a):
        return self.x==a.x and self.y==a.y
