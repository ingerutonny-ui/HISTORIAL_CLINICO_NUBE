from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de tu base de datos (se mantiene igual)
SQLALCHEMY_DATABASE_URL = "postgresql://historial_clinico_nube_user:Y0yL3U0N56j0qS0u5hL936M2yK6vS9rX@dpg-cub9o093967s73d1u83g-a.oregon-postgres.render.com/historial_clinico_nube"

# Motor configurado con parámetros de seguridad total para Render
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "sslmode": "require"
    },
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
