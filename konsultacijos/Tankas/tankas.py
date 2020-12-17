
from random import randint
from os import system

_ = system('cls')

class Tankas:
    x = 0
    y = 0
    taskai = 100
    kryptis = 'n'
    kryptys = {'n': 'šiaurė', 's': 'pietūs', 'e': 'rytai', 'w': 'vakarai'}
    suviai = {'n': 0, 's': 0, 'e': 0, 'w': 0}

    def pirmyn(self):
        self.y += 1
        self.kryptis = 'n'
        self.taskai -= 10
        print("Pirmyn")

    def atgal(self):
        self.y -= 1
        self.kryptis = 's'
        self.taskai -= 10
        print("Atgal")

    def kairėn(self):
        self.x -= 1
        self.kryptis = 'w'
        self.taskai -= 10
        print("Kairėn")

    def dešinėn(self):
        self.x += 1
        self.kryptis = 'e'
        self.taskai -= 10
        print("Dešinėn")
    
    def nusitaikymas(self, target_x, target_y):
        if self.x == target_x:
            if target_y > self.y and self.kryptis == 'n':
                return True
            elif target_y < self.y and self.kryptis == 's':
                return True
            return False
        if self.y == target_y:
            if target_x > self.x and self.kryptis == 'e':
                return True
            if target_x < self.x and self.kryptis == 'w':
                return True
            return False

    def šūvis(self):
        self.suviai[self.kryptis] += 1
        self.taskai -= 10

    def info(self):
        self.taskai -= 10
        print("\n")
        print(f"Kryptis: {self.kryptys[self.kryptis]}")
        print(f"Tanko koordinatės: {self.x}, {self.y}")
        print(f"Šūviai: šiaurė: {self.suviai['n']}, pietūs: {self.suviai['s']}, rytai: {self.suviai['e']}, vakarai: {self.suviai['w']}\n")

class Taikinys():
    def __init__(self, x, y):
        self.x = x
        self.y = y


tankas = Tankas()
taikinys = Taikinys(randint(-5, 6), randint(-5, 6))


while True:
    # print("Įveskite veiksmą")
    print(f"[{tankas.taskai}][taikinys: {(taikinys.x, taikinys.y)}]\np - pirmyn, a = atgal, k - kairėn, d - dešinėn, suvis, info, end")
    pasirinkimas = input()
    if pasirinkimas == "p":
        tankas.pirmyn()
    elif pasirinkimas == "a":
        tankas.atgal()
    elif pasirinkimas == "k":
        tankas.kairėn()
    elif pasirinkimas == "d":
        tankas.dešinėn()
    elif pasirinkimas == "suvis":
        tankas.šūvis()
        if tankas.nusitaikymas(taikinys.x, taikinys.y):
            print('PATAIKEI!')
            tankas.taskai += 100
            taikinys = Taikinys(randint(-5, 6), randint(-5, 6))
            
        else:
            tankas.taskai -= 10
            print('NEPATAIKEI!')
    elif pasirinkimas == "info":
        tankas.info()
    elif pasirinkimas == "end":
        break
    else:
        "Pasirinkote neesantį veiksmą. Bandykite dar kartą"
