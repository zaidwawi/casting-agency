import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, rollback
from auth import requires_auth, AuthError


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)


# here I want to setup the actors action 
  @app.route('/')
  def home():
    return 'welcome to my website'

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actor(jwk):
    actors = Actor.query.all()
    Actor = [actor.format() for actor in actors]
    return jsonify({
      "success": True,
      "actors": [actor.format() for actor in actors]
    }), 200


  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actor(jwk):
    body = request.get_json()
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    if ((age is None) or (name is None) or (gender is None)):
      abort(400)
    
    try:
      the_actor = Actor(name=name, age=age, gender=gender)
      the_actor.insert()

    except Exception:
      abort(500)
  
    return jsonify({
      "success": True,
      "created": the_actor.id
    }), 200

  @app.route('/actors/<int:id>', methods=['GET'])
  @requires_auth('get:actors')
  def get_actor_by_id(jwk, id):
    actors = Actor.query.get(id)
    if actors is None:
      abort(404)
    return jsonify({
      "success": True,
      "actors": actors.format()
    }), 200
  



  @app.route('/actors/<int:id>', methods = ['PATCH'])
  @requires_auth('patch:actor')
  def patch_the_actor(jwk, id):
    body = request.get_json()
    actor = Actor.query.get(id)

    if actor is None:
      abort(404)

    age = body.get('age')
    name = body.get('name')
    gender = body.get('gender')

    if ((age is None) or (name is None) or (gender is None)):
      abort(422)
    
    try:
      if age is not None:
        actor.age = age
      if name is not None:
        actor.name = name
      if gender is not None:
        actor.gender = gender

      actor.update()
    except Exception:
      rollback()
      abort(422)

    return jsonify({
      "success": True,
      "actor": [actor.format()]
    }), 200
  


  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(jwk, id):
    actor = Actor.query.get(id)

    if actor is None:
      abort(404)
    
    try:
      actor.delete()
    except Exception:
      rollback()
      abort(500)

    return jsonify({
      "success": True,
      "movies": [actor.format()]
    }), 200

  
  # here I want to setup the movie actions 


  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movie(jwk):
    movies = Movie.query.all()
    return jsonify({
      "success": True,
      "movies": [movie.format() for movie in movies]

    }), 200
  

  @app.route('/movies/<int:id>', methods=['GET'])
  @requires_auth('get:movies')
  def get_movie_by_id(jwk, id):
    movie = Movie.query.get(id)

    if movie is None:
      abort(404)
    return jsonify({
      "success": True,
      "movie": movie.format()
    }), 200
  

  
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movie')
  def post_movie(jwk):
    body = request.get_json()

    title = body.get('title')
    release_date = body.get('release_date')

    if (title is None) or (release_date is None):
      abort(400)

    try:
      the_movie = Movie()
      the_movie.title = title
      the_movie.release_date = release_date
      the_movie.insert()

      return jsonify({
        "success": True,
        "created_movie": the_movie.format()}), 200
    except Exception:
      abort(500)

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def patch_movie(jwk, id):
    body = request.get_json()
    movie = Movie.query.get(id)

    if movie is None:
      abort(404)
    
    try:
      title = body['title']
      release_date = body['release_date']

      if title is not None:
        movie.title = title
      if release_date is not None:
        movie.release_date = release_date
      movie.update()

    except Exception:
      abort(500)
    
    return jsonify({
        "success": True,
        "movie": movie.format()
      }), 200

  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(jwk, id):
    movie = Movie.query.get(id)

    if movie is None:
      abort(404)

    try:
      movie.delete()
    except Exception:
      rollback()
      abort(500)
    return jsonify({
      "success": True,
      "deleted": movie.format()
      }), 200



      



    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": 'Resource not found '
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": 'unprocessable'
        }), 422

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
          "success": False,
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
    APP.run(host='0.0.0.0', port=8080, debug=True)
