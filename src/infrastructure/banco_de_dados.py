from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define onde o arquivo do banco será salvo
SQLALCHEMY_DATABASE_URL = "sqlite:///./raizes_nordeste.db"

# Cria o motor de conexão (engine) - É ISSO QUE O PYTHON ESTAVA PROCURANDO
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()