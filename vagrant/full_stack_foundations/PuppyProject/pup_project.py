# This Python file makes use of Flask microframework and the database framework
# defined within database_setup.py, which makes use of SQLAlchemy with SQLite. 
# Setup initial flask imports and app definition.
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy, Adopter, Profile
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
@app.route('/')
@app.route('/shelters')
def shelterList():
    """ Displays all shelters within a single summary page. """
    # Query all restaurants and place into a list with the id and name.
    shelters = session.query(Shelter).order_by('name')
    # current occupancy must be worked out for each shelter by counting rows.
    for i in shelters:
        count_pups = session.query(func.count(Puppy.shelter_id)).filter_by(shelter_id=i.id).scalar()
        i.current_occupancy = int(count_pups)
        session.add(i)
        session.commit()
    #    shelter_list.append((str(i.name), i.id))
    # Return the HTML template for shelter lists within the templates folder.
    return render_template('shelter_list.html', shelters=shelters)


@app.route('/shelters/edit/<int:shelter_id>/', methods=['GET', 'POST'])
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
    # Obtain the puppy weight and round to 2 decimal places.
    pup_weight = round(puppy.weight, 2)
    if shelter != None:
        return render_template('puppy_profile.html', puppy=puppy, shelter=shelter, pup_weight=pup_weight)
    else:
        return render_template('puppy_profile.html', puppy=puppy, shelter=shelter, pup_weight=pup_weight)


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
            flash("The shelter was not added to the database, an error occurred!")
            return redirect(url_for('shelterList'))
    else:
        return render_template('new_shelter.html')


@app.route('/shelters/<int:shelter_id>/')
def shelterPuppies(shelter_id):
    """ Displays details about the current puppies at the chosen shelter. """
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    shelter_pups = session.query(Puppy).filter_by(shelter_id=shelter_id).order_by('name')
    return render_template('shelter_puppies.html', shelter=shelter, shelter_pups=shelter_pups)


@app.route('/shelters/<int:shelter_id>/addpuppy/', methods=['GET', 'POST'])
def checkInPuppy(shelter_id):
    """ Provides a page for checking a puppy into a chosen shelter using shelter_id. """
    shelter = session.query(Shelter).filter_by(id = shelter_id).one()
    if request.method == 'POST':
        input_puppy = request.form['checkInPuppyName']
        input_puppy_id = request.form['checkInPuppyId']
        puppy = session.query(Puppy).filter_by(id=input_puppy_id, name=input_puppy).one()
        if (shelter.current_occupancy >= shelter.maximum_capacity) and puppy != []:
            print "The current shelter is at maximum capacity, a new shelter must be made!"
            flash("The shelter %s is at maximum capacity. Please use a different shelter.")
            return redirect(url_for('shelterPuppies', shelter_id=shelter.id))
        else:
            puppy.shelter_id = shelter_id 
            session.add(puppy)
            session.commit()
            print "%s successfully checked into %s" % (puppy.name, shelter.name)
            flash("%s successfully added to %s" % (puppy.name, shelter.name))
            return redirect(url_for('shelterPuppies', shelter_id=shelter.id))
    else:
        return render_template('check_in_puppy.html', shelter=shelter)

@app.route('/puppies/<int:puppy_id>/adopt/', methods=['GET', 'POST'])
def adoptPuppyPage(puppy_id):
    """ Provides a page where adopters can adopt a puppy. """
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    if request.method == 'POST':
        try:
            # Change the adopter_puppy field of adopter to reflect the puppy.
            adopter_id = int(request.form['adopterIDField'])
            adopter = session.query(Adopter).filter_by(id=adopter_id).one()
            adopter.adopted_puppy = puppy.id
            session.add(adopter)
            # Change the shelter id of the puppy to None since it has a home.
            puppy.shelter_id = None
            session.add(puppy)
            session.commit()
            return redirect(url_for('puppyList'))
        except:
            print "The adoption process was unsuccessful."
            return redirect(url_for('puppyList'))
    else:
        return render_template('adopt_puppy.html', puppy=puppy)


def adoptPuppy(puppy_id, adopter_list):
    """ Takes in a chosen puppy id to adopt, along with a list of adopter id's
    who will take ownership of the seelcted puppy. On adoption, the puppy_id
    shall be removed from the shelter, but will remain on the website puppy list. 
    """
    if adopter_list != []:
        puppy = session.query(Puppy).filter_by(id=puppy_id).one()
        for i in adopter_list:
            try:
                adopter_id = int(i)
                adopter = session.query(Adopter).filter_by(id=adopter_id).one()
                adopter.adopted_puppy = puppy.id
                session.add(adopter)
                session.commit()
                print "%s added to adopter %s" % (puppy.name, adopter.name)
                return redirect(url_for('puppyList'))
            except ValueError:
                print "Object inside adopter list is Not a Number!"
                return redirect(url_for('puppyList'))
    else:
        print "The adopter list is empty."
        return redirect(url_for('puppyList'))


# The running variable made from the Python interpretter gets defined as __main__.
# This if statement makes sure the app is only run when executed by the python
# interpretter. If this file is imported from another python module, this code
# will not execute, but the rest of the file is still accesible. 
if __name__ == '__main__':
    # Create a secret key which flask uses for sessions.
    # This would normally be something very secure if the app is live.
    app.secret_key = 'random_super_key'
    # Enable debug support when running from the Python interpretter.
    # This lets the app reload itself each time it detects a code change - very useful.
    app.debug = True
    # Make the module publicly available since we're running it in Vagrant.
    app.run(host='0.0.0.0', port=5000)
