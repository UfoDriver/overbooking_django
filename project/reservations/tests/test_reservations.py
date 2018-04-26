from django.test import TestCase

from . import BaseTestCase


class TestReservations(BaseTestCase):
    URL = '/api/v1/reservations'
    PAYLOAD = {
        'name': 'John Smith',
        'email': 'john@smiths.com',
        'arrival_date': '2020-02-02',
        'departure_date': '2020-02-03'
    }

    def test_fetch_reservations(self):
        resp = self.client.get(self.URL)
        self.assertEqual(resp.status_code, 405)

    def test_create_invalid_reservation(self):
        resp = self.client.post(self.URL, {})
        self.assertEqual(resp.status_code, 400)
        error = {'name': ['This field is required.'],
                 'email': ['This field is required.'],
                 'arrival_date': ['This field is required.'],
                 'departure_date': ['This field is required.']}
        self.assertDictEqual(resp.json(), error)

    def test_reservation_date_in_the_past(self):
        payload = self.get_payload(arrival_date='2000-02-02')
        resp = self.client.post(self.URL, payload)
        self.assertEqual(resp.status_code, 400)
        error = {'arrival_date': ['Cannot set arrival date in the past.']}
        self.assertDictEqual(resp.json(), error)

    def test_reservation_date_in_the_past(self):
        payload = self.get_payload(departure_date='2020-02-01')
        resp = self.client.post(self.URL, payload)
        self.assertEqual(resp.status_code, 400)
        error = {'non_field_errors': ['Departure date must occur after arrival date.']}
        self.assertDictEqual(resp.json(), error)

    def test_create_reservation(self):
        resp = self.client.post(self.URL, self.get_payload())
        self.assertEqual(resp.status_code, 201)
