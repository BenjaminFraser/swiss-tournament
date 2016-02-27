from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import os
from werkzeug import secure_filename
from thegoodybasket import app

# setup upload directory for file-upload functionality.
app.config['UPLOAD_FOLDER'] = 'thegoodybasket/static/item_images/'

# Setup acceptable extensions for uploading files.
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Connect to Database and create database session
engine = create_engine('sqlite:///thegoodybasket.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# For a given upload file, return whether it is an acceptable type.
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Handle a user uploaded file.
@app.route('/upload', methods=["GET","POST"])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Fetch item_id of upload and fetch from DB. 
    category_item_id = request.form['category_item']
    fetched_item = session.query(CategoryItem).filter_by(id=category_item_id).one()
    if fetched_item != None:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Add the filename to the database item object picture field
            fetched_item.picture = filename
            category = fetched_item.category_id
            print "Added picture %s to database" % filename
            session.add(fetched_item)
            session.commit()
            flash('Image successfully updated!')
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
            return redirect(url_for('categoryItems',
                                    category_id=category))

# Create route for home page of the app.
@app.route('/')
@app.route('/home')
def introPage():
    """ Renders the main intro/home page for the goody basket. """
    return render_template('intro.html')

# Show all categories
@app.route('/category/')
def showCategories():
    """ Render the main category listings page."""
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return render_template('categories.html', categories=categories)
    else:
        return render_template('categories.html', categories=categories)

# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    """ Create a new category for the app, provided the user is logged in."""
    # redirect to login page if the user is not currently logged in.
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        # Create the new category and add the user id as the owner.
        newCategory = Category(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')

# Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    """ Allow the creator user to edit the category name."""
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    # Only allow a logged in user with the correct user id to edit.
    if 'username' not in login_session:
        return redirect('/login')
    if editedCategory.user_id != login_session['user_id']:
        flash('You are not authorized to edit this category. Only the category creator may edit.')
        return redirect(url_for('categoryItems', category_id=category_id))
    if request.method == 'POST':
        # Remove and return the csrf token, and compare with form csrf token.
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)


# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    """ Delete a category, along with its associated items. """
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    itemsToDelete = session.query(
        CategoryItem).filter_by(category_id=category_id).all()
    # Only allow the original creator user id to delete the category.
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        flash('You are not authorized to delete this category. Only creators of the category may delete.')
        return redirect(url_for('categoryItems', category_id=category_id))
    if request.method == 'POST':
        # Remove and return the csrf token, and compare with form csrf token.
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)
        session.delete(categoryToDelete)
        # Delete all associated items.
        for item in itemsToDelete:
            session.delete(item)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)


# Show a categories item list
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def categoryItems(category_id):
    """ Render a listing page of the selected categories items."""
    category = session.query(Category).filter_by(id=category_id).one()
    creator = session.query(User).filter_by(id=category.user_id).one()
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('categoryItems.html', items=items, category=category, creator=creator)
    else:
        return render_template('categoryItems.html', items=items, category=category, creator=creator)


# Create a new category item
@app.route('/category/<int:category_id>/items/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    """ Allow the category creator to create a new item. """
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    # Prevent non-creator users adding new items.
    if login_session['user_id'] != category.user_id:
        flash('You are not authorized to add category items to this category. Please create your own category in order to add items.')
        return redirect(url_for('categoryItems', category_id=category_id))
    if request.method == 'POST':
        newItem = CategoryItem(name=request.form['name'], description=request.form['description'], price=request.form[
                           'price'], category_id=category_id, user_id=category.user_id)
        session.add(newItem)
        # Flush and obtain default created item id.
        session.flush()
        createdItemID = newItem.id
        flash('New Category %s Item Successfully Created' % (newItem.name))
        # If upload selected, proceed to upload photo page for item.
        if request.form['button'] == 'upload-image':
            return redirect(url_for('editCategoryItemImage', category_id=category.id, item_id=createdItemID))
        # Otherwise create item without image and return to category items page.
        else:
            return redirect(url_for('categoryItems', category_id=category_id))
    else:
        return render_template('newCategoryItem.html', category=category)

# Edit a category item
@app.route('/category/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    """ Allow the creator to edit the basic item details. """
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    # Only allow creator id to edit items.
    if login_session['user_id'] != category.user_id:
        flash('You are not authorized to edit category items in this category. Please create your own category in order to add items.')
        return redirect(url_for('categoryItems', category_id=category_id))
    if request.method == 'POST':
        # If any of the fields were changed, update them accordingly.
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('Category Item Successfully Edited')
        return redirect(url_for('categoryItems', category_id=category_id))
    else:
        return render_template('editCategoryItem.html', category=category, item_id=item_id, item=editedItem)

# Edit a category item image
@app.route('/category/<int:category_id>/items/<int:item_id>/edit/img', methods=['GET', 'POST'])
def editCategoryItemImage(category_id, item_id):
    """ Allows a user to upload a new image, or edit an existing one. """
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        flash('You are not authorized to edit items from this category. '
                'Only category creators may do so.')
        return redirect(url_for('categoryItems', category_id=category_id))
    return render_template('editItemPhoto.html', category=category, 
                item_id=item_id, item=editedItem)

# Delete a category item
@app.route('/category/<int:category_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    """ Allow a creator user to delete the selected item. """
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()
    if login_session['user_id'] != category.user_id:
        flash('You are not authorized to delete items from this category. You must be the category creator to do so.')
        return redirect(url_for('categoryItems', category_id=category_id))
    if request.method == 'POST':
        token = login_session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)
        session.delete(itemToDelete)
        session.commit()
        flash('Category Item Successfully Deleted')
        return redirect(url_for('categoryItems', category_id=category_id))
    else:
        return render_template('deleteCategoryItem.html', item=itemToDelete, category=category)

# Create a user account page to display basic user info.
@app.route('/users/account/', methods=['GET', 'POST'])
def accountInfo():
    if 'username' not in login_session:
        return redirect('/login')
    user = session.query(User).filter_by(id=login_session['user_id']).one()
    if user != None:
        return render_template('userAccountPage.html', user=user)
    else:
        flash('You must be logged in to view account information.')
        return redirect('/categories')
