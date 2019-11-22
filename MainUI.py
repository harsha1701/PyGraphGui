from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from graphstructure import * 
from UI import * 
import sys
class cbutton(QPushButton):
    def __init__(self,parent,i,main,tool):
        super().__init__(parent)
        self.main=main
        self.tool=tool
        self.j=0 if i>=4 and i<=8 else 128 if i==3 or i==9 else 255
        self.k=255 if i>=2 and i<=6 else 128 if i==1 or i==7 else 0
        self.l=0 if i>=0 and i<=4 else 128 if i==5 or i==11 else 255
        self.setStyleSheet("border:2px solid black;background:rgb(%d,%d,%d)"%(self.j,self.k,self.l))
    def press(self):
        temp=self.main.pane
        if self.tool:
            temp.pointcol=QColor(self.j,self.k,self.l)
        else:
            temp.edgecol=QColor(self.j,self.k,self.l)


class ctab(QWidget):
    def __init__(self,main,tool):
        super().__init__()
        for i in range(12):
            but=cbutton(self,i,main,tool)
            but.setGeometry(70*(i%4),25*(i//4)+10,20,20)
            but.pressed.connect(but.press)

class widget(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.graph=graph()
        self.selected=[]
        self.parent=parent
        # self.prevgraph=[]
        # self.undo=True

        self.editable=True
        self.movable=False
        self.selectable=False
        self.qp=QPainter(self)
        self.pointcol=Qt.red
        self.edgecol=Qt.blue
        self.pen1=QPen(self.pointcol,15,Qt.SolidLine,Qt.RoundCap,Qt.BevelJoin)
        self.pen2=QPen(self.edgecol,5)
        self.update()
        self.setMouseTracking(True)
    def mouseMoveEvent(self, event):
        self.parent.mouse.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))
        

    def mousePressEvent(self,event):
        self.p1=self.graph.nearestpoint(event.pos().x(),event.pos().y())
        if event.button()==Qt.LeftButton:
            if self.editable:
                self.p1.color=self.pointcol
                self.p1=self.graph.insertpoint(self.p1)
            if self.movable:
                self.setCursor(QCursor(Qt.DragMoveCursor))

    
    def mouseDoubleClickEvent(self,event):
        if event.button()==Qt.LeftButton:
            if self.selectable and self.p1 in self.graph.points:
                self.p1=self.graph.insertpoint(self.p1)
                if self.p1 in self.selected:
                    self.selected.remove(self.p1)
                else:
                    self.selected.append(self.p1)       
    
    def mouseReleaseEvent(self,event):
        self.p2=self.graph.nearestpoint(event.pos().x(),event.pos().y())
        print(self.p2.x,self.p2.y)
        if event.button()==Qt.LeftButton:
            if self.editable:
                self.p2.color=self.pointcol
                self.p2=self.graph.insertpoint(self.p2)         
                self.graph.insertedge(self.p1,self.p2,self.edgecol)
            if self.movable:
                self.setCursor(QCursor(Qt.SizeAllCursor))                
                if len(self.selected)==0:
                    self.graph.movepoints(self.graph.points,self.p2.x-self.p1.x,self.p2.y-self.p1.y)
                else:
                    self.graph.movepoints(self.selected,self.p2.x-self.p1.x,self.p2.y-self.p1.y)
                    self.graph.regraph(self.selected)
        # if self.undo:
        #     self.prevgraph.append([self.graph,self.selected])
        # else:
        #     self.undo=True        
        # print(len(self.prevgraph))
        self.update()

    def paintEvent(self,event):
        self.qp.begin(self)
        self.qp.fillRect(QRect(0,0,1000,500),Qt.white)
        for i in self.graph.points:
            if i in self.selected:            
                self.pen1.setBrush(Qt.magenta)
            elif i in self.graph.indiset:
                self.pen1.setBrush(Qt.black)
            elif i in self.graph.vc:
                self.pen1.setBrush(Qt.green)                
            else:
                self.pen1.setBrush(i.color)
            self.qp.setPen(self.pen1)
            self.qp.drawPoint(i.x,i.y)
        for i in self.graph.edges:
            if i.start in self.selected or i.end in self.selected:
                self.pen2.setBrush(Qt.cyan)
            else:
                self.pen2.setBrush(i.color)
            self.qp.setPen(self.pen2)                            
            self.qp.drawLine(i.start.x,i.start.y,i.end.x,i.end.y)
        self.qp.end()


        
    def deleteselected(self):
        for i in self.selected:
            delete(self.graph,i)
        self.update()


class app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyGraphGui")
        self.setStyleSheet(
            """
             QMainWindow{background:rgb(200,210,226);border:0px solid black;}
             QMenuBar{background:white;color:black;border:0px solid black}
             QMenuBar::item:pressed{background:rgb(245,246,247);}
             QMenu{background:rgb(245,246,247);color:black;}
             QFrame{border:0px solid black;border-right:1px solid black}
             QLabel{border:0px solid black;border-right:1px solid black;color:rgb(140,90,145);background:rgb(245,246,247);}
            """
        )
        self.resize(1000,650)

        menubar=self.menuBar()  
        menubar.setGeometry(QRect(0,0,1000,20))

        mfile=menubar.addMenu("File")

        newaction=QAction("New",self)
        newaction.setShortcut("Ctrl+n")
        newaction.triggered.connect(lambda : newgraph(self.pane))
        mfile.addAction(newaction)
        saveaction=QAction("Save",self)
        saveaction.setShortcut("Ctrl+s")
        saveaction.triggered.connect(lambda:savegraph(self.pane))
        mfile.addAction(saveaction)
        openaction=QAction("Open",self)
        openaction.setShortcut("Ctrl+o")
        openaction.triggered.connect(lambda:opengraph(self.pane))
        mfile.addAction(openaction)

        medit=menubar.addMenu("Edit")

        deleteaction=QAction("Delete",self)
        deleteaction.setShortcut("Delete")
        deleteaction.triggered.connect(self.deleteselected)
        medit.addAction(deleteaction)
        # undoaction=QAction("Undo",self)
        # undoaction.setShortcut("Ctrl+z")
        # undoaction.triggered.connect(self.undo)
        # medit.addAction(undoaction)        
        reselectaction=QAction("Reselect",self)
        reselectaction.setShortcut("Esc")
        reselectaction.triggered.connect(self.reselect)
        medit.addAction(reselectaction)
        mhelp=menubar.addMenu("Help")




        self.pane=widget(self)
        self.pane.setGeometry(0,150,1000,500)
        self.editable()

        options=QFrame(self)
        options.setGeometry(0,25,1000,125)


        tools=QFrame(options)
        tools.setGeometry(0,0,200,60)
        tools.setStyleSheet("border-bottom:1px solid black")
        
        label1=QLabel(tools)
        label1.setGeometry(0,0,200,20)
        label1.setText("Tools")
        label1.setAlignment(Qt.AlignCenter)

        pencil=QPushButton(tools)
        pencil.setShortcut("e")
        pencil.clicked.connect(self.editable)
        pencil.setGeometry(70,23,30,30)
        pencil.setIcon(QIcon("Pencil.png"))


        mover=QPushButton(tools)
        mover.setShortcut("m")
        mover.clicked.connect(self.movable)
        mover.setGeometry(105,23,30,30)
        mover.setIcon(QIcon("mover.png"))



        operations=QFrame(options)
        operations.setGeometry(0,60,200,600)
        
        label2=QLabel(operations)
        label2.setGeometry(0,0,200,20)
        label2.setText("Operations")
        label2.setAlignment(Qt.AlignCenter)        

        indisetb=QPushButton(operations)
        indisetb.clicked.connect(self.calindiset)
        indisetb.setGeometry(35,23,30,30)
        indisetb.setText("IS")

        vcb=QPushButton(operations)
        vcb.clicked.connect(self.calvc)
        vcb.setGeometry(75,23,30,30)
        vcb.setText("VC")

        mcb=QPushButton(operations)
        mcb.clicked.connect(self.calmc)
        mcb.setGeometry(115,23,30,30)
        mcb.setText("MC")

        colors=QTabWidget(options)
        colors.setGeometry(250,0,250,130)
        colors.setStyleSheet("border:0px solid black;background:rgb(200,210,226);")
        pointcol=ctab(self,True)
        pointcol.setStyleSheet("border:0px black;")
        edgecol=ctab(self,False)
        colors.addTab(pointcol,"Point Color")
        colors.addTab(edgecol,"Edge Color")        

        self.mouse=QLabel(options)
        self.mouse.setGeometry(800,100,200,20)





    def reselect(self):
        if self.pane.movable:
            self.pane.movable=False
        elif self.pane.editable:
            self.pane.editable=False
        else:
            self.pane.selected=[]
            self.pane.update()
        self.pane.selectable=True
        self.pane.setCursor(QCursor(Qt.ArrowCursor))
    def deleteselected(self):
        pane=self.pane
        pane.graph.delete(pane.selected)
        pane.selected=[]
        pane.update()
    # def undo(self):
    #     if len(self.pane.prevgraph)>0:
    #         temp= self.pane.prevgraph.pop(-1)
    #         self.pane.graph=temp[0]
    #         self.pane.selected=temp[1]
    #         self.pane.undo=False
    #         self.pane.update()
    def editable(self):
        self.pane.editable=True
        self.pane.movable=False
        self.pane.selectable=False
        self.pane.setCursor(QCursor(Qt.CrossCursor))
    def movable(self):
        self.pane.movable=True
        self.pane.editable=False
        self.pane.selectable=False
        self.pane.setCursor(QCursor(Qt.SizeAllCursor))            
    def calindiset(self):
        self.pane.graph.createadja()
        self.pane.graph.indiset=[]
        self.pane.graph.vc=[] 
        indiset(self.pane.graph)
        self.pane.update()       
    def calvc(self):
        self.calindiset()
        for i in self.pane.graph.points:
            if i not in self.pane.graph.indiset:
                self.pane.graph.vc.append(i)
        self.pane.graph.indiset=[]
        self.pane.update()
    def calmc(self):
        self.pane.graph.indiset=[]
        self.pane.graph.vc=[] 
        self.pane.graph.invert()
        indiset(self.pane.graph)
        self.update()
       

        




    

                


window=QApplication(sys.argv)
app=app()
app.show()
window.exec_()
