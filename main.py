# All the imports
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from forms import AddCafeForm, DeleteCafeForm
import os
from dotenv import load_dotenv

load_dotenv() # Load the env variables

# Define base class
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY") # Get flask key
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///cafes.db")
db.init_app(app) # Initialize app with database
bootstrap = Bootstrap5(app) # Get bootstrap

# Configure tables for the DB
class Cafe(db.Model):
    __tablename__ = "cafe"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250))
    coffee_price: Mapped[str] = mapped_column(String(250))

# Setup routes and everything
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cafes')
def cafes():
    the_cafes = Cafe.query.all()
    column_titles = Cafe.__table__.columns.keys()
    clean_titles = []
    # Clean up the titles for aesthetic
    for title in column_titles:
        clean_title = title.replace("_", " ").title()
        clean_titles.append(clean_title)
    return render_template('cafes.html', cafes=the_cafes, titles=clean_titles)

@app.route('/add-cafe', methods=['GET', 'POST'])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit(): # If a POST request is made
        cafe_name = form.cafe_name.data
        map_url = form.map_url.data
        img_url = form.cafe_img_url.data
        location = form.location.data
        has_sockets = form.has_sockets.data
        has_toilet = form.has_toilet.data
        has_wifi = form.has_wifi.data
        can_take_calls = form.can_take_calls.data
        seats = form.seats.data
        coffee_price = form.coffee_price.data
        # Make the cafe object with the user's stuff
        new_cafe = Cafe(
            name=cafe_name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            has_sockets=has_sockets,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            can_take_calls=can_take_calls,
            seats=seats,
            coffee_price=coffee_price,
        )
        db.session.add(new_cafe)
        db.session.commit() # Commit the added cafe change
        flash(f"Successfully added new cafe with name: {cafe_name}!", 'success')
        return redirect(url_for('cafes'))
    else:
        if request.method == 'POST': # If they hit submit but something is bad
            flash("Something went wrong with your submission.", 'danger')
            return redirect(url_for('cafes'))

    return render_template('add.html', form=form)

@app.route('/delete-cafe', methods=['GET', 'POST'])
def delete_cafe():
    del_form = DeleteCafeForm()
    if del_form.validate_on_submit(): # If a POST request is made
        id_to_search = del_form.cafe_id.data
        target_cafe = db.get_or_404(Cafe, id_to_search) # Get the cafe with this id or error
        target_cafe_name = target_cafe.name
        db.session.delete(target_cafe)
        db.session.commit() # commit this change
        flash(f"Successfully deleted cafe {target_cafe_name} with id {id_to_search}", 'success')
        return redirect(url_for('cafes'))
    else:
        if request.method == 'POST': # If they hit submit but something is bad
            flash("Failed to delete the cafe with that ID.", 'danger')
            return redirect(url_for('cafes'))

    return render_template('delete.html', form=del_form)

if __name__ == "__main__":
    app.run(debug=True)