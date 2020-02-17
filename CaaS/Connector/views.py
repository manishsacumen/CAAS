from django.shortcuts import render, redirect, HttpResponse
import json
from django.shortcuts import render
from .config import payload
from .models import SSCConnector
from django.contrib import messages
from ssc.main import collect_events
from Jira import views, models
from Slack.utils import send_message_to_slack
from django.contrib.auth.decorators import login_required
from Slack.models import Slack
from Splunk.models import Splunk
from Splunk.splunk import SplunkEvents
from Rapid7.models import Rapid
from Rapid7.rapidseven import Rapidseven
from ServiceNow.models import Servicenowmodel
from ServiceNow.servicenow import ServiceNowEvents
from Freshdesk.models import Freshdeskmodel
from Freshdesk.freshdesk import FreshdeskEvents
from ZOHO.models import Zohomodel
from ZOHO.zohodesk import ZohodeskEvents
from Pagerduty.models import Pagerdutymodel
from Pagerduty.pagerduty import Pagerdutyincident
from Opsgenie.models import Opsgeniemodel
from Opsgenie.opsgenie import Opsgenieincident
from Zendesk.models import Zendeskmodel
from Zendesk.zendesk import Zendesktickets
from Jitbit.models import Jitbitmodel
from Jitbit.jitbit  import Jitbitticket
import datetime
import logging
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Connector(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def post(self, request):
        try:
            current_user = request.user
            ssc_data = request.POST.dict()
            interval = ssc_data.get('interval')
            api_url = ssc_data.get('api_url')
            api_token = ssc_data.get('api_token')
            overall_score = ssc_data.get('overall_score')
            factor_score = ssc_data.get('factor_score')
            issue_level_event = ssc_data.get('issue_level')
            domain = ssc_data.get('domain')
            try:
                ssc_obj = SSCConnector.objects.filter(user_id = request.user).first()
            except Exception as err:
                logger.error(" Exceptional error%s ", err)
            else:
                if not ssc_obj:
                    new_ssc = SSCConnector(user_id=current_user, interval=interval, api_url=api_url, api_token=api_token,
                                        overall_score=overall_score,
                                        factor_score=factor_score, issue_level_event=issue_level_event, domain=domain)
                    new_ssc.save()
                    logger.info("Your SecurityScoreCard is Registered%s ", request.user.email)
                    messages.success(request, f'Your SecurityScoreCard is Registered')
                else:
                    ssc_obj.interval = interval
                    ssc_obj.api_url = api_url
                    ssc_obj.api_token = api_token
                    ssc_obj.overall_score = overall_score
                    ssc_obj.factor_score = factor_score
                    ssc_obj.issue_level_event =issue_level_event
                    ssc_obj.domain = domain
                    ssc_obj.save()
                    logger.info("Your SecurityScoreCard is updated successfully%s ", request.user.email)
                    messages.success(request, f'Your SecurityScoreCard is Updated Successfully')
            return redirect('/ssc_connector/ssc/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e


@login_required(login_url='/login/')
def dashboard(request):
    try:
        current_user = request.user
        ssc_data =  SSCConnector.objects.filter(user_id = current_user).first()
        slack_data  =  Slack.objects.filter(source_id =  ssc_data).first()
        jira_data = models.Jira.objects.filter(user_id = current_user).first()
        splunk_data  =  Splunk.objects.filter(source_id =  ssc_data).first()
        servicenow_data  =  Servicenowmodel.objects.filter(source_id =  ssc_data).first()
        rapid_data  =  Rapid.objects.filter(source_id =  ssc_data).first()
        freshdesk_data  =  Freshdeskmodel.objects.filter(source_id =  ssc_data).first()
        zohodesk_data  =   Zohomodel.objects.filter(source_id = ssc_data).first()
        pagerduty_data  =  Pagerdutymodel.objects.filter(source_id = ssc_data).first()
        opsgenie_data  =   Opsgeniemodel.objects.filter(source_id = ssc_data).first()
        zendesk_data  =   Zendeskmodel.objects.filter(source_id = ssc_data).first()
        jitbit_data  =   Jitbitmodel.objects.filter(source_id = ssc_data).first()
        logger.info("Dashboard loaded successfully%s ", request.user.email)
        return render(request, 'dashboard/home.html',context={'ssc_data':ssc_data,
                                             'jira_data':jira_data,
                                              'slack_data':slack_data,
                                              'splunk_data':splunk_data, 
                                              'servicenow_data': servicenow_data, 
                                              'rapid_data': rapid_data,
                                              'freshdesk_data': freshdesk_data,
                                              'zohodesk_data': zohodesk_data,
                                              'pagerduty_data' : pagerduty_data,
                                              'opsgenie_data':opsgenie_data,
                                              'zendesk_data':zendesk_data,
                                              'jitbit_data': jitbit_data})
    except Exception as e:
        logger.error("Unexpected Exception occured: %s ", e)
        return e

@login_required(login_url='/login/')
def process_ssc(request, flag_name):
    try:
        ssc_user = SSCConnector.objects.filter(user_id=request.user).first()
        slack_user = Slack.objects.filter(source_id__user_id=request.user).first()
        jira_user = models.Jira.objects.filter(user_id=request.user).first()
        splunk_user =  Splunk.objects.filter(source_id__user_id=request.user).first()
        rapid_user  =  Rapid.objects.filter(source_id__user_id =  request.user).first()
        servicenw_user  =  Servicenowmodel.objects.filter(source_id__user_id =  request.user).first()
        freshdesk_user  =  Freshdeskmodel.objects.filter(source_id__user_id =  request.user).first()
        zohodesk_user  =  Zohomodel.objects.filter(source_id__user_id =  request.user).first()
        pagerduty_user  =  Pagerdutymodel.objects.filter(source_id__user_id =  request.user).first()
        opsgenie_user  =   Opsgeniemodel.objects.filter(source_id__user_id =  request.user).first()
        zendesk_user  =   Zendeskmodel.objects.filter(source_id__user_id =  request.user).first()
        jitbit_user  =   Jitbitmodel.objects.filter(source_id__user_id =  request.user).first()
        slack_flag = slack_user and slack_user.flag
        jira_flag = jira_user and jira_user.flag
        ssc_flag = ssc_user and ssc_user.flag
    except Exception as err:
        print("Getting exception as {}".format(err))
    else:
        if not ssc_flag:
            # To do: disable jira and slack
            pass
        else:
            if not jira_user and not slack_user:
                logger.info("Jira and slack is deactivated%s ", request.user.email)
                # return messages.warning(request, f'No app is configured.. Please configure at least one..!!')
                pass
            if jira_flag and flag_name =='Jira':
                url, username, api_token, options_str = jira_user.app_url, jira_user.email_id, jira_user.api_key, jira_user.jira_config
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                jira_obj = views.Connector(url, username, api_token)
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                sc_jira_response = collect_events(access_key, domain, **options)
                data = process_ssc_response(sc_jira_response)
                logger.info("Jira is start creating issues%s ", request.user.email)
                for each_record in data:
                    current_time = str(datetime.datetime.now())
                    msg = "New SecurityScorecard Issue is reported on {}.".format(current_time)
                    payload["fields"]["summary"] = msg
                    payload["fields"]['description']['content'][0]['content'][0]['text'] = json.dumps(each_record[0])
                    jira_resp = jira_obj.create_issue(**payload)
                else:
                    pass
            if slack_flag and flag_name =='Slack':
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                options_str = slack_user.config
                options_formatted = options_str.replace("'", '"')
                optionss = json.loads(options_formatted)
                sc_slack_response = collect_events(access_key, domain, **optionss)
               
                data = process_ssc_response(sc_slack_response)
                logger.info("to Slack is start sending messages%s ", request.user.email)
                for each_record in data:
                    send_message_to_slack(token=slack_user.auth_token, channel=slack_user.default_channel, message=each_record[0])
            if splunk_user.flag  and flag_name == 'Splunk':
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                url, token, config = splunk_user.api_url, splunk_user.hec_token, splunk_user.config
                options_formatted = config.replace("'", '"')
                options = json.loads(options_formatted)
                sc_splunk_response = collect_events(access_key, domain, **options)
                data = process_ssc_response(sc_splunk_response)
                splunk_obj  =  SplunkEvents(token,url)
                sp = dict()
                for each_record in data:
                    current_time = str(datetime.datetime.now())
                    sp['event'] = json.loads(json.dumps(each_record[0]))
                    splunk_resp = splunk_obj.create_event(json.dumps(sp))
                    print(splunk_resp.json())
            if rapid_user.flag  and flag_name == 'Rapid':
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                url, token, options_str   = rapid_user.url, rapid_user.api_key, rapid_user.config
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                rapid_obj =  Rapidseven(url, token)
                rapid_response = collect_events(access_key, domain, **options)
                data = process_ssc_response(rapid_response)
                for each_record in data:
                    rapid_resp = rapid_obj.create_log(each_record[0])
            if servicenw_user.flag  and flag_name == 'ServiceNow':
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                url, username, password, options_str   = servicenw_user.url, servicenw_user.username, servicenw_user.password, servicenw_user.config
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                snw_obj =  ServiceNowEvents(url, username, password)
                snw_response = collect_events(access_key, domain, **options)
                data = process_ssc_response(snw_response)
                for each_record in data:
                    snw_resp = snw_obj.create_incident(**each_record[0])
            if freshdesk_user.flag  and flag_name == 'Freshdesk':
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                url, username, api_key, options_str   = freshdesk_user.url, freshdesk_user.username, freshdesk_user.api_key, servicenw_user.config
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                fresh_obj =  FreshdeskEvents(username, api_key, url)
                fresh_response = collect_events(access_key, domain, **options)
                data = process_ssc_response(fresh_response)
                for each_record in data:
                    fresh_resp = fresh_obj.create_ticket(**each_record[0])
            if zohodesk_user.flag  and flag_name == 'Zohodesk':
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                token, contact_id, department_id, org_id, options_str   = zohodesk_user.token, zohodesk_user.contact_id,zohodesk_user.department_id,zohodesk_user.org_id,  zohodesk_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                fresh_obj =  ZohodeskEvents(contact_id,department_id,token,org_id)
                fresh_response = collect_events(access_key, domain, **options)
                data = process_ssc_response(fresh_response)
                for each_record in data:
                    fresh_resp = fresh_obj.create_ticket(**each_record[0])
            if pagerduty_user.flag  and flag_name == 'Pagerduty':
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                email, api_key, service_id, options_str   = pagerduty_user.email, pagerduty_user.api_key,pagerduty_user.service_id, pagerduty_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                pagerduty_obj =  Pagerdutyincident(email, api_key,  service_id)
                pagerduty_response = collect_events(access_key, domain, **options)
                data = process_ssc_response(pagerduty_response)
                for each_record in data:
                    fresh_resp = pagerduty_obj.create_incident(str(each_record[0]))
            if opsgenie_user.flag  and flag_name == 'Opsgenie':
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                api_key, service_id, options_str   = opsgenie_user.api_key,opsgenie_user.service_id, opsgenie_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                opsgenie_obj = Opsgenieincident(api_key,  service_id)
                opsgenie_response = collect_events(access_key, domain, **options)
                data = process_ssc_response(opsgenie_response)
                for each_record in data:
                    opsgenie_resp = opsgenie_obj.create_incident(str(each_record[0]))
            if zendesk_user.flag  and flag_name == 'Zendesk':
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                api_key, email, url,  options_str   = zendesk_user.api_key,zendesk_user.email, zendesk_user.url, zendesk_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                zendesk_obj = Zendesktickets(email, api_key, url)
                zendesk_response = collect_events(access_key, domain, **options)
                data = process_ssc_response(zendesk_response)
                for each_record in data:
                    zendesk_resp = zendesk_obj.create_tickets(str(each_record[0]))
            if jitbit_user.flag  and flag_name == 'Jitbit':
                access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
                email, password, url, categoryid,  options_str   = jitbit_user.username,jitbit_user.password, jitbit_user.domain, jitbit_user.categoryId, jitbit_user.config,
                options_formatted = options_str.replace("'", '"')
                options = json.loads(options_formatted)
                jitbit_obj = Jitbitticket(email, password, categoryid, url)
                jitbit_response = collect_events(access_key, domain, **options)
                data = process_ssc_response(jitbit_response)
                for each_record in data:
                    jitbit_resp = jitbit_obj.create_ticket(str(each_record[0]))


        
def process_ssc_response(sc_response):
    for key, each_factor in sc_response.items():
        if isinstance(each_factor, list):
            for each in each_factor:
                tmp = list()
                tmp.append(each)
                yield tmp
        else:
            tmp = list()
            tmp.append(each_factor)
            yield tmp

@login_required(login_url='/login/')
def ssc_test(request):
    try:
        token = request.POST.get('api_token',None)
        domain = request.POST.get('domain',None)
        options = {"fetch_company_overall":True}
        sc_response = collect_events(token, domain, **options)
        if sc_response['overall_resp'] is  not None:
            return HttpResponse("Success")
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e

@login_required(login_url='/login/')
def set_jira_flag(request):
    try:
        set_flag(request, models.Jira, 'Jira')
        return redirect("/ssc_connector/ssc/")
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e

@login_required(login_url='/login/')
def set_slack_flag(request):
    try:
        set_flag(request, Slack, 'Slack')
        return redirect("/ssc_connector/ssc/")
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e


@login_required(login_url='/login/')
def set_ssc_flag(request):
    try:
        set_flag(request, SSCConnector, 'SecurityScoreCard')
        return redirect("/ssc_connector/ssc/")
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e


def set_flag(request, flag_obj, flag_name):
    # ssc = flag_obj.objects.filter(user_id=request.user).first()
    try:
        if flag_name == "Slack":

            ssc = flag_obj.objects.filter(source_id__user_id=request.user).first()
        else:
            ssc = flag_obj.objects.filter(user_id=request.user).first()
        if ssc:
            if ssc.flag:
                msg = "{} is Deactivated".format(flag_name)
                ssc.flag = False
                ssc.save()
                logger.info("Deactivated %s", flag_name)
                messages.warning(request, msg)
            else:
                msg = "{} is Activated".format(flag_name)
                ssc.flag = True
                ssc.save()
                process_ssc(request,flag_name)
                logger.info("Activated %s",  flag_name)
                messages.success(request, msg)
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e


@login_required(login_url='/login/')
def set_splunk_flag(request):
    splunk_data  =  Splunk.objects.filter(source_id__user_id =  request.user).first()
    if splunk_data and splunk_data.flag:
        splunk_data.flag =  False
        splunk_data.save()
    else:
        splunk_data.flag = True
        splunk_data.save()
        flag_name = "Splunk"
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_rapid_flag(request):
    rapid_data  =  Rapid.objects.filter(source_id__user_id =  request.user).first()
    if rapid_data and rapid_data.flag:
        rapid_data.flag =  False
        rapid_data.save()
    else:
        rapid_data.flag = True
        rapid_data.save()
        flag_name = "Rapid"
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")



@login_required(login_url='/login/')
def set_servicenow_flag(request):
    snw_data  =  Servicenowmodel.objects.filter(source_id__user_id =  request.user).first()
    if snw_data and snw_data.flag:
        snw_data.flag =  False
        snw_data.save()
    else:
        snw_data.flag = True
        snw_data.save()
        flag_name = "ServiceNow"
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_freshdesk_flag(request):
    freshdesk_data  =  Freshdeskmodel.objects.filter(source_id__user_id =  request.user).first()
    if freshdesk_data and freshdesk_data.flag:
        freshdesk_data.flag =  False
        freshdesk_data.save()
    else:
        freshdesk_data.flag = True
        freshdesk_data.save()
        flag_name = "Freshdesk"
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")



@login_required(login_url='/login/')
def set_zohodesk_flag(request):
    zohodesk_data  =  Zohomodel.objects.filter(source_id__user_id =  request.user).first()
    if zohodesk_data and zohodesk_data.flag:
        zohodesk_data.flag =  False
        zohodesk_data.save()
    else:
        zohodesk_data.flag = True
        zohodesk_data.save()
        flag_name = "Zohodesk"
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_pagerduty_flag(request):
    pagerduty_data  =  Pagerdutymodel.objects.filter(source_id__user_id =  request.user).first()
    if pagerduty_data and pagerduty_data.flag:
        pagerduty_data.flag =  False
        pagerduty_data.save()
    else:
        pagerduty_data.flag = True
        pagerduty_data.save()
        flag_name = "Pagerduty"
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_opsgenie_flag(request):
    opsgenie_data  =  Opsgeniemodel.objects.filter(source_id__user_id =  request.user).first()
    if  opsgenie_data and  opsgenie_data.flag:
        opsgenie_data.flag =  False
        opsgenie_data.save()
    else:
        opsgenie_data.flag = True
        opsgenie_data.save()
        flag_name = "Opsgenie"
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_zendesk_flag(request):
    zendesk_data  =  Zendeskmodel.objects.filter(source_id__user_id =  request.user).first()
    if  zendesk_data and  zendesk_data.flag:
        zendesk_data.flag =  False
        zendesk_data.save()
    else:
        zendesk_data.flag = True
        zendesk_data.save()
        flag_name = "Zendesk"
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_jitbit_flag(request):
    jitbit_data  =  Jitbitmodel.objects.filter(source_id__user_id =  request.user).first()
    if  jitbit_data and  jitbit_data.flag:
        jitbit_data.flag =  False
        jitbit_data.save()
    else:
        jitbit_data.flag = True
        jitbit_data.save()
        flag_name = "Jitbit"
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")

