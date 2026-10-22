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
                
