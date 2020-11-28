class TaquinResolver:
	def __init__(self, initialNode, finalNode):
		self.initialNode = initialNode
		self.finalNode = finalNode
		self.bestPath = []

	#Heuristique qui renvoie le nombre de tuile mal placée d'un noeud courant par rapport à un noeud final (la tuile vide n'est pas comptabilisé)
	def misplacedTile(self,currentNode):
		h = 0
		rows = len(currentNode.getTiles())
		columns = len(currentNode.getTiles()[0])
		for i in range(0,rows):
			for y in range(0,columns):
				#Pour chaque tuiles, si la tuile au meme indice dans le noeud final n'est pas la meme alors on ajoute 1
				if(currentNode.getTiles()[i][y] != "X"):
					if(currentNode.getTiles()[i][y] != self.finalNode.getTiles()[i][y]):
						h = h + 1
		return h

	#Heurisitque calculant la distance de manhattan (la tuile vide n'est pas comptabilisé)
	def manhattanDistance(self,currentNode):
		manhattanDistance = 0
		rows = len(currentNode.getTiles())
		columns = len(currentNode.getTiles()[0])
		#Pour chaque tuile du noeud courant
		for i in range(0,rows):
			for y in range(0,columns):
				#On recupere les coordonnées de la tuile courante dans le noeuds final
				if(currentNode.getTiles()[i][y] != 'X'):
					coord = self.finalNode.getCoordinateIn2DList(currentNode.getTiles()[i][y])
					#On calcule la distance entre les coordonnées
					manhattanDistance =  manhattanDistance + (abs(i-coord[0])+abs(y-coord[1]))
		return manhattanDistance

	#Heuristique le nombre de tuile qui ne sont pas dans la bonne colonne aditionné avec le nombre de tuile qui ne sont pas sur la bonne ligne
	def tilesOutOfRowAndColumn(self,currentNode):
		h = 0 
		rows = len(currentNode.getTiles())
		columns = len(currentNode.getTiles()[0])
		#Pour chaque tuiles on regarde si elle se situe dans sa pposition finale
		for i in range(0,rows):
			for y in range(0,columns):
				currentTile = currentNode.getTiles()[i][y]
				if(self.finalNode.getCoordinateIn2DList(currentTile)[0] != i):
					h += 1
				if(self.finalNode.getCoordinateIn2DList(currentTile)[1] != y):
					h += 1
		return h
	#Suprime les chemins qui n'ont rien donné pour gardé l'unique chemin optimal
	def findBestPath(self):
		#Pour chaque noeuds en partant de la fin
		i = len(self.bestPath)-1
		while i >= 1 :	
			#On regarde si le noeud courant est un successeurs du noeuds se situant avant le noeuds courant dans la liste 
			while not self.bestPath[i].isInList(self.bestPath[i-1].getSucessors()):
				#Si le noeud courant n'est pas un sucesseurs du noeuds se situant avant le noeud courant dans la liste
				#Alors on supprime le noeuds se situant avant le noeuds courant dans la liste
				self.bestPath.pop(i-1)
				#On continue pour enlever les feuilles inutiles
				i -= 1
			i -= 1
			
	#Algorithme A* implémenté selon l'algo : https://fr.wikipedia.org/wiki/Algorithme_A*
	def aStar(self,heuristicChosen):
		open = []
		closed = []
		open.append(self.initialNode)
		while open :
			#Trie la liste dans l'ordre decroissant
			open.sort(key=lambda x:  -1 *x.getFCost())
			#On depile open puisque le plus cours chemin est a la fin de la liste
			n = open[-1]
			self.bestPath.append(n)
			open.pop(-1)
			#Si le chemin courant est le chemin final alors on s'arrete on a trouve une solution
			if n.equalsTo(self.finalNode):
				#Enleve les noeuds inutilement visite
				self.findBestPath()
				break;
			#Pour chaque successeur np du noeud courant
			for np in n.getSucessors() :
				#Si np existe dans closedList ou np existe dans openList avec un coût inférieur
				flag = 0
				for node in closed :
					if  (node.equalsTo(np) and  np.getFCost() < node.getFCost()):
						flag = 1
						break;
				for node in open:
					if  (node.equalsTo(np) and  np.getFCost() < node.getFCost()):
						flag = 1
						break;
				if flag == 0:
					#Alors on MAJ sont couts et on l'ajoute a la liste open
					np.setGCost( n.getGCost() + 1)
					np.setFCost( np.getGCost() + heuristicChosen(self,np))
					open.append(np)
			closed.append(n)
		return self.bestPath

	#Version de l'algo du cours (Donne de moins bon resultats)
	def aStarV2(self):
		#Declarer deux listes open et closed
		open = []
		closed = []
		#Inserer noeuds initial dans open
		open.append(self.initialNode)
		#Tant que open n'est pas vide
		while open :
			#N = noeud au debut de open
			n = open[0]
			#"On ajoute N au chemin qui sera retourne"
			self.bestPath.append(n)
			#Enlever N de open et l'ajouter dans closed
			open.pop(0)
			closed.append(n)
			#Si n est le but (goal(n) est true), Sortir de la boucle avec succes en retournant le chemin
			if n.equalsTo(self.finalNode):
				self.findBestPath()
				return self.bestPath
			#Pour chaque successeur np de n(chaque np appartenant à transitions(n))
			for np in n.getSucessors() :
				#Initialiser la valeur G(np) à G(N) + C(n,np) ici 1
				np.setGCost(n.getGCost() + 1)
				#Calcul de F(n)
				np.setFCost( np.getGCost() + np.manhattanDistance(self.finalNode))
				flag = 0
				#Si open continent un noeud npp egale à np avec f(np) <= f(npp)
				for npp in open:
					if npp.equalsTo(np) and  np.getFCost() < npp.getFCost():
						#enleve npp de open et inserer np dans open (ordre croissant selon f())
						open.pop(open.index(npp))
						open.append(np)
						open.sort(key=lambda x:  x.getFCost())
						flag = 1
						break;
				#Si closed continent un noeud npp egale à np avec f(np) <= f(npp)
				if flag == 0 :
					for npp in closed:
						if npp.equalsTo(np) and  np.getFCost() < npp.getFCost():
							#enleve npp de closed et inserer np dans open (ordre croissant selon f())
							closed.pop(closed.index(npp))
							open.append(np)
							open.sort(key=lambda x:  x.getFCost())
							break;
				#Si np n'est ni dans open et ni dans closed
				if (not np.isInList(open) and not np.isInList(closed)):
					#Inserer np dans open (ordre croissant selon f(n))
					open.append(np)
					open.sort(key=lambda x:  x.getFCost())
		return "Path not found"

