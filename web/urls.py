from django.conf.urls import url

from .views import Configuration, FailedMails, Home, SendMail, SentMails, Uploads, ViewMail, deleteAllNetwork, validate_license

urlpatterns = [
    url(r'^$', Home, name='home'),
    url(r'^mails/$', ViewMail, name='mails'),
    url(r'^upload/$', Uploads, name='uploads'),
    url(r'^mails/send/$', SendMail, name='send'),
    url(r'^mails/sent/$', SentMails, name='sent'),
    url(r'^mails/delete/all/$', deleteAllNetwork, name='deleteNetwork'),
    url(r'^mails/failed/$', FailedMails, name='failed'),
    url(r'^license/validate/$', validate_license, name='license'),
]
