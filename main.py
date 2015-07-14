from flask import Flask, make_response, render_template, request
import logging
import json
import requests
import config
import random
import string

from google.appengine.ext import ndb

app = Flask(__name__)

CONTENT_TYPE = {'Content-Type': 'application/json;charset=UTF-8'}
LIFX_ENDPOINT = 'https://api.lifx.com/v1beta1'

from jinja2 import Template


class UserAuth(ndb.Model):
    user_id = ndb.StringProperty()
    pin = ndb.StringProperty()
    lifx_token = ndb.StringProperty()


def generate_response(output_speech, card_title="", card_subtitle="", card_content="", session_attributes={}, should_end_session=True):
    response = {
        "version": "1.0",
        "sessionAttributes": {
            "user": {
                "name": "nelson"
            }
        },
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": output_speech
            },
            "card": {
                "type": "Simple",
                "title": card_title,
                "subtitle": card_subtitle,
                "content": card_content
            },
            "shouldEndSession": should_end_session
        }
    }
    return json.dumps(response)

@app.route('/', methods=['GET'])
def get():
    template = Template(open("templates/home.html").read())
    response = template.render(token='token')
    return response


@app.route('/token', methods=['POST'])
def get_token():
    pin = request.form['pin']
    lifx_token = request.form['token']

    user_auth = UserAuth.query(UserAuth.pin == pin).get()
    if user_auth:
        user_auth.lifx_token = lifx_token
        user_auth.put()

        return "OK"
    else:
        return "Pin not found"


@app.route('/commands', methods=['POST'])
def post():
    logging.info(json.dumps(request.json, indent=4, sort_keys=False))

    response = ""

    try:
        action = request.json["request"]["intent"]["slots"]["action"]["value"]
    except TypeError:
        response = generate_response("Action not found.")
        return response, 200, CONTENT_TYPE

    logging.info("Action: %s" % action)

    user_id = request.json["session"]["user"]["userId"]

    logging.info("User_id: %s" % user_id)

    # Check if user we have a LIFx token for this user
    user_auth = UserAuth.query(UserAuth.user_id == user_id).get()

    if not user_auth or not user_auth.lifx_token:

        if not user_auth or not user_auth.pin:
            pin = ''.join(random.choice(string.digits) for _ in range(4))
            entry = UserAuth()
            entry.user_id = user_id
            entry.pin = pin
            entry.put()
        else:
            pin =user_auth.pin

        speech = """Hello! We need your LIFx token.
                    To authenticate please go to https://alexalightsapp.appspot.com
                    and enter pin: {}""".format(pin)

        response = generate_response(
            output_speech=speech,
            card_title="Alexa Lights",
            card_subtitle="Auth required",
            card_content=speech)

        logging.info(json.dumps(json.loads(response), indent=4, sort_keys=False))
        return response, 200, CONTENT_TYPE

    # Query API to convert name to Symbol
    if action == "on":
        response = requests.put(LIFX_ENDPOINT + '/lights/all/power', auth=(user_auth.lifx_token, ''), data={'state': 'on'}).json()

        if response and 'error' in response and response['error']:
            speech = response['error']
        else:
            speech = "Lights on"

    elif action == "off":
        response = requests.put(LIFX_ENDPOINT + '/lights/all/power', auth=(user_auth.lifx_token, ''), data={'state': 'off'}).json()

        if response and 'error' in response and response['error']:
            speech = response['error']
        else:
            speech = "Lights off"

    else:
        speech = "Action unknown"

    response = generate_response(
        output_speech=speech,
        card_title="Turn {} lights.".format(action),
        card_subtitle=speech,
        card_content="")

    logging.info(json.dumps(json.loads(response), indent=4, sort_keys=False))
    return response, 200, CONTENT_TYPE


if __name__ == '__main__':
    app.run()

