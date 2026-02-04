from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL con el parámetro sslmode directamente para asegurar la persistencia
SQLALCHEMY_DATABASE_URL = "postgresql://historial_clinico_nube_user:Y0yL3U0N56j0qS0u5hL936M2yK6vS9rX@dpg-cub9o093967s73d1u83g-a.oregon-postgres.render.com/historial_clinico_nube?sslmode=require"

# Motor optimizado para evitar cierres inesperados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
