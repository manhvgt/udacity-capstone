import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from pytest_mock import mocker

from main import app
from database.models import setup_db, Movie, Actor, db

CASTING_ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlR2RFFIb2ZIQTVGM2dFeDVBRTREQyJ9.eyJpc3MiOiJodHRwczovL21hbmh2Z3QudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY1NGJiM2I2MTY1YzVkZGRlNmZjNTg0YiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjk5NTQ1MzIzLCJleHAiOjE2OTk2MzE3MjMsImF6cCI6IkFaTUFJN1AzeldHbHpVMWd1WU5DZmY5OFhrTEpIdThtIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3ItZGV0YWlscyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWUtZGV0YWlscyIsImdldDptb3ZpZXMiXX0.PM9yt361_U6DWFOIsomATpN7SnFf7JeuF95TroA45SKmVGuP9Rggwh6HjrNTx5gzspDlB1-aH5cgOwsTfNiobro_ifcd6dPEXU9Q3daDlJdF2MKrBKtLdUuEN5D6TWXuYZeYbNLp65MDDgBH7ffScq0VBc1ZV5mh2RDNZ2bfASOHPJHBqSfqqDsL7PAgp4JI7CirVreBel6BX7R5LB_Ax1BBEFi30_dRKFX90ScafmEYgu5G480kl1qTKyRgdYLjnqQPGS9_Eb9VxWdLukSXPs6FHkTf_Bi1Ddse4ivWfdHzvcZg0C_uZBTPHPSsmCskCQNNiN4HYvkR-9MVlYjamw'
CASTING_DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlR2RFFIb2ZIQTVGM2dFeDVBRTREQyJ9.eyJpc3MiOiJodHRwczovL21hbmh2Z3QudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY1NDYwMDJlYTZkNzEzMmVmMjIzZWQ4MyIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjk5NDYwNTI5LCJleHAiOjE2OTk1NDY5MjksImF6cCI6IkFaTUFJN1AzeldHbHpVMWd1WU5DZmY5OFhrTEpIdThtIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9yLWRldGFpbHMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllLWRldGFpbHMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.MQOw4kn0sMx8ZwR53Npb8oms6aV2qddQ5bIVNF-hYdFspu8HNm6U5Cti058haNsUadAzvzUN8DQblrPFtN8ttAp2ELY1gCVWBfYi1O95I-sOFzUe7Uwj2_iEthCPRZ8__psZYAZnvxy377hB1UnpZqN1DMMzfqw8OeCOu-npzLv_j5MS9jEM0tZZ5UWuajuhq8KLwBEbgskUCa6xxPiq-h92T4IMHKbOu1bwCh74GFb--BFZ7fwXKLzJpA3hpUIn2XJgatGGaMgtruJ_nJizx-s6gjfsPLfe8Nb3DPwHu0YwUeubQb258fHdV37dXwGGdhXPrUEbiSbD_fPEap1pHQ'
EXECUTIV_PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlR2RFFIb2ZIQTVGM2dFeDVBRTREQyJ9.eyJpc3MiOiJodHRwczovL21hbmh2Z3QudWsuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE2MjUzNDI5NDkwMjUyMzkzMzQ0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2OTk1NDU4MDksImV4cCI6MTY5OTYzMjIwOSwiYXpwIjoiQVpNQUk3UDN6V0dselUxZ3VZTkNmZjk4WGtMSkh1OG0iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9yLWRldGFpbHMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllLWRldGFpbHMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.k45_Dk6lfbS-JTjrJmxk4jNWmbcOctIr9DHjSfBELmvyD2R8X-LH9lCLhibsRWA0s5dtJII6aUc5aAoO8kwREMglqAuWPzIxpqoHyLEsR3wDvKYFr-Hj4LVxwe89Pb8BFKhKDisIWHvwME1Ll7-sfzAYlRvDeoEBPKVRTbGxmzUOfC5Rt04FqHHpI_TURe5YeqkQnyYYe0ZUL6JkbGjY74UcSA8jAMN6uYAOfCru_zNxfgcUTVqW3A72qMSlVT2PKIJrYbpAOWvFJ7XJJG0a-0ERreCbmZ1gzRtF0IagxmkI9X3-Me0aQu7yceq8ZOouAZKZY5t-_d0Vq10wQHta0A'

test_movie = {
            'title': 'Test Movie',
            'release_date': '2023-10-25',
            'casting_site': 'Test Casting Site',
            'revenue': 1000000,
            'actor_ids': [1]
        }
update_movie = {
            'title': 'Updated Movie',
            'release_date': '2023-10-25',
            'casting_site': 'Test Casting Site',
            'revenue': 222222,
            'actor_ids': [1]
        }

test_actor = {
            'name': 'Test Actor',
            'age': 45,
            'gender': "Male"
        }
update_actor = {
            'name': 'Updated Actor',
            'age': 43,
            'gender': "Male"
        }


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client()
        self.db = db

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.session.remove()
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    #----------------------------------------------------------------------------#
    # get_movies
    #----------------------------------------------------------------------------#
    def test_get_movies(self):
        # Simulate a valid GET request with proper authorization
        response = self.app.get('/movies', headers={
            'Authorization': CASTING_ASSISTANT_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('movies' in data)

    def test_get_movies_no_movies(self, mocker):
        # Simulate a scenario where there are no movies in the database
        mocker.patch('app.Movie.query.all', return_value=[])
        response = self.app.get('/movies', headers={
            'Authorization': CASTING_ASSISTANT_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'])

    def test_get_movies_unauthorized(self):
        # Simulate an unauthorized request with an invalid token
        response = self.app.get('/movies', headers={
            'Authorization': 'invalid_token'
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(data['success'])


    #----------------------------------------------------------------------------#
    # get_movie_details
    #----------------------------------------------------------------------------#
    def test_get_movie_details(self):
        # Simulate a valid GET request with proper authorization
        movie_id = 1  # an actual movie ID
        response = self.app.get(f'/movies/{movie_id}', headers={
            'Authorization': CASTING_ASSISTANT_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('movie_details' in data)
        self.assertTrue('actors_involvement' in data)

    def test_get_movie_details_not_found(self):
        # Simulate a scenario where the requested movie ID is not found
        movie_id = 999  # a non-existing movie ID
        response = self.app.get(f'/movies/{movie_id}', headers={
            'Authorization': CASTING_ASSISTANT_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'])

    def test_get_movie_details_unauthorized(self):
        # Simulate an unauthorized request with an invalid token
        movie_id = 1  # an actual movie ID
        response = self.app.get(f'/movies/{movie_id}', headers={
            'Authorization': 'Bearer invalid_token'  # with an invalid JWT token
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(data['success'])


    #----------------------------------------------------------------------------#
    # create_movie
    #----------------------------------------------------------------------------#
    def test_create_movie(self):
        # Simulate a valid POST request with proper authorization
        data = test_movie
        response = self.app.post('/movies', headers={
            'Authorization': CASTING_DIRECTOR_TOKEN
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('movie_details' in data)

    def test_create_movie_missing_required_fields(self):
        # Simulate a scenario where required fields are missing
        data = {
            'title': 'Test Movie',
        }
        response = self.app.post('/movies', headers={
            'Authorization': CASTING_DIRECTOR_TOKEN
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['success'])

    def test_create_movie_unauthorized(self):
        # Simulate an unauthorized request with an invalid token
        data = test_movie
        response = self.app.post('/movies', headers={
            'Authorization': 'Bearer invalid_token'
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(data['success'])

    #----------------------------------------------------------------------------#
    # update_movie
    #----------------------------------------------------------------------------#
    def test_update_movie(self):
        # Simulate a valid PATCH request with proper authorization
        movie_id = 2  # an actual movie ID
        data = update_movie
        response = self.app.patch(f'/movies/{movie_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('movie_details' in data)

    def test_update_movie_not_found(self):
        # Simulate a PATCH request for a non-existent movie
        movie_id = 999  # non-existent movie ID
        data = update_movie
        response = self.app.patch(f'/movies/{movie_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'])

    def test_update_movie_unauthorized(self):
        # Simulate an unauthorized request with an invalid token
        movie_id = 1 
        data = update_movie
        response = self.app.patch(f'/movies/{movie_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(data['success'])

    #----------------------------------------------------------------------------#
    # delete_movie
    #----------------------------------------------------------------------------#
    def test_delete_movie(self):
        # Simulate a valid DELETE request with proper authorization
        movie_id = 1  # an actual movie ID
        response = self.app.delete(f'/movies/{movie_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('deleted_movie_id' in data)
        self.assertTrue('title' in data)

    def test_delete_movie_not_found(self):
        # Simulate a DELETE request for a non-existent movie
        movie_id = 999  # a non-existent movie ID
        response = self.app.delete(f'/movies/{movie_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'])

    def test_delete_movie_unauthorized(self):
        # Simulate an unauthorized request with an invalid token
        movie_id = 1  # an actual movie ID
        response = self.app.delete(f'/movies/{movie_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(data['success'])

    #----------------------------------------------------------------------------#
    # get_actors
    #----------------------------------------------------------------------------#
    def test_get_actors_success(self):
        response = self.client.get('/actors', headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('actors', data)
        self.assertGreater(len(data['actors']), 0)

    def test_get_actors_failure(self):
        response = self.client.get('/actors', headers={'Authorization': f'Bearer invalid_token'})
        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertNotIn('actors', data)

    def test_get_actors_not_found(self, mocker):
        # Mock the Actor.query.all() to return an empty list
        mocker.patch('app.Actor.query.all', return_value=[])

        response = self.client.get('/actors', headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'})
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertNotIn('actors', data)

    #----------------------------------------------------------------------------#
    # get_actor_details
    #----------------------------------------------------------------------------#
    def test_get_actor_details(self):
        # Simulate a valid GET request with proper authorization
        actor_id = 1  # an actual actor ID
        response = self.app.get(f'/actors/{actor_id}', headers={
            'Authorization': CASTING_ASSISTANT_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('actor_details' in data)
        self.assertTrue('actors_involvement' in data)

    def test_get_actor_details_not_found(self):
        # Simulate a scenario where the requested actor ID is not found
        actor_id = 999  # a non-existing actor ID
        response = self.app.get(f'/actors/{actor_id}', headers={
            'Authorization': CASTING_ASSISTANT_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'])

    def test_get_actor_details_unauthorized(self):
        # Simulate an unauthorized request with an invalid token
        actor_id = 1  # an actual actor ID
        response = self.app.get(f'/actors/{actor_id}', headers={
            'Authorization': 'Bearer invalid_token'  # with an invalid JWT token
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(data['success'])


    #----------------------------------------------------------------------------#
    # create_actor
    #----------------------------------------------------------------------------#
    def test_create_actor(self):
        # Simulate a valid POST request with proper authorization
        data = test_actor
        response = self.app.post('/actors', headers={
            'Authorization': CASTING_DIRECTOR_TOKEN
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('actor_details' in data)

    def test_create_actor_missing_required_fields(self):
        # Simulate a scenario where required fields are missing
        data = {
            'name': 'Test Actor',
        }
        response = self.app.post('/actors', headers={
            'Authorization': CASTING_DIRECTOR_TOKEN
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['success'])

    def test_create_actor_unauthorized(self):
        # Simulate an unauthorized request with an invalid token
        data = test_actor
        response = self.app.post('/actors', headers={
            'Authorization': 'Bearer invalid_token'
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(data['success'])

    #----------------------------------------------------------------------------#
    # update_actor
    #----------------------------------------------------------------------------#
    def test_update_actor(self):
        # Simulate a valid PATCH request with proper authorization
        actor_id = 2  # an actual actor ID
        data = update_actor
        response = self.app.patch(f'/actors/{actor_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('actor_details' in data)

    def test_update_actor_not_found(self):
        # Simulate a PATCH request for a non-existent actor
        actor_id = 999  # non-existent actor ID
        data = update_actor
        response = self.app.patch(f'/actors/{actor_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'])

    def test_update_actor_unauthorized(self):
        # Simulate an unauthorized request with an invalid token
        actor_id = 1 
        data = update_actor
        response = self.app.patch(f'/actors/{actor_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        }, json=data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(data['success'])

    #----------------------------------------------------------------------------#
    # delete_actor
    #----------------------------------------------------------------------------#
    def test_delete_actor(self):
        # Simulate a valid DELETE request with proper authorization
        actor_id = 1  # an actual actor ID
        response = self.app.delete(f'/actors/{actor_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue('deleted_actor_id' in data)
        self.assertTrue('name' in data)

    def test_delete_actor_not_found(self):
        # Simulate a DELETE request for a non-existent actor
        actor_id = 999  # a non-existent actor ID
        response = self.app.delete(f'/actors/{actor_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'])

    def test_delete_actor_unauthorized(self):
        # Simulate an unauthorized request with an invalid token
        actor_id = 1  # an actual actor ID
        response = self.app.delete(f'/actors/{actor_id}', headers={
            'Authorization': EXECUTIV_PRODUCER_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertTrue(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()