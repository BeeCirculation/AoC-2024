import MyVector
from MyVector import Vector

def change(x: Vector):
    a1, b1, a2, b2 = 0, 70, 70, 0
    range1 = b1 - a1
    range2 = b2 - a2
    factor = range2 / range1

    def _map(val):
        return (val - a1) * factor + a2

    return Vector(_map(x.x), _map(x.y))
