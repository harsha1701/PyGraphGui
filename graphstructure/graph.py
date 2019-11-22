from .point import point
from .edge import edge
class graph():
    def __init__(self):
        self.points=[]
        self.edges=[] 
        self.adjacency=[] 
        self.indiset=[]
        self.vc=[]
    def nearestpoint(self,a,b):
        dist=1000
        for i in self.points:
            dist1=((a-i.x)**2+(b-i.y)**2)**(1/2)
            if dist1<dist:
                dist=dist1
                p=point(i.x,i.y)
        if dist>20:
            p=point(a,b)
        return p    
    def insertpoint(self,p):
        try:
            j=self.points.index(p)
        except ValueError:
            self.points.append(p)
        else:
            p=self.points[j]
        return p
    def insertedge(self,a,b,c):
        if a!=b:
            tempedge=edge(a,b)
            try:
                j=self.edges.index(tempedge)
            except ValueError:
                tempedge.color=c
                tempedge.setlength()
                self.edges.append(tempedge)
            else:
                self.edges[j].color=c
    def createadja(self):
        self.adjacency=[[False for i in self.points] for i in self.points]
        for i in self.edges:
            j=self.points.index(i.start)
            k=self.points.index(i.end)
            self.adjacency[j][k]=True
            self.adjacency[k][j]=True

    def getadja(self):
        for i in self.adjacency:
            print(i)
    def movepoints(self,l,m,n):
        for i in l:
            p=self.nearestpoint(i.x+m,i.y+n)
            i.x=p.x
            i.y=p.y
    def regraph(self,s):
        i=0
        while i<len(self.points):
            try:
                j=self.points.index(self.points[i],i+1)
            except ValueError:
                i=i+1
            else:
                k=0
                l=[]
                while k<len(self.edges):
                    if self.edges[k].isnode(self.points[j]):
                        l.append([self.edges[k].getothernode(self.points[j]),self.edges[k].color])
                        del self.edges[k]
                    else:
                        k=k+1
                s.remove(self.points[j])
                s.append(self.points[i])
                del self.points[j]
                temp=self.insertpoint(self.points[i])
                for k in l:
                    self.insertedge(temp,k[0],k[1])
                i=i+1
    def getedges(self,p):
        l=[]
        for i in self.edges:
            if i.isnode(p):
                l.append(i)
        return l
    def delete(self,l):
        for i in l:
            edges=self.getedges(i)
            for j in edges:
                self.edges.remove(j)
            self.points.remove(i)
        del l
    def invert(self):
        self.adjacency=[[True for i in self.points] for i in self.points]
        for i in self.edges:
            j=self.points.index(i.start)
            k=self.points.index(i.end)
            self.adjacency[j][k]=False
            self.adjacency[k][j]=False        
        for i in range(len(self.points)):
            self.adjacency[i][i]=False
