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
	if restaurant_name != []:
		return restaurant_name.name
	else: 
		print "That restaurant ID does not exist."
		return

def change_restaurant_name(restaurant_id, new_name):
	""" Takes an existing restaurant id, and modifies the name. 
		Returns True if successful, and false if no name change carried out.
	"""
	input_id, new_name_in = int(restaurant_id), str(new_name)
	chosen_entry = session.query(Restaurant).filter_by(id = input_id).one()
	# If the entry is valid, change the name accordingly. If not, return False.
	if chosen_entry != []:
		original = chosen_entry.name
		chosen_entry.name = new_name_in
		session.add(chosen_entry)
		session.commit()
		print "%s successfully changed to %s." % (original, new_name_in)
		return True
	else:
		return False

def delete_restaurant(restaurant_id, restaurant_name):
 	""" Removes a restaurant from the database using the input id and name. """
 	# Validate the correct parameter types, or change them accordingly.
 	input_id, name_in = int(restaurant_id), str(restaurant_name)
 	# Fetch chosen entry to be deleted from the database.
 	chosen_entry = session.query(Restaurant).filter_by(id = input_id).one()
 	# If the entry is valid, delete it. If not, return false.
 	if chosen_entry != []:
 		# Match the manual input name to the actual name.
 		if name_in == chosen_entry.name:
 			session.delete(chosen_entry)
 			session.commit()
 			print "%s deleted from the database." % chosen_entry.name
 			return True
 		else:
 			print "The input name does not match the actual name."
 			return False
 	else:
 		print "The selected restaurant id does not exist."
 		return False





