from flask import Flask, request, Response
import json
import os
import logging
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import secrets_secrets
import slack_message_builder
import ssl as ssl_lib
import certifi

# init flask app to host the events adapter
app = Flask(__name__)
app.config['TESTING'] = True

# TODO: You must change this to use ENV instead of a secret file.  AWS will let you do that.
slack_events_adapter = SlackEventAdapter(secrets_secrets.secrets['signing_secret'], "/slack/events", app)
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

# init web client
slack_web_client = WebClient(token=secrets_secrets.secrets["bot_access_token"])
birthday_message_sent = {}


def send_birthday_message(channel: str):
    builder = slack_message_builder.SlackClientMessageBuilder("mandatory_fun")
    message = builder.get_message_payload()
    resp = slack_web_client.chat_postMessage(**message)
    print(json.dumps(resp))
    if channel not in birthday_message_sent:
        birthday_message_sent[channel] = {}


@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    if emoji is ":teferi:":
        send_birthday_message('mandatory_fun')
    print(emoji)


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)))
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
