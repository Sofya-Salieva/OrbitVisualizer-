from pydantic import BaseModel, Field

class OrbitRequest(BaseModel):
    "Модель запроса: параметры орбиты от клиента."
    altitude_km: float = Field(
        default=400.0,
        description="Высота перигея в километрах",
        ge=100, le=100000
    )
    inclination_deg: float = Field(
        default=51.6,
        description="Наклонение орбиты в градусах",
        ge=0, le=180
    )
    eccentricity: float = Field(
        default=0.0,
        description="Эксцентриситет (0 – круг, <1 – эллипс)",
        ge=0, le=0.99
    )
    raan_deg: float = Field(
        default=0.0,
        description="Долгота восходящего узла (RAAN) в градусах",
        ge=0, le=360
    )
    arg_perigee_deg: float = Field(
        default=0.0,
        description="Аргумент перигея в градусах",
        ge=0, le=360
    )
    dt: float = Field(
        default=60.0,
        description="Шаг интегрирования в секундах",
        ge=1, le=3600
    )
    num_points: int = Field(
        default=100,
        description="Количество точек на витке",
        ge=10, le=10000
    )