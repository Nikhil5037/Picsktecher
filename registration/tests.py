from audioop import reverse
from django.test import TestCase
from registration.models import RegisteredUsers
# Create your tests here.
from django.test import TestCase
import json
class RegisterTestCase(TestCase):
    def setUp(self):
        with open("registration/testData.json") as jsonFile:
            self.data = json.load(jsonFile)
            jsonFile.close()
        self.email = self.data['data1']['email'],
        self.password= self.data['data1']['password'],
        self.firstname= self.data['data1']['firstname'],
        self.lastname= self.data['data1']['lastname']
    def test_home_url(self):
        response = self.client.post("/index/")
        self.assertEqual(response.status_code,200)
    def test_signup_form(self):
        response = self.client.post("/register/", data={
            'email': self.email,
            'password': self.password,
            'firstname': self.firstname,
            'lastname': self.lastname
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['success'],True,json.loads(response.content)['message'])
        pass
    # def test_login_form(self):
    #     response = self.client.post("/login/", data={
    #         'email': self.email,
    #         'password': self.password
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.content)['success'],True,json.loads(response.content)['message'])
    #     pass