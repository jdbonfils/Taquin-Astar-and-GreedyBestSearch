from Node import Node
from TaquinResolver import TaquinResolver
from Window import *
import time
#La taille du jeu peut etre de toute taille
finalNode = Node([[1,2,3],[4,5,6,],[7,8,"X"]])

#On genere un point de depart a 1000 mouvements de la solution
#Il exite donc une solution pour le jeu du taqin en 10 mou
#Note : dans la plus part des cas le jeu est realisable en moins de 30 coups pour un 3X3
#Le temps d'execution ne dependant pas tant du nombre de melange
#Le deuxieme parametre correspond au nombre de melange au hasard utitilisé pour generer le noeuds initiale
initialNode = Node.getInitialRandomNode(finalNode,1000)

#Affichage des Noeuds
print(" Initial node : ")
initialNode.displayNode()
print(" Final node : ")
finalNode.displayNode()


#Resoue le puzzle Avec l'Algo A*
#On creer le resolver de Taquin
solver = TaquinResolver(initialNode,finalNode)
#On laisse à l'utilisateur choisir l'heuristique
#La distance hde manhattant est l'heuristique la plus efficace
choixHeuristique = int(input("Choisir l'heuristique - 1: Manhattan Distance     2: Misplaced Tiles    3: Tiles out of row or column \n"))
start_time=time.time()
if choixHeuristique == 2:
    path = solver.aStar(TaquinResolver.misplacedTile)
if choixHeuristique == 3 :
    path = solver.aStar(TaquinResolver.tilesOutOfRowAndColumn)
else:
	#Si le troisieme parametre est a true alors on uitilise l'extension CornerTiles de manhattan distance
    path = solver.aStar(TaquinResolver.manhattanDistance,True)
time_f=time.time()-start_time 

#Affichage des resultats
print("Taille du chemin algorithme A* avec corner: "+ str(len(path)-1))
print("running_time: %.8f\n" %time_f)

#On construit la fenetre qui anime le chemin
w = TaquinWindow(path)
w.show()
