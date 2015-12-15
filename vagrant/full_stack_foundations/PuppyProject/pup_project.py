# This Python file makes use of Flask microframework and the database framework
# defined within database_setup.py, which makes use of SQLAlchemy with SQLite. 
# Setup initial flask imports and app definition.
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies.py import Base, Shelter, Puppy, Adopter, Profile
# Anytime we run an app in Python a special variable called __name__ is defined.
# 
app = Flask(__name__)

engine = create_engine('sqlite:///puppyshelter.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Setup route decorators to create our chosen URL links for the page.
@app.route('/shelters')
def shelterList():
    """ Displays all shelters within a single summary page. """
    # Query all restaurants and place into a list with the id and name.
    shelters = session.query(Shelter).order_by('name')
    #shelter_list = []
    #for i in all_restaurants:
    #    shelter_list.append((str(i.name), i.id))
    # Return the HTML template for restaurant lists within the templates folder.
    return render_template('shelter_list.html', shelters=shelters)


@app.route('/restaurants/edit/<int:restaurant_id>/', methods=['GET', 'POST'])
def editShelter(shelter_id):
    """ A page to rename the chosen shelters name. """
    if request.method == 'POST':
        shelter = session.query(Shelter).filter_by(id=shelter_id).one()
        if shelter != []:
            shelter.name = request.form['changedShelterName']
            session.add(shelter)
            session.commit()
            print "%s successfully changed." % shelter.name
            flash("Shelter successfully renamed.")
            return redirect(url_for('shelterList'))
        else:
            print "The chosen item could not be modified as something went wrong."
            return
    else:
        shelter = session.query(Shelter).filter_by(id=shelter_id).one()
        return render_template('edit_shelter.html', shelter=shelter)


@app.route('/shelters/delete/<int:shelter_id>/', methods=['GET', 'POST'])
def deleteShelter(shelter_id):
    """ Provides a function to remove the selected shelter and puppies from the database. """
    if request.method == 'POST':
        shelter = session.query(Shelter).filter_by(id=shelter_id).one()
        if shelter != []:
            session.delete(shelter)
            session.commit()
            print "Shelter removed from the database."
            # Using the flash function, raise a message to display to the HTML template.
            flash("%s removed from website." % shelter.name)
            return redirect(url_for('shelterList'))
        else:
            print "Shelter was not found within the database."
            return redirect(url_for('shelterList'))
    else:
        shelter = session.query(Shelter).filter_by(id=shelter_id).one()
        return render_template('delete_shelter.html', shelter=shelter)


@app.route('/puppies/')
def puppyList():
    """ Provides a page to display all puppies in the database. """
    # All puppies to obtain name, id, DOB, address, city, state and website.
    puppies = session.query(Puppy).order_by('name')
    # Render the html template for puppy_list to display the required info.
    return render_template('puppy_list.html', puppies=puppies)


@app.route('/puppies/<int:puppy_id>/')
def puppyProfile(puppy_id):
    """ Displays a page dedicated to the chosen puppy. """
    #Query the chosen puppy with puppy id within the database.
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    # Query the puppy of the  obtained above.
    shelter = session.query(Shelter).filter_by(id = puppy.shelter_id).one()
    if puppy_shelter != []:
        return render_template('puppy_profile.html', puppy=puppy, shelter=shelter)
    else:
        return render_template('puppy_profile.html', puppy=puppy)


@app.route('/shelters/new/', methods=['GET', 'POST'])
def createShelter():
    """ Creates a new shelter at which puppies can be given a temporary home. """
    if request.method == 'POST':
        new_shelter = Shelter(name=request.form['newShelterName'],
            address=request.form['newShelterAddress'], city=request.form['newShelterCity'],
            state=request.form['newShelterState'], zipCode=request.form['newShelterZipcode'],
            website=request.form['newShelterWebsite'], 
            maximum_capacity=request.form['newShelterMax'])
        try:
            session.add(new_shelter)
            session.commit()
            print "Successfully created a new Shelter"
            flash("Successfully added %s to the our shelters!" % new_shelter.name)
            return redirect(url_for('shelterList'))
        except:
            print "The entry was no added to the database, an unexpected error occurred."
            flash("The shelter was no added to the database, an error occurred!")
            return redirect(url_for('shelterList'))
    else:
        return render_template('new_shelter.html')


@app.route('/shelters/<int:shelter_id>/')
def shelterPuppies(shelter_id):
    """ Displays details about the current puppies at the chosen shelter. """
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    shelter_pups = session.query(Puppy).filter_by(shelter_id=shelter_id).order_by('name')
    return render_template('shelter_puppies.html', shelter=shelter, shelter_pups=shelter_pups)

















