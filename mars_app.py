from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_scrape = mongo.db.mars_scrape.find_one()
    return render_template("index.html", mars_scrape=mars_scrape)

@app.route("/scrape")
def scraper():
    mars_scrape = mongo.db.mars_scrape
    mars_data = scrape_mars.scrape()
    mars_scrape = mars_data.scrape_mars()

    # mars_scrape = {
    #         "News_Title": mars_scrape["news_title"],
    #         "News_Paragraph": mars_scrape["news_p"],
    #         "Featured_Image": mars_scrape["featured_image_url"],
    #         "Mars_Weather": mars_scrape["mars_weather"],
    #         "Mars_Table": mars_scrape["mars_table_html"],
    #         "Hemisphere_Data": mars_scrape["hemisphere_data"]
    #     }

    mars_scrape.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
