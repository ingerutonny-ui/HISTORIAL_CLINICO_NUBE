from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL sin el parámetro sslmode al final (lo manejaremos en el motor)
SQLALCHEMY_DATABASE_URL = "postgresql://historial_clinico_nube_user:Y0yL3U0N56j0qS0u5hL936M2yK6vS9rX@dpg-cub9o093967s73d1u83g-a.oregon-postgres.render.com/historial_clinico_nube"

# Configuración robusta para Render: SSL obligatorio y reciclaje de conexión
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
