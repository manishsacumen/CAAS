import math
import random
from django.views import View
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .token import account_activation_token
from .models import EmailVerification, Otp, Client
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import smtplib
import os
import smtplib
import imghdr
from email.message import EmailMessage
from .email_template import validation_email, validation_otp
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# This view will take you to dashboard only if the user is loged in
@login_required(login_url='/login/')
def home_view(request):
    return render(request, 'dashboard/home.html')


class LoginView(View):

    def post(self, request):
        try: 
            singin_data = request.POST.dict()
            username = singin_data.get('email',None)
            password = singin_data.get('password',None)
            user = authenticate(username=username, password=password)
            if user:
                # Checkig for email varification status
                Emailverifify = EmailVerification.objects.filter(user_id = user).first()
                if  Emailverifify.status:
                    otp_obj  = Otp.objects.filter(user_id = user).first()
                    if otp_obj:
                        if otp_obj.blocked_time <= datetime.now(tz=timezone.utc):    
                            login(request, user)
                            send_otp(request)
                            logger.info("User logged in successfully Otp send %s ", user.email)
                            return redirect('/otp/')
                        else:
                            logger.info("Blocked user tried to login %s ", user.email)
                            messages.warning(request, f'Your are Temporarily Blocked..Try to login after 1 hr')
                            return redirect('/login/')
                    else:
                        login(request, user)
                        send_otp(request)
                        logger.info("User logged in successfully Otp send %s ", user.email)
                        return redirect('/otp/')
                else:
                    logger.info("Emailverification is not done %s ", user.email)
                    messages.warning(request, f'Your account is not validated')
                    return redirect('/login')
            else:
                logger.info("Invalid Username and Password %s ", username)
                messages.warning(request, f'Invalid Username and Password')
                return redirect('/login/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e

    def get(self, request):
        try:
            if not  request.user.is_authenticated:
                return render(request, 'login/login.html')
            else:
                otp_obj  = Otp.objects.filter(user_id = request.user).first()
                if otp_obj.blocked_time <= datetime.now(tz=timezone.utc):
                    logger.info("User alredy loggedin %s ", request.user.email)
                    return redirect('/ssc_connector/ssc/')
                else:
                    return render(request, 'login/login.html')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e


class RegisterView(View):

    def post(self, request):
        try:
            singup_data = request.POST.dict()
            first_name = singup_data.get('first_name')
            last_name = singup_data.get('last_name')
            username = singup_data.get('email')
            email = singup_data.get('email')
            password = singup_data.get('password')
            cpassword = singup_data.get('cpassword')
            if password != cpassword:
                logger.info("password and cornfirmation password is same %s ", email)
                messages.warning(request, f'Password and Confirm_password does not match"!!')
                return redirect('/register/') 

            # Check for the pre-requisite information about the user
            client  = Client.objects.filter(email=username).first()
            if client:
                # Check for already registered user
                logger.info("User is present in  client table %s ", email)
                user = User.objects.filter(username=username)
                if user.count():
                    logger.info("User already present %s ", email)
                    messages.warning(request, f'Account with given email id is already registered!!! ')
                    return redirect('/register/')

                else:
                    new_user = User.objects.create_user( username, first_name=first_name, last_name=last_name, password=password, email=email)
                    # new_user.is_active  = False
                    logger.info("User created successfully %s ", new_user.email)
                    new_user.save()
                    token = account_activation_token.make_token(new_user)
                    link = settings.DOMAIN +'/activate/?token='+token
                    new_user.save()
                    # Once user data is saved in database an email validation link will be sent.
                    if new_user:
                        verify = EmailVerification.objects.filter(user_id = new_user,status = False).first()
                        if verify:
                            verify.token  = token 
                            verify.save()
                            validation_email(new_user.username,link)
                            logger.info("Activation link for the account is sent to your registered email id %s ", new_user.email)
                            messages.success(request, f'Activation link for the account is sent to your registered email id.')
                        else :
                            email_verify  = EmailVerification.objects.create(user_id = new_user)
                            email_verify.token  = token 
                            email_verify.save()
                            validation_email(new_user.username,link)
                            logger.info("Activation link for the account is sent to your registered email id %s ", new_user.email)
                            messages.success(request, f'Activation link for the account is sent to your registered email id.')
                    return redirect('/register/')
            else:
                logger.info("You are not allowed to register..Please contact admin for help. %s ", email)
                messages.warning(request, f'You are not allowed to register..Please contact admin for help..!!!')
                return redirect('/register/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e
  
    def get(self,  request):
        try:
            if not  request.user.is_authenticated:
                return render(request, 'login/register.html')
            else:
                logger.info("User alredy loggedin %s ", request.user.email)
                return redirect('/ssc_connector/ssc/')
        except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e

        

def activate(request):
    try:
        token = request.GET['token']
        Emailverify = EmailVerification.objects.filter(token = token).first()
        if Emailverify:
            logger.info("Email Verified Successfully %s ", Emailverify.user_id.email)
            user = User.objects.filter(id = Emailverify.user_id.id).first()
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    try:
        if user is not None and account_activation_token.check_token(user, token):
            logger.info("Token is verified successfully%s ", Emailverify.user_id.email)
            user.active = True
            user.save()
            Emailverify.status  = True
            Emailverify.save()
            messages.success(request, f'Thanks for validating the account...Login Now!!')
            return redirect('/login')
        else:
            logger.info("User is not present or token verification failed ")
            return render(request, 'login/login.html')
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e


@login_required(login_url='/login/')
def logout_view(request):
    try:
        logout(request)
        logger.info("logout successfully")
        return redirect('/login/')
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e


def send_otp(request):
    try:
        otp_obj  = Otp.objects.filter(user_id = request.user).first()
        otp  = generateOTP()
        if otp_obj:
            if otp_obj.blocked_time < datetime.now(tz=timezone.utc):
                if otp_obj.number_attempt < 3:
                    otp_obj.token  = otp
                    otp_obj.save()
                    message = otp
                    recepitent = request.user.username
                    email_send = validation_otp(recepitent, message )
                    if email_send:
                        return messages.success(request, f'Otp has been send to your email please check your email ')
            else:
                messages.warning(request, f'Account is blocked for 1 hour ')
        else:
            create_otp = Otp(user_id = request.user,token = otp,number_attempt = 0, blocked_time = datetime.now(tz=timezone.utc))
            create_otp.save()
            logger.info("otp objects for user is created")
            message = otp
            recepitent = request.user.username
            email_send = validation_otp(recepitent, message )
            return messages.warning(request, f'Otp has been send to your email please check your email ')
    except Exception as e:
            logger.error("Unexpected Exception occured: %s ", e)
            return e 

@login_required(login_url='/login/')
def opt_resend(request):
    try:
        send_otp(request)
        logger.info("otp is resend %s",request.user.email)
        return redirect('/otp/')
    except Exception as e:
        logger.error("Unexpected Exception occured: %s ", e)
        return e

@login_required(login_url='/login/')
def validate_otp(request):
    try:
        otp_obj  = Otp.objects.filter(user_id = request.user).first()
        data  = request.POST.dict()
        if otp_obj:
            if otp_obj.blocked_time <= datetime.now(tz=timezone.utc):
                if otp_obj.number_attempt < 3:
                    if otp_obj.token  == int(data.get('otp')):
                        otp_obj.number_attempt = 0
                        otp_obj.save()
                        logger.info("otp is validated successfully %s",request.user.email)
                        return redirect('/ssc_connector/ssc/')
                    else:
                        otp_obj.number_attempt += 1
                        otp_obj.save()
                        logger.info("otp  validation failed %s",request.user.email)
                        messages.warning(request, f'Otp is incorrect')
                        return redirect('/otp/')
                elif otp_obj.number_attempt == 3:
                    logger.info("user is blocked for  1 hour %s",request.user.email)
                    otp_obj.blocked_time = datetime.now(tz=timezone.utc) + timedelta(hours=1)
                    otp_obj.number_attempt = 0
                    otp_obj.save()
                    messages.warning(request, f'Blocked')
                    return redirect('/login/')
            messages.warning(request, f'Blocked')
            return redirect('/otp/')
    except Exception as e:
        logger.error("Unexpected Exception occured: %s ", e)
        return e




                

def generateOTP() : 
  
    # Declare a digits variable   
    # which stores all digits  
    digits = "0123456789"
    OTP = "" 
  
   # length of password can be chaged 
   # by changing value in range 
    for i in range(6) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP 