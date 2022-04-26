'''
Created on Apr 4, 2022

@author: noahw
'''

import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import numpy as np

#refEL and inferredEL are lists of 2-element lists
def naiveIS (refEL,inferredEL):
    
    print("\nNaive Inference Score\n-------------------")
    # TODO
    refCopy = refEL.copy()
    infCopy = inferredEL.copy()
    
    for infEdge in inferredEL:
        
        if infEdge in refCopy:
            refCopy.remove(infEdge)
            infCopy.remove(infEdge)
    
    #All that should remain in the "copies" are the list-unique edges
    print("\tNumber of Original Edges: " + str(len(refEL)))
    #For refCopy, those are edges that should have been inferred but weren't
    print("\tNumber of Missing Edges: " + str(len(refCopy)))
    #For infCopy, those are edges that should not have been inferred but were
    print("\tNumber of Over-Inferred Edges: " + str(len(infCopy)))
    ratio = (len(refEL)-len(infCopy)-len(refCopy))/len(refEL)
    
    print("\tNaive Inference Score: " + str(ratio))
    return ratio

def integrate(x, y):
    sm = 0
    for i in range(1, len(x)):
        h = x[i] - x[i-1]
        sm += h * (y[i-1] + y[i]) / 2

    return sm

def recPrec(orgEdges,infEdges):
    
    print("\tNumber of Inferred Edges: " + str(len(infEdges)))
    
    prec = []
    recall = []
    correct = 0
    rank = 0
    for e in infEdges:
        if checkExistence(e[0], e[1], orgEdges):
            rank += 1
            if e in orgEdges:
                correct += 1
            prec.append(correct/rank)
            recall.append(correct/len(orgEdges))
    
    auc = integrate(recall,prec)
    print("\tArea Under The Precision-Recall Curve: " + str(auc))
    print("\tLength of Recall: " + str(len(recall)))
    print("\tLength of Precision: " + str(len(prec)))
    
    #plt.plot(recall,prec)
    #plt.xlabel("Recall")
    #plt.xlim([-0.01,max(recall)*10/9])
    #plt.ylabel("Precision")
    #plt.ylim([0,1])
    #plt.title("Precision Recall Curve")
    #plt.show()
    
    return [recall,prec]

def checkExistence(i,j,orgEdges):
    if [i,j] in orgEdges or [j,i] in orgEdges:
        return True
    return False

def plotPRCurve(name,ran,nav,dif,sea):
    
    plt.plot(ran[0], ran[1], label='Random Guess')
    plt.plot(nav[0], nav[1], label='Navigation Efficiency')
    plt.plot(dif[0], dif[1], label='Diffusion Efficiency')
    plt.plot(sea[0], sea[1], label='Search Information')
    plt.xlabel('Recall')
    plt.xlim([-0.1,1.1])
    plt.ylabel('Precision')
    plt.ylim([-0.1,1.1])
    plt.title(name + " Precision Recall Curve")
    #plt.legend()
    plt.show()
    
    pass

def main():
    
    root = tk.Tk()
    root.withdraw()
    
    fileOrder = ["Original Edge List","Inferred Edge List for Nav Eff","Inferred Edge List for Diff Eff","Inferred Edge List for Search Info"]
    key = []
    
    for i in range(len(fileOrder)):
        
        key.append([])
        
        user = filedialog.askopenfilename(title = fileOrder[i])
        fileParse = user.split('/')
        print(fileOrder[i] +": "+fileParse[-1])
        key[i].append("\\\\" + fileParse.pop())
        
        path = fileParse.pop(0)
        for folder in fileParse:
            path = path + "\\\\" + folder
        key[i].append(path)
        
        file = open(path+key[i][0],"r")
        edges = file.readlines()
        file.close()
        
        
        key[i].append([])
        for e in edges:
            edgeL = e.split(',')
            if edgeL[0] != "Tail":
                edgeL.pop()
                key[i][2].append(edgeL)
        if i != 0:
            key[i].extend(recPrec(key[0][2],key[i][2]))
        else:
            numEs = len(key[0][2])
            randPredict = numEs/(numEs*2)
            
            key[i].extend([[0,1],[randPredict,randPredict]])
            print("Number of Original Edges: " + str(numEs))
            #naiveIS(key[0][2],key[1][2])
        print("")
    
    names = ["C Elegans","Macaque 1", "Macaque 4", "Mouse 2016", "Macaque 2016"]
    
    plotPRCurve(names[2],[key[0][3],key[0][4]],[key[1][3],key[1][4]],[key[2][3],key[2][4]],[key[3][3],key[3][4]])
    
    pass


if __name__ == '__main__':
    main()
    pass
        