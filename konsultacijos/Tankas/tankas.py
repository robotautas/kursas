from random import randint

class Tankas:
    x = 0
    y = 0
    kryptis = 'n'
    suviai = {'n': 0, 's': 0, 'e': 0, 'w': 0}

    def pirmyn(self):
        self.y += 1
        self.kryptis = 'n'
        print("Pirmyn")

    def atgal(self):
        self.y -= 1
        self.kryptis = 's'
        print("Atgal")

    def kairėn(self):
        self.x -= 1
        self.kryptis = 'w'
        print("Kairėn")

    def dešinėn(self):
        self.x += 1
        self.kryptis = 'e'
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
        print("Iššauta")

    def info(self):
        print("Info:")
        print(f"Kryptis: {self.kryptis}")
        print(f"Koordinatės: X: {self.x}, Y: {self.y}")
        print(f"Šūviai: šiaurė: {self.suviai['n']}, pietūs: {self.suviai['s']}, rytai: {self.suviai['e']}, vakarai: {self.suviai['w']}")
    
class Taikinys():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_coords(self):
        print(f'Taikinys yra {self.x}, {self.y}')


tankas = Tankas()
taikinys = Taikinys(randint(-5, 6), randint(-5, 6))
taikinys.get_coords()


while True:
    print("Įveskite veiksmą")
    print("p - pirmyn, a = atgal, k - kairėn, d - dešinėn, suvis, info, end")
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
            taikinys = Taikinys(randint(-5, 6), randint(-5, 6))
            taikinys.get_coords()
        else:
            print('NEPATAIKEI!')
    elif pasirinkimas == "info":
        tankas.info()
    elif pasirinkimas == "end":
        break
    else:
        "Pasirinkote neesantį veiksmą. Bandykite dar kartą"
