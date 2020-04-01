import unittest
import requests
import json

from application import app
from application import validate_url

test_app = app.test_client()
tiny_api_url = 'https://agn54nepyg.execute-api.us-east-2.amazonaws.com/beta/create'
tiny_url_home = 'https://agn54nepyg.execute-api.us-east-2.amazonaws.com/beta/'

class TestAppliction(unittest.TestCase):
    def test_validate_url_1(self):
        url = 'google.com'
        self.assertFalse(validate_url(url))

    def test_validate_url_2(self):
        url = 'http://www.google.com'
        self.assertTrue(validate_url(url))

    def test_validate_url_3(self):
        url = 'https://docs.aws.amazon.com/zh_cn/codepipeline/latest/userguide/tutorials-simple-s3.html'
        self.assertTrue(validate_url(url))

    def test_validate_url_4(self):
        url = 'ftp://myhome.com'
        self.assertTrue(validate_url(url))

    def test_post_request_1(self):
        headers = {'Content-Type': 'application/json', 'X-Api-Key': 'Kelvin0123456'}
        long_url = 'https://stackoverflow.com/questions/8814472/how-to-make-an-html-back-link'
        resp = requests.post(
            tiny_api_url,
            headers=headers,
            data=json.dumps({
                "long_url": long_url
            }
            )
        )

        self.assertEqual(resp.status_code, 200)

    def test_post_request_2(self):
        headers = {'Content-Type': 'application/json', 'X-Api-Key': 'asdfasddafs'}
        long_url = 'https://stackoverflow.com/questions/8814472/how-to-make-an-html-back-link'
        resp = requests.post(
            tiny_api_url,
            headers=headers,
            data=json.dumps({
                "long_url": long_url
            }
            )
        )

        self.assertEqual(resp.status_code, 401)

    def test_get_request_1(self):
        resp = requests.get(tiny_url_home + 'ZX1pOytdYPN')
        self.assertEqual(resp.url, 'https://docs.aws.amazon.com/zh_cn/cognito/latest/developerguide/what-is-amazon-cognito.html')

    def test_get_request_2(self):
        resp = requests.get(tiny_url_home + 'AAAssadfad')
        self.assertEqual(resp.url, 'https://objects.ruanbekker.com/assets/images/404-blue.jpg')


if __name__ == '__main__':
    unittest.main()
