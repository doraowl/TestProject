from django.shortcuts import render
from django.http import HttpResponse
from HttpServer.models import *
from HttpServer.methods import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

@csrf_exempt
def getAllPersonsAndPosts(request):
    resultDict={}
    if request.method == 'GET':
        query=Person.objects.all()
        result=[entry.json() for entry in query] 
        resultDict["response"]="success"
        resultDict["query"]=result
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
    else:
        resultDict["response"]="wrong method"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
@csrf_exempt
def getPersonById(request):
    if request.method == 'POST':
        resultDict={}
        try:
            json_data = json.loads(request.body)
            idQuery=json_data["id"]
        except:
            resultDict["response"]="incorrect JSON"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        if(type(idQuery) is list):
            query=Person.objects.filter(id__in=json_data["id"])
        else:
            query=Person.objects.filter(id=json_data["id"])
        result=[entry.json() for entry in query] 
        resultDict["response"]="success"
        resultDict["query"]=result
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
    else:
        resultDict["response"]="wrong method"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
@csrf_exempt
def getPostById(request):
    if request.method == 'POST':
        resultDict={}
        try:
            json_data = json.loads(request.body)
            idQuery=json_data["id"]
        except:
            resultDict["response"]="incorrect JSON"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        if(type(idQuery) is list):
            query=Post.objects.filter(id__in=json_data["id"])
        else:
            query=Post.objects.filter(id=json_data["id"])
        result=[entry.json() for entry in query] 
        resultDict["response"]="success"
        resultDict["query"]=result
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
    else:
        resultDict["response"]="wrong method"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
@csrf_exempt
def createPerson(request):
    if request.method == 'POST':
        resultDict={}
        try:
            json_data = json.loads(request.body)
            person=Person(login=json_data["login"],password=json_data["password"])
        except:
            resultDict["response"]="incorrect JSON"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        person.save()
        query=Person.objects.filter(id=person.id)
        result=[entry.json() for entry in query] 
        resultDict["response"]="success"
        resultDict["query"]=result
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
    else:
        resultDict["response"]="wrong method"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
@csrf_exempt
def createPost(request):
    if request.method == 'POST':
        resultDict={}
        try:
            json_data = json.loads(request.body)
            post=Post(text=json_data["text"],author_id=json_data["author_id"])
        except:
            resultDict["response"]="incorrect JSON"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        try:
            post.save()
        except:
            resultDict["response"]="author does not exist"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        query=Post.objects.filter(id=post.id)
        result=[entry.json() for entry in query]
        resultDict["response"]="success"
        resultDict["query"]=result
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
    else:
        resultDict["response"]="wrong method"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
def updatePerson(person, login, password):
    if(login!=None):
        person.login=login
    if(password!=None):
        person.password=password
    person.save()
    query=Person.objects.filter(id=person.id)
    result=[entry.json() for entry in query] 
    return result
@csrf_exempt
def editPerson(request):
    if request.method == 'POST':
        resultDict={}
        try:
            json_data = json.loads(request.body)
            id=json_data["id"]
        except:
            resultDict["response"]="incorrect JSON"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        try:
            person=Person.objects.get(id=id)
            login=json_data.get("login",None)
            password=json_data.get("password",None)
        except:
            resultDict["response"]="person does not exist"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        result=updatePerson(person, login, password) 
        resultDict["response"]="success"
        resultDict["query"]=result
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
    else:
        resultDict["response"]="wrong method"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))

@csrf_exempt
def editPost(request):
    if request.method == 'POST':
        resultDict={}
        try:
            json_data = json.loads(request.body)
            id=json_data["id"]
        except:
            resultDict["response"]="incorrect JSON"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        try:
            post=Post.objects.get(id=id)
            text=json_data.get("text",None)
            if(text!=None):
                post.text=text
        except:
            resultDict["response"]="post does not exist"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        try:
            author_id=json_data.get("author_id",None)
            if(author_id!=None):
                author=Person.objects.get(id=author_id)
                if(author!=None):
                    post.author_id=author_id
            post.save()
        except:
            resultDict["response"]="author does not exist"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))

        query=Post.objects.filter(id=post.id)
        result=[entry.json() for entry in query]
        resultDict["response"]="success"
        resultDict["query"]=result
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
    else:
        resultDict["response"]="wrong method"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
@csrf_exempt
def deletePerson(request):
    if request.method == 'POST':
        resultDict={}
        try:
            json_data = json.loads(request.body)
            idQuery=json_data["id"]
        except:
            resultDict["response"]="incorrect JSON"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        if(type(idQuery) is list):
            query=Person.objects.filter(id__in=json_data["id"])
            if(len(query)==0):
                resultDict["response"]="post does not exist"
                return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
            Person.objects.filter(id__in=json_data["id"]).delete()
        else:
            query=Person.objects.filter(id=json_data["id"])
            if(len(query)==0):
                resultDict["response"]="post does not exist"
                return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
            Person.objects.filter(id=json_data["id"]).delete()
        resultDict["response"]="success"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
    else:
        resultDict["response"]="wrong method"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
@csrf_exempt
def deletePost(request):
    if request.method == 'POST':
        resultDict={}
        try:
            json_data = json.loads(request.body)
            idQuery=json_data["id"]
        except:
            resultDict["response"]="incorrect JSON"
            return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
        if(type(idQuery) is list):
            query=Post.objects.filter(id__in=json_data["id"])
            if(len(query)==0):
                resultDict["response"]="post does not exist"
                return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
            Post.objects.filter(id__in=json_data["id"]).delete()
        else:
            query=Post.objects.filter(id=json_data["id"])
            if(len(query)==0):
                resultDict["response"]="post does not exist"
                return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
            Post.objects.filter(id=json_data["id"]).delete()
        resultDict["response"]="success"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))
    else:
        resultDict["response"]="wrong method"
        return HttpResponse(json.dumps(resultDict, ensure_ascii=False).encode('utf8'))