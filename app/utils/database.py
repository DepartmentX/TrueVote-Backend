from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your actual DB credentials
DB_USER = "avnadmin"
DB_PASSWORD = "AVNS_sscUzfV7fnGG1NSIKOq"
DB_HOST = "mysql-se-nimeshhiruna.l.aivencloud.com"
DB_PORT = "24099"
DB_NAME = "defaultdb"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
