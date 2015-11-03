# Configuration component for sqlalchemy starts here.
# 
# Carry out imports for upcoming code in the file.
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship 

from sqlalchemy import create_engine

# Create an instance of the declarative base class we just imported.
Base = declarative_base()

# Configuration ends here (first part - the second part is at the end).

# Create restaurant class as an extension of python base class.
# Within this class we create a representation of our table
# inside the created database.
class Shelter(Base):
	# Create a table using __tablename__ = 'some_tablename'
    __tablename__ = 'shelter'
	# Create columns of the table shelter, using instances of Column class.
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    address = Column(String(150))
    city = Column(String(40))
    state = Column(String(40))
    zip_code = Column(Integer)
    website = Column(String(80))
    


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    date_of_birth = Column(Date)
    picture = Column(String)
    breed = Column(String(40))
    gender = Column(String(8))
    weight = Column(Numeric(10))
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    # Create a variable restaurant which is the relationship between class Restaurant.
    shelter = relationship(Shelter)



# Last part of Configuration component of sqlalchemy.
#
# Create an instance of creat engine class that produces a new
# file for use with sqlite in this case.
engine = create_engine('sqlite:///puppies.db')

# Add classes we created as tables into the database 'engine',
# as just created above.
Base.metadata.create_all(engine)