# Generated by Django 5.0.2 on 2024-05-27 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0002_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='attachment',
            field=models.FileField(max_length=500, upload_to='feedbacks'),
        ),
    ]
