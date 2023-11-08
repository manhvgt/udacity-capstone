import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .main import app
from .database.models import setup_db, Movie, Actor, db

CASTING_ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlR2RFFIb2ZIQTVGM2dFeDVBRTREQyJ9.eyJpc3MiOiJodHRwczovL21hbmh2Z3QudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY1NGJiM2I2MTY1YzVkZGRlNmZjNTg0YiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjk5NDYxNjgxLCJleHAiOjE2OTk1NDgwODEsImF6cCI6IkFaTUFJN1AzeldHbHpVMWd1WU5DZmY5OFhrTEpIdThtIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3ItZGV0YWlscyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWUtZGV0YWlscyIsImdldDptb3ZpZXMiXX0.BODap_7dc90Vua0feC95uNzlxTGrF1tWiRICfHzj-kI_j00nXCxZ5XiRvj4XIGuWVAI7kmKJzSUHalaww1z8lFKCTNZFDizyimCLYcFo_HkinkUBsRorborw6rstv6rP7vwLCHP4ZAaDiAPmQ_-CLq9YUYyWI6zkteL0IqCieJayspMSY8MReXn5vOmGk4Hab01DkVvNd9Y4jL1Nu5ZF0oneAOY8EqTY6aGRq49Bqui8z3Z1VwAiq16rvFj5XIlGPnmXiBKfJO8KUt1uqRi0FIlmyLdp9Fuy9pTtiOu1N-SUNLqgZyPhOrFO5t1sSHMmLVrnm_BQgOcZneAR6-Cc1Q'
CASTING_DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlR2RFFIb2ZIQTVGM2dFeDVBRTREQyJ9.eyJpc3MiOiJodHRwczovL21hbmh2Z3QudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY1NDYwMDJlYTZkNzEzMmVmMjIzZWQ4MyIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjk5NDYwNTI5LCJleHAiOjE2OTk1NDY5MjksImF6cCI6IkFaTUFJN1AzeldHbHpVMWd1WU5DZmY5OFhrTEpIdThtIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9yLWRldGFpbHMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllLWRldGFpbHMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.MQOw4kn0sMx8ZwR53Npb8oms6aV2qddQ5bIVNF-hYdFspu8HNm6U5Cti058haNsUadAzvzUN8DQblrPFtN8ttAp2ELY1gCVWBfYi1O95I-sOFzUe7Uwj2_iEthCPRZ8__psZYAZnvxy377hB1UnpZqN1DMMzfqw8OeCOu-npzLv_j5MS9jEM0tZZ5UWuajuhq8KLwBEbgskUCa6xxPiq-h92T4IMHKbOu1bwCh74GFb--BFZ7fwXKLzJpA3hpUIn2XJgatGGaMgtruJ_nJizx-s6gjfsPLfe8Nb3DPwHu0YwUeubQb258fHdV37dXwGGdhXPrUEbiSbD_fPEap1pHQ'
EXECUTIV_PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlR2RFFIb2ZIQTVGM2dFeDVBRTREQyJ9.eyJpc3MiOiJodHRwczovL21hbmh2Z3QudWsuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE2MjUzNDI5NDkwMjUyMzkzMzQ0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2OTk0NjA1NjIsImV4cCI6MTY5OTU0Njk2MiwiYXpwIjoiQVpNQUk3UDN6V0dselUxZ3VZTkNmZjk4WGtMSkh1OG0iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9yLWRldGFpbHMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllLWRldGFpbHMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.hlJ48uywQm1aCOr6G8k9Wb2Otf21k5hL-EUtct6SBnPmKxKLRBgvDVUWmxsqoyKUAf7Z1QokhnOnQVJaDkd5ar9v3rNKzE4J6jQVU2-EsN_J5mBDQAGCyxIYE19rE4sxLe1310rSBHyYyZ0Iqa0XPuh0JIf_GpHXNZlRRr_5HcWnDgLkvhJ8HcPmfbtUl_Cb9wl0UfJ54LQz7C0SetDrumOHxVwiJkMgsfxaRfEYQ8IgWApp54322hJbz_TkHBfiSBGov8Q6Y1cU3656HLTsbgodUMl_8x8pTwi6HwqRXbWkApEYw9DzJjrbliqkv2-YpU99Oy0uuKSFwIOIU1n1mw'

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

    def test_get_movies_no_movies(self):
        # Simulate a scenario where there are no movies in the database
        response = self.app.get('/movies', headers={
            'Authorization': CASTING_ASSISTANT_TOKEN
        })
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'])

    def test_get_movies_unauthorized(self):
        # Simulate an unauthorized request with an invalid token
        response = self.app.get('/movies', headers={
            'Authorization': 'invalid_token_here'
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
            'Authorization': 'Bearer invalid_token_here'  # with an invalid JWT token
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
            'Authorization': 'Bearer invalid_token_here'
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


    #----------------------------------------------------------------------------#
    # get_actor_details
    #----------------------------------------------------------------------------#


    #----------------------------------------------------------------------------#
    # create_actor
    #----------------------------------------------------------------------------#


    #----------------------------------------------------------------------------#
    # update_actor
    #----------------------------------------------------------------------------#


    #----------------------------------------------------------------------------#
    # delete_actor
    #----------------------------------------------------------------------------#


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()