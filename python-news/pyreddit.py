from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import unidecode

app = Flask(__name__)
ask = Ask(app, '/')


def get_headlines(retry=False):
    url = 'https://reddit.com/r/python/.json?limit=20'
    r = requests.get(url)
    if not r.ok:
        if retry:
            return get_headlines()
        return statement('Error retrieving python headlines.')
    titles = [unidecode.unidecode(listing['data']['title']) for listing in r.json()['data']['children'] if listing['data']['author'] != 'AutoModerator']
    titles = '... '.join(titles[:10])
    return statement(titles)


@ask.launch
def start_skill():
    msg = "Would you like to hear what's new in python?"
    return question(msg)


@ask.intent("AMAZON.YesIntent")
def share_headlines():
    return get_headlines(retry=True)


@ask.intent("GetNewsIntent")
def get_news_headlines():
    return get_headlines(retry=True)


@ask.intent("AMAZON.NoIntent")
def exit():
    msg = "Why did you bother me then?"
    return statement(msg)


@ask.intent('AMAZON.HelpIntent')
def help():
    msg = "You can ask Python news for the latest news, or, you can say exit. What can I help you with?"
    return question(msg).reprompt(msg)


@ask.intent('AMAZON.StopIntent')
def stop():
    msg = "Goodbye"
    return statement(msg)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    msg = "Goodbye"
    return statement(msg)


@ask.session_ended
def session_ended():
    return "", 200
