from django.shortcuts import render, redirect, HttpResponse
import json
from django.shortcuts import render
from .config import payload, servicenow_payload
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
from .models import TargetApplication
from .jira_conection import JiraConnect
from .slack_connection import SlackConnect
from .splunk_connection import SplunkConnect
from .rapid_connection import RapidConnect
from .servicenow_connection import ServicenowConnect
from .pagerduty_connection import PagerdutyConnect
from .zohodesk_connection import ZohodeskConnect
from .opsgrnie_connection import OpsgenieConnect
from .zendesk_connection import ZendeskConnect
from .jira_conection import JiraConnect

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
                                              'jitbit_data': jitbit_data })
    except Exception as e:
        logger.error("Unexpected Exception occured: %s ", e)
        return e

@login_required(login_url='/login/')
def process_ssc(request, flag_name):
    try:
        ssc_user = SSCConnector.objects.filter(user_id=request.user).first()
        ssc_flag = ssc_user and ssc_user.flag
    except Exception as err:
        print("Getting exception as {}".format(err))
    else:
        if not ssc_flag:
            # To do: disable jira and slack
            pass
        else:
            if flag_name =='Jira':
                jira_class = JiraConnect(request,ssc_user)
                jira_send  =  jira_class.send_data()
            else:
                pass
            if flag_name =='Slack':
                slack_obj = SlackConnect(request, ssc_user)
                slack_send  = slack_obj.send_data()
            if flag_name == 'Splunk':
                splunk_obj =  SplunkConnect(request, ssc_user)
                splunk_obj.send_data()
            if flag_name == 'Rapid':
                rapid_obj = RapidConnect(request, ssc_user)
                rapid_obj.send_data()
            if flag_name == 'ServiceNow':
                servicenw_obj =  ServicenowConnect(request, ssc_user)
                servicenw_obj.send_data()
            # if freshdesk_flag  and flag_name == 'Freshdesk':
            #     access_key, base_url, domain = ssc_user.api_token, ssc_user.api_url, ssc_user.domain
            #     url, username, api_key, options_str   = freshdesk_user.url, freshdesk_user.username, freshdesk_user.api_key, servicenw_user.config
            #     options_formatted = options_str.replace("'", '"')
            #     options = json.loads(options_formatted)
            #     fresh_obj =  FreshdeskEvents(username, api_key, url)
            #     fresh_response = collect_events(access_key, domain, **options)
            #     data = process_ssc_response(fresh_response)
            #     for each_record in data:
            #         fresh_resp = fresh_obj.create_ticket(**each_record[0])
            if flag_name == 'Zohodesk':
                zoho_obj  = ZohodeskConnect(request, ssc_user)
                zoho_obj.send_data()

            if flag_name == 'Pagerduty':
                pagerduty_obj =  PagerdutyConnect(request, ssc_user)
                pagerduty_obj.send_data()
            if flag_name == 'Opsgenie':
                opsgenie_obj  = OpsgenieConnect(request, ssc_user)
                opsgenie_obj.send_data()
        
            if flag_name == 'Zendesk':
                zendesk_obj   = ZendeskConnect(request, ssc_user)
                zendesk_obj.send_data()
            if flag_name == 'Jitbit':
                jitbit_obj = JiraConnect(request, ssc_user)
                jitbit_obj.send_data()


        
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
        msg = "Splunk is Deactivated"
        messages.success(request, msg)
    else:
        splunk_data.flag = True
        splunk_data.save()
        flag_name = "Splunk"
        msg = "Splunk is Activated"
        messages.success(request, msg)
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_rapid_flag(request):
    rapid_data  =  Rapid.objects.filter(source_id__user_id =  request.user).first()
    if rapid_data and rapid_data.flag:
        rapid_data.flag =  False
        rapid_data.save()
        msg = "Rapid7 is Deactivated"
        messages.success(request, msg)
    else:
        rapid_data.flag = True
        rapid_data.save()
        flag_name = "Rapid"
        msg = "Rapid7 is Activated"
        messages.success(request, msg)
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")



@login_required(login_url='/login/')
def set_servicenow_flag(request):
    snw_data  =  Servicenowmodel.objects.filter(source_id__user_id =  request.user).first()
    if snw_data and snw_data.flag:
        snw_data.flag =  False
        snw_data.save()
        msg = "Servicenow is Deactivated"
        messages.success(request, msg)
    else:
        snw_data.flag = True
        snw_data.save()
        flag_name = "ServiceNow"
        msg = "Servicenow is Activated"
        messages.success(request, msg)
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_freshdesk_flag(request):
    freshdesk_data  =  Freshdeskmodel.objects.filter(source_id__user_id =  request.user).first()
    if freshdesk_data and freshdesk_data.flag:
        freshdesk_data.flag =  False
        freshdesk_data.save()
        msg = "Freshdesk is Deactivated"
        messages.success(request, msg)
    else:
        freshdesk_data.flag = True
        freshdesk_data.save()
        flag_name = "Freshdesk"
        msg = "Freshdesk is Activated"
        messages.success(request, msg)
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")



@login_required(login_url='/login/')
def set_zohodesk_flag(request):
    zohodesk_data  =  Zohomodel.objects.filter(source_id__user_id =  request.user).first()
    if zohodesk_data and zohodesk_data.flag:
        zohodesk_data.flag =  False
        zohodesk_data.save()
        msg = "Zohodesk is Deactivated"
        messages.success(request, msg)
    else:
        zohodesk_data.flag = True
        zohodesk_data.save()
        flag_name = "flag_name"
        msg = "Zohodesk is Activated"
        process_ssc(request,flag_name)
        messages.success(request, msg)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_pagerduty_flag(request):
    pagerduty_data  =  Pagerdutymodel.objects.filter(source_id__user_id =  request.user).first()
    if pagerduty_data and pagerduty_data.flag:
        pagerduty_data.flag =  False
        pagerduty_data.save()
        msg = "Pagerduty is Deactivated"
        messages.success(request, msg)
    else:
        pagerduty_data.flag = True
        pagerduty_data.save()
        flag_name = "Pagerduty"
        msg = "Pagerduty is Activated"
        messages.success(request, msg)
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_opsgenie_flag(request):
    opsgenie_data  =  Opsgeniemodel.objects.filter(source_id__user_id =  request.user).first()
    if  opsgenie_data and  opsgenie_data.flag:
        opsgenie_data.flag =  False
        opsgenie_data.save()
        msg = "Opsgenie is Deactivated"
        messages.success(request, msg)
    else:
        opsgenie_data.flag = True
        opsgenie_data.save()
        flag_name = "Opsgenie"
        msg = "Opsgenie is Activated"
        messages.success(request, msg)
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_zendesk_flag(request):
    zendesk_data  =  Zendeskmodel.objects.filter(source_id__user_id =  request.user).first()
    if  zendesk_data and  zendesk_data.flag:
        zendesk_data.flag =  False
        zendesk_data.save()
        msg = "Zendesk is Deactivated"
        messages.success(request, msg)
    else:
        zendesk_data.flag = True
        zendesk_data.save()
        flag_name = "Zendesk"
        msg = "Zendesk is Activated"
        messages.success(request, msg)
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")


@login_required(login_url='/login/')
def set_jitbit_flag(request):
    jitbit_data  =  Jitbitmodel.objects.filter(source_id__user_id =  request.user).first()
    if  jitbit_data and  jitbit_data.flag:
        jitbit_data.flag =  False
        jitbit_data.save()
        msg = "Jitbit is Activated"
        messages.success(request, msg)
    else:
        jitbit_data.flag = True
        jitbit_data.save()
        flag_name = "Jitbit"
        msg = "Jitbit is Deactivated"
        messages.success(request, msg)
        process_ssc(request,flag_name)
    return redirect("/ssc_connector/ssc/")

