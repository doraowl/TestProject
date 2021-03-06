"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase
from HttpServer.views import *
from HttpServer.models import *
from django.http import HttpRequest
from django.test.client import RequestFactory
from unittest import mock
# TODO: Configure your database in settings.py and sync before running tests.

class SimpleTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        super(SimpleTest, cls).setUpClass()
        Person.objects.all().delete()
        Post.objects.all().delete()
        Person.objects.create(login="TestLogin1", password="TestPassword1")
        Person.objects.create(login="TestLogin2", password="TestPassword2")
        Person.objects.create(login="TestLogin3", password="TestPassword3")
        Post.objects.create(text="TestText1",author_id=1)
        Post.objects.create(text="TestText2",author_id=2)
        Post.objects.create(text="TestText3",author_id=3)
        django.setup()
        
    def test_getAllPersonsAndPosts(self):
        request=HttpRequest()
        request.method='GET'
        jsonData=json.loads(getAllPersonsAndPosts(request).content)
        self.assertEqual(jsonData['response'], "success")
        self.assertEqual(len(jsonData['query']),3)

    def test_getPersonById(self):
        view="getPersonById"
        person=Person.objects.first()
        data=json.dumps({"id":1})
        content_type="text/html; charset=utf-8"
        request = self.factory.post(view,data=data,content_type=content_type)
        jsonData=json.loads(getPersonById(request).content)
        self.assertEqual(jsonData['response'], "success")
        query=jsonData["query"][0]
        self.assertEqual(query["id"], person.id)
        self.assertEqual(query["login"], person.login)
        self.assertEqual(query["password"], person.password)

    def test_getPostById(self):
        view="getPostById"
        post=Post.objects.first()
        data=json.dumps({"id":post.id})
        content_type="text/html; charset=utf-8"
        request = self.factory.post(view,data=data,content_type=content_type)
        jsonData=json.loads(getPostById(request).content)
        self.assertEqual(jsonData['response'], "success")
        query=jsonData["query"][0]
        self.assertEqual(query["id"], post.id)
        self.assertEqual(query["text"], post.text)
    def test_createPerson(self):
        view="createPerson"
        data=json.dumps({"login": "newlyCreatedLogin","password": "newlyCreatedPass"})
        content_type="text/html; charset=utf-8"
        request = self.factory.post(view,data=data,content_type=content_type)
        jsonData=json.loads(createPerson(request).content)
        self.assertEqual(jsonData['response'], "success")
        query=jsonData["query"][0]
        person=Person.objects.get(id=query["id"])
        self.assertEqual(person.login, "newlyCreatedLogin")
        self.assertEqual(person.password, "newlyCreatedPass")
    def test_createPost(self):
        view="createPost"
        person=Person.objects.first()
        data=json.dumps({"text": "newlyCreatedText","author_id": person.id})

        content_type="text/html; charset=utf-8"
        request = self.factory.post(view,data=data,content_type=content_type)
        jsonData=json.loads(createPost(request).content)
        self.assertEqual(jsonData['response'], "success")
        query=jsonData["query"][0]
        post=Post.objects.get(id=query["id"])
        self.assertEqual(post.text, "newlyCreatedText")
        self.assertEqual(post.author_id, person.id)
    def test_editPerson(self):
        view="editPerson"
        data=json.dumps({"id":1, "login": "editedLogin","password": "editedPass"})
        content_type="text/html; charset=utf-8"
        request = self.factory.post(view,data=data,content_type=content_type)
        person=Person.objects.get(id=1)
        self.assertNotEqual(person.login,"editedLogin")
        self.assertNotEqual(person.login,"editedPass")
        jsonData=json.loads(editPerson(request).content)
        self.assertEqual(jsonData['response'], "success")
        query=jsonData["query"][0]
        newPerson=Person.objects.get(id=query["id"])
        self.assertEqual(newPerson.login, "editedLogin")
        self.assertEqual(newPerson.password, "editedPass")

    @mock.patch('HttpServer.views.updatePerson')
    def test_editPersonMock(self,updatePersonMock):
        person=Person.objects.first()
        updatePersonMock.return_value=[{"id":person.id, "login": "editedLogin","password": "editedPass", "posts":[]}]
        view="editPerson"
        data=json.dumps({"id":person.id, "login": "editedLogin","password": "editedPass"})
        content_type="text/html; charset=utf-8"
        request = self.factory.post(view,data=data,content_type=content_type)
        jsonData=json.loads(editPerson(request).content)
        self.assertEqual(jsonData['response'], "success")
        query=jsonData["query"][0]
        self.assertEqual(query['login'], "editedLogin")
        self.assertEqual(query['password'], "editedPass")

    def test_editPost(self):
        view="editPost"
        data=json.dumps({"id":2, "text": "editedText","author_id": 3})
        content_type="text/html; charset=utf-8"
        request = self.factory.post(view,data=data,content_type=content_type)
        post=Post.objects.get(id=2)
        self.assertNotEqual(post.text,"editedText")
        self.assertNotEqual(post.author_id,3)
        jsonData=json.loads(editPost(request).content)
        self.assertEqual(jsonData['response'], "success")
        query=jsonData["query"][0]
        newPost=Post.objects.get(id=query["id"])
        self.assertEqual(newPost.text, "editedText")
        self.assertEqual(newPost.author_id, 3)
    def test_deletePerson(self):
        view="deletePerson"
        person = Person.objects.first()
        data=json.dumps({"id":person.id})
        content_type="text/html; charset=utf-8"
        request = self.factory.post(view,data=data,content_type=content_type)
        person=Person.objects.get(id=1)
        self.assertNotEqual(person,None)
        jsonData=json.loads(deletePerson(request).content)
        self.assertEqual(jsonData['response'], "success")
    def test_deletePost(self):
        view="deletePost"
        post = Post.objects.first()
        data=json.dumps({"id":post.id})
        content_type="text/html; charset=utf-8"
        request = self.factory.post(view,data=data,content_type=content_type)
        post=Post.objects.get(id=1)
        self.assertNotEqual(post,None)
        jsonData=json.loads(deletePost(request).content)
        self.assertEqual(jsonData['response'], "success")