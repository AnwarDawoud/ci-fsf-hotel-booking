# Generated by Django 3.2.23 on 2024-01-18 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_your_choice', '0013_alter_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
