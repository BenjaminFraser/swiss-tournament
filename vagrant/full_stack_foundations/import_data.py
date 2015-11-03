from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
theOneAndOnlyRestaurant = Restaurant(name = 'King Cheese Palace')
session.add(theOneAndOnlyRestaurant)
session.commit()

bigmac = MenuItem(name = 'Big Mac', course = 'Main', price = '3.50', restaurant = 'theOneAndOnlyRestaurant')
session.add(bigmac)
session.commit()