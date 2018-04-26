import copy
import json

from django.core import serializers
from django.test import TestCase


class BaseTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_payload(self, **kwargs):
        assert hasattr(self, 'PAYLOAD'), 'Class {} has no PAYLOAD attribute'.format(type(self))
        payload = copy.deepcopy(self.PAYLOAD)
        payload.update(**kwargs)
        return payload

    def do_json_put(self, url, data):
        # Temporary stub, will be unneded with regular self.client in django 2.1.
        # PR is https://github.com/django/django/pull/9645
        data = json.dumps(data, cls=serializers.json.DjangoJSONEncoder)
        return self.client.put(url, data, content_type='application/json')
