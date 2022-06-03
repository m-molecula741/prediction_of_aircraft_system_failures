import numpy as np
import matplotlib.pyplot as plt

def bubble_max_row(m, col):
    n = len(m)
    max_row = None
    for r in range(col, n):
        if max_row is None or abs(m[r][col]) > abs(m[max_row][col]):
            max_row = r
    if max_row != col:
        m[col], m[max_row] = m[max_row], m[col]

def solve_gauss(m):
    n = len(m)
    for k in range(n - 1):
        bubble_max_row(m, k)
        for i in range(k + 1, n):
            div = m[i][k] / m[k][k]
            m[i][-1] -= div * m[k][-1]
            for j in range(k, n):
                m[i][j] -= div * m[k][j]
    for k in range(n):
        m[k] = [a / m[k][k] for a in m[k]]

    x = [0 for i in range(n)]
    for k in range(n - 1, -1, -1):
        x[k] = (m[k][-1] - sum([m[k][j] * x[j] for j in range(k + 1, n)]))
    return x


def f2(x,mkn2):
    return mkn2[0] * (x**2) + mkn2[1] * x + mkn2[2]


def P2(x, y,mkn2):
    return sum((f2(xi,mkn2) - yi)**2 for xi, yi in zip(x, y))

def main(x,y):



    m2 = [[sum(xi**4 for xi in x), sum(xi**3 for xi in x), sum(xi**2 for xi in x), sum(yi*xi**2 for xi, yi in zip(x, y)),],
        [sum(xi**3 for xi in x), sum(xi**2 for xi in x), sum(xi for xi in x), sum(xi*yi for xi, yi in zip(x, y))],
        [sum(xi**2 for xi in x), sum(xi for xi in x), len(x), sum(yi for yi in y)]]




    mkn2 = solve_gauss(m2)





    return mkn2