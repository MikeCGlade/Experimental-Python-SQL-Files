from models import Base, User, Address
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pathlib import Path

db_folder = Path("database")
db_folder.mkdir(exist_ok=True)
db_file = db_folder / "data.db"

engine = create_engine(f"sqlite:///{db_file}", echo=True)

Base.metadata.create_all(engine)


    
if __name__ == "__main__":
    
    with Session(engine) as session:
        spongebob = User(name="spongebob", fullname="spongebob squarepants", addresses=[Address(email_address="spongebob@sqlalchemy.org")])
        sandy = User(name="sandy", fullname="sandy cheeks", addresses=[Address(email_address="sandy@sqlalchemy.org"), Address(email_address="sandy@squirrelpower.org")])
        
        patrick = User(name="patrick", fullname="patrick star")
        
        session.add_all([spongebob, sandy, patrick])
        
        session.commit()