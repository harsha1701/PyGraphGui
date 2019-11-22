from PyQt5.QtCore import *
class edge:
    def __init__(self,a,b):
        self.start=a
        self.end=b
        self.color=Qt.blue
        self.length=100000
    def __eq__(self,b):
        return self.isnode(b.start) and self.isnode(b.end)
    def isnode(self,a):
        return self.start==a or a==self.end
    def getothernode(self,node):
        if node==self.start:
            return self.end
        else:
            return self.start
    def setlength(self):
        self.length=((self.start.x-self.end.x)**2+(self.start.y-self.end.y)**2)**0.5 
