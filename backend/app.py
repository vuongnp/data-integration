from flask import Flask, request, Response, jsonify
from database.db import initialize_db
from database.general import General
from flask_cors import CORS
import pymongo
import os
from dotenv import load_dotenv

from statictic.getStatistic import countByYear, countByGenre

load_dotenv()

app = Flask(__name__)

# app.config['MONGODB_SETTINGS'] = {
#     'host': 'mongodb+srv://vuongnp:1234566@vuongcluster1.gl4g4.mongodb.net/film'
# }
app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv("MONGODB_URI")
}
client = pymongo.MongoClient(os.getenv("MONGODB_CLIENT"))
db = client.film

CORS(app)

initialize_db(app)

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
    movies = General.objects.search_text(text).order_by('$text_score')
    res = {'data': movies}
    return res

@app.route('/category', methods=['GET'])
def get_movies_by_catogory():
    text = request.args.get("text")
    movies=''
    if text=='imdb':
        movies = General.objects(rating__exists=True).order_by('-rating')
    else:
        movies = General.objects(genres__icontains=text).order_by('-rating')
    res = {'data': movies}
    return res

@app.route('/statistic', methods=['GET'])
def get_statistic():
    general = list(db.general.find({},{'_id':0}))
    label1,data1 = countByYear(general)
    label2,data2 = countByGenre(general)
    statisticYear={'labels':label1, 'data':data1}
    statisticGenres = {'labels':label2, 'data':data2}
    res = {'statisticYear': statisticYear, 'statisticGenres':statisticGenres}
    return res

@app.route('/stat', methods=['GET'])
def stat_movie():
    text = request.args.get("text")
    movies = Movie.objects.search_text(text).order_by('$text_score')
    return Response(movies.to_json(), mimetype="application/json", status=200)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
