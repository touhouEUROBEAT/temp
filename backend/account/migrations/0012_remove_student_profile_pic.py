# Generated by Django 4.0.6 on 2022-08-29 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_student_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='profile_pic',
        ),
    ]