from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
 
Base = declarative_base()

# Create an association table to create a many to many relationship.
association_table = Table('association', Base.metadata,
    Column('puppy_id', Integer, ForeignKey('puppy.id')),
    Column('adopter.id', Integer, ForeignKey('adopter.id'))
)

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximum_capacity = Column(Integer, default=30)
    current_occupancy = Column(Integer)
    shelter_pups = relationship("Puppy")
    
class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    weight = Column(Numeric(10))
    shelter = relationship(Shelter)
    adopter = relationship("Adopter", secondary=association_table, backref="puppies")

class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable=False)
    adopted_puppy = Column(Integer, ForeignKey('puppy.id'))

class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, ForeignKey('puppy.id'), primary_key = True)
    photo = Column(String)
    description = Column(String(250))
    special_needs = Column(String(250))
    puppyprofile = relationship(Puppy)


engine = create_engine('sqlite:///puppyshelter.db')
 

Base.metadata.create_all(engine)