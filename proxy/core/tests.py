import django
django.setup()
from django.test import TestCase, RequestFactory

# Create your tests here.
# Third-party imports...
from nose.tools import assert_true, assert_is_not_none, assert_equal, assert_in, assert_false
from html2text import html2text
import unittest
import requests, requests_cache
from proxy import settings
from .views import retrieve_event
from proxy.constants import EVENT_ID
import time

def test_request_response():
    # Send a request to the API server and store the response.
    response = requests.get('https://demo.calendar42.com/api/v2/events/', headers={'Authorization': 'Token ' + settings.API_TOKEN})
    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok)

def test_retrieve_event():
    factory = RequestFactory()
    request = factory.get('/events-with-subscriptions/' + EVENT_ID + '/')
    # Call the service, which will send a request to the server.
    api_response = retrieve_event(request)

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(api_response)

def test_response_content():
    json_str = '{"names": ["API", "Michel", "Jasper", "Bob", "Dennis", "Edmon", "Aslesha","Lars"], "id": "7e578a8e918fcbb21b7e2af0ff6d9bac_14770339790223", "title":"Drink a cup of coffee with C42 Team"}'
    factory = RequestFactory()
    request = factory.get('/events-with-subscriptions/' + EVENT_ID + '/')
    api_response = retrieve_event(request)
    text = html2text(api_response.content).strip().replace('\n', '')
    assert_in(json_str, text)

def test_response_for_incorrect_event_id():
    factory = RequestFactory()
    request = factory.get('/events-with-subscriptions/' + '1234' + '/')
    api_response = retrieve_event(request)
    text = html2text(api_response.content).strip()
    assert_in('Incorrect event ID, please check correct ID', text)

def test_cached_response():
    factory = RequestFactory()
    request = factory.get('/events-with-subscriptions/' + EVENT_ID + '/')
    retrieve_event(request)
    assert_true(retrieve_event.cache)
    requests_cache.clear()
    retrieve_event(request)
    assert_false(retrieve_event.cache)
