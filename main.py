from fastapi import FastAPI
from orbit_calc import calculate_orbit
from schemas import OrbitRequest

# Создаём приложение FastAPI с названием
app = FastAPI(
    title="Orbit Visualizer API",
    version="1.0.0",
    description="Сервер для расчёта орбит спутников"
)

@app.post("/orbit", summary="Рассчитать траекторию")
def get_orbit(params: OrbitRequest):
    "Принимает параметры орбиты и возвращает массив точек траектории. Каждая точка — список [x, y, z] в метрах."

    trajectory = calculate_orbit(
        altitude_km=params.altitude_km,
        inclination_deg=params.inclination_deg,
        eccentricity=params.eccentricity,
        raan_deg=params.raan_deg,
        arg_perigee_deg=params.arg_perigee_deg,
        dt=params.dt,
        num_points=params.num_points
    )

    trajectory_serializable = []
    for point in trajectory:
        serializable_point = [float(coord) for coord in point]
        trajectory_serializable.append(serializable_point)

    return {"trajectory": trajectory_serializable}

@app.get("/")
def root():
    return {"message": "Orbit Visualizer API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)