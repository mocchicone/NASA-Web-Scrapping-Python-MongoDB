from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars2

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data2=mars_data)


@app.route("/scrape")
def scraper():
    
    mars_data2 = scrape_mars2.scrape()
    mongo.db.collection.update({}, mars_data2, upsert=True)
    
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)