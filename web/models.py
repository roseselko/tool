from django.db import models

# Create your models here.
class Config(models.Model):
    pass


class Network(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    email = models.EmailField(max_length=100, default='')
    domain = models.CharField(max_length=100, default='', blank=True)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class SentMail(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    email = models.EmailField(max_length=100, default='')
    domain = models.CharField(max_length=100, default='', blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class FailedMail(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    email = models.EmailField(max_length=100, default='')
    domain = models.CharField(max_length=100, default='', blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class MailUpload(models.Model):
    file = models.FileField(upload_to="box")

    def __str__(self):
        return "Emails"

class Attachment(models.Model):
    file_html = models.FileField(upload_to="html")
    file_text = models.FileField(upload_to="html/text", blank=True, null=True)

    def __str__(self):
        return "Attachments"
