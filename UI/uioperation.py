from PyQt5.QtWidgets import QFileDialog
import pickle
def savegraph(pane):
    filePath, _ = QFileDialog.getSaveFileName(pane, "Save Graph", "", "graph(*.graph)")
    with open(filePath,'wb') as f:
            pickle.dump(pane.graph.points,f)
            pickle.dump(pane.graph.edges,f)
def opengraph(pane):
    filePath, _ = QFileDialog.getOpenFileName(pane, "Open Graph", "", "graph(*.graph)")
    with open(filePath,'rb') as f:
            pane.graph.points=pickle.load(f)
            pane.graph.edges=[]
            edges=pickle.load(f)
            for i in edges:
                    pane.graph.insertedge(pane.graph.insertpoint(i.start),pane.graph.insertpoint(i.end),i.color)
    pane.update()
def newgraph(pane):
    pane.graph.points=[]
    pane.graph.edges=[]
    pane.selected=[]
    pane.flag=False
    pane.update()