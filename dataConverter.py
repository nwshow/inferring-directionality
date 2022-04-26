'''
Created on Apr 5, 2022

@author: noahw
'''
import networkx as netx
import numpy as np
import csv
import sys

def edgeListImporter(path, fn):
    
    file = open(path + fn,"r")
    print(file.readline())
    lines = file.readlines()
    file.close()
    
    graph = netx.DiGraph()
    for l in lines:
        parse = l.split(',')
        
        #If the edge is new to the graph
        if not(graph.has_edge(parse[0], parse[1])):
            graph.add_edge(parse[0], parse[1], weight = float(parse[2]))
        #Else if the weight is already a list
        elif isinstance(graph.edges[parse[0], parse[1]]['weight'], list):
            graph.edges[parse[0], parse[1]]['weight'].append(float(parse[2]))
        #Otherwise, shift weight from num to list
        else:
            init = graph.edges[parse[0], parse[1]]['weight']
            valList = [init, float(parse[2])]
            graph.add_edge(parse[0], parse[1], weight = valList)
    
    for u, v, w in graph.edges(data ="weight"):
        if isinstance(w,list):
            graph.add_edge(u, v, weight = np.mean(w))
    
    print(netx.info(graph))
    return graph

def graphml_importer(path,fn):
#Parameters
#    filename: string of GraphML file path
#Product:
#    g: graph represented by the gmlFile
    g = netx.read_graphml(path+fn)
    print(fn)
    print(netx.info(g))
    return g

def graphToAdj(g, path, output):
    
    nodeList = netx.nodes(g)
    
    adjMat = [[""]]
    for n in nodeList:
        adjMat[0].append(n)
    
    count = 1
    for i in nodeList:
        adjMat.append([i])
        for j in nodeList:
            weight = g.get_edge_data(i,j,default = {'weight':0})
            adjMat[count].append(str(weight['weight']))
        count += 1
    
    print(str(len(adjMat)) + " x " + str(len(adjMat[0])))
    
    with open(path+output, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerows(adjMat)
    pass

def graphToEdgeList(g, path, output):
    eL = netx.edges(g,data = True)
    
    pass

def posToDistMat(path, fn, output):
#Does not check for duplicate node entries
    file = open(path + fn,"r")
    print(file.readline())
    lines = file.readlines()
    file.close()
    
    nodes = {}
    distMat = [[""]]
    for line in lines:
        parse = line.split(',')
        nodes.update({parse[0]:[parse[1],parse[2],parse[3]]})
        distMat[0].append(parse[0])
        distMat.append([parse[0]])
    
    skipRow = True
    for row in distMat:
        if skipRow:
            skipRow = False
        else:
            skipCol = True
            for col in distMat[0]:
                if skipCol:
                    skipCol = False
                else:
                    deltaX = (float(nodes[row[0]][0]) - float(nodes[col][0]))**2
                    deltaY = (float(nodes[row[0]][1]) - float(nodes[col][1]))**2
                    deltaZ = (float(nodes[row[0]][2]) - float(nodes[col][2]))**2
                    dist = (deltaX+deltaY+deltaZ)**(1/2)
                    row.append(dist)
            
    #TODO Write Code to change position data to distance matrix
    print(str(len(distMat)) + " x " + str(len(distMat[0])))
    
    with open(path+output, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerows(distMat)
    
    print("Position List to Distance Matrix Conversion Complete")
    print("")
    pass

def tester():
    print("Hello World")
    
    #TODO add file selector
    path = "C:\\Users\\noahw\\OneDrive\\Documents\\School\\8 Senior Spring\\Computing the Brain\\Project Data"
    fn = "\\Drosophila 2\\drosophila_medulla_1.graphml"
    output = "\\Drosophila 2\\Drosophila2-Adjacency Matrix"
    temp = fn.split('.')
    exten = temp[-1]
    
    if exten == "graphml":
        print("Building Graph from GraphML file")
        g = graphml_importer(path,fn)
        
        print(netx.info(g))
        
        nodes = list(g.nodes(data = True))
        print(nodes[0])
        #print(nodes[45])
        
        edges = list(g.edges(data = True))
        print(edges[0])
        
        
        print(netx.is_directed(g))
        print(netx.is_weighted(g))
        #graphToAdj(g, path, output)
    
    print("Analysis Complete")

def main(path, filename, output, posBool):
    
    temp = filename.split('.')
    exten = temp[-1]
    
    if exten == "graphml":
        print("Building Graph from GraphML file")
        g = graphml_importer(path,filename)
        graphToAdj(g,path,output)
    
    elif posBool:
        print("Building Distance Matrix from CSV file")
        posToDistMat(path, filename, output)
    
    else:
        print("Building Graph from Edge List file")
        g = edgeListImporter(path, filename)
        graphToAdj(g,path,output)
    
    print("Main Run Complete")


if __name__ == '__main__':
    params = sys.argv
    print(params)
    
    if params[1] == 't':
        tester()
    elif params[1] == 'm':
        main(params[2],params[3],params[4],params[5])
    else:
        print("No appropriate call sign.")
        print("Needs to start with 't' for test or 'm' for main")
    pass
    