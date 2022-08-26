from xmlrpc.client import Server
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
import json
from .models import Collection, Movie, User
from .serializers import CollectionSerializer

# Create your views here.

def user(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        username = data["username"]
        password = data["password"]
        if User.objects.filter(username=username):
            return JsonResponse({"error":"User already exists"})
        else:
            user = User(username=username, password=password)
            user.save()
            return JsonResponse({"username": user.username})
            # todo: return access token

def movies(request):
    url = "https://demo.credy.in/api/v1/maya/movies/"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            movies = response.json()['results']
            for movie_data in movies:
                movie = Movie(title = movie_data['title'], description = movie_data['description'], genres = movie_data['genres'], uuid = movie_data['uuid'])
                movie.save()
            if response.json()['next'] == None:
                break
            else:
                url = response.json()['next']
        
    return HttpResponse("Success")

def collection(request):
    if request.method == "GET":
        data = Collection.objects.all().values()
        context = {
            "collections": list(data)
        }
        return JsonResponse(context)
    
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        title = data["title"]
        description = data["description"]
        collection = Collection(title=title, description=description)
        collection.save()
        return JsonResponse({"collection_uuid": collection.uuid})

def collection_detail(request, id):
    if request.method == "GET":
        try:
            data = Collection.objects.get(uuid=id)
            serializer = CollectionSerializer(data)
            return JsonResponse(serializer.data)
        except:
            return JsonResponse({"error": "uuid not found"})

    if request.method == "DELETE":
        try:
            data = Collection.objects.get(uuid=id)
            data.delete()
            return JsonResponse({"message": "collection deleted successfully"})
        except:
            return JsonResponse({"error": "uuid not found"})

def request_count(request):
    hit = request.session.get('hit')
    if not hit:
        request.session['hit'] = 1
    else: 
        request.session['hit'] += 1
    return JsonResponse({"requests": request.session['hit']})

def request_count_reset(request):
    request.session['hit'] = 0
    return JsonResponse({"message": "request count reset successfully"})