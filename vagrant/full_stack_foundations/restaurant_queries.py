from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from random import randint
import datetime
import random
from sqlalchemy import desc
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def list_restaurants():
    """ Returns all the puppies names, id and DOB in alphebetical order. """
    all_restaurants = session.query(Restaurant).order_by('name')
    restaurant_list = []
    for i in all_restaurants:
        restaurant_list.append((str(i.name), i.id))
    return restaurant_list

def add_restaurant(new_name):
	""" Creates a new restaurant and inserts it into the database. """
	new_restaurant = Restaurant(name=str(new_name))
	try:
	    session.add(new_restaurant)
	    session.commit()
	    return
	except: 
		pass

def fetch_name_from_id(restaurant_id):
	""" Fetches the corresponding restaurant name from the DB. """
	restaurant_in = int(restaurant_id)
	restaurant_name = session.query(Restaurant).filter_by(id=restaurant_in).first()
	return restaurant_name.name

def change_restaurant_name(restaurant_id, new_name):
	""" Takes an existing restaurant id, and modifies the name. 
		Returns True if successful, and false if no name change carried out.
	"""
	input_id, new_name_in = int(restaurant_id), str(new_name)
	chosen_entry = session.query(Restaurant).filter_by(id = input_id).one()
	if chosen_entry != []:
		original = chosen_entry.name
		chosen_entry.name = new_name_in
		session.add(chosen_entry)
		session.commit()
		print "%s successfully changed to %s." % (original, new_name_in)
		return True
	else:
		return False




