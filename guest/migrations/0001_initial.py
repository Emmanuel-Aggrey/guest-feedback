# Generated by Django 5.0.2 on 2024-02-10 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('outlets', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('company', models.CharField(blank=True, max_length=200, null=True)),
                ('head_about_us', models.CharField(blank=True, choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('x', 'X'), ('instagram', 'Instagram')], max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('excellent', models.BooleanField(default=False)),
                ('good', models.BooleanField(default=False)),
                ('fair', models.BooleanField(default=False)),
                ('poor', models.BooleanField(default=False)),
                ('staff_to_recommend', models.CharField(blank=True, max_length=200, null=True)),
                ('comments', models.TextField(blank=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='outlets.comment')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='guest.guest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
