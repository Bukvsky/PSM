import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parametry
A = 10
B = 25
C = 8 / 3
dt = 0.03
dt_euler = 0.005
t_start = 0
t_end = 100

# Wartości początkowe
initial_conditions = np.array([1, 1, 1])

def equations(state):
    x, y, z = state
    dx_dt = A * (y - x)
    dy_dt = -x * z + B * x - y
    dz_dt = x * y - C * z
    return np.array([dx_dt, dy_dt, dz_dt])

def euler_method(start_val, dt, t_s, t_e):
    t_points = np.arange(t_s, t_e, dt)
    solution = np.zeros((len(t_points), len(start_val)))
    solution[0] = start_val
    for i in range(1, len(t_points)):
        solution[i] = solution[i-1] + dt * equations(solution[i-1])
    return t_points, solution

def midpoint_method(start_val, dt, t_s, t_e):
    t_points = np.arange(t_s, t_e, dt)
    solution = np.zeros((len(t_points), len(start_val)))
    solution[0] = start_val
    for i in range(1, len(t_points)):
        k1 = dt * equations(solution[i-1])
        k2 = dt * equations(solution[i-1] + 0.5 * k1)
        solution[i] = solution[i-1] + k2
    return t_points, solution

def rk4_method(start_val, dt, t_s, t_e):
    t_points = np.arange(t_s, t_e, dt)
    solution = np.zeros((len(t_points), len(start_val)))
    solution[0] = start_val
    for i in range(1, len(t_points)):
        k1 = equations(solution[i-1])
        k2 = equations(solution[i-1] + 0.5 * dt * k1)
        k3 = equations(solution[i-1] + 0.5 * dt * k2)
        k4 = equations(solution[i-1] + dt * k3)
        solution[i] = solution[i-1] + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6
    return t_points, solution

# Obliczenia
t_euler, sol_euler = euler_method(initial_conditions, dt_euler, t_start, t_end)
t_midpoint, sol_midpoint = midpoint_method(initial_conditions, dt, t_start, t_end)
t_rk4, sol_rk4 = rk4_method(initial_conditions, dt, t_start, t_end)

# Wykresy 2D
plt.figure(figsize=(18, 5))

# x vs z
plt.subplot(1, 3, 1)
plt.plot(sol_euler[:, 0], sol_euler[:, 2], label="Euler", alpha=0.6)
plt.plot(sol_midpoint[:, 0], sol_midpoint[:, 2], label="Midpoint", alpha=0.6)
plt.plot(sol_rk4[:, 0], sol_rk4[:, 2], label="RK4", alpha=0.6)
plt.title("x vs z")
plt.xlabel("x")
plt.ylabel("z")
plt.legend()

# y vs z
plt.subplot(1, 3, 2)
plt.plot(sol_euler[:, 1], sol_euler[:, 2], label="Euler", alpha=0.6)
plt.plot(sol_midpoint[:, 1], sol_midpoint[:, 2], label="Midpoint", alpha=0.6)
plt.plot(sol_rk4[:, 1], sol_rk4[:, 2], label="RK4", alpha=0.6)
plt.title("y vs z")
plt.xlabel("y")
plt.ylabel("z")
plt.legend()

# x vs y
plt.subplot(1, 3, 3)
plt.plot(sol_euler[:, 0], sol_euler[:, 1], label="Euler", alpha=0.6)
plt.plot(sol_midpoint[:, 0], sol_midpoint[:, 1], label="Midpoint", alpha=0.6)
plt.plot(sol_rk4[:, 0], sol_rk4[:, 1], label="RK4", alpha=0.6)
plt.title("x vs y")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

plt.tight_layout()
plt.show()

# Wykres 3D
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(sol_euler[:, 0], sol_euler[:, 1], sol_euler[:, 2], label='Euler', alpha=0.5)
ax.plot(sol_midpoint[:, 0], sol_midpoint[:, 1], sol_midpoint[:, 2], label='Midpoint', alpha=0.7)
ax.plot(sol_rk4[:, 0], sol_rk4[:, 1], sol_rk4[:, 2], label='RK4', alpha=0.9)
ax.set_title('Trajektorie 3D')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.legend()
plt.show()
