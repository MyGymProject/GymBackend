from sqlalchemy import create_engine
from config import setting
from sqlalchemy.orm import sessionmaker,declarative_base


 
engine=create_engine(url=setting.get_db_url(),echo=True)

sessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base=declarative_base()


def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
