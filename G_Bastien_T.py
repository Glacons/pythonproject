# -*- coding: utf-8 -*-

import random
import datetime
import os
import time

class Player :
    
    keyboard_key = {'z':(-1,0),
                    'q':(0,-1),
                    's':(1,0),
                    'd':(0,1),
                    'l': "leave"}
    
    def __init__(self, name, points = 0, start = (0,0)):
        self.name = name
        self.points = points
        self.position = start
        self.before = start 
        self.compare = start 

    # Permet au joueur de se déplacer et de quitter la partie en cours
    def move(self) :
        
        key = input("Mouvement (z,q,s,d) or (l) : ")
        while key not in Player.keyboard_key.keys() :
            
            key = input("Mouvement (z,q,s,d) or (l) : ")
                    
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
        self.bonusT = []
        self.malusF = []
        self.bool_freeze = False
        self.valDiff = {"1": [3,10,22], "2": [5,16,10], "3": [8,22,5]}
        
    # Dessine le plateau
    def draw(self):
        os.system("cls")
        for line in range(self.board_size):
            for col in range(self.board_size):
                if (line,col) in self.candies :
                    print("*",end=" ")
                elif (line,col) in self.bonusT : 
                    print("T",end=" ")
                elif (line,col) in self.malusF :
                    print("ƒ",end=" ") 
                elif (line,col) == self.player.position :
                    print("O",end=" ")                
                else : 
                    print(".",end=" ")
            print()
            
    # Fait apparaitre un bonbon, bonus et malus
    def pop_candy(self):
        new_candy = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if new_candy not in self.candies and new_candy not in self.bonusT and new_candy not in self.malusF :
            self.candies.append(new_candy)
    
    def pop_temps(self):
        bonus_temp = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if bonus_temp not in self.candies and bonus_temp not in self.bonusT and bonus_temp not in self.malusF :
            self.bonusT.append(bonus_temp)

    def pop_malus(self):
        malus_freeze = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if malus_freeze not in self.candies and malus_freeze not in self.bonusT and malus_freeze not in self.malusF :
            self.malusF.append(malus_freeze)
             
    # Vérifie s'il y a un bonbon, malus ou bonus à prendre (et le prend)
    def check_candy(self):
        if self.player.position in self.candies:
            self.player.points += 1
            self.candies.remove(self.player.position)
    
    def check_temps(self) :
        if self.player.position in self.bonusT:
            delta = datetime.timedelta(0,3)
            self.end = self.end + delta
            self.bonusT.remove(self.player.position)

    def check_malus(self) :
        if self.player.position in self.malusF:
            self.bool_freeze = True
            self.malusF.remove(self.player.position)


    def print_time(self):
        
        restant = self.end - datetime.datetime.today()
        if restant >= datetime.timedelta(seconds=0) : #timedelta mit à 0 sinon il veut pas faire le >= pour ne pas que le timer affiche une valeur négative
            print("Temps restants : ", restant.seconds)

    #A chaque fin de partie ça va prendre nom score et le jour et le mettre dans le txt
    def Ajouter_Scoreboard(self):

        # Prendre la date du jour
        today = datetime.date.today()
        date = today.strftime("%d/%m/%Y")

        # Créer un fichier texte ou l'ouvrir s'il existe déjà
        with open("Scoreboard.txt", "a+") as file:
            file.write(self.player.name + " " + str(self.player.points) + " " + date + "\n")

    @staticmethod
    #lit le fichier et print les 10 meilleurs
    def Lire_Scoreboard():         
        
        with open("Scoreboard.txt", "r") as file:
            data = file.readlines()
        
        data_split = [i.split() for i in data]

        classement = sorted(data_split, key=lambda infosparties: int(infosparties[1]), reverse=True) # reverse=true pour affichage décroissant
        #prendre les listes(nom,pts,date) dans la liste(datasplit) il prend chaque listes il va aller voir dedans la position 1 -> les pts et après ça il va classer les listes par ordres décroissants dans le score
        
        print("\n----- Scoreboard -----")
        for i in range(0, 10):
            try:  # Exception au cas où si il n'y a pas 10 joueurs
                print(i + 1,"\t" + "\t".join(classement[i]))
            except:
                pass
        
        
    # Joue une partie complète
    def play(self,diffi):

        self.draw()
        
        self.end = Game.end_time(1,0)
        now = datetime.datetime.today()
        
        while now < self.end :
            self.player.move()
            if self.player.position[0] < 0 :
                self.player.position = (self.board_size-1,self.player.position[1])
            elif self.player.position[1] < 0 :
                self.player.position = (self.player.position[0],self.board_size-1)
            elif self.player.position[0] > self.board_size-1 :
                self.player.position = (0,self.player.position[1])        
            elif self.player.position[1] > self.board_size-1 :
                self.player.position = (self.player.position[0],0)
            
            self.check_candy()
            self.check_temps()
            self.check_malus()
            

            if random.randint(1,self.valDiff[diffi][0]) == 1 :
                self.pop_candy()
            if random.randint(1,self.valDiff[diffi][1]) == 1 :
                self.pop_temps()
            if random.randint(1,self.valDiff[diffi][2]) == 1 :
                self.pop_malus()

            self.draw()
            self.print_time()
            
            #booléen pour ne pas perturber l'affiche du plateau lorsque qu'on ramasse un malus
            if self.bool_freeze == True :
                print("Impossible de bouger, trop froid !!")
                time.sleep(2)
                self.bool_freeze = False
            
            now = datetime.datetime.today()
        
        os.system("cls")
        print("----- Terminé -----")
        print(self.player.name,"avez", self.player.points, "points")
        self.Ajouter_Scoreboard()
        self.Lire_Scoreboard()
        input("\nAppuyez sur ENTER pour continuer ...")
        time.sleep(3)
        os.system("cls")

    @staticmethod
    # retourne le moment où le jeu est censé être fini
    def end_time(delta_minute, delta_second):
        delta = datetime.timedelta(minutes=delta_minute, seconds=delta_second)
        end = datetime.datetime.today() + delta
        return end

class Menu():
    #affiche un menu à choix multiples
    def Main(self):
        os.system("cls")
        Menu.Logo()
        while True:
            Menu.Affichage()
            choix = input("\nVotre choix: ")

            if choix == "1":
                
                player_name = input("Entrez votre pseudo: ")
                while len(player_name) > 5 or " " in player_name:
                    print("ERREUR : Votre pseudo comporte plus de 5 caractères et il ne peut pas contenir d'espace\n")
                    player_name = input("Entrez votre pseudo: ")
                diffi = Menu.Difficulte()
                while diffi != "1" and diffi != "2" and diffi != "3":
                    diffi = Menu.Difficulte()
                p = Player(player_name)
                g = Game(p)
                g.play(diffi)
            elif choix == "2":
                os.system("cls")                                 
                Game.Lire_Scoreboard()
                input("\nAppuyer sur ENTER pour continuer ...")
                os.system("cls")
            elif choix == "3":              
                Menu.Règles()
                os.system("cls")                
            elif choix == "4":
                print("Merci d'avoir joué")
                os._exit(1)
            else:
                print("Mauvais choix ...")


    @staticmethod
    def Règles():
        os.system("cls")
        print("Voici les règles:\n"
        "Ceci est un jeu de plateau où le joueur(vous \"0\") devra récuperer un maximum de bonbons dans un temps imparti.\n"
        "Pour se faire vous devrez vous déplacer avec les touches Z(haut), Q(gauche), S(bas), D(droite).\n"
        "Il existe trois types d'objets ramassables qui apparaitront de façons aléatoire :\n"
        "-  * les bonbons ceux-ci vous attribueront 1 points lorsque vous passerez dessus.\n"
        "-  T un bonus de temps de 3 secondes.\n"
        "-  ƒ un malus vous gelant pendant 2 secondes.")

        input("\nAppuyez sur ENTER pour retourner au menu ...")

    @staticmethod
    def Logo():
        print("\n"
            "   _____                _       _____           _     \n"
            "  / ____|              | |     |  __ \         | |    \n"  
            " | |     __ _ _ __   __| |_   _| |__) |   _ ___| |__  \n"  
            " | |    / _` | '_ \ / _` | | | |  _  / | | / __| '_ \ \n" 
            " | |___| (_| | | | | (_| | |_| | | \ \ |_| \__ \ | | |\n"
            "  \_____\__,_|_| |_|\__,_|\__, |_|  \_\__,_|___/_| |_|\n"
            "                           __/ |                      \n"
            "                          |___/                       \n"
)


    @staticmethod

    def Affichage():
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


    @staticmethod
    def Difficulte():
        os.system("cls")
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


if __name__ == "__main__" :
     
    g = Menu()
    g.Main()

    
    
    
