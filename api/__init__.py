# api/init.py
from flask import Flask, render_template, jsonify, request
import json
import os

def create_app():

    app = Flask(__name__)


    @app.route('/')
    def index():
        return "ok"

    @app.route('/add_movie', methods=['POST'])
    def add_movie():
        print("Received request to add movie")
        movie_data = request.get_json()

        try:
            with open('data/movies.json', 'r') as file:
                movies = json.load(file)
        except FileNotFoundError:
            movies = []

        movies.append(movie_data)

        with open('data/movies.json', 'w') as file:
            json.dump(movies, file, indent=2)

        return jsonify({'message': 'Film ajouté avec succès!'})

    @app.route('/get_movies')
    def get_movies():
        try:
            with open('data/movies.json', 'r') as file:
                movies = json.load(file)
        except FileNotFoundError:
            movies = []

        return jsonify(movies)
    
    @app.route('/get_movie/<titre>', methods=['GET'])
    def get_movie(titre):
        try:
            with open('data/movies.json', 'r') as file:
                movies = json.load(file)
        except FileNotFoundError:
            movies = []

        # Recherchez le film avec le titre dans la liste de films
        film = next((movie for movie in movies if movie['title'] == titre), None)

        if film:
            # Si le film est trouvé, retournez les informations du film en format JSON
            return jsonify(film)
        else:
            # Si le film n'est pas trouvé, retournez une réponse avec un code d'erreur (par exemple, 404 Not Found)
            return jsonify({'error': 'Film non trouvé'}), 404
        

    @app.route('/update_movie/<titre>', methods=['POST'])
    def update_movie(titre):
        # Récupérez les nouvelles données du film à partir de la requête JSON
        new_movie_data = request.get_json()

        try:
            # Chargez la liste actuelle des films
            with open('data/movies.json', 'r') as file:
                movies = json.load(file)
        except FileNotFoundError:
            # Si le fichier n'existe pas, initialisez la liste à vide
            movies = []

        # Recherchez le film à mettre à jour dans la liste
        for movie in movies:
            if movie['title'] == titre:
                # Mettez à jour les informations du film
                movie.update(new_movie_data)
                break

        # Sauvegardez la liste mise à jour dans le fichier
        with open('data/movies.json', 'w') as file:
            json.dump(movies, file, indent=2)

        # Réponse JSON indiquant que la mise à jour a réussi
        return jsonify({'success': True})


    return app
