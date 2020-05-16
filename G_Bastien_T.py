# -*- coding: utf-8 -*-

import random
import datetime
import os#modif
import time#modif

class Player :#modif
    
    keyboard_key = {'z':(-1,0),
                    'q':(0,-1),
                    's':(1,0),
                    'd':(0,1),
                    'l': "leave",
                    'p': "pause"}
    
    def __init__(self, name, points = 0, start = (0,0)):#modif
        self.name = name
        self.points = points
        self.position = start
        self.before = start 
        self.compare = start 


    def move(self) :#modif
        
        key = input("Mouvement (z,q,s,d) or (l,p) : ")
        while key not in Player.keyboard_key.keys() :
            
            key = input("Mouvement (z,q,s,d) or (l,p) : ")
                    
        if key == "l":
            g.Main()

        else:
            move = Player.keyboard_key[key]

            if self.before != (self.compare[0] + move[0], self.compare[1] + move[1]): 

                self.before = self.compare 
                self.compare = (self.compare[0] + move[0], self.compare[1] + move[1]) 
                self.position = (self.position[0] + move[0], self.position[1] + move[1]) 

class Game :
    
    def __init__(self, player, size=10):
        self.player = player
        self.board_size = size
        self.candies = []
        self.bonusT = [] #Modif
        self.malusF = [] #modif
        self.valDiff = {"1": [3,10], "2": [5,16], "3": [8,22]} #modif
        
    # Dessine le plateau
    def draw(self):#modif
        os.system("cls")
        for line in range(self.board_size):
            for col in range(self.board_size):
                if (line,col) in self.candies :
                    print("*",end=" ")
                elif (line,col) in self.bonusT : 
                    print("T",end=" ") 
                elif (line,col) == self.player.position :
                    print("O",end=" ")
                else : 
                    print(".",end=" ")
            print()
            
    # Fait apparaitre un bonbon
    def pop_candy(self):#modif
        new_candy = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if new_candy not in self.candies and new_candy not in self.bonusT and new_candy not in self.malusF : #Modif
            self.candies.append(new_candy)
    
    def pop_temps(self): #Modif
        bonus_temp = (random.choice(range(self.board_size)),random.choice(range(self.board_size))) #Modif
        if bonus_temp not in self.candies and bonus_temp not in self.bonusT and bonus_temp not in self.malusF : #Modif
            self.bonusT.append(bonus_temp) #Modif

    def pop_malus(self): #modif
        malus_freeze = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if malus_freeze not in self.candies and malus_freeze not in self.bonusT and malus_freeze not in self.malusF :
            self.malusF.append(malus_freeze)
             
    # Regarde s'il y a un bonbon à prendre (et le prend)
    def check_candy(self):
        if self.player.position in self.candies:
            self.player.points += 1
            self.candies.remove(self.player.position)
    
    def check_temps(self) : #Modif
        if self.player.position in self.bonusT:
            delta = datetime.timedelta(0,3)
            self.end = self.end + delta
            self.bonusT.remove(self.player.position)

    def check_malus(self) :
        if self.player.position in self.malusF:
            
            self.malusF.remove(self.player.position)


    def print_time(self):#modif
        
        restant = self.end - datetime.datetime.today()
        if restant >= datetime.timedelta(seconds=0) : #timedelta set a 0 sinon il veut pas faire le >=
            print("Temps restants : ", restant.seconds)


    def Ajouter_Scoreboard(self):#a chaque fin de partie ca va prendre nom score et temps dans le txt

        # Prendre la date du jour
        today = datetime.date.today()
        date = today.strftime("%d/%m/%Y")

        # Créer un fichier texte ou l'ouvrir s'il existe déjà
        with open("Scoreboard.txt", "a+") as file:
            file.write(self.player.name + " " + str(self.player.points) + " " + date + "\n")

    @staticmethod
    def Lire_Scoreboard():#lit le score et print les 10 plus haut

        #  Lire le fichier et imprimer le top x des joueurs
        with open("Scoreboard.txt", "r") as file:
            data = file.readlines()
        
        data_split = [i.split() for i in data]

        top_10 = sorted(data_split, key=lambda infosparties: int(infosparties[1]), reverse=True) # Int car sinon bug reverse=true pour décroissant
        #prendre les listes(nom,pts,date) dans la liste(datasplit) il prend chaque listes il va aller voir dedans la pos 1 -> les pts et après ca il va classer les listes par ordres décroissants dans le score
        
        print("\n----- Scoreboard -----")
        for i in range(0, 10):
            try:  # Exception pour si il n'y a pas 10 joueurs
                print(i + 1,"\t" + "\t".join(top_10[i]))
            except:
                pass
        
        
    # Joue une partie complète
    def play(self,diffi):#modif
        os.system("cls")
        print("--- Début de la partie ---")
        self.draw()
        
        self.end = Game.end_time(1,0) #Modif self ajouté pour le rappeler dans la fonction check_temps
        now = datetime.datetime.today()
        
        while now < self.end : #Modif
            self.player.move() #Modif
            if self.player.position[0] < 0 :
                self.player.position = (self.board_size-1,self.player.position[1])
            elif self.player.position[1] < 0 :
                self.player.position = (self.player.position[0],self.board_size-1)
            elif self.player.position[0] > self.board_size-1 :
                self.player.position = (0,self.player.position[1])        
            elif self.player.position[1] > self.board_size-1 :
                self.player.position = (self.player.position[0],0)
            
            self.check_candy()
            self.check_temps() #Modif
            

            if random.randint(1,self.valDiff[diffi][0]) == 1 :
                self.pop_candy()
            if random.randint(1,self.valDiff[diffi][1]) == 1 : #Modif
                self.pop_temps() #Modif

            self.draw()
            self.print_time()#modif
            
            now = datetime.datetime.today()
        
        os.system("cls")
        print("----- Terminé -----")
        print(self.player.name,"avez", self.player.points, "points")#modif
        self.Ajouter_Scoreboard()
        self.Lire_Scoreboard()
        input("\nAppuyer sur ENTER pour continuer ...")
        time.sleep(3)
        os.system("cls")

    @staticmethod
    # retourne le moment où le jeu est censé être fini
    def end_time(delta_minute, delta_second):
        delta = datetime.timedelta(minutes=delta_minute, seconds=delta_second)
        end = datetime.datetime.today() + delta
        return end

class Menu():#modif

    def Main(self):
        os.system("cls")
        Menu.Logo()
        while True:
            Menu.Affichage()
            choix = input("\nVotre choix: ")

            if choix == "1":
                
                player_name = input("Entrer votre pseudo: ")
                while len(player_name) > 5 or " " in player_name:
                    print("ERREUR : Votre pseudo comporte plus de 5 caractères et il ne peut pas contenir d'espace\n")
                    player_name = input("Entrer votre pseudo: ")
                diffi = Menu.Difficulte()#modif
                p = Player(player_name)
                g = Game(p)
                g.play(diffi)
            elif choix == "2":
                os.system("cls")
                Game.Lire_Scoreboard()
                input("\nAppuyer sur ENTER pour continuer ...")
            elif choix == "3":
                Menu.Règles()
            elif choix == "4":
                print("Merci d'avoir joué")
                os._exit(1)
            else:
                print("Bad choice ...")

    @staticmethod
    def Difficulte():#modif
        print("\n"
            "     ___________________________________  \n"
            "    /            DIFFICULTES            \ \n"
            "    \___________________________________/ \n"
            "     |                                 |  \n"
            "     |   [ 1 ]    Facile               |  \n"
            "     |   [ 2 ]    Normal               |  \n"
            "     |   [ 3 ]    Difficile            |  \n"
            "     \_________________________________/  \n"
        )
        return input("Entrez votre choix : ")


    @staticmethod
    def Règles():#modif
        os.system("cls")
        print("Voici les règles:\n"
        "Ceci est un jeu de plateau où le joueur(vous \"0\") devra récuperer un maximum de bonbons dans un temps imparti.\n"
        "Pour se faire vous devrez vous déplacer avec les touches Z(haut), Q(gauche), S(bas), D(droite).\n"
        "Il existe deux types d'objets ramassables qui apparaitront de façons aléatoire :\n"
        "-  * les bonbons ceux-ci vous attribueront 1 points lorsque vous passerez dessus.\n"
        "-  T un bonus de temps de 3 secondes.")

        input("\nAppuyer sur ENTER pour retourner au menu ...")

    @staticmethod #modif
    def Logo():
            print("\n"
          "   ____        _                  _____                       \n"
          "  |  _ \      | |                / ____|                      \n"
          "  | |_) | __ _| |__   ___  _   _| |  __  __ _ _ __ ___   ___  \n"
          "  |  _ < / _` | '_ \ / _ \| | | | | |_ |/ _` | '_ ` _ \ / _ \ \n"
          "  | |_) | (_| | |_) | (_) | |_| | |__| | (_| | | | | | |  __/ \n"
          "  |____/ \__,_|_.__/ \___/ \__,_|\_____|\__,_|_| |_| |_|\___| \n")
    @staticmethod

    def Affichage():#modif

        print("\n"
            "     ___________________________________  \n"
            "    /               MENU                \ \n"
            "    \___________________________________/ \n"
            "     |                                 |  \n"
            "     |   [ 1 ]    Jouer                |  \n"
            "     |   [ 2 ]    Scoreboard           |  \n"
            "     |   [ 3 ]    Règles               |  \n"
            "     |   [ 4 ]    Quit.                |  \n"
            "     \_________________________________/  \n")
        



if __name__ == "__main__" : #modif
     
    g = Menu()
    g.Main()

    
    
    
