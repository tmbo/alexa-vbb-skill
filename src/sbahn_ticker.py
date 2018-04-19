#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from src import utils
from src import vbb
from src import speech


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = ("Die S-Bahn lässt grüßen. "
                     "Frage nach der nächsten Abfahrt, zum Beispiel mit: "
                     "'Alexa, frage bahn info wann die nächste bahn fährt'")
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Bitte frage doch nach der nächsten Bahnfahrt."
    should_end_session = False
    return speech.response(session_attributes, card_title, speech_output,
                           reprompt_text, should_end_session)


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Sänk you for traveling wis se S-Bahn!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return speech.response({}, card_title, speech_output,
                           None, should_end_session)


def set_station_in_session(intent, session):
    """Sets the station in the session and prepares the speech to reply."""

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'station_name' in intent['slots']:
        station_name = intent['slots']['station_name']['value']
        session_attributes = {"station_name": station_name}
        speech_output = "Ok, deine Station " + \
                        station_name + \
                        " ist gespeichert. Du kannst mich nach dem nächsten " \
                        "Zug fragen indem du folgendes sagst: " \
                        "wann kommt der nächste zug?"
        reprompt_text = "Du kannst mich nach dem nächsten Zug fragen indem du " \
                        "" \
                        "" \
                        "" \
                        "folgendes sagst: " \
                        "wann kommt der nächste zug?"
    else:
        speech_output = "Ich habe deine Station nicht verstanden. " \
                        "Bitte versuche es noch einmal."
        reprompt_text = "Ich habe deine Station nicht verstanden. " \
                        "Bitte sag mir deine Station, indem du zum Beispiel " \
                        "folgendes sagest: " \
                        "meine station ist griebnitzsee"
    return speech.response(session_attributes, card_title, speech_output,
                           reprompt_text, should_end_session)


def next_train_speech_output():
    station = "Griebnitzsee"
    departures = vbb.fetch_next_trains_for_stop()
    formatted_departures = utils.voice_join([
        "{} nach {} in {}".format(
                d["name"], d["direction"], utils.wait_time_str(d["time"]))
        for d in departures
    ])
    if len(departures) == 1:
        return "Von {} fährt: {}.".format(
                station, formatted_departures)
    elif len(departures) > 1:
        return "Von {} fahren: {}.".format(
                station, formatted_departures)
    else:
        return "Entschuldige, ich konnte keine Abfahrten finden."


def get_next_train(intent, session):
    session_attributes = {}
    reprompt_text = None

    speech_output = next_train_speech_output()
    should_end_session = True
    # if session.get('attributes', {}) and "station_name" in session.get(
    #         'attributes', {}):
    #
    #     should_end_session = True
    # else:
    #     speech_output = "Ich weiß nicht was deine Station ist. " \
    #                     "Bitte teile mir zuerst deine S-Bahn station mit."
    #     should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return speech.response(session_attributes, intent['name'], speech_output,
                           reprompt_text, should_end_session)


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    if session.get('attributes', {}) and "station_name" in session.get(
            'attributes', {}):
        return get_next_train()
    else:
        return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "set_station":
        return set_station_in_session(intent, session)
    elif intent_name == "request_train":
        return get_next_train(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == \
            "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """

    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.a15c6fcd-13de-4d4e-bb9a-46759f860fb6"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


if __name__ == '__main__':
    logging.basicConfig(level="DEBUG")
    print(next_train_speech_output())
    print(vbb.fetch_stops_by_name("Berlin"))
