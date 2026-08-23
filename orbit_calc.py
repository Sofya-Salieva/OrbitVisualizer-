import numpy as np

MU_EARTH = 3.986004418e14    #гравитационный параметр Земли
R_EARTH = 6371e3                # радиус Земли в метрах

def orbital_to_cartesian(a, e, i, raan, argp, true_anomaly):
    "Перевод орбитальных элементов в декартовы координаты"
    # Расстояние от центра Земли
    r = a * (1 - e**2) / (1 + e * np.cos(true_anomaly))
    # Координаты в орбитальной плоскости (ось X – к перигею)
    x_orb = r * np.cos(true_anomaly)  
    y_orb = r * np.sin(true_anomaly)
    z_orb = 0.0

    # Скорость в орбитальной плоскости
    p = a * (1 - e**2)
    h = np.sqrt(MU_EARTH * p)
    vx_orb = - (MU_EARTH / h) * np.sin(true_anomaly)
    vy_orb = (MU_EARTH / h) * (e + np.cos(true_anomaly))
    vz_orb = 0.0

    # Матрица поворота вокруг Z на RAAN
    cos_raan, sin_raan = np.cos(raan), np.sin(raan)
    Rz_raan = np.array([[cos_raan, -sin_raan, 0],
                        [sin_raan,  cos_raan, 0],
                        [0,         0,        1]])
    # Вокруг X на наклонение
    cos_i, sin_i = np.cos(i), np.sin(i)
    Rx_i = np.array([[1, 0, 0],
                     [0, cos_i, -sin_i],
                     [0, sin_i,  cos_i]])
    # Вокруг Z на аргумент перигея
    cos_argp, sin_argp = np.cos(argp), np.sin(argp)
    Rz_argp = np.array([[cos_argp, -sin_argp, 0],
                        [sin_argp,  cos_argp, 0],
                        [0,         0,        1]])
    # Полная матрица поворота из орбитальной плоскости в инерциальную
    R = Rz_raan @ Rx_i @ Rz_argp

    pos = R @ np.array([x_orb, y_orb, z_orb])
    vel = R @ np.array([vx_orb, vy_orb, vz_orb])
    return pos, vel



def calculate_orbit(altitude_km=400, inclination_deg=51.6, eccentricity=0.0,
    raan_deg=0.0, arg_perigee_deg=0.0, dt=60, num_points=100):

    # Переводим градусы в радианы
    i = np.deg2rad(inclination_deg)
    raan = np.deg2rad(raan_deg)
    argp = np.deg2rad(arg_perigee_deg)

    # Радиус перигея
    r_perigee = R_EARTH + altitude_km * 1000
    # Большая полуось
    a = r_perigee / (1 - eccentricity) if eccentricity != 0 else r_perigee

    # Начальная истинная аномалия (в перигее)
    nu0 = 0.0
    pos0, vel0 = orbital_to_cartesian(a, eccentricity, i, raan, argp, nu0)

    state0 = np.hstack([pos0, vel0])
    
    T = 2 * np.pi * np.sqrt(a**3 / MU_EARTH)
    
    # Интегрирование
    t = 0.0
    trajectory = [pos0.tolist()]
    state = state0.copy()
    
    while t < T:
        h = min(dt, T - t)
        state = rk4_step(ody, t, state, h)
        trajectory.append(state)
        t += h
        trajectory.append(state[:3].tolist())
       
    return trajectory
        
def ody(t, state):
    x, y, z, vx, vy, vz = state
    r = np.array([x, y, z])
    r_norm = np.linalg.norm(r)
    ax, ay, az = -MU_EARTH * r / r_norm**3
    return np.array([vx, vy, vz, ax, ay, az])

def rk4_step(func, t, state, dt):
    k1 = func(t, state)
    k2 = func(t + dt/2, state + dt/2 * k1)
    k3 = func(t + dt/2, state + dt/2 * k2)
    k4 = func(t + dt, state + dt * k3)
    return state + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)

