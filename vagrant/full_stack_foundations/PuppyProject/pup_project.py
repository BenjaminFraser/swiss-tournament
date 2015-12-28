# This Python file makes use of Flask microframework and the database framework
# defined within database_setup.py, which makes use of SQLAlchemy with SQLite. 
# Setup initial flask imports and app definition.
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy, Adopter, Profile
# Import form templates for WTForms template classes.
from form_templates import *
# Import logging module to allow information logging to a file.
import logging 

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

# Setup logging to a file to store info from last app run only.
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)


# Setup route decorators to create our chosen URL links for the page.
@app.route('/')
def puppyHavenIntro():
    """ Loads the main intro landing page for Puppy Haven. """
    return render_template('puppy_haven_intro.html')


@app.route('/shelters/')
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
    form = CreateShelterForm(request.form)
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    if request.method == 'POST' and form.validate():
        if shelter != []:
            shelter.name = form.name.data
            shelter.address = form.address.data
            shelter.city = form.state.data
            shelter.state = form.state.data
            shelter.zipCode = form.state.data
            shelter.website = form.website.data
            shelter.maximum_capacity = form.maximum_capacity.data
            session.add(shelter)
            session.commit()
            print "%s successfully changed." % shelter.name
            flash("Shelter successfully renamed.")
            return redirect(url_for('shelterList'))
        else:
            print "The chosen item could not be modified as something went wrong."
            return
    else:
        return render_template('edit_shelter.html', shelter=shelter, form=form)


@app.route('/shelters/delete/<int:shelter_id>/', methods=['GET', 'POST'])
def deleteShelter(shelter_id):
    """ Provides a function to remove the selected shelter and puppies from the database. """
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    if request.method == 'POST':
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


@app.route('/puppies/<int:puppy_id>/edit/', methods=['GET', 'POST'])
def editPuppy(puppy_id):
    """ Page to allow editting of puppy details. """
    # Create a variable form, an instance of WTForms CreatePuppyForm object.
    form = CreatePuppyForm(request.form)
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    if request.method == 'POST' and form.validate():
        if puppy != []:
            puppy.name = form.name.data
            puppy.gender = form.gender.data
            puppy.dateOfBirth = form.birthday.data
            puppy.shelter_id = form.shelter_id.data
            puppy.weight = form.weight.data
            try:
                session.add(puppy)
                session.commit()
                print "%s successfully changed." % puppy.name
                flash("%s successfully renamed." % puppy.name)
                return redirect(url_for('puppyList'))
            except:
                print "The entry was not added to the database, an unexpected error occurred."
                flash("The Puppy was not modified, an error occurred!")
                return redirect(url_for('puppyList'))
        else:
            print "The chosen puppy could not be modified as something went wrong."
            return redirect(url_for('puppyList'))
    else:
        return render_template('edit_puppy.html', puppy=puppy, form=form)


@app.route('/puppies/<int:puppy_id>/delete/', methods=['GET', 'POST'])
def deletePuppy(puppy_id):
    """ Permanently delete a puppy from the database. """
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    if request.method == 'POST':
        if puppy != []:
            session.delete(puppy)
            session.commit()
            print "%s removed from the database." % puppy.name
            # Using the flash function, raise a message to display to the HTML template.
            flash("%s removed from website." % puppy.name)
            return redirect(url_for('puppyList'))
        else:
            print "Puppy was not found within the database."
            return redirect(url_for('puppyList'))
    else:
        return render_template('delete_puppy.html', puppy=puppy)


@app.route('/puppies/new/', methods=['GET', 'POST'])
def createPuppy():
    """ Creates a new puppy entry and adds it to the database. """
    form = CreatePuppyForm(request.form)
    if request.method == 'POST' and form.validate():
        new_puppy = Puppy(name=form.name.data,
            gender=form.gender.data, dateOfBirth=form.birthday.data,
            shelter_id=form.shelter_id.data, weight=form.weight.data)
        try:
            session.add(new_puppy)
            session.commit()
            print "Successfully created a new Puppy"
            flash("Successfully added %s to the our website!" % new_puppy.name)
            return redirect(url_for('puppyList'))
        except:
            print "The entry was no added to the database, an unexpected error occurred."
            flash("The puppy was not added to the database, an error occurred!")
            return redirect(url_for('puppyList'))
    else:
        return render_template('new_puppy.html', form=form)


@app.route('/shelters/new/', methods=['GET', 'POST'])
def createShelter():
    """ Creates a new shelter at which puppies can be given a temporary home. """
    form = CreateShelterForm(request.form)
    if request.method == 'POST' and form.validate():
        new_shelter = Shelter(name=form.name.data, address=form.address.data,
            city=form.city.data, state=form.state.data, zipCode=form.zipCode.data,
            website=form.website.data, maximum_capacity=form.maximum_capacity.data)
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
        return render_template('new_shelter.html', form=form)


@app.route('/shelters/<int:shelter_id>/')
def shelterPuppies(shelter_id):
    """ Displays details about the current puppies at the chosen shelter. """
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    shelter_pups = session.query(Puppy).filter_by(shelter_id=shelter_id).order_by('name')
    return render_template('shelter_puppies.html', shelter=shelter, shelter_pups=shelter_pups)


@app.route('/shelters/<int:shelter_id>/addpuppy/', methods=['GET', 'POST'])
def checkInPuppy(shelter_id):
    """ Provides a page for checking a puppy into a chosen shelter using shelter_id. """
    form = CheckInPuppyForm(request.form)
    shelter = session.query(Shelter).filter_by(id = shelter_id).one()
    if request.method == 'POST' and form.validate():
        input_puppy = form.name.data
        input_puppy_id = form.puppy_id.data
        try:
            puppy = session.query(Puppy).filter_by(id=input_puppy_id, name=input_puppy).one()
            if (shelter.current_occupancy >= shelter.maximum_capacity) and puppy != []:
                print "The current shelter is at maximum capacity, a new shelter must be made!"
                flash("The shelter %s is at maximum capacity. Please use a different shelter." % shelter.name)
                return redirect(url_for('shelterPuppies', shelter_id=shelter.id))
            else:
                puppy.shelter_id = shelter_id 
                session.add(puppy)
                session.commit()
                print "%s successfully checked into %s" % (puppy.name, shelter.name)
                flash("%s successfully added to %s" % (puppy.name, shelter.name))
                return redirect(url_for('shelterPuppies', shelter_id=shelter.id))
        except:
            print "The input puppy id and name was not found in the database."
            flash("The input puppy id and name was not found, please try again.")
            return redirect(url_for('shelterPuppies', shelter_id=shelter.id))

    else:
        return render_template('check_in_puppy.html', shelter=shelter, form=form)

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
