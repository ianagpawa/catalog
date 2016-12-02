from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Restaurant, MenuItem
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
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['delete_menu_item']:
            session.delete(item)
            session.commit()
            flash('A menu item was deleted!')
            redirect('showMenu', restaurant_id = restaurant_id)
    else:
        return render_template('deletemenuitem.html', item = item)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
