import os
import unittest

import fastapi.testclient

import main
import db
import config

TEST_DATA = {
    'example.com'      : '5ababd603b', # md5('example.com')[0:9] 
    'another-test.com' : 'd4d374de56'  # md5('another-test.com'][0:9]
}

TEST_DB_LOCATION = '/dev/shm/test.db'

def get_settings_override():
    return config.Settings(datastore=TEST_DB_LOCATION)

main.app.dependency_overrides[main.get_settings] = get_settings_override
client = fastapi.testclient.TestClient(main.app)

class TestAPI(unittest.TestCase):
    def setUp(self):
        db.drop(os.path.join(TEST_DB_LOCATION))
        db.create(os.path.join(TEST_DB_LOCATION))
        db.update(os.path.join(TEST_DB_LOCATION))
        self.client = client
        
    def tearDown(self):
        db.drop(os.path.join(TEST_DB_LOCATION))

    def test_make(self):
        response = self.client.post(
            '/make',
            data = {
                'url' : 'http://google.com'
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        response = self.client.get(
            '/' + TEST_DATA.get('example.com', '')
        )
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent(self):
        response = self.client.get(
            '/' + 'NONEXISTENT'
        )
        self.assertEqual(response.status_code, 404)

    def test_make_api(self):
        response = self.client.put(
            '/api/make/',
            json = {
                'url' : 'another-test.com'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), { "url" : 'http://testserver/' + TEST_DATA.get('another-test.com', '') })
