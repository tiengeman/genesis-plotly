from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pathlib

# importando o mongo, desisti do sqlite
username = 'ianfelipe'
password = 'MateMatica16'
valor_despesa = 0

uri = f"mongodb+srv://{username}:{password}@cluster0.hbs6exg.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Project']

colecao = db.get_collection('Usuários')

##

Base = declarative_base()
DB_PATH = pathlib.Path("app.db")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    sector = Column(String)
    password_hash = Column(String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

engine = None
Session = None

def init_db():
    global engine, Session
    engine = create_engine("sqlite:///" + str(DB_PATH))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

def get_user(email):
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        return user
    except Exception as e:
        print(f"Error getting user: {e}")
    finally:
        session.close()

def create_user(email, username, password, sector="", hashed_password=None):
    session = Session()
    try:
        if not hashed_password:
            hashed_password = generate_password_hash(password)
        new_user = User(email=email, username=username, sector=sector, password_hash=hashed_password)
        session.add(new_user)
        session.commit()
        return new_user
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        session.close()
