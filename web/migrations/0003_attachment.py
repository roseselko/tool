# Generated by Django 3.2.8 on 2021-10-15 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_mailupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='html')),
            ],
        ),
    ]
