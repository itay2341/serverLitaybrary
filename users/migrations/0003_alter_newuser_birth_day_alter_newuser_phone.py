# Generated by Django 4.0.6 on 2022-07-20 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_newuser_birth_day_alter_newuser_otp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='birth_day',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]