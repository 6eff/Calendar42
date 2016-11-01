from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.conf import settings
# Create your views here.
import requests
import requests_cache
import json
from proxy.constants import BASE_URL
from proxy.constants import CACHE_NAME

requests_cache.install_cache(cache_name=CACHE_NAME, backend='memory', expire_after=42)

def retrieve_event(request):
    url = request.path
    event_id = url.split("/")[-2]
    if request.method == "GET":
        api_token = settings.API_TOKEN
        r_name = requests.get(BASE_URL + 'events/' + event_id, headers={'Authorization': 'Token ' + api_token})
        if r_name.status_code == 404:
            return HttpResponseNotFound('<h1>Incorrect event ID, please check correct ID</h1>')
        r_participants = requests.get(BASE_URL + "/event-subscriptions/?event_ids=[" + event_id + "]", headers={'Authorization': 'Token ' + api_token})
        name_dict = r_name.json()
        title = name_dict['data'][0]['title']
        participants_dict = r_participants.json()
        data = participants_dict['data']
        names = []
        for i, val in enumerate(data):
            names.append(val['subscriber']['first_name'])
        event = {'id': event_id, 'title': title, 'names': names}
        event_json = json.dumps(event)
        retrieve_event.cache = r_name.from_cache

    return render(request, 'index.html', {'event_json': event_json})
