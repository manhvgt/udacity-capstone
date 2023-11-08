## Imports
import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from dotenv import find_dotenv, dotenv_values
import json

from .database.models import setup_db, Movie, Actor, db
from .auth.auth import requires_auth


## Loading environement variable
ENV_FILE = find_dotenv(raise_error_if_not_found = True)
if ENV_FILE:
    env = dotenv_values(ENV_FILE)

debug_mode = os.getenv('DEBUG_MODE')

#----------------------------------------------------------------------------#
# Create app and config
#----------------------------------------------------------------------------#
app = Flask(__name__)
# Setup db
with app.app_context():
    setup_db(app, debug_mode)

# Set up CORS. Allow '*' for origins.
CORS(app, resources={r"/*": {"origins": "*"}})

# Use the after_request decorator to set Access-Control-Allow
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers'\
        , 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods'\
        , 'GET,POST,DELETE,PATCH,OPTIONS')
    return response

#----------------------------------------------------------------------------#
# General
#----------------------------------------------------------------------------#
## print debug
def print_debug(str):
    debug_mode = os.getenv('DEBUG_MODE')
    if not debug_mode:
        print(str)

# index
@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    return jsonify({
        "success": True,
        "message": "working"
    })


#----------------------------------------------------------------------------#
# Endpoints for Movies.
#----------------------------------------------------------------------------#
# Get all movies in short form
@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    try:
        # DB query
        movies = Movie.query.all()

        if not movies:
            abort(404)

        movies_list = [movie.format_short() for movie in movies]

        # Result
        return jsonify({
            'success': True,
            'movies': movies_list
        })

    except Exception as e:
        print_debug(e)
        abort(500)


# Get movies details (including involved actor) by movie_id
@app.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movie-details')
def get_movie_details(payload, movie_id):
    try:
        # Query the movie by movie_id
        movie = Movie.query.get(movie_id)

        # not found
        if movie is None:
            abort(404)

        # Get actor IDs from the movie's actor_ids attribute
        actor_ids = movie.actor_ids
        actors = []
        if actor_ids:
            # Query 
            actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()
        # Format acor inftormation
        actors = [actor.format_short() for actor in actors]

        # Format movie and actor information
        movie_details = movie.format_details()

        return jsonify({
            'success': True,
            'movie_details': movie_details,
            'actors_involvement': actors
        })
    
    except Exception as e:
        print_debug(e)
        abort(500)


# Create a new movie and return result with movie details
@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):
    try:
        # Get data from the request JSON
        data = request.get_json()
        title = data.get('title')
        release_date = data.get('release_date')
        casting_site = data.get('casting_site')
        revenue = data.get('revenue')
        actor_ids = data.get('actor_ids', [])

        # Check if required fields are provided
        if not title or not release_date:
            abort(400, 'Title and release_date are required fields')

        # Create a new movie instance
        new_movie = Movie(
            title=title,
            release_date=release_date,
            casting_site=casting_site,
            revenue=revenue,
            actor_ids=actor_ids
        )

        # Insert the new movie into the database
        new_movie.insert()

        # Return the movie details after insertion
        return jsonify({
            'success': True,
            'message': 'Movie created successfully',
            'movie_details': new_movie.format_details()
        })
    except Exception as e:
        db.session.rollback()
        print_debug(e)
        abort(500)


# Update movie details by movie_id
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, movie_id):
    try:
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        # get request data
        data = request.get_json()
        title = data.get('title', movie.title)
        release_date = data.get('release_date', movie.release_date)
        casting_site = data.get('casting_site', movie.casting_site)
        revenue = data.get('revenue', movie.revenue)
        actor_ids = data.get('actor_ids', movie.actor_ids)

        # Update
        movie.title = title
        movie.release_date = release_date
        movie.casting_site = casting_site
        movie.revenue = revenue
        movie.actor_ids = actor_ids
        movie.update()

        # result
        return jsonify({
            'success': True,
            'message': 'Movie details updated successfully',
            'movie_details': movie.format_details()
        })
    except Exception as e:
        db.session.rollback()
        print_debug(e)
        abort(500)


# Delete a movie by movie_id
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    try:
        # Query
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        # title 
        title = movie.title

        # delete
        movie.delete()

        return jsonify({
            'success': True,
            'message': 'Movie deleted successfully',
            'deleted_movie_id': movie_id,
            'title': title
        })
    except Exception as e:
        db.session.rollback()
        print_debug(e)
        abort(500)


#----------------------------------------------------------------------------#
# Endpoints for Actors.
#----------------------------------------------------------------------------#
# Get all actors in short form
@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    try:
        # DB query
        actors = Actor.query.all()

        if not actors:
            abort(404)

        actors_list = [actor.format_short() for actor in actors]

        # Result
        return jsonify({
            'success': True,
            'actors': actors_list
        })

    except Exception as e:
        print_debug(e)
        abort(500)


# Get actors details (including involving movies if any) by actor_id
@app.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actor-details')
def get_actor_details(payload, actor_id):
    try:
        # Query the actor by actor_id
        actor = Actor.query.get(actor_id)

        # not found
        if actor is None:
            abort(404)

        # Get the list of movies involving the actor
        movies = Movie.query.filter(Movie.actor_ids.contains([actor_id])).all()
        movies_involvement = [
                {'id': movie.id, 'title': movie.title} 
                for movie in movies
            ]

        # Format actor and movies information
        actor_details = actor.format_details()

        return jsonify({
            'success': True,
            'actor_details': actor_details,
            'movies_involvement': movies_involvement
        })
    
    except Exception as e:
        print_debug(e)
        abort(500)


# Create a new actor and return result with actor details
@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):
    try:
        # Get data from the request JSON
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')

        # Check if required fields are provided
        if not name or not gender:
            abort(400, 'Name and gender are required fields')

        # Create a new actor instance
        new_actor = Actor(
            name=name,
            age=age,
            gender=gender,
        )

        # Insert the new actor into the database
        new_actor.insert()

        # Return the actor details after insertion
        return jsonify({
            'success': True,
            'message': 'actor created successfully',
            'actor_details': new_actor.format_details()
        })
    except Exception as e:
        db.session.rollback()
        print_debug(e)
        abort(500)


# Update actor details by actor_id
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, actor_id):
    try:
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        # get request data
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')

        # Update
        actor.name = name
        actor.age = age
        actor.gender = gender
        actor.update()

        # result
        return jsonify({
            'success': True,
            'message': 'actor details updated successfully',
            'actor_details': actor.format_details()
        })
    except Exception as e:
        db.session.rollback()
        print_debug(e)
        abort(500)


# Delete a actor by actor_id
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    try:
        # Query
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)

        # delated actor name 
        name = actor.name

        # delete
        actor.delete()

        return jsonify({
            'success': True,
            'message': 'actor deleted successfully',
            'deleted_actor_id': actor_id,
            'deleted_actor_name': name
        })
    except Exception as e:
        db.session.rollback()
        print_debug(e)
        abort(500)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)