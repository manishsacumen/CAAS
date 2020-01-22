from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import SSForm
from .models import SSCConnector
from django.contrib import messages
from ssc.scorecard import Company
from django.contrib.auth.models import User
from Jira import views, models
from Slack.utils import send_message_to_slack, dict_to_message
from Slack.models import  Slack
from ssc.main import collect_events


def home_manish(request):
    if request.method == 'POST':
        form = SSForm(request.POST)
        if form.is_valid():

            form.save()
    else:
        form = SSForm()
    return render(request, 'dashboard/ssc.html', {'form': form})


def home(request):
    if request.POST:
        current_user = request.user
        ssc_data = request.POST.dict()
        interval = ssc_data.get('interval')
        api_url = ssc_data.get('api_url')
        api_token = ssc_data.get('api_token')
        overall_score = ssc_data.get('overall_score')
        factor_score = ssc_data.get('factor_score')
        issue_level_event = ssc_data.get('issue_level')
        domain = ssc_data.get('domain')
        # import pdb; pdb.set_trace()
        new_ssc = SSCConnector(user_id= current_user, interval=interval, api_url=api_url, api_token=api_token, overall_score=overall_score, 
                                factor_score=factor_score, issue_level_event=issue_level_event, domain=domain)
        new_ssc.save()
        messages.success(request, f'Your SecurityScore Card is Registered')
        return redirect('/home/')
    return render(request, 'dashboard/dashboard.html')


def process_ssc(request):

    current_user = request.user
    jira_user = models.Jira.objects.filter(user_id=request.user).first()
    url, username, api_token = jira_user.app_url, jira_user.email_id, jira_user.api_key
    jira_obj = views.Connector(url, username, api_token)
    ssc_user = SSCConnector.objects.filter(user_id=request.user).first()
    if ssc_user:
        access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
        sc_obj = Company(access_key, domain)
        config_date = {"from_date":"2020-01-04", "to_date":"2020-01-06"}
        response = sc_obj.get_overall_score(**config_date)
        print(response)
        payload = {
            "fields": {
                "project":
                    {
                        "key": "FIR"
                    },
                "summary": "Security Scorecard Issue Created by Manish.",
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {"type": "paragraph", "content":
                            [{"type": "text", "text": "Description for the issue"}]
                         }
                    ]
                },
                "issuetype": {
                    "name": "Bug"
                }
            }
        }
        import pdb
        pdb.set_trace()
        # jira_resp = jira_obj.create_issue(**payload)
        slck = Slack.objects.filter(source_id = ssc_user.id).first()
        if slck:
            send_message_to_slack(token = slck.auth_token, channel = slck.default_channel, message = response[0],)



def ssc_test(request):
    token = request.POST.get('api_token',None)
    domain = request.POST.get('domain',None)
    sc_response = collect_events(token, domain)
    if sc_response:
        return HttpResponse("Success")




# class SaveSSC(TemplateView):
#     # import pdb
#     # pdb.set_trace()
#     template_name = "dashboard/ssc.html"
#
#     def post(self, request):
#         # import pdb
#         # pdb.set_trace()
#         if request.method == 'POST':
#             import pdb
#             pdb.set_trace()
#             form = SSForm(request.POST)
#             if form.is_valid():
#                 # import pdb
#                 # pdb.set_trace()
#                 print("Successfully validated.")
#                 form.save()
#                 # pass  # does nothing, just trigger the validation
#         else:
#             form = SSForm()
#             form = {}
#         return super(TemplateView, self).render_to_response(form)


