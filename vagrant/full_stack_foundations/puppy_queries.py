from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
from random import randint
import datetime
import random
from sqlalchemy import desc
engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def list_puppies():
	""" Returns all the puppies names, id and DOB in alphebetical order. """
    all_puppies = session.query(Puppy).order_by('name')
    for i in all_puppies:
        print i.name, i.id, i.dateOfBirth


def young_puppies():
	""" Returns all the puppies younger than 6 months. """
	
	#First attempt at the problem using python as below:
	younger_years = session.query(Puppy).all()
	new_list = []

	for i in younger_years:
		if i.dateOfBirth>datetime.date(2015, 05, 02):
			print i.id, i.name, i.dateOfBirth


def better_young_puppies():
	""" Returns all the puppies younger than 6 months, youngest first. """

	birthdays = session.query(Puppy).filter(Puppy.dateOfBirth>='2015-05-02').order_by(desc(Puppy.dateOfBirth))
	for i in birthdays:
		print i.id, i.name, i.dateOfBirth
	# to then put this into a new list of young puppies: 
	young_puppies = []
	for i in birthdays:
		# The str() ensures the object displays in the list as readable. 
		# In reality, the datetime format dateOfBirth is in should be kept
		# in that format for as long as possible to remain useful in functions. 
		young_puppies.append([str(i.id), str(i.name), str(i.dateOfBirth)])


def ascending_weights():
	"""" Returns all puppies id, name and weights in ascending order of weight. """

	weights = session.query(Puppy).order_by(Puppy.weight)
    puppy_weights = []
	for i in weights:
		puppy_weights.append([str(i.id), str(i.name), str(i.weight)])

def puppy_shelter():
	""" Returns all puppies located in one shelter location """

	shelter_group = session.query(Puppy).order_by(Puppy.shelter_id)
	for i in shelter_group:
		# Because shelter table is linked to the puppy table via a foreign
		# key, we can call column data from shelter without stating a join!
		# As shown by i.shelter.name below...
		print i.id, i.name, i.shelter_id, i.shelter.name





