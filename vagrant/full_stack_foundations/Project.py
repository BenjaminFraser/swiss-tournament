# This Python file makes use of Flask microframework and the database framework
# defined within database_setup.py, which makes use of SQLAlchemy with SQLite. 
# Setup initial flask imports and app definition.
from flask import Flask, render_template, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# Anytime we run an app in Python a special variable called __name__ is defined.
# 
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
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
@app.route('/restaurants')
def restaurantList():
    """ Displays all restaurant names within a single summary page. """
    # Query all restaurants and place into a list with the id and name.
    all_restaurants = session.query(Restaurant).order_by('name')
    restaurant_list = []
    for i in all_restaurants:
        restaurant_list.append((str(i.name), i.id))
    return render_template('restaurant_list.html', restaurant_list=restaurant_list)
    #output = ""
    #output += '<html><body><h1><u>Our restaurants!</u></h1>'
    # Create a view, edit and delete page, with URLs, for each restaurant.
    #for i in restaurant_list:
    #    output += '<h3><u>%s</u></h3>' % i[0]
    #    output += '<ul><li><a href="/restaurants/%s/">View menu</a></li>' % i[1]
    #    output += '<li><a href="/restaurants/%s/edit">Edit</a>' % i[1]
    #    output += '<li><a href="/restaurants/%s/delete">Delete</a></li></ul><br>' % i[1]
    #output += '<p>Cant find your restaurant? Add one <a href ="/restaurants/new">here.</a>'
    #output += '</body></html>'
    #return output

# Make a dynamic decorator which creates a page for the restaurant id.
@app.route('/restaurants/<int:restaurant_id>/')
# Create a restaurant menu dynamic page, listing that specific restaurant
# menu items, using the restaurant_id as the parameter. 
def restaurantMenu(restaurant_id):
    #Query the first restaurant within the database.
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # Query the menu items of the restaurant obtained above.
    menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('main_menu.html', restaurant=restaurant, menu_items=menu_items)
    # Main title name of the chosen restaurant, with menu items listed below.
    #output = ""
    #output += '<html><body><h1><strong><u>%s</u></strong></h1>' % restaurant.name
    #for i in menu_items:
    #    output += '<h3><strong><u>%s</u></strong></h3>' % i.name
    #    output += '<p><i>%s</i></p>' % i.price
    #    output += '<p><i>%s</i></p>' % i.description
    #    output += '<p><a href="/restaurants/%s/%s/edit/">Edit</a></p>' % (restaurant.id, i.id)
    #    output += '<p><a href="/restaurants/%s/%s/delete/">Delete</a></p><br>' % (restaurant.id, i.id)
    #output += '<p><i>Something extra to add to the existing menu? add it <a href ="/restaurants/%s/new/">here.</a></i></p><br>' % restaurant_id
    #output += '<p><i>Click <a href ="/restaurants">here.</a> to return to all restaurants.</i></p>'
    #output += '</body></html>'
    #return output

@app.route('/restaurants/new')
def newRestaurant():
    return render_template('new_restaurant.html')
    #output = ""
    #output += '<html><body><h1>Create a new restaurant</h1>'
    #output += '<form method = "POST" enctype = "multipart/form-data" action = "/restaurants/new">'
    #output += '<h2>New restaurant name:</h2>'
    #output += '<input type = "text" name = "newRestaurantEntry"><br>'
    #output += '<input type = "submit" value = "Create">'
    #output += '</body></html>'
    #return output

@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    output = ""
    output += '<html><body><h1><u>%s</u></h1>' % restaurant.name
    output += '<h2>Enter the details of the new menu item below.</h2><br>'
    output += '<form method = "POST" enctype = "multipart/form-data" action = "/restaurants/%s/new">' % restaurant_id
    output += '<h3>New menu item name:</h3>'
    output += '<input type = "text" name = "newMenuItemName"><br><br>'
    output += '<h3>New menu item description:</h3>'
    output += '<textarea cols="40" rows="5" name="newMenuItemDescription"></textarea><br><br>'
    output += '<input type = "submit" value = "Create Item!">'
    output += '<h5>Changed your mind? Click <a href="/restaurants/%s/">here</a> to return.</h5>' % restaurant.id
    output += '</body></html>'
    return output

@app.route('/restaurants/<int:restaurant_id>/<int:id>/edit/')
def editMenuItem(restaurant_id, id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=id).one()
    output = ""
    output += '<html><body><h1><u>%s</u></h1>' % restaurant.name
    output += '<h2><u>%s</u></h2><br>' % item.name
    output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/%s/edit/">' % (restaurant.id, item.id)
    output += '<h3>Enter a new name for the menu item below:</h3>'
    output += '<input type="text" name="changeMenuName"><br><br>'
    output += '<h3>Enter a new description for the menu item:</h3>'
    output += '<textarea cols="40" rows="5" name="changeMenuDescription"></textarea><br><br>'
    output += '<input type="submit" value="Change" placeholder="New Name"></form>'
    output += '<h5>Changed your mind? Click <a href="/restaurants/%s/">here</a> to return.</h5>' % restaurant.id
    output += '</body></html>'
    return output

@app.route('/restaurants/<int:restaurant_id>/<int:id>/delete/')
def deleteMenuItem(restaurant_id, id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=id).one()
    output = ""
    output += '<html><body><h1><u>%s</u></h1>' % restaurant.name
    output += '<html><body><h2><u>%s</u></h1>' % item.name
    output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/%s/%s/edit/"' % (restaurant.id, item.id)
    output += '<h3><i>Are you sure you want to delete the menu item listed above?</i></h3><br><br>'
    output += '<input type="submit" value="Delete"></form>'
    output += '<h5>Changed your mind? Click <a href="/restaurants/%s/">here</a> to return.</h5>' % restaurant.id
    output += '</body></html>'
    return output



# The running variable made from the Python interpretter gets defined as __main__.
# This if statement makes sure the app is only run when executed by the python
# interpretter. If this file is imported from another python module, this code
# will not execute, but the rest of the file is still accesible. 
if __name__ == '__main__':
    # Enable debug support when running from the Python interpretter.
    # This lets the app reload itself each time it detects a code change - very useful.
    app.debug = True
    # Make the module publicly available since we're running it in Vagrant.
    app.run(host='0.0.0.0', port=5000)