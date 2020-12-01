from tkinter import *
class TaquinWindow :
	#Constructeur de la TaquinWindow
	def __init__(self, path):
		#Chemin a animer
		self.path = path
		#Variable indiquant a quel noeuds du chemin nous en sommes 
		self.pathIdx  = 0 ;
		#On recuperer la taille du jeu
		self.rows = len(path[0].getTiles())
		self.columns = len(path[0].getTiles()[0])
		self.FONT=('Ubuntu', 27, 'bold')
		self.master = Tk()
		self.cnv = Canvas(self.master, width=(100*self.columns), height=(100*self.rows), bg='gray70')
		#Bouton pour affiche le bouton Suivant
		self.cnv.pack(side='left')
		self.btnN=Button(text="      Next move      ", command=self.nextMove)
		self.master.bind('Right', self.nextMove)
		self.btnN.pack()
		#Bouton pour afficher le mouvement précédent
		self.btnP=Button(text="  Previous move  ", command=self.previousMove)
		self.master.bind('d', self.previousMove)
		self.btnP.pack()
		#Boutton pour redemarrer l'animation
		self.btnR=Button(text="Restart Animation", command=self.restart)
		self.master.bind('r', self.restart)
		self.btnR.pack()
		#Label affichant bravo à la fin
		self.lbl = Label(text=" ", font=('Ubuntu', 20, 'bold'),justify=CENTER, width=10)
		self.lbl.pack(side="left")
		#Permet de controler la gesiton de restart et du  nextmove toutes les 300ms
		self.finished = False

	#Permet d'initaliser les tuiles et l'interface graphique
	def init(self) :
		#On definit un tableau vide du nombre de tuiles +1
		self.items = [None for i in range(self.columns * self.rows +1)]
		#On recupere le premier noeud du chemin
		node = self.path[self.pathIdx]
		#Pour chaque tuile du noeud
		for i in range(self.rows):
		    for j in range(self.columns):
		        x = 100*j
		        y =  100*i 
		        A, B, C=(x, y), (x+100, y+100), (x+50, y+50)
		        #On creer la tuile et on l'enregistre dans items
		        rect=self.cnv.create_rectangle(A, B, fill="royal blue")
		        if(node.getTiles()[i][j] != "X" ):
		            nro = node.getTiles()[i][j]
		        else:
		        	#La tuile X prend la valeur rows * columns
		            nro = self.rows * self.columns
		        #On creer le texte sur la tuile
		        txt=self.cnv.create_text(C, text=nro, fill="yellow",font=self.FONT)
		        self.items[nro]=(rect, txt)
		#On recupere la derniere tuiles de la liste. Cette tuile correspond à la tuile X 
		rect, txt=self.items[self.rows * self.columns]
		#On supprime cette tuile
		self.cnv.delete(txt)
		self.cnv.delete(rect)
		self.lbl.configure(text="")

	#Affiche le prochain noeuds du chemin. La fonction est executer toutes les 300ms jusqu'a ce que le chemin soit fini
	def nextMove(self, event=None):
		#On peut avancer dans le chemin jusqu'a ce qu'on soit à la dernière tuile
	    if( self.pathIdx < len(self.path)-1 ):
	    	#Pour chaque tuile
	        for i in range(self.rows):
	            for j in range(self.columns):
	                if self.path[self.pathIdx].getTiles()[i][j] == "X":
	                	#Pour chaque tuile du noeuds on cherche la position de la tuiles "X"
	                    tmpI = i
	                    tmpJ = j
	                    #Puis on regarde a cette position, la tuile qu'il y a au noeud suivant
	                    value = self.path[self.pathIdx+1].getTiles()[i][j]
	                    for y in range(self.rows):
	                        for z in range(self.columns):
	                        	#Puis on regarde où cette meme tuile se situe maintenant (cela nous permet de deduire le sens de la tuile en la comparant a son ancienne position)
	                            if value == self.path[self.pathIdx].getTiles()[y][z] :
	                                tmpY = y
	                                tmpZ = z
	                    #Apartir des tmp , on determine le sens de move()
	                    if tmpI < tmpY :
	                        self.cnv.move(self.items[value][0],0, -100)
	                        self.cnv.move(self.items[value][1],0, -100)
	                    elif tmpI > tmpY :
	                        self.cnv.move(self.items[value][0],0, +100)
	                        self.cnv.move(self.items[value][1], 0, +100)
	                    elif tmpJ < tmpZ :
	                        self.cnv.move(self.items[value][0],-100,0 )
	                        self.cnv.move(self.items[value][1], -100, 0)
	                    elif tmpJ > tmpZ :
	                        self.cnv.move(self.items[value][0],100, 0)
	                        self.cnv.move(self.items[value][1], 100, 0)
	                      #On incremente de 1 pour passer à la tuile suivante si l'utilisateur reclic sur ce boutton
	                    self.pathIdx += 1
	                    #Si on est au dernier mouvement , alors on affiche un message. On passe al variable finished a false
	                    if self.pathIdx == len(self.path)-1:
	                    	self.lbl.configure(text="Resolved !")
	                    	self.finished = True
	                    #Cette variable passe a false si on est au dernier mouvement
	                    if not self.finished :
	                    	#Execute la fonction nextMove toutes les n ms
	                    	self.master.after(250,self.nextMove)
	                    return 1
	    else:
	        return 0

	#Permet d'afficher le noeuds précedent dans le chemin
	def previousMove(self, event=None):
		#On peut revenir en arriere a part si on est au debut du chemin
		if( self.pathIdx != 0 ):
			#Pour chaque tuiles :
			for i in range(self.rows):
				for j in range(self.columns):
					#Pour chaque tuile du noeuds on cherche la position de la tuiles "X"
					if self.path[self.pathIdx].getTiles()[i][j] == "X":
						tmpI = i
						tmpJ = j
						#Puis on regarde a cette position la tuile qu'il y avait au noeud précedent
						value = self.path[self.pathIdx-1].getTiles()[i][j]
						for y in range(self.rows):
							for z in range(self.columns):
								#Puis on regarde où cette meme tuile se situe maintenant (cela nous permet de deduire le sens de la tuile en la comparant a son ancienne position)
								if value == self.path[self.pathIdx].getTiles()[y][z] :
									tmpY = y
									tmpZ = z
						#Apartir des tmps , on determine le sens de move()
						if tmpI < tmpY :
							self.cnv.move(self.items[value][0],0, -100)
							self.cnv.move(self.items[value][1],0, -100)
						elif tmpI > tmpY :
							self.cnv.move(self.items[value][0],0, +100)
							self.cnv.move(self.items[value][1], 0, +100)
						elif tmpJ < tmpZ :
							self.cnv.move(self.items[value][0],-100,0 )
							self.cnv.move(self.items[value][1], -100, 0)
						elif tmpJ > tmpZ :
							self.cnv.move(self.items[value][0],100, 0)
							self.cnv.move(self.items[value][1], 100, 0)
						#On decremente de 1 pour passer à la tuile precedente si l'utilisateur reclic sur ce boutton
						self.pathIdx -= 1
						return 1
		else:
			return 0

	#Relance l'animation
	def restart(self):
		if self.finished:
			self.finished = False
			#On remet l'index du chemin pour recommencer a 0
			self.pathIdx = 0
			#On detruit toutes les tuiles
			for i in range(1, self.rows*self.columns+1):
				self.cnv.delete(self.items[i][0])
				self.cnv.delete(self.items[i][1])
			#On reinitialise l'interface
			self.init()
			self.master.after(1000,self.nextMove)

	#Permet d'animer les noeuds du chemin passe au constructeur de l'objet
	def show(self):
		#Initialise les tuiles
		self.init()
		#Lance l'animation apres 1sec
		self.master.after(1000,self.nextMove)
		self.master.mainloop()

