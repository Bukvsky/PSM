import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from math import sin, cos, pi


matplotlib.use('Agg')
plt.switch_backend('Agg')


class PendulumSimulator:
    def __init__(self, length=1.0, gravity=9.81, mass=1.0):
        self.length = length
        self.gravity = gravity
        self.mass = mass

    def angular_acceleration(self, angle):
        return -(self.gravity / self.length) * sin(angle)

    def run_simulation(self, method, theta0, omega0, dt, total_time):
        steps = int(total_time / dt)
        time = np.linspace(0, total_time, steps + 1)

        df = pd.DataFrame(index=time, columns=['angle', 'omega'], dtype=np.float64)
        df.index.name = 'time'
        df.iloc[0] = [float(theta0), float(omega0)]

        if method == 'euler':
            for i in range(steps):
                alpha = self.angular_acceleration(df.iloc[i]['angle'])
                df.iloc[i + 1, 1] = df.iloc[i]['omega'] + alpha * dt
                df.iloc[i + 1, 0] = df.iloc[i]['angle'] + df.iloc[i]['omega'] * dt

        elif method == 'improved_euler':
            for i in range(steps):
                alpha1 = self.angular_acceleration(df.iloc[i]['angle'])
                omega_pred = df.iloc[i]['omega'] + alpha1 * dt
                theta_pred = df.iloc[i]['angle'] + df.iloc[i]['omega'] * dt

                alpha2 = self.angular_acceleration(theta_pred)
                df.iloc[i + 1, 1] = df.iloc[i]['omega'] + 0.5 * (alpha1 + alpha2) * dt
                df.iloc[i + 1, 0] = df.iloc[i]['angle'] + 0.5 * (df.iloc[i]['omega'] + omega_pred) * dt

        elif method == 'rk4':
            for i in range(steps):
                theta = float(df.iloc[i]['angle'])
                omega = float(df.iloc[i]['omega'])

                k1_theta = omega
                k1_omega = self.angular_acceleration(theta)

                k2_theta = omega + 0.5 * dt * k1_omega
                k2_omega = self.angular_acceleration(theta + 0.5 * dt * k1_theta)

                k3_theta = omega + 0.5 * dt * k2_omega
                k3_omega = self.angular_acceleration(theta + 0.5 * dt * k2_theta)

                k4_theta = omega + dt * k3_omega
                k4_omega = self.angular_acceleration(theta + dt * k3_theta)

                df.iloc[i + 1, 1] = omega + (dt / 6) * (k1_omega + 2 * k2_omega + 2 * k3_omega + k4_omega)
                df.iloc[i + 1, 0] = theta + (dt / 6) * (k1_theta + 2 * k2_theta + 2 * k3_theta + k4_theta)

        # Oblicz energie
        angles = df['angle'].to_numpy()
        omegas = df['omega'].to_numpy()

        df['kinetic'] = 0.5 * self.mass * (self.length * omegas) ** 2
        df['potential'] = self.mass * self.gravity * self.length * (1 - np.cos(angles))
        df['total'] = df['kinetic'] + df['potential']

        return df


def save_energies_plot(df, method_name, filename):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(df.index, df['kinetic'], 'b-', label='E. kinetyczna')
    ax.plot(df.index, df['potential'], 'g-', label='E. potencjalna')
    ax.plot(df.index, df['total'], 'r--', label='E. całkowita')

    ax.set_xlabel('Czas [s]')
    ax.set_ylabel('Energia [J]')
    ax.set_title(f'Energie wahadła - {method_name}')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)


def save_trajectory_plot(df, length, method_name, filename):
    angles = df['angle'].to_numpy()
    x = length * np.sin(angles)
    y = -length * np.cos(angles)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, 'b-', linewidth=1.5)
    ax.plot([0, x[0]], [0, y[0]], 'r-', linewidth=2)

    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_title(f'Trajektoria - {method_name}')
    ax.grid(True, alpha=0.3)
    ax.axis('equal')

    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)


def compare_methods():
    pendulum = PendulumSimulator(length=1.0, gravity=9.81, mass=1.0)
    theta0 = pi / 3
    omega0 = 0.0
    dt = 0.05
    total_time = 30

    methods = {
        'Euler': 'euler',
        'Ulepszony Euler': 'improved_euler',
        'RK4': 'rk4'
    }

    results = {}
    for name, method in methods.items():
        print(f"Symulacja: {name}...")
        results[name] = pendulum.run_simulation(method, theta0, omega0, dt, total_time)

    # Zapis wykresów do plików
    for name, df in results.items():
        save_energies_plot(df, name, f'energie_{name.lower().replace(" ", "_")}.png')
        save_trajectory_plot(df, pendulum.length, name, f'trajektoria_{name.lower().replace(" ", "_")}.png')

    # Wykres porównawczy
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {'Euler': 'blue', 'Ulepszony Euler': 'green', 'RK4': 'red'}

    for name, df in results.items():
        ax.plot(df.index, df['angle'], color=colors[name], label=name, linewidth=1.5)

    ax.set_xlabel('Czas [s]')
    ax.set_ylabel('Kąt [rad]')
    ax.set_title('Porównanie metod numerycznych')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig('porownanie_metod.png')
    plt.close(fig)

    print("Wykresy zostały zapisane do plików PNG.")


if __name__ == "__main__":
    compare_methods()