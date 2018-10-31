
# Sam Lu SI 364
# I referenced code from HW 3 for this
# also code from the WTForms example with itunes
# https://www.pythonsheets.com/notes/python-sqlalchemy.html

###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
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
    lat = db.Column(db.Integer)
    long = db.Column(db.Integer)
    locationid = (db.Integer, db.ForeignKey('locations.locationid'))

    def __repr__(self):
        return "{} at {} (Gas station ID: {})".format(self.gasname, self.road, self.gasid)

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

    def validate_type(form, field): # TODO 364: Set up custom validation for this form
        displaydata = field.data
        if "gas station" not in displaydata:
            raise ValidationError("You must have 'gas station' within your second input!")

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

@app.route('/')
def index():
    form = PlaceForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET

    # if form.validate_on_submit():
    #     url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    #     key = "AIzaSyCWhfoQXqSoKBkK0kjnrE3N0tSwVe10pWw"
    #     location = form.location.data
    #     specifics = form.type.data
    #     searchstring = specifics + " " + location #this combines the two inputs into a searchable string that will be used in the api call
    #     request = requests.get(url, params = {"query":searchstring, "key":key})
    #     result = request.json()
    #
    #     for x in result["results"]:
    #         locationdict = x["geometry"]["location"]
    #         locstring = str(locationdict["lat"]) + "," + str(locationdict["lng"])
    #         lat = locationdict["lat"]           #lat of gas station
    #         long = locationdict["lng"]          #longitude of gas station
    #         name = x["name"]                    # name of the gas station
    #         address = x["formatted_address"]
    #         splitad = address.split(",")        # this is just for getting individual bits
    #         road = splitad[0]                   # road address of gas station
    #         city = splitad[1]                   #city of gas station - to go into the Locations table
    #         state = splitad[2].split()[0]       #state of gas station - to go in locations table
    #
    #         newloc = Locations(city = city, state = state)
    #         newgas = Gassy(gasname = name, road = road, lat = lat, long = long)
    #
    #         db.session.add(newloc)
    #         db.session.add(newgas)
    #         db.session.commit()

        # return redirect(url_for(''))
    return render_template('index.html',form=form)

@app.route('/results', methods=['GET', 'POST'])
def results(): # all the results (after calls made to google place api, this should be what shows up)
    form = PlaceForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        biglist = [] # this is the final list that will be iterated through to return the results from the search
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        key = "AIzaSyCWhfoQXqSoKBkK0kjnrE3N0tSwVe10pWw"
        params = {}

        location = form.location.data
        specifics = form.type.data
        searchstring = specifics + " " + location
        params["query"] = searchstring
        params["key"] = key
        response = requests.get(url, params)
        result = response.json()

        for x in result["results"]:
            locationdict = x["geometry"]["location"]
            locstring = str(locationdict["lat"]) + "," + str(locationdict["lng"])
            lat = locationdict["lat"]           #lat of gas station
            long = locationdict["lng"]          #longitude of gas station
            name = x["name"]                    # name of the gas station
            address = x["formatted_address"]
            splitad = address.split(",")        # this is just for getting individual bits
            road = splitad[0]                   # road address of gas station
            city = splitad[1]                   #city of gas station - to go into the Locations table
            state = splitad[2].split()[0]       #state of gas station - to go in locations table

            newloc = Locations(city = city, state = state)
            newgas = Gassy(gasname = name, road = road, lat = lat, long = long)
            db.session.add(newloc)
            db.session.add(newgas)
            db.session.commit()
            biglist.append((name, road, city, state)) # appends a tuple with information about each of the individual gas stations to the final list of tuples

        return render_template('results.html', finaltuplist = biglist)
    flash('All fields are required!')
    return redirect(url_for('index'))

@app.route('/all_gas')
def all_gas():
    stats = Gassy.query.all()
    return render_template('stations.html', stations=stats)

@app.route('/all_loc')
def all_loc():
    locs = Locations.query.all()
    return render_template('searchedlocations.html', locations=locs)

# @app.route('/searches') # this app route returns a list of everything that the user has inputted into the form basically
# def all_loc():
#     locs = Locations.query.all()
#     return render_template('searchedlocations.html', locations=locs)

if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual
