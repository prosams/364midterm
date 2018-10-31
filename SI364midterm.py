
# Sam Lu SI 364
# I referenced code from HW 3 for this

###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError# Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length# Here, too
from flask_sqlalchemy import SQLAlchemy
import requests
import json

## App setup code
app = Flask(__name__)
app.debug = True

## All app.config values
app.config['SECRET_KEY'] = 'hard to guess string from si364'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/midterm"
## Provided:
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)

######################################
######## HELPER FXNS (If any) ########
######################################

##################
##### MODELS #####
##################

class Locations(db.Model):
    __tablename__ = "locations"
    locationid = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))

    def __repr__(self):
        return "{}, {} (ID: {})".format(self.city, self.state, self.locationid)

class Gassy(db.Model):
    __tablename__ = "gasstations"
    gasid = db.Column(db.Integer, primary_key=True)
    gasname = db.Column(db.String(64)) #name of the gas station
    road = db.Column(db.String(64))
    locationid = (db.Integer, db.ForeignKey('locations.locationid'))

    def __repr__(self):
        return "{}, {} (ID: {})".format(self.gasname, self.road, self.locationid)

###################
###### FORMS ######
###################

class PlaceForm(FlaskForm):
    location = StringField("Please enter the place you want to search for — ideally, city. ", validators=[Required(), Length(min=0,  max=64)])
    type = StringField("Please enter the brand you want to look up followed by 'gas station' (ie. Shell gas station or just 'gas station' if brand doesn't matter)", validators=[Required(), Length(min=0,  max=64)])
    submit = SubmitField("Submit")

    def validate_name(form, field): # TODO 364: Set up custom validation for this form
        displaydata = field.data
        splitcheck = displaydata.split(" ")
        if len(splitcheck) >  5: #your name of the location cannot exceed 5 words! ! !
            raise ValidationError("The name of your location cannot exceed 5 words.")

## Error handling routes - THIS IS COPIED FROM HOMEWORK 3
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


#######################
###### VIEW FXNS ######
#######################

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PlaceForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if form.validate_on_submit():
        name = form.name.data
        newname = Name(name)
        db.session.add(newname)
        db.session.commit()
        return redirect(url_for('all_names'))
    return render_template('base.html',form=form)

@app.route('/all_searched_gas')
def all_searched_gas():
    stats = Gassy.query.all()
    return render_template('stations.html', stations=stats)

@app.route('/all_searched_loc')
def all_searched_loc():
    locs = Locations.query.all()
    return render_template('searchedlocations.html', locations=locs)

@app.route('/results')
def results(): # all the results (after calls made to google place api)
    return render_template('searchedlocations.html', locations=locs)

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!

if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual
