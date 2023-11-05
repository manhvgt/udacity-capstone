## Imports
import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .app import app
from .database.models import Movie, Actor, db
from .auth.auth import AuthError, requires_auth
from .errors import print_debug

#----------------------------------------------------------------------------#
# General
#----------------------------------------------------------------------------#
# Use the after_request decorator to set Access-Control-Allow
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers'\
        , 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods'\
        , 'GET,POST,DELETE,PATCH,OPTIONS')
    return response

# index
@app.route('/')
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
def get_movies():
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


# Get movies details by movie_id
@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
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
            'actors': actors
        })
    
    except Exception as e:
        print_debug(e)
        abort(500)


# Create a new movie and return result with movie details
@app.route('/movies', methods=['POST'])
def create_movie():
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
            'movie': new_movie.format_details()
        })
    except Exception as e:
        db.session.rollback()
        print_debug(e)
        abort(500)


# Update movie details by movie_id
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
def update_movie(movie_id):
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
            'movie': movie.format_details()
        })
    except Exception as e:
        db.session.rollback()
        print_debug(e)
        abort(500)


# Delete a movie by movie_id
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
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


