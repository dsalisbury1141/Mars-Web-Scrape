

from flask import Flask, render_template, redirect,jsonify
from flask_pymongo import PyMongo
import scrape_mars

import time

#creating an instance
app = Flask(__name__)
#using Pymongo to connect
mongo = PyMongo(app, uri = "mongodb://localhost:27017/app")
mongo.db.collection.drop()
#app.static_folder = 'static'

#Adding route to render index using mongo db
@app.route("/")
def home():

    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars = mars_data)

@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)