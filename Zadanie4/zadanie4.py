import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# Stałe fizyczne
g = 9.81
alpha = 30
alpha_rad = np.radians(alpha)
m = 1.0
r = 0.1

# Momenty bezwładności
I_kula = (2 / 5) * m * r ** 2
I_sfera = (2 / 3) * m * r ** 2

# Warunki początkowe
s0 = 0.0
v0 = 0.0
beta0 = 0.0
omega0 = 0.0

# Parametry symulacji
t_start = 0.0
t_end = 5.0
dt = 0.01


def acceleration(I, m, r, alpha):
    return g * np.sin(alpha) / (1 + I / (m * r ** 2))


def midpoint_step(t, y, I, m, r, alpha):
    a = acceleration(I, m, r, alpha)
    epsilon = a / r

    def derivatives(y):

        s, v, beta, omega = y
        return np.array([v, a, omega, epsilon])

    k1 = derivatives(y)
    y_mid = y + 0.5 * dt * k1
    k2 = derivatives(y_mid)

    return y + dt * k2


def simulate(I, m, r, alpha):
    steps = int((t_end - t_start) / dt) + 1
    t = np.linspace(t_start, t_end, steps)
    y = np.zeros((steps, 4))  # [s, v, beta, omega]
    y[0] = [s0, v0, beta0, omega0]

    for i in range(1, steps):
        y[i] = midpoint_step(t[i - 1], y[i - 1], I, m, r, alpha)

    return t, y


# Przeprowadzenie symulacji dla obu obiektów
t_kula, y_kula = simulate(I_kula, m, r, alpha_rad)
t_sfera, y_sfera = simulate(I_sfera, m, r, alpha_rad)


s_kula, v_kula, beta_kula, omega_kula = y_kula.T
s_sfera, v_sfera, beta_sfera, omega_sfera = y_sfera.T


# Obliczenie energii
def calculate_energies(s, v, omega, I, m, alpha):
    h = (s.max() - s) * np.sin(alpha)
    E_pot = m * g * h
    E_kin_lin = 0.5 * m * v ** 2
    E_kin_rot = 0.5 * I * omega ** 2
    E_tot = E_pot + E_kin_lin + E_kin_rot
    return E_pot, E_kin_lin, E_kin_rot, E_tot


E_pot_kula, E_kin_lin_kula, E_kin_rot_kula, E_tot_kula = calculate_energies(
    s_kula, v_kula, omega_kula, I_kula, m, alpha_rad)
E_pot_sfera, E_kin_lin_sfera, E_kin_rot_sfera, E_tot_sfera = calculate_energies(
    s_sfera, v_sfera, omega_sfera, I_sfera, m, alpha_rad)


fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Symulacja toczenia się kuli i sfery po równi pochyłej')

# Wykres położenia
axs[0, 0].plot(t_kula, s_kula, label='Kula')
axs[0, 0].plot(t_sfera, s_sfera, label='Sfera')
axs[0, 0].set_xlabel('Czas [s]')
axs[0, 0].set_ylabel('Położenie [m]')
axs[0, 0].set_title('Położenie w funkcji czasu')
axs[0, 0].legend()
axs[0, 0].grid()

# Wykres kąta obrotu
axs[0, 1].plot(t_kula, beta_kula, label='Kula')
axs[0, 1].plot(t_sfera, beta_sfera, label='Sfera')
axs[0, 1].set_xlabel('Czas [s]')
axs[0, 1].set_ylabel('Kąt obrotu [rad]')
axs[0, 1].set_title('Kąt obrotu w funkcji czasu')
axs[0, 1].legend()
axs[0, 1].grid()

# Wykres energii kuli
axs[1, 0].plot(t_kula, E_pot_kula, label='Energia potencjalna')
axs[1, 0].plot(t_kula, E_kin_lin_kula, label='Energia kinetyczna (postępowa)')
axs[1, 0].plot(t_kula, E_kin_rot_kula, label='Energia kinetyczna (obrotowa)')
axs[1, 0].plot(t_kula, E_tot_kula, 'k--', label='Energia całkowita')
axs[1, 0].set_xlabel('Czas [s]')
axs[1, 0].set_ylabel('Energia [J]')
axs[1, 0].set_title('Energie kuli')
axs[1, 0].legend()
axs[1, 0].grid()

# Wykres energii sfery
axs[1, 1].plot(t_sfera, E_pot_sfera, label='Energia potencjalna')
axs[1, 1].plot(t_sfera, E_kin_lin_sfera, label='Energia kinetyczna (postępowa)')
axs[1, 1].plot(t_sfera, E_kin_rot_sfera, label='Energia kinetyczna (obrotowa)')
axs[1, 1].plot(t_sfera, E_tot_sfera, 'k--', label='Energia całkowita')
axs[1, 1].set_xlabel('Czas [s]')
axs[1, 1].set_ylabel('Energia [J]')
axs[1, 1].set_title('Energie sfery')
axs[1, 1].legend()
axs[1, 1].grid()

plt.tight_layout()
plt.show()