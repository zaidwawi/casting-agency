import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import create_app
from models import *


access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklrMDFXSHlhMGpGRjl1ZkJ0LXNnTSJ9.eyJpc3MiOiJodHRwczovL3phaWQtYWhtYWQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNjMxZWEyN2Y3NTQzMDA3MGI4OTI4MiIsImF1ZCI6Im1vdmllIiwiaWF0IjoxNjE3MTA5NDIzLCJleHAiOjE2MTcxMTY2MjMsImF6cCI6ImxYc3FGQ2VFTjFzRmQ3TjdjS0FpQ3lkQmZ4ajV3aU5FIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.pEUFlAi9v2k3XVTUKfWtB2U-TCGd_SfT6obyWiqAyo-JSlNaDWb90bnC99N3USyGTLWkFDnGzuHJAw9pAlvJDCA__yVZeGrueHL1o8A07S8Rm0FWsAZyJS3ckgSMs3eRmFxRc3mgbqtPSflHKx22GcEwUaxdwtkp3aw9Vd8SB7yNRlUrSduvU70PvATSR0JinUugF4uUnxNU8fVVnx4tI69ytK16kkSFfi-AGcZh0zOgwcdJK7gvsCNUo90ebhm5dw07oshSR6pvRqebAmtuUuQ7cvvloALUO0osytOKp9Z6-57rOc9BIo3QPawUgFMzmJKDNgjf37bzclQVLf0Yrw'


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path=os.environ["DATABASE_URL"]
        setup_db(self.app, self.database_path)
        self.exec_prod = access_token

        self.movie_new = {
            "title": "avenger",
            "release_date": "1996"
        }
        self.update_the_movie ={
            "title": "the updated movie",
            "release_date": "this is the new date"
        }
        self.new_actors = {
            "name": "zaid",
            "age": "16",
            "gender": "male"
        }
        self.update_the_actor = {
            "name": "the new name",
            "age": "70",
            "gender": "new gender"
        }



# test the movie (patch, delete, post, get)


    def create_newMovie(self):
        response = self.client().post(
            '/movies',
            headers={
                "Authorization": 'Bearer '+self.exec_prod
            },
            json=self.movie_new
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    def delete_movie(self):
        # create a demo or a fake movie that will be deleted
        demo_movie={ 
            "title": "demo",
            "release_date": "2020-2-22"
        }
        response=self.client().post(
            '/movies',
            headers={'Authorization': 'Bearer '+self.exec_prod}, 
            json = demo_movie
        )
        data = json.loads(response.data)
        the_movie_id=data['movie']['id']

        responses = self.client().delete(
            '/movies/{}'.format(the_movie_id),
            headers={
                'Authorization': 'Bearer '+self.exec_prod
            }
        )
        data = json.loads(responses.data)
        self.assertEqual(responses.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movie(self):
    #We will create a movie to update later in the test
        new_movie = {
            'title': 'This an update test movie',
            'release_date':'1990'
                        }
        res = self.client().post('/Movies', headers={
                        'Authorization': 'Bearer ' + self.exec_prod
                        }, json = new_movie)
        data = json.loads(res.data)
        ids= data['movie']['id']
        #We will execute the test for update
        update_movie = self.update_movie
        res = self.client().patch('/Movies/{}'.format(ids), headers={
                        'Authorization': 'Bearer ' + self.exec_prod
                        }, json=update_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)




# test the actors (patch, delete, get, post)


    def create_new_actor():
        response = self.client().post(
            '/Actors',
            headers={
                'Authorization': 'Bearer ' + self.exec_prod
            }, json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    

    def test_delete_actor(self):
        # I will  make a new actor to delete it later 
        new_actor = {
            'name': 'name1',
            'age': '21',
            'gender': 'male'
        }
        response = self.client().post(
            '/Actors',
            headers={
                'Authorization': 'Bearer ' + self.exec_prod
            }, json=new_actor)
        data = json.loads(response.data)
        ids = data['actor']['id']
        response = self.client().delete(
            '/Actors/{}'.format(ids),
            headers={
                'Authorization': 'Bearer ' + self.exec_prod
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_update_actor(self):
        # make a new actor to update ot later
        new_actor = {
            'name': 'not updated yet',
            'age': '32',
            'gender': 'Male'
        }
        response = self.client().post(
            '/Actors',
            headers={
                'Authorization': 'Bearer ' + self.exec_prod
            } ,json = new_actor)
        data = json.loads(response.data)
        ids = data['actor']['id']
        update_actor = self.update_actor
        response = self.client().patch(
            '/Actors/{}'.format(ids),
            headers={
                'Authorization': 'Bearer ' + self.exec_prod
            }, json=update_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)



    def test_get_the_actors(self):
        response = self.client().get(
            '/actors',
            headers={
                'Authorization': 'Bearer '+self.exec_prod
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)