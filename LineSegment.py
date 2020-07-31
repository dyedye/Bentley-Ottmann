class LineSegment:
    def __init__(self, p1, p2, comparator):
        self.p1 = p1
        self.p2 = p2

        p1x, p1y = self.p1
        p2x, p2y = self.p2

        dx = p2x - p1x
        dy = p2y - p1y
        a = dy
        b = -dx
        c = dx*p1y - dy*p1x
        self.coeffs = (a, b, c)
        self.comparator = comparator

    def __eq__(self, other):
        val_self = self.comparator(self)
        if type(other) == float or type(other) == int:
            val_other = other
        else:
            val_other = self.comparator(other)
        return val_self == val_other

    def __neq__(self, other):
        val_self = self.comparator(self)
        if type(other) == float or type(other) == int:
            val_other = other
        else:
            val_other = self.comparator(other)
        return val_self != val_other

    def __lt__(self, other):
        val_self = self.comparator(self)
        if type(other) == float or type(other) == int:
            val_other = other
        else:
            val_other = self.comparator(other)
        return val_self < val_other

    def __gt__(self, other):
        val_self = self.comparator(self)
        if type(other) == float or type(other) == int:
            val_other = other
        else:
            val_other = self.comparator(other)
        return val_self > val_other

    def __le__(self, other):
        val_self = self.comparator(self)
        if type(other) == float or type(other) == int:
            val_other = other
        else:
            val_other = self.comparator(other)
        return val_self <= val_other

    def __ge__(self, other):
        val_self = self.comparator(self)
        if type(other) == float or type(other) == int:
            val_other = other
        else:
            val_other = self.comparator(other)
        return val_self >= val_other

    def __str__(self):
        return 'line between ' + str(self.p1) + ' and ' + str(self.p2)


def intersects(line1, line2):
    a1, b1, c1 = line1.coeffs
    def line1_func(x, y): return a1*x + b1*y + c1

    a2, b2, c2 = line2.coeffs
    def line2_func(x, y): return a2*x + b2*y + c2

    res1 = line1_func(*line2.p1)*line1_func(*line2.p2) <= 0
    res2 = line2_func(*line1.p1)*line2_func(*line1.p2) <= 0
    return res1 and res2


def get_intersection(line1, line2):
    if not intersects(line1, line2):
        return None
    a1, b1, c1 = line1.coeffs
    a2, b2, c2 = line2.coeffs
    denom = a2*b1 - a1*b2
    if denom == 0:
        # ２線分の交点のうち、y座標が最大の点を持ってくる
        return sorted([line1.p1, line1.p2, line2.p1, line2.p2],
                      key=lambda x: x[1])[-1]

    x = -(b1*c2 - b2*c1)/denom
    y = (a1*c2 - a2*c1)/denom
    return x, y
