
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
        A, B, C = self.points
        AB = self.distance(A, B)
        BC = self.distance(B, C)
        AC = self.distance(A, C)
        return (math.sqrt(AB ** 2 + BC ** 2) == AC) or (math.sqrt(AB ** 2 + AC ** 2) == BC) or (math.sqrt(AC ** 2 + BC ** 2) == AB)
    
    def is_inside(self, point):
        A, B, C = self.points
        min_bounds = [min(A[i], B[i], C[i]) for i in range(len(A))]
        max_bounds = [max(A[i], B[i], C[i]) for i in range(len(A))]
        return all(min_bound <= point[i] <= max_bound for i, (min_bound, max_bound) in enumerate(zip(min_bounds, max_bounds)))

    def diagonal_length(self):
        A, B, C = self.points
        AB = self.distance(A, B)
        AC = self.distance(A, C)
        return math.sqrt(AB ** 2 + AC ** 2)

    def distance(self, point1, point2):
        return math.sqrt(sum((coord1 - coord2) ** 2 for coord1, coord2 in zip(point1, point2)))

class Cuboid(Shape):
    def is_cuboid(self, n):
        vectors = [[self.points[j][i] - self.points[0][i] for i in range(len(self.points[0]))] for j in range(1, n)]
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                if sum(vectors[i][k] * vectors[j][k] for k in range(len(vectors[i]))) != 0:
                    return False
        return True
    
    def is_inside(self, point):
        A, B, C, D = self.points
        min_bounds = [min(A[i], B[i], C[i], D[i]) for i in range(len(A))]
        max_bounds = [max(A[i], B[i], C[i], D[i]) for i in range(len(A))]
        return all(min_bound <= point[i] <= max_bound for i, (min_bound, max_bound) in enumerate(zip(min_bounds, max_bounds)))

    def diagonal_length(self):
        A, B, C, D = self.points
        length = self.distance(A, B)
        width = self.distance(A, C)
        height = self.distance(A, D)

        return math.sqrt(length ** 2 + width ** 2 + height ** 2)

    def distance(self, point1, point2):
        return math.sqrt(sum((coord1 - coord2) ** 2 for coord1, coord2 in zip(point1, point2)))

def main():
    try:
        with open('coordinates.txt', 'r') as file:
            coordinates = [tuple(map(float, line.strip().split(","))) for line in file]

        #if len(coordinates) != 4 and len(coordinates) != 5:
            #raise ValueError("Input file should contain exactly 4 or 5 points.")

        if len(coordinates[0]) == len(coordinates[1]) == len(coordinates[2]) == 2:
            shape = Rectangle(coordinates[0:3])
        elif len(coordinates[0]) == len(coordinates[1]) == len(coordinates[2]) == 3:
            shape = Cuboid(coordinates[0:4])
        else:
            try:
                shape = Cuboid(coordinates[0:5])
            except:
                print("Invalid file format.")
                return

        if isinstance(shape, Rectangle):
            if not shape.is_rectangle():
                print("Given points do not form a rectangle.")
                return
        elif isinstance(shape,Cuboid):
            if not shape.is_cuboid(4):
                print("Given points do not form a cuboid.")
                return

        if isinstance(shape, Rectangle):
            print("Point X is inside the rectangle ABC." if shape.is_inside(coordinates[-1]) else "Point X is not inside the rectangle ABC.")
        elif isinstance(shape, Cuboid):
            print("Point X is inside the cuboid ABCD." if shape.is_inside(coordinates[-1]) else "Point X is not inside the cuboid ABCD.")

        print("Diagonal length:", shape.diagonal_length())
    except FileNotFoundError:
        print("File 'coordinates.txt' not found.")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()

