
import math

class Shape:
    def __init__(self, points):
        self.points = points
    
    def is_inside(self, point):
        raise NotImplementedError("Method 'is_inside' must be implemented in subclasses.")

    def diagonal_length(self):
        raise NotImplementedError("Method 'diagonal_length' must be implemented in subclasses.")

class Rectangle(Shape):
    def is_rectangle(self):
        '''
        Provjera da li su tri tocke vrhovi pravokutnika
        '''
        A, B, C = self.points
        # Izracun udaljenosti izmedju tocaka
        AB = self.distance(A, B)
        BC = self.distance(B, C)
        AC = self.distance(A, C)

        return (math.sqrt(AB ** 2 + BC ** 2) == AC) or (math.sqrt(AB ** 2 + AC ** 2) == BC) or (math.sqrt(AC ** 2 + BC ** 2) == AB)
    
    def is_inside(self, point):
        '''
        Provjera da li se tocka nalazi unutar pravokutnika
        '''
        if len(point) != 2:
            raise ValueError("Pogresan format zadane tocke.")                 
        A, B, C = self.points
        min_bounds = [min(A[i], B[i], C[i]) for i in range(len(A))]
        max_bounds = [max(A[i], B[i], C[i]) for i in range(len(A))]
        return all(min_bound <= point[i] <= max_bound for i, (min_bound, max_bound) in enumerate(zip(min_bounds, max_bounds)))

    def diagonal_length(self):
        '''
        Izracun dijagonale pravokutnika
        '''        
        A, B, C = self.points
        AB = self.distance(A, B)
        AC = self.distance(A, C)
        return math.sqrt(AB ** 2 + AC ** 2)

    def distance(self, point1, point2):
        '''
        Izracun udaljenosti izmedju tocaka
        '''          
        return math.sqrt(sum((coord1 - coord2) ** 2 for coord1, coord2 in zip(point1, point2)))

class Cuboid(Shape):
    def is_cuboid(self):
        '''
        Provjera da li su zadane tocke vrhovi kvadra
        '''        
        A, B, C = self.points[0:3]
        # Izracun udaljenosti izmedju tocaka
        AB = self.distance(A, B)
        BC = self.distance(B, C)
        AC = self.distance(A, C)
        # Provjera da li su tri tocke vrhovi pravokutnika
        is_rectangle = (math.sqrt(AB ** 2 + BC ** 2) == AC) or (math.sqrt(AB ** 2 + AC ** 2) == BC) or (math.sqrt(AC ** 2 + BC ** 2) == AB)
        if is_rectangle:
            # Izracun tocke cetvrtog vrha pravokutnika
            P = self.find_fourth_edge(A, B, C)
            if P:
                P = (P[0], P[1], A[2])
            else:
                return False
            # Izracun mogucih koordinata za dobivanje visine kvadra
            D = self.points[-1]
            AD = (A[0], A[1], D[2])
            BD = (B[0], B[1], D[2])
            CD = (C[0], C[1], D[2])
            PD = (P[0], P[1], D[2])
            # Provjera da li su zadane samo dvije vrijednosti visine vrhova kvadra
            if len(set([A[-1],B[-1],C[-1],P[-1],D[-1]])) != 2:
                return False
            # Provjera koordinata točke D
            if D == AD or D == BD or D == CD or D == PD:
                return True
            else:
                return False
        else:
            return False

    @staticmethod    
    def find_fourth_edge(point1, point2, point3):
        '''
        Izracun tocke cetvrtog vrha pravokutnika
        '''         
        # Izracun vektora iz prvog vrha pravokutnika prema druga dva
        vector1 = (point2[0] - point1[0], point2[1] - point1[1])
        vector2 = (point3[0] - point1[0], point3[1] - point1[1])

        # Provjera da li su tri tocke vrhovi pravokutnika
        if vector1[0] * vector2[0] + vector1[1] * vector2[1] != 0:
            return False

        # Izracun tocke cetvrtog vrha pravokutnika
        point4 = (point1[0]+ vector1[0] + vector2[0], point1[1] + vector1[1] + vector2[1])
        return point4        
        
    def is_inside(self, point):
        '''
        Provjera da li se tocka nalazi unutar kvadra
        '''
        if len(point) != 3:
            raise ValueError("Pogresan format zadane tocke.")         
        A, B, C, D = self.points
        min_bounds = [min(A[i], B[i], C[i], D[i]) for i in range(len(A))]
        max_bounds = [max(A[i], B[i], C[i], D[i]) for i in range(len(A))]
        return all(min_bound <= point[i] <= max_bound for i, (min_bound, max_bound) in enumerate(zip(min_bounds, max_bounds)))

    def diagonal_length(self):
        '''
        Izracun dijagonale kvadra
        '''          
        A, B, C, D = self.points
        length = self.distance(A, B)
        width = self.distance(A, C)
        height = self.distance(A, (A[0], A[1], D[2]))

        return math.sqrt(length ** 2 + width ** 2 + height ** 2)

    def distance(self, point1, point2):
        '''
        Izracun udaljenosti izmedju tocaka
        '''         
        return math.sqrt(sum((coord1 - coord2) ** 2 for coord1, coord2 in zip(point1, point2)))

def main():
    try:
        with open('coordinates.txt', 'r') as file:
            coordinates = [tuple(map(float, line.strip().split(","))) for line in file]

        if len(coordinates) > 3 and len(coordinates[0]) == len(coordinates[1]) == len(coordinates[2]) == 2:
            shape = Rectangle(coordinates[0:3])
        elif len(coordinates) > 4 and len(coordinates[0]) == len(coordinates[1]) == len(coordinates[2]) == 3:
            shape = Cuboid(coordinates[0:4])
        else:
            raise ValueError("Nedefinirani oblik ili pogresan format.")

        if isinstance(shape, Rectangle):
            if not shape.is_rectangle():
                print("Zadane tocke ne oblikuju pravokutnik.")
                return
        elif isinstance(shape,Cuboid):
            if not shape.is_cuboid():
                print("Zadane tocke ne oblikuju kvadar.")
                return

        if isinstance(shape, Rectangle):
            print("Tocka X se nalazi unutar pravokutnika ABC." if shape.is_inside(coordinates[-1]) else "Tocka X se ne nalazi unutar pravokutnika ABC.")
        elif isinstance(shape, Cuboid):
            print("Tocka X se nalazi unutar kvadra ABCD." if shape.is_inside(coordinates[-1]) else "Tocka X se ne nalazi unutar kvadra ABCD.")

        print("Duzina dijagonale:", shape.diagonal_length())
    except FileNotFoundError:
        print("Datoteka 'coordinates.txt' nije nadena.")
    except ValueError as e:
        print("Greska kod unesenih vrijednosti: ", e)

if __name__ == "__main__":
    main()

