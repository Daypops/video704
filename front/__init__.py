# front/init.py
from flask import Flask, render_template, jsonify, redirect, url_for, request, g, session
import json
import os
import sys
from http.client import HTTPConnection

sys.path.append('/app')
import db

def create_app(config=None):

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if config is not None:
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        error_message = request.args.get('error_message', '')
        return render_template('index.html', error_message=error_message)

    @app.route('/users')
    def get_users():
        dbf = db.get_db()
        users = dbf.execute('SELECT * FROM user').fetchall()
        return jsonify(users)
    
    @app.route('/add_movie', methods=['POST'])
    def add_movie():

        connection = HTTPConnection('api', 5000)

        data = request.get_json()

        connection.request('POST', "/add_movie", headers={"Content-type": "application/json"}, body=json.dumps(data))

        response = connection.getresponse()
        
        return response.read()
    
    @app.route('/ajouter')
    def ajouter():
        return render_template('ajouter.html')
    
    
    @app.route('/update_movie/<titre>', methods=['POST'])
    def update_movie(titre):

        connection = HTTPConnection('api', 5000)

        data = request.get_json()

        connection.request('POST', f"/update_movie/{titre}", headers={"Content-type": "application/json"}, body=json.dumps(data))

        response = connection.getresponse()
        
        return response.read()


    
    @app.route('/modifier/<titre>')
    def modifier_film(titre):
        # Connexion au service API
        connection = HTTPConnection('api', 5000)

        # Envoi de la requête GET pour récupérer les détails d'un film spécifique
        connection.request('GET', f"/get_movie/{titre}", headers={"Accept": "application/json"})

        # Obtention de la réponse
        response = connection.getresponse()

        # Vérification du code de statut
        if response.status == 200:
            # Si la réponse est réussie, lire le contenu et le décoder en JSON
            content = response.read().decode('utf-8')
            film = json.loads(content)  # Conversion du JSON en objet Python

            # Afficher la page de modification avec les informations du film
            return render_template('modifier.html', film=film)
        else:
            # Sinon, retourner un message d'erreur
            return jsonify({'error': 'Erreur lors de la récupération des détails du film'}), response.status

    
    @app.route('/voir')
    def voir():
        try:
            with open('data/movies.json', 'r') as file:
                movies = json.load(file)
        except FileNotFoundError:
            movies = []
        return render_template('voir.html', movies=movies)
    
    @app.route('/get_movies', methods=['GET'])
    def get_movies():
        # Connexion au service API
        connection = HTTPConnection('api', 5000)

        # Envoi de la requête GET pour récupérer les films
        connection.request('GET', "/get_movies", headers={"Accept": "application/json"})

        # Obtention de la réponse
        response = connection.getresponse()

        # Vérification du code de statut
        if response.status == 200:
            # Si la réponse est réussie, lire le contenu et le décoder en JSON
            content = response.read().decode('utf-8')
            return content, 200, {'Content-Type': 'application/json'}
        else:
            # Sinon, retourner un message d'erreur
            return jsonify({'error': 'Erreur lors de la récupération des films'}), response.status

    
    @app.route('/accueil')
    def accueil():
        try:
            with open('data/movies.json', 'r') as file:
                movies = json.load(file)
        except FileNotFoundError:
            movies = []

        return render_template('accueil.html', movies=movies)

    @app.route('/login', methods=['POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            dbf = db.get_db()
            user = dbf.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password)).fetchone()

            if user:
                session['user_id'] = user['id']
                return redirect(url_for('accueil'))
            else:
                error_message = "Identifiants invalides. Veuillez réessayer."
                return redirect(url_for('index', error_message=error_message))

    @app.route('/register', methods=['POST'])
    def register():
        if request.method == 'POST':
            new_username = request.form.get('newUsername')
            new_password = request.form.get('newPassword')

            dbf = db.get_db()
            dbf.execute('INSERT INTO user (username, password) VALUES (?, ?)', (new_username, new_password))
            dbf.commit()

            success_message = "Compte créé avec succès. Vous pouvez maintenant vous connecter."
            return redirect(url_for('index', error_message=success_message))
        
    db.init_app(app)

    return app

