from django.shortcuts import redirect, render
import os, secrets, time, base64, glob, smtplib, email, ssl
from django.core.mail import send_mail, EmailMultiAlternatives, send_mass_mail
from django.template.loader import render_to_string, get_template
from pathlib import Path
import shutil
from io import FileIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from uuid import uuid4
from django.conf import settings
from django.contrib import messages
from web.models import Attachment, MailUpload, Network
from django.http import JsonResponse
from datetime import datetime, date
from censusname import Censusname
from faker import Faker
from django.core.files.storage import default_storage
import requests
import socket

def get_referer(request):
	referer = request.META.get('HTTP_REFERER')
	if not referer:
		return None
	return referer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
media_path = os.path.join(BASE_DIR,'media')

def validate(mobile, code, pc):
    url = settings.ADMIN_SITE+"/validate_license/"
    headers = {
        "Content-Type": "application/json"
    }
    param = {
        "mobile": mobile,
        "code": code,
        "pc": pc
    }
    x = requests.get(url, params=param, headers=headers)
    return x.json()

def gen_num(length=16, charset="0123456789"):
            return "".join([secrets.choice(charset) for _ in range(0, length)])

def gen_code(length, charset="0123456789abcdefghijklmnopqrstuvwxyz_"):
            return "".join([secrets.choice(charset) for _ in range(0, length)])

def Home(request):
    if not get_referer(request):
        return redirect("license")
    return render(request, "home.html")

def validate_license(request):
    if request.is_ajax():
        mobile = request.POST["mobile"]
        code = request.POST["code"]
        pc = socket.gethostname()
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        verify = validate(mobile, code, pc)
        if verify["status"] == True:
            msg = {"success": "Message"}
        else:
            msg = {"error": verify["message"]}
        return JsonResponse(msg)
    return render(request, "validate.html")


def deleteAllNetwork(request):
    instance = Network.objects.all().delete()
    messages.success(request, "Deleted Successfully.")
    return redirect("mails")

def ViewMail(request):
    if not get_referer(request):
        return redirect("license")
    mails = Network.objects.all().order_by("-pk")
    context = {
        "mails": mails
    }
    return render(request, "mails.html", context)

def Uploads(request):
    if not get_referer(request):
        return redirect("license")
    if request.method == 'POST' and request.FILES:
        email_file = request.FILES["email"]
        instance = MailUpload.objects.create(file=email_file)
        open_emails_file = open(instance.file.path, "r")
        read_opened_emails_file = open_emails_file.read()
        mails = read_opened_emails_file.strip()
        mail = mails.split()
        count = len(mail)
        for m in mail:
            Domain = m.split('@')[1]
            domainName = Domain.split(".")[0]
            user = m.split("@")[0]
            instance2 = Network.objects.create(
                name = user,
                email = m,
                domain = Domain,
                active = True
            )
        messages.success(request, "You have successfully uploaded "+str(count)+" emails.")
        return redirect("mails")
    return render(request, "uploads.html")

def SendMail(request):
    if not get_referer(request):
        return redirect("license")
    if request.is_ajax():
        fake = Faker()
        time_now = datetime.now()
        current_time = time_now.strftime("%H:%M:%S")
        d = datetime.strptime(current_time, "%H:%M:%S")
        new_time = d.strftime("%I:%M %p")
        date_now = date.today()
        current_date = date_now.strftime("%a %d, %b %Y")
        content = request.POST["message"]
        text_content = request.POST["text_message"]
        attachment = request.FILES["attachment"]
        d_subject = request.POST["subject"]
        smtp_host = request.POST["smtp"]
        smtp_user = request.POST["smtp_user"]
        smtp_pass = request.POST["smtp_pass"]
        smtp_port = request.POST["smtp_port"]
        reply_to = request.POST["reply_to"]
        attachment_name = request.POST["attachment_name"]
        url = request.POST["url_link"]
        
        domain_prefix = request.POST["domain_prefix"]
        auto_gen_sender_name = request.POST["gen_sender_name"]
        auto_gen_email_name = request.POST["gen_email_name"]
        instance = Attachment.objects.create(file_html=attachment)
        if request.POST["sender_name"] != "":
            sender_name = request.POST["sender_name"]
        if request.POST["email_name"] != "":
            email_name = request.POST["email_name"]
        emails = Network.objects.all()
        
        for m in emails:
            rand_token = uuid4()
            company_name = fake.company()
            company_address = fake.address()
            company_mobile = fake.phone_number()
            company_phone = company_mobile.split("x")[0].lstrip("0")
            fname = Censusname(nameformat='{given}')
            lname = Censusname(nameformat='{surname}')
            first_name = fname.generate()
            last_name = lname.generate()
            if auto_gen_sender_name == "yes":
                fullname = first_name.lower() + ''+last_name.lower()
            else:
                fullname = sender_name
            if auto_gen_email_name == "yes":
                full_name = first_name + ' ' + last_name
            else:
                full_name = email_name
            rand_id = fullname+"@"+domain_prefix.lower()
            from_email = full_name +"<"+rand_id+">"
            domainName = m.domain.split(".")[0]
            repl_html = content.replace("[[-Email-]]", m.email).replace("[[-Domain-]]", m.domain).replace("[[-Date-]]", current_date).replace("[[-Name-]]", m.name.capitalize()).replace("[[-Link-]]", url).replace("[[-Time-]]", new_time).replace("[[-Domain_Name-]]", domainName).replace("[[-Company_Address-]]", company_address).replace("[[-Company_Name-]]", company_name).replace("[[-Company_Phone-]]", company_phone)
            repl_text = text_content.replace("[[-Email-]]", m.email).replace("[[-Domain-]]", m.domain).replace("[[-Date-]]", current_date).replace("[[-Name-]]", m.name.capitalize()).replace("[[-Link-]]", url).replace("[[-Time-]]", new_time).replace("[[-Domain_Name-]]", domainName).replace("[[-Company_Address-]]", company_address).replace("[[-Company_Name-]]", company_name).replace("[[-Company_Phone-]]", company_phone)
            if attachment != "":
                f = open(instance.file_html.path, "r")
                read_attached = f.read()
                repl_attachment = read_attached.replace("[[-Email-]]", m.email).replace("[[-Domain-]]", m.domain).replace("[[-Date-]]", current_date).replace("[[-Name-]]", m.name.capitalize()).replace("[[-Link-]]", url).replace("[[-Time-]]", new_time).replace("[[-Domain_Name-]]", domainName).replace("[[-Company_Address-]]", company_address).replace("[[-Company_Name-]]", company_name).replace("[[-Company_Phone-]]", company_phone)
                # a = open(instance.file_html.path, "w")
                directory = m.name+"_"+str(gen_code(5))
                pathd = os.path.join(settings.BASE_DIR, directory)
                os.mkdir(pathd)
                b = open(os.path.join(settings.BASE_DIR, directory+"/"+attachment_name+".html"), "w")
                b.write(repl_attachment)
                b.close()
                attached_files = glob.glob(os.path.join(settings.BASE_DIR, directory+"/"+attachment_name+".html"))

            c = {
                'Name': m.name.capitalize(), "Email": m.email, "Link": url, "Time": new_time,
                "Date": current_date, "Domain": m.domain, "Domain_Name": domainName, "Token": rand_token,
                "Company_Address": company_address, "Company_Name": company_name, "Company_Phone": company_phone
            }
            send_email = MIMEMultipart("alternative")
            send_email["From"] = from_email
            send_email["To"] = m.email
            send_email["Subject"] = d_subject

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(repl_text, 'plain')
            part2 = MIMEText(repl_html, 'html')

            send_email.attach(part1)
            send_email.attach(part2)
            if attachment != "":
                part3 = MIMEBase("application", "octet-stream")
                s = open(os.path.join(settings.BASE_DIR, directory+"/"+attachment_name+".html"), "r")
                if attached_files != []:
                    for files in attached_files:
                        part3.set_payload(s.read())
                        encoders.encode_base64(part3)
                        part3.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {attachment_name+'.html'}",
                        )
                send_email.attach(part3)
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, m.email, send_email.as_string())
            if attachment != "":
                shutil.rmtree(settings.BASE_DIR / directory, ignore_errors=True)
        server.quit()
        msg = {"success": "Cool"}
        return JsonResponse(msg)
    mails = Network.objects.all()
    ctx = {
        "email_count": len(mails)
    }
    return render(request, "send.html", ctx)

def SentMails(request):
    if not get_referer(request):
        return redirect("license")
    return render(request, "sent-mails.html")

def FailedMails(request):
    if not get_referer(request):
        return redirect("license")
    return render(request, "failed-mails.html")

def Configuration(request):
    if not get_referer(request):
        return redirect("license")
    return render(request, "configuration.html")
