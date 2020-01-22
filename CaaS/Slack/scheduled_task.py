from celery import shared_task
from ssc import Company


@shared_task
def send_scheduled_alert():
    from .models import Slack
    from .utils import send_message_to_slack, dict_to_message

    print("Started")

    installations = Slack.objects.filter(is_active=True)
    for installation in installations:
        company = Company(
            access_key=installation.api_key,
            domain=installation.domain,
        )

        scores = company.get_overall_score()

        message = dict_to_message(scores[0])

        send_message_to_slack(
            token=installation.auth_token,
            channel=installation.default_channel,
            message=message,
        )
