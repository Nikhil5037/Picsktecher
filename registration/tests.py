from audioop import reverse
from django.test import TestCase
from registration.models import RegisteredUsers
# Create your tests here.
from django.test import TestCase
import json
class RegisterTestCase(TestCase):
    def setUp(self):
        with open("registration/testData.json") as jsonFile:
            data = json.load(jsonFile)
            jsonFile.close()
        print(data)
        self.email =RegisteredUsers.objects.create(email=data['data1']['email'])
        self.password = data['data1']['password']
        self.firstname = data['data1']['firstname']
        self.lastname =data['data1']['lastname']
    def test_signup_url(self):
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
        