from django.test import TestCase

from . import BaseTestCase


class TestConfig(BaseTestCase):
    # @TODO: use django resolve for urls
    URL = '/api/v1/config'
    PAYLOAD = {
        'rooms': 100,
        'overbooking': 10
    }

    def test_fetch_config(self):
        resp = self.client.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), {'rooms': 100, 'overbooking': 0})

    def test_put_invalid_config(self):
        resp = self.client.put(self.URL, {}, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        error = {'overbooking': ['This field is required.'],
                 'rooms': ['This field is required.']}
        self.assertDictEqual(resp.json(), error)

    def test_put_valid_config(self):
        resp = self.do_json_put(self.URL, self.get_payload(rooms=110))
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), {'rooms': 110, 'overbooking': 10})

    def test_put_invalid_values(self):
        resp = self.do_json_put(self.URL, self.get_payload(rooms=-1, overbooking=-10))
        self.assertEqual(resp.status_code, 400)
        error = {'overbooking': ['Overbooking cannot be negative.'],
                 'rooms': ['Room number cannot be less than one.']}
        self.assertDictEqual(resp.json(), error)
