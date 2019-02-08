from vector_2d import Vector


class PointList(object):
    def __init__(self):
        self.set = set()
        self.__lista = []
        self.__x_boundaries = None
        self.__y_boundaries = None

    def calc_bounding_box(self):
        ordered_x = sorted(self.set, key=lambda point: point.x)
        ordered_y = sorted(self.set, key=lambda point: point.y)
        self.__x_boundaries = ordered_x[0][0], ordered_x[-1][0]
        self.__y_boundaries = ordered_y[0][1], ordered_y[-1][1]

    @property
    def leftest(self) -> float:
        return self.__x_boundaries[0]

    @property
    def rightest(self) -> float:
        return self.__x_boundaries[1]

    @property
    def highest(self) -> float:
        return self.__y_boundaries[0]

    @property
    def lowest(self) -> float:
        return self.__y_boundaries[1]

    def __getitem__(self, item: int) -> Vector:
        return self.__lista[item]

    def __iter__(self):
        return iter(self.__lista)

    def order_list(self):
        self.__lista = list(self.set)
        self.sort()

    @property
    def lista(self):
        return self.__lista

    def sort(self):
        lista_n = self.__lista[:]
        self.__lista = [lista_n.pop(), ]
        while len(lista_n) > 0:
            nearest = 0
            for i, v in enumerate(lista_n):
                if abs(self.__lista[-1] - v) < abs(self.__lista[-1] - lista_n[nearest]):
                    nearest = i
            self.__lista.append(lista_n.pop(nearest))

    def add(self, element: Vector):
        self.set.add(element.int_vector())

    def append(self, element: Vector):
        self.__lista.append(element)

    def remove(self, item: Vector):
        self.lista.remove(item)

    def pop(self, index: int = -1):
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self.set)

    def __str__(self):
        return str(self.__lista)
