# Generated by Django 4.0.6 on 2022-07-19 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('name', models.CharField(max_length=60, null=True)),
                ('author', models.CharField(max_length=20, null=True)),
                ('yearPublished', models.CharField(max_length=4, null=True)),
                ('category', models.CharField(max_length=10, null=True)),
                ('imgURL', models.TextField(blank=True, max_length=250, null=True)),
                ('info', models.TextField(blank=True, max_length=2000, null=True)),
                ('cost', models.IntegerField()),
                ('copies', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('loanDays', models.IntegerField(verbose_name='days to loan the book')),
                ('loanFee', models.IntegerField(verbose_name='fee per day')),
                ('status', models.BooleanField(default=True)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('start_date', models.CharField(max_length=13, null=True)),
                ('return_date', models.CharField(max_length=13, null=True)),
                ('status', models.IntegerField(default=2341)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='library.book')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.type'),
        ),
    ]
