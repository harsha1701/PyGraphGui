def indiset(graph):
    def isind(l):
        if len(l)==0:
            return False
        for i in l:
            for j in l:
                if graph.adjacency[i][j]:
                    return False
        return True
    def func(l,k):
        if len(l)>=k and isind(l):
            for i in l:
                graph.indiset.append(graph.points[i])
            return True
        v=False
        for i in range(len(l)):
            x=l.pop(0)
            v=v or func(l,k)
            if v:
                return True
            l.append(x)
        return False
    k=len(graph.points)
    l=list(range(k))
    flag=False
    while ~flag:
        flag=func(l,k)
        k=k-1
        if k==0:
            break



