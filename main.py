from Node import Node
from TaquinResolver import TaquinResolver
from Window import *
import time


finalNode = Node([[1,2,3],[4,5,6],[7,8,"X"]])
#On genere un point de depart a 1000 mouvements de la solution
#Il exite donc une solution pour le jeu du taqin en 10 mou
#Note : dans la plus part des cas le jeu est realisable en moins de 30 coups
#Le temps d'execution ne dependant pas tant du nombre de melange
initialNode = Node.getInitialRandomNode(finalNode,1000)

#Affichage des Noeuds
print(" Initial node : ")
initialNode.displayNode()
print(" Final node : ")
finalNode.displayNode()

#On creer le resolver
solver = TaquinResolver(initialNode,finalNode)
#On laisse à l'utilisateur choisir l'heuristique
choixHeuristique = int(input("Choisir l'heuristique - 1: Manhattan Distance     2: Misplaced Tiles    3: Tiles out of row or column \n"))
start_time=time.time()
if choixHeuristique == 2:
    path = solver.aStar(TaquinResolver.misplacedTile)
if choixHeuristique == 3 :
    path = solver.aStar(TaquinResolver.tilesOutOfRowAndColumn)
else:
    path = solver.aStar(TaquinResolver.manhattanDistance)
time_f=time.time()-start_time  

#Affichage du chemin dans la ligne de commande
print("Chemin : ") 
[node.displayNode() for node in path]

print("Taille du chemin : "+ str(len(path)-1))
print("running_time: %.8f\n" %time_f)

#On construit la fenetre qui anime le chemin
w = TaquinWindow(path)
w.show()
