from numbers import Number
from fractions import Fraction

class Matrix:
    def __init__(self, rows):
        if not rows:
            raise ValueError("matrix cannot be empty")

        width = len(rows[0])
        if any(len(row) != width for row in rows):
            raise ValueError("rows must be same length")

        self.rows = [list(row) for row in rows]
        self.nrows = len(rows)
        self.ncols = width

    def __repr__(self):
        return f"Matrix({self.rows!r})"

    def __add__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented

        if self.nrows != other.nrows or self.ncols != other.ncols:
            raise ValueError("matrix dimensions must match for addition")
        rows = [
            [a+b for a,b in zip(row_a, row_b)]
            for row_a, row_b in zip(self.rows, other.rows)
        ]
        return Matrix(rows)

    def __sub__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented

        if self.nrows != other.nrows or self.ncols != other.ncols:
            raise ValueError("matrix dimensions must match for subraction")
        rows = [
            [a-b for a,b in zip(row_a, row_b)]
            for row_a, row_b in zip(self.rows, other.rows)
        ]
        return Matrix(rows)

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            if isinstance(other, Number):
                result = [
                    [element * other for element in row]
                    for row in self.rows
                ]
                return Matrix(result)
            else:
                return NotImplemented
        
        if self.ncols != other.nrows:
            raise ValueError("matrix dimensions are incompatible for multiplication")

        rows = [
            [
                sum(self.rows[i][k] * other.rows[k][j]
                    for k in range(self.ncols))
                for j in range(other.ncols)
            ]
            for i in range(self.nrows)
        ]
        return Matrix(rows)

    def __rmul__(self, other):
        if not isinstance(other, Number):
            return NotImplemented
        result = [
            [element * other for element in row]
            for row in self.rows
        ]
        return Matrix(result)

    def det(self):
        if self.nrows != self.ncols:
            raise ValueError("cannot find determinant of non square matrix")
        col = 0
        result = 1
        m_copy = Matrix(self.rows)
        m = m_copy.rows
        swap = ref(m_copy.rows)
        for rows in range(m_copy.nrows):
            result *= m[rows][col]
            col += 1
        return result * ((-1) ** swap)

def ref(m):
    nrows = len(m)
    ncols = len(m[0])
    r = 0
    swap = 0
    for c in range(ncols):
        if r>=nrows: break

        max = 0
        for i in range(r, nrows):
            if abs(m[i][c]) > max:
                max = abs(m[i][c])
                max_i = i
        if max == 0:
            continue
        if max_i!=r:
            row_swap(m, r, max_i)
            swap += 1

        for i in range(r+1, nrows):
            if m[i][c] == 0:
                continue
            scale = -m[i][c]/m[r][c]
            add_row_scaled(m, i, r, scale)
        r += 1
    return swap          

def row_swap(m, i, j):
    m[i], m[j] = m[j], m[i]

def row_mult(m, i, k):
    m[i] = [k*x for x in m[i]]

def add_row_scaled(m, target, source, k):
    m[target] = [t + s*k for t,s in zip(m[target], m[source])]
