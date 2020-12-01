from Node import Node
from TaquinResolver import TaquinResolver
from Window import *
import time
#La taille du jeu peut etre de toute taille
finalNode = Node([[1, 2, 3], [4, 5, 6], [7, 8, "X"]])

#On genere un point de depart a 1000 mouvements de la solution
#Il exite donc une solution pour le jeu du taqin en 10 mou
#Note : dans la plus part des cas le jeu est realisable en moins de 30 coups pour un 3X3
#Le temps d'execution ne dependant pas tant du nombre de melange
#Le deuxieme parametre correspond au nombre de melange au hasard utitilisé pour generer le noeuds initiale
initialNode = Node.getInitialRandomNode(finalNode, 20 )

#Affichage des Noeuds initial et final
print(" Initial node : ")
initialNode.displayNode()
print(" Final node : ")
finalNode.displayNode()

#On creer le resolver de Taquin
choixHeuristique = int(input("Choisir l'heuristique - 1: Manhattan Distance   2: ManhattanDistance + Corner tiles  3: Misplaced Tiles    4: Tiles out of row or column    5: Gasching Heuristic  \n"))
solver = TaquinResolver(initialNode,finalNode)
#On laisse à l'utilisateur choisir l'heuristique
#La distance hde manhattant est l'heuristique la plus efficace
if choixHeuristique == 1 :
	print("Distance de manhattan")
	path = solver.aStar(TaquinResolver.manhattanDistance,False)
elif choixHeuristique == 3:
	print("Misplacedtiles")
	path = solver.aStar(TaquinResolver.misplacedTile)
elif choixHeuristique == 4 :
	print("Tiles out of row and column")
	path = solver.aStar(TaquinResolver.tilesOutOfRowAndColumn)
elif choixHeuristique == 5 :
	print("Gaschnig heuristic")
	path = solver.aStar(TaquinResolver.gaschnig)
else:
	#Si le troisieme parametre est a true alors on uitilise l'extension CornerTiles de manhattan distance
	print("Distance de manhattan + Corner Tiles")
	path = solver.aStar(TaquinResolver.manhattanDistance,True)

#Affichage des resultats
print("Taille du chemin :"+ str(len(path)-1))

#On construit la fenetre qui anime le chemin
w = TaquinWindow(path)
w.show()
