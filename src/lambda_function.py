import boto3
import json
import decimal
from datetime import datetime
import inflect
from boto3.dynamodb.conditions import Key, Attr


inflect = inflect.engine()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Remembrall')


def lambda_handler(event, context):
    if event['request']['type'] == 'LaunchRequest':
        return launch_request_handler(event['request'], event['session'])
    elif event['request']['type'] == 'IntentRequest':
        return intent_handler(event['request'], event['session'])


def launch_request_handler(request_info, session_info):
    # LaunchIntent function
    session_attributes = {}
    card_title = "Remembrall"
    speech_output = "Hi Welcome to Remembrall"
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def intent_handler(request_info, session_info):
    # IntentRequest handler
    if request_info['intent']['name'] == 'StoreIntent':
        return store_intent_handler(request_info, session_info)
    elif request_info['intent']['name'] == 'ContinueIntent':
        return continue_intent_handler(request_info, session_info)
    elif request_info['intent']['name'] == 'RetrieveIntent':
        return retrieve_intent_handler(request_info, session_info)
    elif request_info['intent']['name'] = 'AMAZON.HelpIntent' :
        return handle_help_request()
    elif request_info['intent']['name'] == 'AMAZON.CancelIntent' or request_info['intent']['name'] == 'AMAZON.StopIntent':
        return handle_session_end_request()

def store_intent_handler(request_info, session_info):
    # StoreIntent handler
    session_attributes = {}
    card_title = "Remembrall"
    speech_output = "I have noted it down. Do you want me to note anything else"
    reprompt_text = ""
    should_end_session = False
    table_write(request_info, session_info)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def continue_intent_handler(request_info, session_info):
    # ContinueIntent handler
    try:
        request_info['intent']['slots']['false']['value']
        return handle_session_end_request()
    except:
        request_info['intent']['slots']['false']['value']
        store_intent_handler(request_info, session_info)


def retrieve_intent_handler(request_info, session_info):
    item = table_read(request_info, session_info)
    if(len(item) != 0):
        item = item[0]
        if (item['itemBool']):
            session_attributes = {}
            card_title = "Remembrall"
            speech_output = "It is " + item['location'] + '...Do you want to find anything else?'
            reprompt_text = ""
            should_end_session = False
        else:
            session_attributes = {}
            card_title = "Remembrall"
            speech_output = 'They are '  + item['location'] + ' <break time="2s"/> Do you want to find anything else?'
            reprompt_text = ""
            should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))
    else:
        session_attributes = {}
        card_title = "Remembrall"
        speech_output = 'Sorry, I do not have any details about it ' + ' <break time="2s"/> Do you want to find anything else?'
        reprompt_text = ""
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    session_attributes = {}
    card_title = "Remembrall"
    speech_output = 'Thank You for using remembrall. Bye'
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def table_write(request, session):
    # items is false item is true
    bool = False
    item = request['intent']['slots']['item']['value']
    if inflect.singular_noun(item) is False:
        bool = True
    table.put_item(
        Item={
            'userID': session['user']['userId'],
            'itemName': item,
            'itemBool': bool,
            'location': request['intent']['slots']['location']['value'],
            'loggedTime': str(datetime.utcnow().time()),
            'loggedDate': str(datetime.utcnow().date())
        }
    )


def table_read(request, session):
    item = request['intent']['slots']['item']['value']
    response = table.scan(FilterExpression=Attr('userID').eq(session['user']['userId']) & Attr('itemName').eq(item))
    item = response['Items']
    return(item)


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    # builds the speechlet response
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output,
            "ssml": "<speak>" + output + "</speak>"
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output,
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text,
            }
        },
        "shouldEndSession": should_end_session
    }


def build_response(session_attributes, speechlet_response):
    # returns the response json
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
