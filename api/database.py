from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión (Asegúrate de que NO tenga espacios al principio o al final)
SQLALCHEMY_DATABASE_URL = "postgresql://historial_clinico_nube_user:Y0yL3U0N56j0qS0u5hL936M2yK6vS9rX@dpg-cub9o093967s73d1u83g-a.oregon-postgres.render.com/historial_clinico_nube"

# Configuración de motor blindada para Render
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10
    },
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
