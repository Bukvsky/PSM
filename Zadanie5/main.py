import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

g = 6.6743e-11
dt = 7200
n = math.ceil(31556926 / dt)

mk = 7.347e22
mz = 5.972e24
ms = 1.989e30

rzk = 384000000
rzs = 1.5e11

v_k = math.sqrt(g * mz / rzk)
v_s = math.sqrt(g * ms / rzs)

xk, yk = 0, rzk
vx, vy = v_k, 0

xz, yz = 0, rzs
s_vx, s_vy = v_s, 0

księżyc_x, księżyc_y = np.zeros(n), np.zeros(n)
ziemia_x, ziemia_y = np.zeros(n), np.zeros(n)

for i in range(n):
    księżyc_x[i] = xk + xz
    księżyc_y[i] = yk + yz
    ziemia_x[i] = xz
    ziemia_y[i] = yz

    wx, wy = -xk, -yk
    dzk = math.sqrt(wx**2 + wy**2)
    ux, uy = wx / dzk, wy / dzk
    a_k = g * mz / dzk**2
    ax, ay = ux * a_k, uy * a_k

    m_xk, m_yk = xk + vx * dt / 2, yk + vy * dt / 2
    m_vx, m_vy = vx + ax * dt / 2, vy + ay * dt / 2
    xk += m_vx * dt
    yk += m_vy * dt
    vx += ax * dt
    vy += ay * dt

    s_wx, s_wy = -xz, -yz
    dzs = math.sqrt(s_wx**2 + s_wy**2)
    s_ux, s_uy = s_wx / dzs, s_wy / dzs
    a_s = g * ms / dzs**2
    s_ax, s_ay = s_ux * a_s, s_uy * a_s

    m_xz, m_yz = xz + s_vx * dt / 2, yz + s_vy * dt / 2
    m_s_vx, m_s_vy = s_vx + s_ax * dt / 2, s_vy + s_ay * dt / 2
    xz += m_s_vx * dt
    yz += m_s_vy * dt
    s_vx += s_ax * dt
    s_vy += s_ay * dt

plt.figure(figsize=(8, 8))
plt.plot(ziemia_x, ziemia_y, label="Ziemia", color='blue')
plt.plot(księżyc_x, księżyc_y, label="Księżyc", color='orange')
plt.scatter([0], [0], color='gold', s=300, label="Słońce")
plt.title("Ruch Księżyca względem Słońca (falowanie wokół orbity Ziemi)")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.legend()
plt.axis('equal')
plt.grid()
plt.tight_layout()
plt.show()