from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.conf import settings
from decouple import config

# RESTRICT THE VENDOR FROM ACCESSING CUSTOMER PAGE AND VICE VERSA.
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# GET CURRENT USER ROLE AND REDIRECT TO APPRORIATE PAGE
def get_user_role(user) -> str:
    if user.role == 1:
        redirectUrl = "vendorDashboard"
    elif user.role == 2:
        redirectUrl = "customerDashboard"
    elif user.role == None and user.is_superadmin:
        redirectUrl = "/admin"
    return redirectUrl


# SEND ACCOUNT ACTIVATION EMAIL
def send_custom_email(request, user, email_type):
    """
    Generic function to send custom emails based on the email_type.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)

    if email_type == 'verification':
        subject = "Kindly activate your account"
        template_name = "accounts/emails/email_verification.html"
    elif email_type == 'password_reset':
        subject = "Reset your password"
        template_name = "accounts/emails/reset_password.html"
    else:
        # Handle unknown email_type or provide default behavior
        raise ValueError("Invalid email_type")

    context = {
        "user": user,
        "domain": current_site,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user),
    }

    message = render_to_string(template_name, context)
    to_email = user.email
    mail = EmailMessage(subject, message, from_email=from_email, to=[to_email])
    mail.send()


# SEND VENDOR APPROVAL EMAIL
def send_vendor_approval_email(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email =  context['user'].email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()