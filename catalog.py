from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Restaurant, MenuItem
#   imports for authentication
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Music Catalog Application'

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


def get_restaurant(restaurant_id):
    return session.query(Restaurant).filter_by(id = restaurant_id).one()


def add_to_db(obj):
    session.add(obj)
    session.commit()



@app.route("/restaurants/JSON/")
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants = [restaurant.serialize for restaurant in restaurants])


@app.route("/")
@app.route("/restaurants/")
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants = restaurants)


@app.route("/restaurant/new/", methods = ['GET', 'POST'])
def newRestaurant():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        restaurant_name = request.form['restaurant_name']
        newRestaurant = Restaurant(name = restaurant_name)
        add_to_db(newRestaurant)
        flash("New restaurant (%s) was created!" % restaurant_name)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template("newrestaurant.html")


@app.route("/restaurant/<int:restaurant_id>/edit/", methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = get_restaurant(restaurant_id)
    if request.method == 'POST':
        if request.form['edit_restaurant_name']:
            editted_name = request.form['edit_restaurant_name']
            restaurant.name = editted_name
            add_to_db(restaurant)
            flash('Restaurant name has been edited!')
            return redirect(url_for('showRestaurants'))
    else:
        return render_template("editrestaurant.html", restaurant = restaurant)



@app.route("/restaurant/<int:restaurant_id>/delete/",
            methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        if request.form['delete_restaurant']:
            session.delete(restaurant)
            session.commit()
            flash('Restaurant has been deleted!')
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant = restaurant)



@app.route("/restaurant/<int:restaurant_id>/menu/JSON")
def showMenuJSON(restaurant_id):
    restaurant = get_restaurant(restaurant_id)
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return jsonify(MenuItems=[item.serialize for item in items])

@app.route("/restaurant/<int:restaurant_id>/")
@app.route("/restaurant/<int:restaurant_id>/menu/")
def showMenu(restaurant_id):
    restaurant = get_restaurant(restaurant_id)
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)



@app.route("/restaurant/<int:restaurant_id>/menu/new/",
            methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = get_restaurant(restaurant_id)
    if request.method == "POST":
        if request.form['item_name'] and request.form['item_price'] and request.form['item_description']:
            item_name = request.form['item_name']
            item_price = request.form['item_price']
            item_description = request.form['item_description']
            newItem = MenuItem( name = item_name,
                                price = item_price,
                                description = item_description,
                                restaurant_id = restaurant_id)
            add_to_db(newItem)
            flash('A new menu item was created for %s' % restaurant.name)
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/JSON/')
def showMenuItemJSON(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id = item_id).one()
    return jsonify(MenuItems = item.serialize)

@app.route("/restaurant/<int:restaurant_id>/menu/<int:item_id>/edit/",
            methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = get_restaurant(restaurant_id)
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == "POST":
        if request.form['edit_item_name']:
            editted_item_name = request.form['edit_item_name']
            item.name = editted_item_name
        if request.form['edit_item_price']:
            editted_item_price = request.form['edit_item_price']
            item.price = editted_item_price
        if request.form['edit_item_description']:
            editted_item_description = request.form['edit_item_description']
            item.description = editted_item_description
        add_to_db(item)
        flash("Menu item (%s) was edited!" % item.name)
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant = restaurant,
                            item = item)



@app.route("/restaurant/<int:restaurant_id>/menu/<int:item_id>/delete/",
            methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['delete_menu_item']:
            session.delete(item)
            session.commit()
            flash('A menu item was deleted!')
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', item = item)



@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html", STATE = state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
	del login_session['access_token']
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    else:

    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
