from flask import Flask, make_response, render_template, request
import logging
import json
import requests
import config

app = Flask(__name__)

CONTENT_TYPE = {'Content-Type': 'application/json;charset=UTF-8'}
LIFX_ENDPOINT = 'https://api.lifx.com/v1beta1'

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


@app.route('/', methods=['POST'])
def post():
    logging.info(json.dumps(request.json, indent=4, sort_keys=False))

    response = ""

    try:
        action = request.json["request"]["intent"]["slots"]["action"]["value"]
    except TypeError:
        response = generate_response("Action not found.")
        return response, 200, CONTENT_TYPE

    logging.info("Action: %s" % action)

    # Query API to convert name to Symbol
    if action == "on":
        response = requests.put(LIFX_ENDPOINT + '/lights/all/power', auth=config.AUTH, data={'state': 'on'}).json()

        if response and 'error' in response and response['error']:
            speech = response['error']
        else:
            speech = "Lights on"

    elif action == "off":
        response = requests.put(LIFX_ENDPOINT + '/lights/all/power', auth=config.AUTH, data={'state': 'off'}).json()

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

