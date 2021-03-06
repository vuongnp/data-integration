from flask import Flask, request, Response, jsonify
from database.db import initialize_db
from database.general import General
from flask_cors import CORS
import pymongo
import os
from dotenv import load_dotenv
import numpy as np
import json

from statictic.getStatistic import countByYear, countByGenre, avgRating, results

load_dotenv()

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv("MONGODB_URI")
}
client = pymongo.MongoClient(os.getenv("MONGODB_CLIENT"))
db = client.film

CORS(app)

initialize_db(app)

# model = pickle.load(open('./models/KMeans.pkl', 'rb'))

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to data intergration server !!</h1>"

@app.route('/movies', methods=['GET'])
def get_movies():
    page = request.args.get("page")
    limit = request.args.get("limit")

    movies = General.objects()
    if page:
        start = int(limit)*(int(page)-1)
        end = start+int(limit)
        movies = movies[start:end]  
    res = {'data': movies}
    return res

@app.route('/search', methods=['GET'])
def search_movies():
    text = request.args.get("text")
    page = request.args.get("page")
    limit = request.args.get("limit")
    movies = General.objects.search_text(text).order_by('$text_score')
    length=len(movies)
    if page:
        start = int(limit)*(int(page)-1)
        end = start+int(limit)
        movies = movies[start:end]
    res = {'data': movies,'length':length}
    return res

@app.route('/category', methods=['GET'])
def get_movies_by_catogory():
    text = request.args.get("text")
    page = request.args.get("page")
    limit = request.args.get("limit")
    movies=''
    if text=='imdb':
        movies = General.objects(rating__exists=True).order_by('-rating')[:100]
    else:
        movies = General.objects(genres__icontains=text).order_by('-rating')
    length=len(movies)
    if page:
        start = int(limit)*(int(page)-1)
        end = start+int(limit)
        movies = movies[start:end]
    res = {'data': movies,'length':length}
    return res

@app.route('/statistic', methods=['GET'])
def get_statistic():
    general = list(db.general.find({},{'_id':0}))
    label1,data1 = countByYear(general)
    label2,count,label3,avg,label4,countSources = results(general)
    # label2,data2 = countByGenre(general)
    statisticYear={'labels':label1, 'data':data1}
    statisticGenres = {'labels':label2, 'data':count}
    statisticAvgRating = {'labels':label3, 'data':avg}
    statisticNumUrls = {'labels':label4, 'data':countSources}
    # statisticGenres = {'labels':label2, 'data':data2}
    res = {'statisticYear': statisticYear, 'statisticGenres':statisticGenres, 'statisticAvgRating':statisticAvgRating, 'statisticNumUrls':statisticNumUrls}
    return res

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
