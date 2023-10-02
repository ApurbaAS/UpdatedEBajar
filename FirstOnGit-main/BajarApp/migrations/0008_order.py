# Generated by Django 4.2.5 on 2023-09-30 14:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BajarApp', '0007_rename_contuct_number_user_client_contact_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BajarApp.user_client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BajarApp.product')),
            ],
        ),
    ]
