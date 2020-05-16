# -*- coding: utf-8 -*-

import random
import datetime

class Player :
    
    keyboard_key = {'z':(-1,0),
                    'q':(0,-1),
                    's':(1,0),
                    'd':(0,1)}
    
    def __init__(self, name, points = 0, start = (0,0)):
        self.name = name
        self.points = points
        self.position = start
        self.ancien = start #modif

    def move (self) :
        
        key = input("Mouvement (z,q,s,d) : ")
        while key not in Player.keyboard_key.keys() :
            key = input("Mouvement (z,q,s,d) : ")
        
        move = Player.keyboard_key[key]
        if self.ancien == (self.position[0] + move[0], self.position[1] + move[1]): #modif
            print("impossible") #modif
        else :
            self.ancien = self.position #modif
            self.position = (self.position[0] + move[0], self.position[1] + move[1]) #modif
        
    

class Game :
    
    def __init__(self, player, size=10):
        self.player = player
        self.board_size = size
        self.candies = []
        self.bonusT = [] #Modif

        
    # Dessine le plateau
    def draw(self):
        for line in range(self.board_size):
            for col in range(self.board_size):
                if (line,col) in self.candies :
                    print("*",end=" ")
                elif (line,col) in self.bonusT : #Modif
                    print("T",end=" ") #Modif
                elif (line,col) == self.player.position :
                    print("O",end=" ")
                else : 
                    print(".",end=" ")
            print()
            
    # Fait apparaitre un bonbon
    def pop_candy(self):
        new_candy = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if new_candy not in self.candies and new_candy not in self.bonusT : #Modif
            self.candies.append(new_candy)
    
    def pop_temps(self): #Modif
        bonus_temp = (random.choice(range(self.board_size)),random.choice(range(self.board_size))) #Modif
        if bonus_temp not in self.candies and bonus_temp not in self.bonusT : #Modif
            self.bonusT.append(bonus_temp) #Modif
             
    # Regarde s'il y a un bonbon à prendre (et le prend)
    def check_candy(self):
        if self.player.position in self.candies:
            self.player.points += 1
            self.candies.remove(self.player.position)
    
    def check_temps(self) : #Modif
        if self.player.position in self.bonusT:
            delta = datetime.timedelta(0,5)
            self.end = self.end + delta
            self.bonusT.remove(self.player.position)

    def print_time(self):#modif
        restant = self.end - datetime.datetime.today() 
        print("Temps restants : ", restant)
        
        
    # Joue une partie complète
    def play(self):
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
            print(self.end) #Modif

            
            if random.randint(1,3) == 1 :
                self.pop_candy()
            if random.randint(1,16) == 1 : #Modif
                self.pop_temps() #Modif
            
                
            self.draw()
            self.print_time()#modif
            
            now = datetime.datetime.today()
        
        
        print("----- Terminé -----")
        print(self.player.name,"avez", self.player.points, "points")#modif


    @staticmethod
    # retourne le moment où le jeu est censé être fini
    def end_time(delta_minute, delta_second):
        delta = datetime.timedelta(minutes=delta_minute, seconds=delta_second)
        end = datetime.datetime.today() + delta
        return end
        



if __name__ == "__main__" :
     
    p = Player(input("Entrez votre nom : "))#modif
    g = Game(p)
    g.play()

    
    
    
