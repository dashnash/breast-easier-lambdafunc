"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

import logging
from alexa import build_speechlet_response, build_response


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("event.session.application.applicationId=" +
                  event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.03df35c2-53f4-4120-9e96-30d5b05b9df4"):
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


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    logging.debug("on_session_started requestId=" + session_started_request['requestId']
                  + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    logging.debug("on_launch requestId=" + launch_request['requestId'] +
                  ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    logging.debug("on_intent requestId=" + intent_request['requestId'] +
                  ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "StartFeed":
        return start_feed(intent, session)
    elif intent_name == "EndFeed":
        return end_feed(intent, session)
    else:
        raise ValueError("Invalid intent")


def start_feed(intent, session):
    """ Records the start of the feed and side, and builds return message"""
    card_title = intent['name']
    side = intent['slots']['BreastSide']['value']
    speech_output = "Starting feeding on the {0} side. " \
                    "You are more than just a milk machine.".format(side)
    should_end_session = False

    return build_response({}, build_speechlet_response(card_title, speech_output, None,
                                                       should_end_session))


def end_feed(intent, session):
    """ Ends the feed and builds the return message"""
    card_title = intent['name']
    speech_output = "Thank you for tracking you're nursing with breast easier. " \
                    "Nice jugs, Stephanie."

    return build_response({}, build_speechlet_response(card_title, speech_output, None, True))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Breast Easier. " \
                    "Please start tracking a session by saying, " \
                    "Start nursing on my right or left side."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please start tracking a session by saying, " \
                    "Start nursing on my right or left side."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    logging.debug("on_session_ended requestId=" + session_ended_request['requestId'] +
                  ", sessionId=" + session['sessionId'])
    # add cleanup logic here



def main():
    pass


if __name__ == "__main__":
    main()