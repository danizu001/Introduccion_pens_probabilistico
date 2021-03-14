import random
import math
from bokeh.plotting import figure, show
def colocarMuestras(num_muestras):
    coord=[]
    arre=[]
    for i in range(num_muestras):
        for j in range(num_muestras):
            arre.append((i,j))
    for i in range(num_muestras):
        x=random.choice(arre)
        coord.append([(x),0])
        for j in range(len(arre)):
            if(x==arre[j]):
                arre.pop(j)
                break
    return coord
def distEucl(x,y,x1,y1):
    dist=math.sqrt((x-x1)**2+(y-y1)**2)
    return dist
def menorDist(coord):
    vec_dis=[]
    for i in range(len(coord)):
        for j in range(len(coord)):
            if j>i:
                x,y = coord[i][0]
                x1,y1=coord[j][0]
                dist=distEucl(x, y, x1, y1)
                vec_dis.append([coord[i][0],coord[j][0],dist])
    return vec_dis
def minimo(vec_dis):
    menor=vec_dis[0][2]
    pos=0
    for i in range(len(vec_dis)):
        if vec_dis[i][2]<menor:
            menor=vec_dis[i][2]
            pos=i
    return menor,pos
def cluster(vec_dis,coord,num_cluster=2):
    menor,pos=minimo(vec_dis)
    band=0
    cont=0
    for i in range(len(coord)):
        if (coord[i][1]==0):
            cont+=1
    if (num_cluster > 0 and cont > num_cluster):
        for j in range(len(coord)):
            if (vec_dis[pos][0]==coord[j][0] and coord[j][1]!=0):
                clu=coord[j][1]
                for i in range(len(coord)):
                    if(coord[i][0]==vec_dis[pos][1]):
                        coord[i][1]=clu
                        vec_dis[pos][2]=1000
                        band=1
                        cluster(vec_dis,coord,num_cluster)
            if (vec_dis[pos][1]==coord[j][0] and coord[j][1]!=0):
                clu=coord[j][1]
                for i in range(len(coord)):
                    if(coord[i][0]==vec_dis[pos][0]):
                        coord[i][1]=clu
                        vec_dis[pos][2]=1000
                        band=1
                        cluster(vec_dis,coord,num_cluster)
        if(band==0):
            for j in range(len(coord)):
                if(coord[j][0]==vec_dis[pos][0] or coord[j][0]==vec_dis[pos][1]):         
                    coord[j][1]=num_cluster
            vec_dis[pos][2]=1000
            num_cluster-=1   
            cluster(vec_dis,coord,num_cluster)
    if(num_cluster==0):
        faltantes=[]
        cluster1=[]
        cluster2=[]
        for i in range(len(coord)):
            if (coord[i][1]==0):
                faltantes.append(coord[i][0])
            if (coord[i][1]==1):
                cluster1.append(coord[i][0])
            if (coord[i][1]==2):
                cluster2.append(coord[i][0])
        res=distCluster(faltantes, cluster1, cluster2)
        for i in range(len(coord)):
            for j in range(len(faltantes)):
                if coord[i][0]==res[j][0]:
                    coord[i][1]=res[j][1]
    return coord
def distCluster(faltantes,cluster1,cluster2):
    bc1=[]
    bc2=[]
    res=[]
    min1=[]
    min2=[]
    for i in faltantes:
        for j in cluster1:
            bc1.append([0,0,distEucl(i[0],i[1],j[0],j[1])])
        for j in cluster2:
            bc2.append([0,0,distEucl(i[0],i[1],j[0],j[1])])
        min1=minimo(bc1)
        min2=minimo(bc2)
        if min1<=min2:
            res.append([i,1])
        if min2<min1:
            res.append([i,2])
    return res
def graficar(coord):
    p = figure(plot_width=400, plot_height=400)
    for i in range(len(coord)):
        if(coord[i][1]==2):
            p.circle(coord[i][0][0],coord[i][0][1], color="navy")
        if(coord[i][1]==1):
            p.circle(coord[i][0][0],coord[i][0][1], color="red")
    show(p)
        
if __name__=='__main__':
    coord=[]
    num_muestras=int(input("Digite el numero de muestras que desea colocar en el campo"))
    coord=colocarMuestras(num_muestras)
    vec_dis=menorDist(coord)
    col=cluster(vec_dis,coord)
    graficar(col)