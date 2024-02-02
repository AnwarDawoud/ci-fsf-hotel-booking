# Generated by Django 3.2.23 on 2024-02-02 04:05

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_your_choice', '0002_delete_logentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=255)),
                ('night_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('room_number', models.IntegerField(blank=True, null=True)),
                ('main_photo', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('amenities', models.CharField(blank=True, max_length=255, null=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotels_as_manager', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Hotels',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_your_choice.hotel')),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='other_photos',
            field=models.ManyToManyField(blank=True, related_name='hotel_photos', to='hotel_your_choice.Photo'),
        ),
    ]
