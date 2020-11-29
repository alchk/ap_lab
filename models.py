from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, orm
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('postgresql://ivanalchuk:deafult@localhost:5432/ap_lab')
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

class User(Base):
   __tablename__ = "users"
   id = Column(Integer, primary_key=True)

   first_name = Column(String)
   last_name = Column(String)
   password = Column(String)
   user_name = Column(String)


class Wallet(Base):
   __tablename__ = "wallets"
   id = Column(Integer, primary_key=True)

   balance = Column(Integer)
   owner_id = Column(Integer, ForeignKey(User.id))
   is_default = Column(Boolean)

   owner = orm.relationship(User, backref = "wallets", lazy = "joined")