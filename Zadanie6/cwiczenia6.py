import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import ImageMagickWriter

# Data
N = 100
L = np.pi
dx = L / N
c = 1.0
dt = 0.01
T = 10.0
steps = int(T / dt)

y = np.zeros((steps, N + 1))
v = np.zeros((N + 1))

E_kinetic = np.zeros(steps)
E_potential = np.zeros(steps)
E_total = np.zeros(steps)

for i in range(N + 1):
    y[0, i] = np.sin(i * dx)
    v[i] = 0.0


# Functions
def calculate_acceleration(positions, dx):
    acceleration = np.zeros(len(positions))
    for i in range(1, len(positions) - 1):
        acceleration[i] = c ** 2 * (positions[i - 1] - 2 * positions[i] + positions[i + 1]) / dx ** 2
    acceleration[0] = 0.0
    acceleration[-1] = 0.0
    return acceleration


def calculate_energy(positions, velocities, dx):
    E_k = 0.0
    for i in range(N + 1):
        E_k += 0.5 * dx * velocities[i] ** 2

    E_p = 0.0
    for i in range(N):
        E_p += 0.5 * ((positions[i + 1] - positions[i]) ** 2) / dx

    return E_k, E_p


# Midpoint
for t in range(steps - 1):
    current_positions = y[t].copy()
    a = calculate_acceleration(current_positions, dx)
    half_v = v.copy() + 0.5 * a * dt
    y[t + 1] = current_positions + half_v * dt
    y[t + 1, 0] = 0.0
    y[t + 1, -1] = 0.0
    new_a = calculate_acceleration(y[t + 1], dx)
    v = half_v + 0.5 * new_a * dt
    E_kinetic[t], E_potential[t] = calculate_energy(y[t], v, dx)
    E_total[t] = E_kinetic[t] + E_potential[t]

E_kinetic[-1], E_potential[-1] = calculate_energy(y[-1], v, dx)
E_total[-1] = E_kinetic[-1] + E_potential[-1]
time = np.linspace(0, T, steps)

# Plot of energy
plt.figure(figsize=(10, 6))
plt.plot(time, E_kinetic, label='Kinetic Energy')
plt.plot(time, E_potential, label='Potential Energy')
plt.plot(time, E_total, label='Total Energy')
plt.xlabel('Time')
plt.ylabel('Energy')
plt.title('String Energies Over Time')
plt.legend()
plt.grid(True)
plt.savefig('string_energies.png')
plt.show()

# Visualize string motion
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot(np.linspace(0, L, N + 1), y[0])
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Position (x)')
ax.set_ylabel('Displacement (y)')
ax.set_title('String Wave Simulation')
ax.grid(True)


def update(frame):
    line.set_ydata(y[frame])
    return line,


ani = FuncAnimation(fig, update, frames=min(steps, 200), interval=50, blit=True)
plt.show()

plt.figure(figsize=(10, 6))
x_vals = np.linspace(0, L, N + 1)
for i in range(0, steps, steps // 5):
    plt.plot(x_vals, y[i], label=f't = {i * dt:.2f}')
plt.xlabel('Position (x)')
plt.ylabel('Displacement (y)')
plt.title('String Positions at Different Times')
plt.legend()
plt.grid(True)
plt.show()
plt.close()