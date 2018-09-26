# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_marsdata
from pymongo import MongoClient

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)
# db = client.mars

app.config['MONGO_URI']= "mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)



# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():

    # Find data
    mars_info = mongo.db.mars.find({})

    # return template and data
    return render_template("index.html", mars_info=mars_info)


# Route that will trigger scrape functions
@app.route("/scrape")
def Scrape():

    # Run scraped functions
    # mars_info = db.mars
    mars_data= scrape_marsdata.Scrape()
    # mars_info.update(
        # {},
        # mars_data,
        # upsert=True
    #)

    mars_info={
        "title":mars_data["news_title"],
        "paragraph":mars_data["news_p"],
        "feature_img_url":mars_data["feature_img_url"],
        "weather":mars_data["mars_weather"],
        "facts":mars_data["mars_facts"],
        "hemisphere_imgs":mars_data["hemisphere_imgs"],

    }

    # Insert forecast into database
    mongo.db.mars.insert_one(mars_info)

    #redirect back to home page
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
