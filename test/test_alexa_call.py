import logging
import unittest
from test import BaseTestCase

class TestPostFromAlexa(BaseTestCase):
    def test_turn_on(self):
        request_body = {
            "session": {
                "new": True,
                "sessionId": "amzn1.echo-api.session.8dd5e3cc-b0e9-4dc4-9e78-cb7c76a07c44",
                "user": {
                    "userId": "amzn1.account.AHSMN72XJPRTGNUUYRUDD7EINGYQ"
                }
            },
            "version": "1.0",
            "request": {
                "intent": {
                    "slots": {
                        "action": {
                            "name": "action",
                            "value": "on"
                        }
                    },
                    "name": "turn"
                },
                "type": "IntentRequest",
                "requestId": "amzn1.echo-api.request.68c848f5-c3b0-4b74-9016-a8caf6333b3a"
            }
        }

        response = self.app.post_json('/', request_body)
        self.assertEqual(response.status, "200 OK")
        self.assertNotEqual(response.json_body, None)
        self.assertNotEqual(response.json_body["response"]["outputSpeech"]["text"], "")

    def test_turn_off(self):
        request_body = {
            "session": {
                "new": True,
                "sessionId": "amzn1.echo-api.session.8dd5e3cc-b0e9-4dc4-9e78-cb7c76a07c44",
                "user": {
                    "userId": "amzn1.account.AHSMN72XJPRTGNUUYRUDD7EINGYQ"
                }
            },
            "version": "1.0",
            "request": {
                "intent": {
                    "slots": {
                        "action": {
                            "name": "action",
                            "value": "off"
                        }
                    },
                    "name": "turn"
                },
                "type": "IntentRequest",
                "requestId": "amzn1.echo-api.request.68c848f5-c3b0-4b74-9016-a8caf6333b3a"
            }
        }

        response = self.app.post_json('/', request_body)
        self.assertEqual(response.status, "200 OK")
        self.assertNotEqual(response.json_body, None)
        self.assertNotEqual(response.json_body["response"]["outputSpeech"]["text"], "")

