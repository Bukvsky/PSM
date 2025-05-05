import numpy as np
import matplotlib.pyplot as plt


n = 41
N = n - 1
h = 1
size = N * N


def index(i, j):
    return i * N + j

A = np.zeros((size, size))
b = np.zeros(size)


for i in range(N):
    for j in range(N):
        idx = index(i, j)
        A[idx, idx] = -4


        if i < N - 1:
            A[idx, index(i+1, j)] = 1
        else:
            b[idx] -= 50


        if i > 0:
            A[idx, index(i-1, j)] = 1
        else:
            b[idx] -= 100


        if j < N - 1:
            A[idx, index(i, j+1)] = 1
        else:
            b[idx] -= 200


        if j > 0:
            A[idx, index(i, j-1)] = 1
        else:
            b[idx] -= 150


T = np.linalg.solve(A, b)


T_grid = np.zeros((n, n))


T_grid[0, :] = 150   # dolna krawędź
T_grid[-1, :] = 200  # górna krawędź
T_grid[:, 0] = 100   # lewa krawędź
T_grid[:, -1] = 50   # prawa krawędź


for i in range(1, n - 1):
    for j in range(1, n - 1):
        T_grid[i, j] = T[index(j - 1, i - 1)]

# Wykres
plt.figure(figsize=(8, 6))
plt.imshow(T_grid, cmap='hot', origin='lower')
plt.colorbar(label='Temperatura (°C)')
plt.title('Rozkład temperatury w płytce (40x40)')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
