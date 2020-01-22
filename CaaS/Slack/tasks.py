from celery.decorators import task

from .models import SlackRequest
from .utils import send_message_to_slack, dict_to_message
from ssc import Company
from Connector.models import SSCConnector

@task
def respond_to_slack_message(request_id):
    request = SlackRequest.objects.get(id=request_id)
    valid_messages = ['overall', 'factor']
    ss_connect  = SSCConnector.objects.filter(id = request.installation.source_id.id).first()
    if not request.is_complete:
        if request.message not in valid_messages:
            send_message_to_slack(
                token=request.installation.auth_token,
                channel=request.channel,
                message="Sorry. Invalid command.",
            )
            return None

        company = Company(
            access_key=ss_connect.api_token,
            domain=ss_connect.domain,
        )

        scores = company.get_overall_score()

        message = dict_to_message(scores[0])
        # message = "hii"

        send_message_to_slack(
            token=request.installation.auth_token,
            channel=request.channel,
            message=message,
        )
        request.is_complete = True
        request.save()
