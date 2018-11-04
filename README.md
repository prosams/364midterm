# 364midterm
si 364 midterm project — Gas Station Locator

This app takes in a location and brand of gas and then looks up gas stations in that locale using the Google Places API. You have the option of just searching for gas stations in general by simply typing "gas station" and not specifying the company. You also have the option of leaving comments about any of the individual gas stations via a form that allows you to input the name of a gas station, it's rating out of 5 stars, and then any comments you might have.

There are three tables in the database: a table for locations (broader city), a table for the individual gas stations, and a table for user comments and opinions. There is a one to many relation between the locations table and the gas stations table, because one location can have many gas stations. However, any given individual gas station will only have one location.

#### view functions ####
- / the main page of the app. The main form where you can input the location/city you want to search for and either the brand of gas station or just "gas station"
- /results after you fill out the main form, you should be automatically redirected here. This page shows you the results of your search. (ie. 20 results max regarding what you searched for)
- /all_gas this page shows you all of the gas stations currently in the database right now.
- /all_loc shows you all of the locations in the database.
- /opinion is the page with a second form that allows the user to input any of their opinions.
- /opinionresults this page shows you the opinion that you have just inputted.
- /all_ops this page shows you all of the user opinions currently stored in the database. 
