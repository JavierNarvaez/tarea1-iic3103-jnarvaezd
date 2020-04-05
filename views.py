from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context 
import requests
from Tarea1.settings import BASE_DIR


def homepage(request): #la barra buscadora y todos los capitulos con ciertos datos (son link buttons)

    response_inicial = requests.get("https://rickandmortyapi.com/api/episode").json() #llama a la página 1
    num_pages = response_inicial["info"]["pages"]
    episodes = []

    for i in range(int(num_pages)):
        response = requests.get("https://rickandmortyapi.com/api/episode/?page=" + str(i+1)).json()
        for dicc in response['results']:
            episodes.append(dicc)
    

    home_template = open(BASE_DIR + "/Tarea1/Templates/home_temp.html")

    plt = Template(home_template.read())

    home_template.close()

    ctx = Context({"list_episodes": episodes, "total_episodes": len(episodes)}) 

    doc = plt.render(ctx)


    return HttpResponse(doc)

def episode(request, id): #sin id, url ni creación
    
    response = requests.get("https://rickandmortyapi.com/api/episode/" + str(id)).json()
    name = response['name']
    air_date = response['air_date']
    episode = response['episode']
    characters = response['characters'] #links para consultas API

    list_characters = []

    for ele in characters:
        response = requests.get(ele).json()
        list_characters.append(response)


    episode_template = open(BASE_DIR + "/Tarea1/episode_temp.html")

    plt = Template(episode_template.read())

    episode_template.close()

    ctx = Context({"name": name, "air_date": air_date, "episode": episode, "characters": list_characters})

    doc = plt.render(ctx)

    return HttpResponse(doc)

def character(request, id): #sin id, url ni creación. Con todos sus lugares y episodios

    response = requests.get("https://rickandmortyapi.com/api/character/" + str(id)).json()
    name = response["name"]
    status = response["status"]
    species = response["species"]
    ch_type = response["type"]
    gender = response["gender"]
    origin = response["origin"]
    location = response["location"]
    image = response["image"]  #url
    episode = response["episode"]  #lista con los url de cada episodio
    last_location =  requests.get(location['url']).json()
    if origin['url'] != "":
        origin_location = requests.get(origin['url']).json()
    else:
        origin_location = "Es un lugar con name unkwown"

    list_episodes = []
    for ele in episode:
        response = requests.get(ele).json()
        list_episodes.append(response)


    character_template = open(BASE_DIR + "/Tarea1/character_temp.html")

    plt = Template(character_template.read())

    character_template.close()

    ctx = Context({"name": name, "status": status, "species": species, "ch_type": ch_type, "gender": gender, "origin": origin_location,
    "location": last_location, "image": image, "episodes": list_episodes}) 

    doc = plt.render(ctx)

    return HttpResponse(doc)

def location(request, id):
    response = requests.get("https://rickandmortyapi.com/api/location/" + str(id)).json()
    name = response["name"]
    loc_type = response["type"]
    dimension = response["dimension"]
    residents = response["residents"]

    list_residents = []
    for ele in residents:
        response = requests.get(ele).json()
        list_residents.append(response)

    location_template = open(BASE_DIR + "/Tarea1/location_temp.html")

    plt = Template(location_template.read())

    location_template.close()

    ctx = Context({"name": name, "loc_type": loc_type, "dimension": dimension, "residents": list_residents}) 

    doc = plt.render(ctx)

    return HttpResponse(doc)
    
def search(request): #iterar sobre las pages
    query = request.GET["query_input"]
    aux_query = "?name=" + query

    response_episodes_inicial = requests.get("https://rickandmortyapi.com/api/episode/" + aux_query).json()
    episodes = []
    if "error" not in response_episodes_inicial.keys():
        proximo = "https://rickandmortyapi.com/api/episode/" + aux_query
        while proximo != "":
            response_episodes = requests.get(proximo).json()
            for dicc in response_episodes['results']:
                episodes.append(dicc)
            proximo = response_episodes['info']['next']


    response_characters_inicial = requests.get("https://rickandmortyapi.com/api/character/" + aux_query).json()
    characters = []
    if "error" not in response_characters_inicial:
        proximo = "https://rickandmortyapi.com/api/character/" + aux_query
        while proximo != "":
            response_characters = requests.get(proximo).json()
            for dicc in response_characters['results']:
                characters.append(dicc)
            proximo = response_characters['info']['next']
    

    response_locations_inicial = requests.get("https://rickandmortyapi.com/api/location/" + aux_query).json()
    locations = []
    if "error" not in response_locations_inicial:
        proximo = "https://rickandmortyapi.com/api/location/" + aux_query
        while proximo != "":
            response_locations = requests.get(proximo).json()
            for dicc in response_locations['results']:
                locations.append(dicc)
            proximo = response_locations['info']['next']

    search_template = open(BASE_DIR + "/Tarea1/search_temp.html")

    plt = Template(search_template.read())

    search_template.close()

    ctx = Context({"query": query, "episodes": episodes, "characters": characters, "locations": locations}) 

    doc = plt.render(ctx)

    return HttpResponse(doc)

    