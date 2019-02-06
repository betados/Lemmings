from vector_2d import Vector, distance_point_segment, VectorPolar


class PointList(object):
    def __init__(self):
        self.set = set()
        self.lista = []

    @property
    def leftest(self):
        return sorted(self.set, key=lambda point: point.x)[0]

    @property
    def rightest(self):
        return sorted(self.set, key=lambda point: point.x)[-1]

    @property
    def highest(self):
        return sorted(self.set, key=lambda point: point.y)[0]

    @property
    def lowest(self):
        return sorted(self.set, key=lambda point: point.y)[-1]

    def __getitem__(self, item: int) -> Vector:
        return self.lista[item]

    def __iter__(self):
        return iter(self.set)

    def sort(self):
        lista_n = self.lista[:]
        self.lista = [lista_n.pop(), ]
        while len(lista_n) > 0:
            nearest = 0
            for i, v in enumerate(lista_n):
                if abs(self.lista[-1] - v) < abs(self.lista[-1] - lista_n[nearest]):
                    nearest = i
            self.lista.append(lista_n.pop(nearest))

    def append(self, element: Vector):
        self.set.add(element)
        self.lista = list(self.set)
        self.sort()

    def remove(self, item: Vector):
        self.set.remove(item)

    def pop(self, index: int = -1):
        return self.set.pop(index)

    def __len__(self) -> int:
        return len(self.set)

    def __str__(self):
        return str(self.lista)
