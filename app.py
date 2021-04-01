import os
from flask import (Flask, request, abort, jsonify)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, rollback
from auth import requires_auth, AuthError


def create_app(test_config=None):

    # create and configure the app

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

# create the actors action here 

    @app.route('/actors', methods=['GET']) # set a get request for actors
    @requires_auth('get:actors')
    def get_actors(jwk):
        actor = Actor.query.all() # get all actors detail 
        return jsonify({
            "success": True,
            "actors": [actors.format() for actors in actor]
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['GET']) # get the actorst by_id
    @requires_auth('get:actors')
    def get_actor(jwk, actor_id):
        actor = Actor.query.get(actor_id) # I get the code here by id 
        if actor is None: # if there is no actor I will abort 404 or (not found)
            abort(404)
        return jsonify({
            "success": True,
            "actor": actor.format()
        }), 200

    @app.route('/actors', methods=['POST']) # post an actor
    @requires_auth('post:actors')
    def post_actors(jwk):
        body = request.get_json()

        add_actor = Actor() 

        name = body.get('name') # I get the name
        age = body.get('age') # I get the age 
        gender = body.get('gender') # I get the gender 
        if (name is None) or (age is None) or (gender is None): # if there is no age-name-gender I want to give 422 error 
            abort(422)
        try:
            if name is not None: # if the name is not None (thats mean if the name exist)
                add_actor.name = name
            if age is not None: 
                add_actor.age = age
            if gender is not None:
                add_actor.age = age

            add_actor.insert() # I insert the data to the database 
        except Exception:
            abort(500)
        return jsonify({
            "success": True,
            "created_actor": add_actor.format()
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['PATCH']) # patch the data or (update it)
    @requires_auth('patch:actors')
    def edit_actors(jwk, actor_id):
        body = request.get_json() 
        
        actor = Actor.query.get(actor_id)

        if actor is None: # if there is no actor I want to raise 404 error (not found)
            abort(404)

        new_name = body.get('name')
        new_age = body.get('age') # get the age and the name as will as the gender 
        new_gender = body.get('gender')

        if (new_name is None) or (new_age is None) or (new_gender is None):
            abort(422)

        try:
            if new_name is not None:
                actor.name = new_name
            if new_age is not None:
                actor.age = new_age # if the data i exist => I will add it to thhe database
            if new_gender is not None:
                actor.gender = new_gender

            actor.update()
        except:
            rollback() #d if there is something wrong I want to rollback I set this func in the models.py 
            abort(422)

        return jsonify({
            "success": True,
            "patched_actor": actor.format()
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwk, actor_id):
        actor = Actor.query.get(actor_id) # get the actor by id 
        if actor is None:
            abort(404)

        try:
            actor.delete() # if there is nothing wrong I will delete it 
        except Exception:
            rollback() # but if there is an error I want to rollback and raise 500 error
            abort(500)

        return jsonify({
            "success": True,
            "deleted_actor": actor.format()
        }), 200


# here I will setup the movie (get , patch , post and delete) requests



    @app.route('/movies', methods=['GET']) # get the movie 
    @requires_auth('get:movies')
    def get_movies(jwk):
        movies = Movie.query.all()

        return jsonify({
            "success": True,
            "movies": [movie.format() for movie in movies]
        })

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(jwk, movie_id):
        movie = Movie.query.get(movie_id) # get the movie by id 
        if movie is None:
            abort(404) # if the movie does not exist I want to raise 404 error 
        return jsonify({
            "success": True,
            "movie": [movie.format()]
        })

    @app.route('/movies', methods=['POST']) # create movie 
    @requires_auth('post:movies')
    def post_movies(jwk):
        body = request.get_json()

        new_title = body.get('title') 
        new_release_date = body.get('release_date')

        if (new_title is None) or (new_release_date) is None: # if the new title and new release date are empty I want to raise 400 error 
            abort(400)

        try:
            if (new_title is not None) and (new_release_date is not None): # if the new title and release date are not empty I want to add them
                movie = Movie(
                    title=new_title,
                    release_date=new_release_date
                )
            movie.insert() # insert the data

        except Exception:
            abort(500)

        return jsonify({
            "success": True,
            "created_movie": movie.id
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies(jwk, movie_id):

        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(404)

        body = request.get_json()

        title = body.get("title")
        release_date = body.get("release_date")

        if (title is None) or (release_date is None):
            abort(422)

        try:
            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.relaese_date = release_date
            movie.update()

        except Exception:
            abort(422)


        return jsonify({
            "success": True,
            "patched_movie": movie.format()
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwk, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)

        try:
            movie.delete()
        except Exception:
            rollback()
            abort(422)


        return jsonify({
            "success": True,
            "deleted_movie": movie.format()
        }), 200



# handle error =====================================================================


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success":False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403


    @app.errorhandler(404)
    def resource_not_found_error(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'unprocessable'
        }), 422



    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run()
