import copy
import random
class Node:
	#Constructeur de la classe node
	def __init__(self, List2D = None):
		self.gCost = 0
		self.fCost = 0 
		#Construit un noeuds manuellement si aucune liste 2D n'est donnée au constructeur
		if(List2D == None) :
			rows = int(input("Saisir le nombre de ligne :"))
			columns  = int(input("Saisir le nombre de colonnes :"))
			#On initialise la liste 2D à zero
			self.tiles = [ [0]*columns for _ in range(rows) ]
			#On initialise la liste des valeurs que peut prendre une tuile
			valeursPossible = list(range(1, rows*columns))
			valeursPossible.append('X')
			#Pour chaque tuile on renseigne sa valeur parmis celle disponible dans la liste des valeur possible
			for i in range(0,rows):
				#On ne peut pas utiliser un for ici puisque l'on increment le compteur que sous certaines conditions
				y = 0
				while y < columns :
					print("\n Choisir valeur parmi celles proposés : " + str(valeursPossible))
					choix = input("Saisir la valeur de la tuile : ")
					if(choix.isnumeric()):
						choix = int(choix)
					if(choix not in valeursPossible):
						#Si l'utilisateur n'as pas saisi une valeur valid alors on lui redemande de saisir
						print("Saisi invalid \n")
					else:
						self.tiles[i][y] = choix
						valeursPossible.pop(valeursPossible.index(choix))
						y += 1
		else:
			self.tiles = List2D

	def setGCost(self,cost):
		self.gCost = cost
	def setFCost(self,cost):
		self.fCost = cost
	def getGCost(self):
		return self.gCost
	def getFCost(self):
		return self.fCost
	#Retourne la liste 2D
	def getTiles(self):
		return self.tiles

	#Donne les coordonnees d'une tuile dans un noeuds
	def getCoordinateIn2DList(self,elem):
		#Pour chaque ligne
		for row in range(0,len(self.getTiles())):
			#Si l'element se trouve sur la ligne
			if(elem in self.getTiles()[row]):
				#Alors on renvoie la ligne et la  colonne que l'on trouve grace à index
				col = self.getTiles()[row].index(elem)
				return row,col
		return -1,-1

	#Permet d'afficher un noeud (un etat du jeu)
	def displayNode(self):
		for row in self.getTiles():
			r = ""
			for elem in row:
				r = r + str(elem) + " "
			print("|"+r+"| \n")
		print("\n")
	#Permet d'inverser les tuiles dont les indices sont passés en parametre
	def swapTiles(self,idx1,idy1,idx2,idy2):
		self.tiles[idx1][idy1], self.tiles[idx2][idy2], = self.tiles[idx2][idy2],self.tiles[idx1][idy1] 

	#Renvoie une liste de noeud successeurs du noeuds
	def getSucessors(self):
		nodesList = []
		nodeTiles = []
		coord = self.getCoordinateIn2DList("X")
		#On teste pour chaque bord, si la tuile n'est pas sur le bord alors il a un successeur en plus
		if(coord[0] != 0):
			nodeTiles = copy.deepcopy(self.getTiles())
			#On switch les deux cases
			nodeTiles[coord[0]][coord[1]], nodeTiles[coord[0]-1][coord[1]] = nodeTiles[coord[0]-1][coord[1]], nodeTiles[coord[0]][coord[1]]
			nodesList.append(Node(nodeTiles))
			nodeTiles = []
		if(coord[1] != 0):
			nodeTiles = copy.deepcopy(self.getTiles())
			#On switch les deux cases
			nodeTiles[coord[0]][coord[1]], nodeTiles[coord[0]][coord[1]-1] = nodeTiles[coord[0]][coord[1]-1], nodeTiles[coord[0]][coord[1]]
			nodesList.append(Node(nodeTiles))
			nodeTiles = []
		if(coord[0] != len(self.getTiles()) - 1 ):
			nodeTiles = copy.deepcopy(self.getTiles())
			#On switch les deux cases
			nodeTiles[coord[0]][coord[1]], nodeTiles[coord[0]+1][coord[1]] = nodeTiles[coord[0]+1][coord[1]], nodeTiles[coord[0]][coord[1]]
			nodesList.append(Node(nodeTiles))
			nodeTiles = []
		if(coord[1] != len(self.getTiles()[0] )- 1):
			nodeTiles = copy.deepcopy(self.getTiles())
			#On switch les deux cases
			nodeTiles[coord[0]][coord[1]], nodeTiles[coord[0]][coord[1]+1] = nodeTiles[coord[0]][coord[1]+1], nodeTiles[coord[0]][coord[1]]
			nodesList.append(Node(nodeTiles))
			nodeTiles = []

		return nodesList
	#Verifie que le noeud passé en paramtere possède bien les meme tuiles
	def equalsTo(self,node):
		rows = len(self.getTiles())
		columns = len(self.getTiles()[0])
		#Pour chaque tuiles on regarde si elle se situe dans sa pposition finale
		for i in range(0,rows):
			for y in range(0,columns):
				if(self.getTiles()[i][y] != node.getTiles()[i][y]) :
					return False
		return True

	def isInList(self,nodeList):
		for node in nodeList:
			if self.equalsTo(node) :
				return True
		return False
	#Methode static
	@staticmethod
	#Calcul un noeuds au hasard à partir d'un noeud final. Cela permet de s'assurer qu'il existe bien
	#un chemindu noeuds initiale vers le noeuds finale
	def getInitialRandomNode(finalNode, nombreMouvement ):
	    successors = finalNode.getSucessors()
	    predecessor = finalNode
	    #On maleange nombreMouvement fois 
	    for i in range(nombreMouvement):
	        #On prend un sucesseur au hasard
	        currentNode = random.choice(successors)
	        #On recupere sa liste des sucesseur
	        successors = currentNode.getSucessors()
	        #Un des sucesseur du noeud corespond aux prédécesseur de ce meme noeud, on l'enleve pour que se soit mieux melangé 
	        #evite par exemple de faire l'action "NORD","SUD" puis de nouveau "NORD" (le manlange ne serait pas efficace)
	        for node in successors :
	            if(node.equalsTo(predecessor)):
	                successors.pop(successors.index(node))
	        predecessor = currentNode
	    return currentNode
