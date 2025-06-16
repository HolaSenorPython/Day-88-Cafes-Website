from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, BooleanField, IntegerField
from wtforms.validators import DataRequired, URL

# Add Cafe Form!
class AddCafeForm(FlaskForm):
    cafe_name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = URLField("Cafe Map URL", validators=[DataRequired(), URL()])
    cafe_img_url = URLField("Cafe Image Url", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Has sockets? 🔌") # No data required on Boolean Fields: they can be left empty to indicate false
    has_toilet = BooleanField("Has toilets? 🚽")
    has_wifi = BooleanField("Has wifi? 🛜")
    can_take_calls = BooleanField("Can you take calls in cafe?")
    seats = StringField("How many seats? (optional)")
    coffee_price = StringField("Coffee price? 💵 (optional)")
    submit = SubmitField("Submit the Cafe! 😏")

# Delete cafe form
class DeleteCafeForm(FlaskForm):
    cafe_id = IntegerField("Enter the ID of the Cafe you would like to delete.")
    submit = SubmitField("Delete Cafe 🙂‍↔️🙅🏾‍♂️")