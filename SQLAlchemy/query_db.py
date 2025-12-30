from models import User, Address
from sqlalchemy import select
from sqlalchemy.orm import Session
from create_db import engine

with Session(engine) as session:

    # 1 Print SpongeBob and Sandy
    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
    for user in session.scalars(stmt):
        print(user)

    # 2️ Get Sandy's specific address
    stmt = (
        select(Address)
        .join(Address.user)
        .where(User.name == "sandy")
        .where(Address.email_address == "sandy@sqlalchemy.org")
    )
    sandy_address = session.scalars(stmt).one()  # Ensure exactly one row exists
    print(sandy_address.email_address, sandy_address.user.name)

    # 3️ Get Patrick and add an address
    stmt = select(User).where(User.name == "patrick")
    patrick = session.scalars(stmt).one()
    patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))

    # 4️ Update Sandy's email
    sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"

    session.commit()  # Save changes

    print(sandy_address)

    # 5️ Remove Sandy's address and delete Patrick
    sandy = session.get(User, sandy_address.user.id)
    sandy.addresses.remove(sandy_address)
    session.delete(patrick)

    session.commit()  # Save changes

    # 6️ Print all remaining users
    stmt = select(User)
    for user in session.scalars(stmt):
        print(user)
