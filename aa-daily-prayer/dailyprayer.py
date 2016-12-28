from bs4 import BeautifulSoup
from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import unidecode

app = Flask(__name__)
ask = Ask(app, '/aa-prayer')


def get_aa_prayer():
    url = 'http://www.aa.org/pages/en_US/daily-reflection'
    r = requests.get(url)
    if not r.ok:
        print(r.status)
        return statement('Error retrieving daily prayer.')
    soup = BeautifulSoup(r.text, 'html.parser')
    msg = []
    msg.append(soup.find_all('div', {'class': 'daily-reflection-header-title'})[0].text)
    msg.append(soup.find_all('div', {'class': 'daily-reflection-header-content'})[0].text)
    msg.append(soup.find_all('div', {'class': 'daily-reflection-content-title'})[0].text)
    msg.append(soup.find_all('div', {'class': 'daily-reflection-content'})[0].text)

    msg = [unidecode.unidecode(m) for m in msg]
    msg = '... '.join(msg)
    print(msg)
    return statement(msg)


@ask.launch
def start_skill():
    msg = "Would you like to hear today's prayer?"
    return question(msg)


@ask.intent("YesIntent")
def share_headlines():
    return get_aa_prayer()


@ask.intent("NoIntent")
def exit():
    msg = "Goodbye."
    return statement(msg)


if __name__ == '__main__':
    app.run(debug=True)