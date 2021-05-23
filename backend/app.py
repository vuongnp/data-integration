from flask import Flask, request, Response, jsonify
from database.db import initialize_db
from database.general import General
from flask_cors import CORS
import json

app = Flask(__name__)

# app.config['MONGODB_SETTINGS'] = {
#     'host': 'mongodb+srv://vuongnp:1234566@vuongcluster1.gl4g4.mongodb.net/film'
# }
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://hoangcongtue99:hoangcongtue99@cluster0.etpgx.mongodb.net/film'
}

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
    return Response(movies.to_json(), mimetype="application/json", status=200)

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

# @app.route('/home', methods=['GET'])
# def get_home():
#     imdb = Movie.objects(imdb__exists=True).order_by('-imdb')[:30]
#     action = Movie.objects(genres__icontains='action').order_by('-imdb')[:30]
#     animation = Movie.objects(genres__icontains='animation').order_by('-imdb')[:30]
#     kid = Movie.objects(genres__icontains='kid').order_by('-imdb')[:30]
#     movies = (imdb.to_json(),action.to_json(),animation.to_json(),kid.to_json())
#     # print(movies.to_json())
#     res = Response(movies, mimetype="application/json", status=200)
#     return res


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
