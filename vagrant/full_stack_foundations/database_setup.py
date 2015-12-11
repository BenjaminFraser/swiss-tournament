# Configuration component for sqlalchemy starts here.
# 
# Carry out imports for upcoming code in the file.
import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship 

from sqlalchemy import create_engine

# Create an instance of the declarative base class we just imported.
Base = declarative_base()

# Configuration ends here (first part - the second part is at the end).

# Create restaurant class as an extension of python base class.
# Within this class we create a representation of our table
# inside the created database.
class Restaurant(Base):
	# Create a table using __tablename__ = 'some_tablename'
	__tablename__ = 'restaurant'
	# Create columns of the table restaurant, using instances of Column class.
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    # Create a variable restaurant which is the relationship between class Restaurant.
    restaurant = relationship(Restaurant)

    # Create a serialize function to format data for sending as JSON objects.
    @property
    def serialize(self):
        # Serialize data so its ideal for sending as JSON objects
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'price': self.price,
            'course': self.course
        }




# Last part of Configuration component of sqlalchemy.
#
# Create an instance of creat engine class that produces a new
# file for use with sqlite in this case.
engine = create_engine('sqlite:///restaurantmenu.db')

# Add classes we created as tables into the database 'engine',
# as just created above.
Base.metadata.create_all(engine)