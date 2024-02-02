# Generated by Django 3.2.23 on 2024-02-02 05:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_your_choice', '0003_auto_20240202_0405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('guests', models.PositiveIntegerField()),
                ('issued_date', models.DateField(auto_now_add=True)),
                ('rating', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Booking Active'), ('canceled', 'Booking Canceled'), ('rescheduled', 'Booking Rescheduled')], default='active', max_length=20)),
                ('canceled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='canceled_bookings', to=settings.AUTH_USER_MODEL)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_your_choice.hotel')),
                ('original_booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel_your_choice.booking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('text', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='hotel_your_choice.booking')),
                ('hotel', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='hotel_your_choice.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'booking')},
            },
        ),
    ]
