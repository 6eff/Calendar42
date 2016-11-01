## Calendar42

Project uses Django 1.10.2

*
Idea was to use minimal setup and libraries to get things done.
As test requires basically just getting some information from an external API and making minimal changes to it rendering it back to a user, all minimal logic was done in the views. However it's still a reusable app.
Combined API response is fairly small data, thus memory was used as caching endpoint. I've decided that easiest of available alternatives would be using `requests_cache`.
`Nose` was used for testing as most documented framework, imo.
For development `virtualenv` was used, as easiest tool for setting environments, imo.
*

#### Setup
- clone this repo
- cd in `proxy42api`
- install `pip`
- set your python environment, activate it `$ source $ENV/bin/activate`
- use `requirements.txt` to install needed packages `$ pip install -r requirements.txt`
- fire up the server `$ python manage.py runserver`
- navigate to `http://127.0.0.1:8000/events-with-subscriptions/$EVENT_ID/`, depending on which ip and port your server is running. You should see combined response from calendar42 API with event ID, TITLE and participants.
- ##### to get correct results from calendar42 API you'll have to get your API token and export it to your environment

#### Testing
- ensure you're in root directory
- execute `$ nosetests --verbosity=2 proxy` (verbosity used to visualize which tests where executed and results of each test)

In case of any problems with the code, please contact me directly.
