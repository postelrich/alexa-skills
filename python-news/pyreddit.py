from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import unidecode

app = Flask(__name__)
ask = Ask(app, '/')


def get_headlines():
    url = 'https://reddit.com/r/python/.json?limit=20'
    r = requests.get(url)
    if not r.ok:
        print(r.status)
        return statement('Error retrieving python headlines.')
    titles = [unidecode.unidecode(listing['data']['title']) for listing in r.json()['data']['children'] if listing['data']['author'] != 'AutoModerator']
    titles = '... '.join(titles[:10])
    return statement(titles)


@ask.launch
def start_skill():
    msg = "Would you like to hear what's new in python?"
    return question(msg)


@ask.intent("YesIntent")
def share_headlines():
    return get_headlines()


@ask.intent("NoIntent")
def exit():
    msg = "Why did you bother me then?"
    return statement(msg)


if __name__ == '__main__':
    app.run(debug=True)
