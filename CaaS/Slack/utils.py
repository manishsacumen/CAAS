import requests

from django.template.loader import render_to_string


def send_message_to_slack(token, channel, message):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    if isinstance(message, dict):
        message = dict_to_message(message)
    data = {
        'channel': channel,
        'text': message,
        'as_bot': True,
    }

    response = requests.post(url, data=data, headers=headers)

    return response


def dict_to_message(data):
    message = render_to_string('formats/overall_score.txt', data)
    return message
